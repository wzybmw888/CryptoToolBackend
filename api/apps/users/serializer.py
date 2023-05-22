from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer, SetPasswordRetypeSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import UserExchangeAccount

User = get_user_model()


class RegisterSerializer(UserCreatePasswordRetypeSerializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(source="avatar_thumbnail")

    class Meta:
        model = User
        fields = ["id", "username", "level", "avatar_url", "email", "last_login", "is_superuser"]
        read_only_fields = ["id", "level", "username", "last_login", "is_superuser"]


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
               此方法往token的有效负载 payload 里面添加数据
               例如自定义了用户表结构，可以在这里面添加用户邮箱，头像图片地址，性别，年龄等可以公开的信息
               这部分放在token里面是可以被解析的，所以不要放比较私密的信息
               :param user: 用戶信息
               :return: token
               """
        token = super().get_token(user)
        # 添加个人信息
        token['name'] = user.username
        return token

    def validate(self, attrs):
        """
                此方法为响应数据结构处理
                原有的响应数据结构无法满足需求，在这里重写结构如下：
                {
                    "refresh": "xxxx.xxxxx.xxxxx",
                    "access": "xxxx.xxxx.xxxx",
                    "expire": Token有效期截止时间,
                    "username": "用户名",
                    "email": "邮箱"
                }

                :param attrs: 請求參數
                :return: 响应数据
                """
        data = super().validate(attrs)
        # 获取Token对象
        refresh = self.get_token(self.user)
        # 加个token的键，值和access键一样
        data['token'] = data['access']
        # 然后把access键干掉
        del data['access']
        # 令牌到期时间
        data['expire'] = refresh.access_token.payload['exp']  # 有效期
        # 用户名
        data['username'] = self.user.username
        # 邮箱
        data['email'] = self.user.email

        data["is_superuser"] = self.user.is_superuser
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]

    def set_userinfo(self):
        user = self.context["request"].user
        context = self.context["request"].data
        validated_data = self.validated_data
        user.nickname = validated_data.get('nickname',context["nickname"])
        user.sign = validated_data.get('nickname',context["sign"])
        user.save()


class PasswordSerializer(SetPasswordRetypeSerializer):
    def set_password(self):
        new_password = self.validated_data["new_password"]
        user = self.context["request"].user
        print(user)
        user.set_password(new_password)
        user.save()


class UserExchangeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExchangeAccount
        fields = "__all__"

