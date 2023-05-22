# ！/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: mossloo
@software: PyCharm
@file: validators.py
@time: 2023/3/27 0027 15:33
@describe: django验证器
实现：文件上传验证器：可以验证上传文件的大小、文件扩展名、MIME类型
"""
import mimetypes  # MIME类型模块
from os.path import splitext  # 分离文件名和扩展名函数
from django.core.exceptions import ValidationError  # 验证错误异常类
from django.template.defaultfilters import filesizeformat  # 文件大小格式化函数
from django.utils.deconstruct import deconstructible  # 可反序列化类装饰器
from django.utils.translation import gettext_lazy as _  # 用于翻译提示信息


# 创建一个可解构的类，用于文件验证
@deconstructible
class FileValidator(object):
    extension_message = _("Extension '%(extension)s' not allowed. " "Allowed extensions are: '%(allowed_extensions)s.'")
    mime_message = _("MIME type '%(mimetype)s' is not valid. " "Allowed types are: %(allowed_mimetypes)s.")
    min_size_message = _("The current file %(size)s, which is too small. " "The minumum file size is %(allowed_size)s.")
    max_size_message = _("The current file %(size)s, which is too large. " "The maximum file size is %(allowed_size)s.")

    def __init__(self, *args, **kwargs):
        self.allowed_extensions = kwargs.pop("allowed_extensions", None)
        self.allowed_mimetypes = kwargs.pop("allowed_mimetypes", None)
        self.min_size = kwargs.pop("min_size", 0)
        self.max_size = kwargs.pop("max_size", None)

    def __call__(self, value):
        # 检查文件扩展名
        ext = splitext(value.name)[1][1:].lower()
        if self.allowed_extensions and ext not in self.allowed_extensions:
            message = self.extension_message % {
                "extension": ext,
                "allowed_extensions": ", ".join(self.allowed_extensions),
            }
            raise ValidationError(message)

        # 检查MIME类型
        mimetype = mimetypes.guess_type(value.name)[0]
        if self.allowed_mimetypes and mimetype not in self.allowed_mimetypes:
            message = self.mime_message % {
                "mimetype": mimetype,
                "allowed_mimetypes": ", ".join(self.allowed_mimetypes),
            }
            raise ValidationError(message)

        # 检查文件大小
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                "size": filesizeformat(filesize),
                "allowed_size": filesizeformat(self.max_size),
            }

            raise ValidationError(message)

        elif filesize < self.min_size:
            message = self.min_size_message % {
                "size": filesizeformat(filesize),
                "allowed_size": filesizeformat(self.min_size),
            }

            raise ValidationError(message)
