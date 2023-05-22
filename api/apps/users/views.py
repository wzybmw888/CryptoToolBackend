import base64
import datetime

import ccxt
import requests
from django.contrib.auth import get_user_model
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import UserProfile, UserExchangeAccount
from users.serializer import UserSerializer, RegisterSerializer, TokenSerializer, UserInfoSerializer, \
    PasswordSerializer, UserExchangeAccountSerializer
from users.swagger_response import register_swagger_params, login_swagger_params, \
    code_swagger_params, logout_swagger_params, userinfo_swagger_params, change_password_swagger_params, \
    api_record_swagger_params, balance_swagger_params, change_userinfo_swagger_params, api_get_swagger_params
from utils import custom_config
from utils.public import get_username_from_jwt
from utils.verify.captcha import Captcha
from io import BytesIO
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# Create your views here.
User = get_user_model()
jwt_auth = JWTAuthentication()


class UserView(ViewSet, viewsets.GenericViewSet):
    serializer_class = None
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    pagination_class = None  # 取消分页

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == "register":
            return RegisterSerializer
        elif self.action == "login":
            return TokenSerializer
        elif self.action == "userinfo":
            return UserInfoSerializer
        elif self.action == "retrieve":
            return UserSerializer
        elif self.action == "list":
            return UserSerializer
        elif self.action == "partial_update":
            return UserSerializer
        elif self.action == "change_password":
            return PasswordSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(**code_swagger_params)
    @action(methods=["get"], detail=False, url_name="code", url_path="login/code")
    def code(self, request):
        username = request.GET.get("username")
        module = request.GET.get("module")
        # 后端生成验证码，发送给前端
        cap = Captcha.instance()
        text, image = cap.generate_captcha()
        # 实例化管道,保存图片流数据
        out = BytesIO()
        # 图片保存管道中,png格式
        image.save(out, 'png')
        # 读取得时候指针回零0
        out.seek(0)
        img_data = out.getvalue()
        # 将bytes转成base64
        code = base64.b64encode(img_data).decode()
        print(text)
        # 如果是注册接口，检查用户是否注册，没有存在可以通过
        user = UserProfile.objects.filter(username=username)
        if module == "register":
            if user:
                return Response({"status": 401, "msg": "该用户存在，清登录!"})
            else:
                cache.set(f'{username}_code', text.lower(), timeout=300)
                return Response({"status": 200, "data": code})
        if module == "login":
            # 检查用户是否存在,不存在返回401
            if user:
                cache.set(f'{username}_code', text.lower(), timeout=300)
                return Response({"status": 200, "data": code})
            else:
                return Response({"status": 401, "msg": "该用户不存在，请注册！"})

    @swagger_auto_schema(**login_swagger_params)
    @action(methods=["post"], detail=False, url_name="login", url_path="login")
    def login(self, request):
        username = request.data.get("username")
        user_code = request.data.get("code").lower()
        code = cache.get(username + "_code")
        if code and user_code == code:
            user = UserProfile.objects.filter(username=username).first()
            if user:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.user
                user.last_login = datetime.datetime.now()
                user.save()
                # 缓存token信息
                cache.set(f'{user.username}_token', serializer.get_token(user))
                return Response(
                    {"status": 200, "msg": "登录成功！", "data": serializer.validated_data})
            else:
                return Response({"status": 201, "msg": "用户不存在,登录失败！"})
        else:
            return Response({"status": 202, "msg": "验证码错误!"})

    @swagger_auto_schema(**register_swagger_params)
    @action(methods=["post"], detail=False, url_name="register", url_path="register",
            serializer_class=RegisterSerializer)
    def register(self, request):
        """用户注册"""
        # 首先查询下是否有这个用户，没有才可以注册
        user = UserProfile.objects.filter(username=request.data.get("username"))
        if user:
            return Response(
                {
                    "status": 404,
                    "msg": "用户已存在，请登录！",
                }
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()
            output_serializer = UserSerializer(instance=user, context={"request": request})
            return Response(
                {
                    "status": 200,
                    "msg": "注册成功",
                    "data": output_serializer.data
                }
            )
        else:
            return Response(
                {
                    "status": 403,
                    "msg": "注册校验不通过",
                    "data": serializer.errors
                }
            )

    @swagger_auto_schema(**logout_swagger_params)
    @action(
        ["get"],
        detail=False,
        url_name="logout",
        url_path="logout",
        authentication_classes=[JWTAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        user = get_username_from_jwt(request)
        username = user.username
        # 删除token缓存
        cache.delete(f'{username}_token')
        return Response({
            "status": 200,
            "msg": username + "已退出"
        })

    @swagger_auto_schema(**userinfo_swagger_params)
    @action(
        ["GET"],
        detail=False,
        url_path="userinfo",
        url_name="userinfo",
        authentication_classes=[JWTAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def userinfo(self, request):
        """获取当前登录人的信息"""
        user = User.objects.get(username=request.user)
        output_serializer = self.get_serializer(user)
        return Response({
            "status": 200,
            "data": output_serializer.data
        })

    @swagger_auto_schema(**change_password_swagger_params)
    @action(
        ["POST"],
        detail=False,
        url_name="change_password",
        url_path="change_password",
        authentication_classes=[JWTAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_password()
        return Response({
            "status": 200,
            "msg": "密码修改成功！",
            "data": serializer.validated_data
        })

    @swagger_auto_schema(**change_userinfo_swagger_params)
    @action(
        ["put"],
        detail=False,
        url_name="change_userinfo",
        url_path="change_userinfo",
        authentication_classes=[JWTAuthentication],
        permission_classes=[IsAuthenticated],
        serializer_class=UserInfoSerializer
    )
    def change_userinfo(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        serializer.set_userinfo()
        return Response({
            "status": 200,
            "msg": "修改成功！",
            "data": serializer.validated_data
        })


# 用户交易所账户信息视图
class UserExchangeAccountView(ViewSet, viewsets.GenericViewSet):
    serializer_class = None
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    pagination_class = None  # 取消分页

    def get_queryset(self):
        queryset = UserExchangeAccount.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == "record":
            return UserExchangeAccountSerializer
        elif self.action == "exchange_api_info":
            return UserExchangeAccountSerializer

    # 记录用户的apikey和secret、password等信息
    @swagger_auto_schema(**api_record_swagger_params)
    @action(methods=["post"], detail=False, url_name="record", url_path="record",
            authentication_classes=[JWTAuthentication],
            permission_classes=[IsAuthenticated])
    def record(self, request):
        # 从jwt中获取用户信息
        username = get_username_from_jwt(request)
        # 获取接口信息
        exchange_name = request.data.get("exchange_name")
        api_key = request.data.get("api_key")
        secret_key = request.data.get("secret_key")
        password = request.data.get("password")
        # 目前支持的交易所
        field_list = ["OKX", "BINANCE"]

        if exchange_name not in field_list:
            return Response({"status": 403, "msg": "交易所不在支持列表当中"})
        # 根据用户名查询用户对象
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"status": 401, "msg": "用户不存在"})

        # 创建 UserExchangeAccount 对象并保存到数据库
        serializer = self.get_serializer(data={
            "exchange_name": exchange_name, "username": user.id,
            "api_key": api_key, "secret_key": secret_key, "password": password
        })
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "msg": "用户API保存成功"})
        else:
            return Response({"status": 402, "msg": "用户API保存失败", "data": serializer.errors})

    # 从数据库中获取用户的apikey和secret、password等信息
    @swagger_auto_schema(**api_get_swagger_params)
    @action(methods=["get"], detail=False, url_path="exchange_api_info", url_name="exchange_api_info",
            authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated])
    def exchange_api_info(self, request, *args, **kwargs):
        username = get_username_from_jwt(request)
        exchange_name = request.GET.get('exchange_name', '')
        print(username, exchange_name)
        user_account = UserExchangeAccount.objects.filter(username=username, exchange_name=exchange_name).last()
        if user_account:
            serializer = self.get_serializer(instance=user_account,  many=False)
            print(serializer.data)
            return Response({"status": 200, "data": serializer.data})
        else:
            return Response({"status": 404, "msg": "未找到指定的交易所账户信息"})

    # 获取用户交易所余额
    @swagger_auto_schema(**balance_swagger_params)
    @action(methods=["get"], detail=False, url_path="balance", url_name="balance",
            authentication_classes=[JWTAuthentication],
            permission_classes=[IsAuthenticated])
    def balance(self, request):
        # 从jwt中获取用户信息
        username = get_username_from_jwt(request)
        # 获取请求参数中的当前页码和每页显示的记录数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        exchange_name = request.GET.get("exchange_name")
        # 从数据库中根据用户名查找到对应的apikey和secret，通过ccxt来获取用户余额
        user_account = UserExchangeAccount.objects.filter(username=username,exchange_name=exchange_name).last()
        api_key = user_account.api_key
        secret_key = user_account.secret_key
        password = user_account.password
        exchange = ccxt.okx({
            'apiKey': api_key,
            'secret': secret_key,
            'password': password,
            'enableRateLimit': True,
            'proxies': custom_config.proxies
        })
        try:
            assets = exchange.fetch_balance()
            tickers = exchange.fetch_tickers()
        except Exception as e:
            return Response({"status": 400, "msg": "api调用失败"})

        # 对币种资产列表进行过滤和分页处理
        filtered_assets = []
        for name in assets["total"]:
            symbol = name + "/USDT"
            value = tickers[symbol]['last'] * assets["total"][name]
            if value >= 0.001:
                asset = {
                    'name': name,
                    'free': round(assets['free'][name], 4),
                    'used': round(assets['used'][name], 4),
                    'total': round(assets['total'][name], 4),
                    'value': round(value, 4),
                }
                filtered_assets.append(asset)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        asset_list = filtered_assets[start_index:end_index]

        # 将币种资产列表序列化为JSON格式，并返回给前端
        data = {
            "status": 200,
            'total': len(filtered_assets),
            'data': asset_list,
        }
        return Response(data)

    @action(methods=["get"], detail=False, url_path="send_email", url_name="发送邮箱验证码")
    def send_email(self, request):
        username = request.GET.get("username")
        user = UserProfile.objects.filter(username=username).first()
        if user and user.email:
            code = get_random_string(6)
            email_subject = '重置密码'  # 邮件主题
            email_body = '验证码:' + code  # 邮件正文
            from_email = 'lc13135698897@163.com'  # 发件人邮箱
            to_email = [user.email]  # 收件人邮箱
            try:
                send_mail(email_subject, email_body, from_email, to_email, fail_silently=False)
                cache.set(f'{username}_email_code', code.lower(), timeout=300)
                return Response({"status": 200, "msg": "重置密码邮件已发送"})
            except Exception as e:
                print(e)
                return Response({"status": 400, "msg": "邮件发送失败"})
        else:
            return Response({"status": 400, "msg": "用户邮箱不存在"})


class GitHubOAuth2LoginView(ViewSet, viewsets.GenericViewSet):
    @action(methods=["get"], detail=False, url_path="auth", url_name="第三方登录")
    def github_callback(self, request):
        access_token_url = 'https://github.com/login/oauth/access_token'
        user_info_url = 'https://api.github.com/user'
        client_id = '4016a0e2d868083a22b5'
        client_secret = '5567b491a88ab4bf8514c93a6f4125dd39cf488e'
        redirect_uri = 'http://127.0.0.1:5001/Auth'

        # get the authorization code from the request
        code = request.GET.get('code')
        # exchange the code for an access token
        access_token_response = requests.post(access_token_url, data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
        }, headers={
            'Accept': 'application/json'
        })
        access_token = access_token_response.json().get('access_token')
        print(access_token_response.json())
        # get user info using the access token
        user_info_response = requests.get(user_info_url, headers={
            'Authorization': f'token {access_token}',
            'Accept': 'application/json',
        })
        user_info = user_info_response.json()
        print(user_info)
        return Response(
            {"status": 200, "msg": "登录成功！", "data": user_info})
