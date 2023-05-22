# ！/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: mossloo
@software: PyCharm
@file: filters.py
@time: 2023/3/27 0027 15:13
@describe: 这段代码使用django filters库实现一个用于过滤Django认证系统中用户的过滤器集合
"""
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

# 获取User模型，查找和过滤用户
User = get_user_model()


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ["username"]

