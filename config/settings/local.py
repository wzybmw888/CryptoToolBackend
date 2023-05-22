from datetime import timedelta

from .common import *

SECRET_KEY = 'django-insecure-d!&31cge#n4$dx^!cj=*adm1bxf^y$zk)arryb^p5a(q+gvm96'

INSTALLED_APPS += []

# 允许所有域名来访问我们的服务器
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5000",  # Vue3前端的地址
# ]
CORS_ALLOW_METHODS = [
    "DELETE",
    "PUT",
    "POST",
    "GET",
    "PATCH",
    "OPTIONS"
]
CORS_ALLOW_HEADERS = [
    'Content-Type',
    "Access-Token",
    "token",
    "user",
    "Authorization",
    "username"
]

DEBUG = True

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'  # SMTP 服务器地址
EMAIL_PORT = 25  # SMTP 服务器端口
EMAIL_HOST_USER = 'lc13135698897@163.com'  # SMTP 服务器用户名
EMAIL_HOST_PASSWORD = 'PTWUXCVRDSQJJXSO'  # SMTP 服务器密码
EMAIL_USE_TLS = True  # 开启 TLS 加密
DEFAULT_FROM_EMAIL = 'lc13135698897@163.com'  # 发件人邮箱

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "CryptoTraderWeb",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "127.0.0.1",
        "PORT": 3306,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# 自定义用户模型
AUTH_USER_MODEL = 'users.UserProfile'

# 定义加密方式
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]


# 在 setting 配置认证插件的参数
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),  # 访问令牌的有效时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # 刷新令牌的有效时间

    'ROTATE_REFRESH_TOKENS': False,  # 若为True，则刷新后新的refresh_token有更新的有效时间
    'BLACKLIST_AFTER_ROTATION': True,  # 若为True，刷新后的token将添加到黑名单中,
    # When True,'rest_framework_simplejwt.token_blacklist',should add to INSTALLED_APPS

    'ALGORITHM': 'HS256',  # 对称算法：HS256 HS384 HS512  非对称算法：RSA
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,  # if signing_key, verifying_key will be ignore.
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),  # Authorization: Bearer <token>
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # if HTTP_X_ACCESS_TOKEN, X_ACCESS_TOKEN: Bearer <token>
    'USER_ID_FIELD': 'id',  # 使用唯一不变的数据库字段,将包含在生成的令牌中以标识用户

}

# swagger配置
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'token',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}



# celery 配置
broker_url = "redis://127.0.0.1:6379/9"

# 第三方社交登录配置
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': 'd405866ff18165109130',
            'secret': '3af6a3a5e79c971a66ff3d327f5eeb712d2bb1b8',
            'key': ''
        }
    }
}