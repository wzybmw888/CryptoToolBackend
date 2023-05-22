"""
swagger响应体
"""
from drf_yasg import openapi

# 定义响应体的Schema

# 登录接口文档
login_responses = {
    200: openapi.Response(
        description='操作成功',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, default=200),
                "msg": openapi.Schema(type=openapi.TYPE_STRING, default="操作成功"),
                "data":
                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "token": openapi.Schema(type=openapi.TYPE_STRING),
                        "expire": openapi.Schema(type=openapi.TYPE_STRING),
                        "username": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_superuser": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    })
            }
        )
    ),
    401: openapi.Response(
        description='未经授权的访问',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                'msg': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    ),
    402: openapi.Response(
        description='验证码错误',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=402),
                'msg': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    ),
}

register_responses = {
    200: openapi.Response(
        description='操作成功',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, description='状态码', example=200),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, description='返回信息', example='注册成功'),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description='用户数据',
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户ID', example=4),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名', example='wwa112'),
                        'level': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户等级', example=0),
                        'avatar_url': openapi.Schema(type=openapi.TYPE_STRING, description='头像链接',
                                                     example='http://127.0.0.1:8000/media/CACHE/images/users/avatars/wwa112/default/85d34d380b7d9f19276c6ba53f8faaf8.jpeg'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱',
                                                example='1472078824@qq.com'),
                        'last_login': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                                     description='上次登录时间', example='2022-01-01 12:00:00'),
                        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否为超级管理员',
                                                       example=False)
                    }
                )
            }
        )
    ),
    403: openapi.Response(
        description='操作失败',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, description='状态码', example=203),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, description='错误信息', example='注册校验不通过'),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'username': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING, example='已存在一位使用该名字的用户。'),
                            description='用户名重复错误'
                        )
                    }
                )
            }
        )
    ),
    404: openapi.Response(
        description='用户已存在，请登录！',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, description='状态码', example=404),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, description='错误信息', example='用户已存在，请登录！'),
            }
        )
    ),
}

register_swagger_params = {
    'method': 'post',
    'operation_description': '用户注册。',
    'operation_summary': '用户注册。',
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'phone', 'email', 'password', 're_password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            're_password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    'responses': register_responses,
    'tags': ['用户信息']
}

login_swagger_params = {
    "method": 'post',
    "operation_description": '用户登录。',
    "operation_summary": '用户登录',
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password', 'code'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'code': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    "responses": login_responses,
    'tags': ['用户信息']
}

code_swagger_params = {
    "method": 'get',
    "operation_description": '为用户注册或登录生成验证码',
    "operation_summary": '生成验证码',
    "manual_parameters": [
        openapi.Parameter(
            name='username',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=True,
            description='生成验证码的用户名'
        ),
        openapi.Parameter(
            name='module',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=True,
            description='要为其生成验证码的模块：“register”或“login”。'
        ),
    ],
    "responses": {
        200: openapi.Response(
            description='操作成功',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'data': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        401: openapi.Response(
            description='未经授权的访问',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'msg': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
    },
    'tags': ['用户信息']
}

logout_swagger_params = {
    'method': 'get',
    'operation_description': '用户退出登录',
    'operation_summary': "用户退出登录",
    'manual_parameters': [
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            required=True,
            description='JWT 认证的 Token，格式为 Bearer + 空格 + token'
        ),
    ],
    "security": [{"Bearer": []}],
    'responses': {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='wwa11234已退出')
            }
        ),
        401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='登录已过期，请重新登录')
            }
        )

    },
    'tags': ['用户信息']
}

userinfo_swagger_params = {
    'method': 'get',
    'operation_description': '获取当前登录人的信息',
    'operation_summary': "获取当前登录用户的信息",
    'manual_parameters': [
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            required=True,
            description='JWT 认证的 Token，格式为 Bearer + 空格 + token'
        ),
    ],
    'responses': {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                        'last_login': openapi.Schema(type=openapi.TYPE_STRING,
                                                     example='2023-04-26T15:56:49.622198+08:00'),
                        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, example='wwa11234'),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING, example=''),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING, example=''),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, example='1472078824@qq.com'),
                        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                        'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        'date_joined': openapi.Schema(type=openapi.TYPE_STRING,
                                                      example='2023-04-26T12:04:46.309990+08:00'),
                        'level': openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
                        'avatar': openapi.Schema(type=openapi.TYPE_STRING,
                                                 example='http://127.0.0.1:8000/media/users/avatars/wwa11234/default.jpeg'),
                        'nickname': openapi.Schema(type=openapi.TYPE_STRING, example='小王'),
                        'phone': openapi.Schema(type=openapi.TYPE_STRING, example=''),
                        'sign': openapi.Schema(type=openapi.TYPE_STRING, example='努力！'),
                        'info': openapi.Schema(type=openapi.TYPE_STRING, example=''),
                        'current_ip': openapi.Schema(type=openapi.TYPE_STRING, example=''),
                        'last_ip': openapi.Schema(type=openapi.TYPE_STRING, example=''),
                        'groups': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                 items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                        'user_permissions': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                           items=openapi.Schema(type=openapi.TYPE_OBJECT))
                    }
                )
            }
        )
        ,
        401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='登录已过期，请重新登录')
            }
        )
    },
    'security': [{'Bearer': []}],
    'tags': ['用户信息']
}

change_password_swagger_params = {
    'method': 'post',
    'operation_description': '修改密码',
    'operation_summary': "修改用户密码",
    'manual_parameters': [
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            required=True,
            description='JWT 认证的 Token，格式为 Bearer + 空格 + token'
        ),
    ],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['current_password', 're_new_password', 'new_password'],
        properties={
            'current_password': openapi.Schema(type=openapi.TYPE_STRING, description='旧密码'),
            're_new_password': openapi.Schema(type=openapi.TYPE_STRING, description='新密码'),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='重复输入密码'),
        }
    ),
    'responses': {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='密码修改成功！'),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'new_password': openapi.Schema(type=openapi.TYPE_STRING, example='xxx123'),
                        're_new_password': openapi.Schema(type=openapi.TYPE_STRING, example='xxx123'),
                        'current_password': openapi.Schema(type=openapi.TYPE_STRING, example='xxx..123')
                    }
                )
            }
        ),
        401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='登录已过期，请重新登录')
            }
        )
    },
    'security': [{'Bearer': []}],
    'tags': ['用户信息']
}

api_record_swagger_params = {
    'method': 'post',
    'operation_summary': "保存用户交易所API信息",
    'manual_parameters': [
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            required=True,
            description='JWT 认证的 Token，格式为 Bearer + 空格 + token'
        ),
    ],
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'exchange_name', 'api_key', 'secret_key', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
            'exchange_name': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=['OKX', 'BINANCE'],
                description='交易所名称'
            ),
            'api_key': openapi.Schema(type=openapi.TYPE_STRING, description='API Key'),
            'secret_key': openapi.Schema(type=openapi.TYPE_STRING, description='Secret Key'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码')
        }),
    'responses': {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='用户API保存成功'),
            },
            description='用户API保存成功'
        ),
        401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='用户不存在'),
            },
            description='用户不存在'
        ),
        402: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=402),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='用户api保存失败'),
            },
            description='用户api保存失败'
        ),
        403: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=403),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='交易所不在支持列表中'),
            },
            description='交易所不在支持列表中'
        ),
    },
    'security': [{'Bearer': []}],
    'tags': ['用户交易所信息']
}

# 修改用户信息
change_userinfo_swagger_params = {
    'method': 'put',
    'operation_description': '修改用户信息',
    'operation_summary': "修改用户信息",
    'request_body': openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
            'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='昵称'),
            'sign': openapi.Schema(type=openapi.TYPE_STRING, description='个人签名'),
        }
    ),
    'responses': {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, example=200),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='信息修改成功！'),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'username': openapi.Schema(type=openapi.TYPE_STRING, example='admin'),
                        'nickname': openapi.Schema(type=openapi.TYPE_STRING, example='xxx'),
                        'sign': openapi.Schema(type=openapi.TYPE_STRING, example='加油！')
                    }
                )
            }
        ),
        401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_INTEGER, example=401),
                'msg': openapi.Schema(type=openapi.TYPE_STRING, example='登录已过期，请重新登录')
            }
        )
    },
    'security': [{'Bearer': []}],
    'tags': ['用户信息']
}

# 从数据库中获取用户的apikey和secret、password等信息
api_get_swagger_params = {
    'method': 'get',
    'operation_description': '获取用户交易所API密钥信息',
    'operation_summary': "获取用户交易所API密钥信息",
    'manual_parameters': [openapi.Parameter(
        'exchange_name',
        openapi.IN_QUERY,
        description='交易所名称',
        type=openapi.TYPE_STRING,
    )],
    'responses': {
        200: openapi.Response(
            description='成功获取用户交易所API密钥信息',
            examples={
                'application/json': {
                    'status': '200',
                    'data': {
                        'username': 'wwa1122',
                        'exchange_name': 'OKX',
                        'api_key': '29f89033-c5b1-4f3a-9a38-5f2a87771f91',
                        'secret_key': '27C36D75F813ED7E67CC2DF3DF6CC3A3',
                        'password': 'Wangqiang@123'
                    }
                }
            }
        ),
        401: '授权失败',
        404: '未找到指定的交易所账户信息'
    },
    'tags': ['用户交易所信息']
}

# 用户交易所余额信息
balance_swagger_params = {
    'method': 'get',
    'operation_summary': '获取用户钱包余额信息',
    'manual_parameters': [
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            required=True,
            description='JWT 认证的 Token，格式为 Bearer + 空格 + token'
        ), openapi.Parameter(
            name='page',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description='当前页, default is 1'
        ),
        openapi.Parameter(
            name='page_size',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description='总页数, default is 10'
        ),
    ],
    'responses': {
        200: openapi.Response(
            type=openapi.TYPE_OBJECT,
            description='请求成功',
            examples={
                "application/json": {
                    "status": 200,
                    "total": 2,
                    "data": [
                        {"name": "BTC", "free": 0.01, "used": 0.02, "total": 0.03, "value": 100},
                        {"name": "ETH", "free": 0.11, "used": 0.12, "total": 0.23, "value": 200},
                    ]
                }
            },
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                title="Response",
                properties={
                    "status": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description="状态码",
                        example=200
                    ),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="余额信息",
                        additional_properties=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="币种余额信息",
                            properties={
                                "free": openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description="可用数量"
                                ),
                                "used": openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description="冻结数量"
                                ),
                                "total": openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description="总量"
                                ),
                                "value": openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description="资产价值"
                                )
                            }
                        ),
                    ),
                },
            ),
        ),
        400: openapi.Response(
            type=openapi.TYPE_OBJECT,
            description='请求失败',
            examples={
                "application/json": {
                    "status": 400,
                    "msg": "api调用失败"
                }
            },
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                title="Response",
                properties={
                    "status": openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description="状态码",
                        example=400
                    ),
                    "msg": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="错误信息",
                        example="api调用失败"
                    )
                }
            ),
        ),
    },
    'tags': ['用户交易所信息']
}
