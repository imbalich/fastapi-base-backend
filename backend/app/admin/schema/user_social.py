#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : user_social.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 21:21
'''
from backend.common.enums import UserSocialType
from backend.common.schema import SchemaBase


class UserSocialSchemaBase(SchemaBase):
    source: UserSocialType
    open_id: str | None = None
    uid: str | None = None
    union_id: str | None = None
    scope: str | None = None
    code: str | None = None


class CreateUserSocialParam(UserSocialSchemaBase):
    user_id: int


class UpdateUserSocialParam(SchemaBase):
    pass