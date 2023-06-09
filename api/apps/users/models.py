import os
import random

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from imagekit.models import ImageSpecField  # 图片处理模块
from pilkit.processors import ResizeToFill  # 图片处理器
from users.avatar_generator import AvatarGenerator
from utils.validators import FileValidator
from django.utils.translation import gettext_lazy as _  # 用于翻译提示信息


# Create your models here.
def default_sign():
    signs = ["开心最重要", "努力！", "加油！"]
    return random.choice(signs)


def default_nickname():
    nicknames = ["小王", "小红", "小李"]
    return random.choice(nicknames)


def user_avatar_path(instance, filename):
    # 用户头像存储路径的构建函数，将头像按照用户名存储到 users/avatars 目录下。
    return os.path.join("users", "avatars", instance.username, filename)


class UserProfile(AbstractUser):
    AVATAR_MAX_SIZE = 2 * 1024 * 1024
    AVATAR_ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
    AVATAR_DEFAULT_FILENAME = "default.jpeg"
    LEVEL_TYPE = ((0, "普通用户"), (1, "管理员"))
    level = models.CharField(max_length=50, verbose_name="角色", choices=LEVEL_TYPE, default=0, null=False)
    avatar = models.ImageField(
        _("avatar"),
        upload_to=user_avatar_path,
        validators=[FileValidator(max_size=AVATAR_MAX_SIZE, allowed_extensions=AVATAR_ALLOWED_EXTENSIONS)],
        blank=True,
    )
    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[ResizeToFill(70, 70)],
        format="jpeg",
        options={"quality": 100},
    )
    nickname = models.CharField(max_length=30, verbose_name="用户昵称", default=default_nickname)
    phone = models.CharField(max_length=11)
    sign = models.CharField(max_length=50, verbose_name="个人签名", default=default_sign)
    info = models.CharField(max_length=150, verbose_name="个人简介", default='')
    current_ip = models.CharField(max_length=32, verbose_name="用户当前ip地址", blank=True, null=True)
    last_ip = models.CharField(max_length=32, verbose_name="用户上一次访问的ip地址", blank=True, null=True)

    class Meta:
        db_table = "user_profile"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.avatar:
                self.set_default_avatar()
        super(UserProfile, self).save(*args, **kwargs)

    def set_default_avatar(self):
        avatar_byte_array = AvatarGenerator.generate(self.username)
        self.avatar.save(
            self.AVATAR_DEFAULT_FILENAME,
            ContentFile(avatar_byte_array),
            save=False,
        )


class UserExchangeAccount(models.Model):
    Exchange = [
        ("OKX", "OKX"),
        ("BINANCE", "BINANCE"),
    ]
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="usernames")
    exchange_name = models.CharField(max_length=18, choices=Exchange)
    api_key = models.CharField(max_length=64, blank=True, null=True)
    secret_key = models.CharField(max_length=64, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=True,verbose_name="api密码")

    class Meta:
        db_table = "user_exchange_account"
        verbose_name = "用户交易所资金余额"
        verbose_name_plural = verbose_name


