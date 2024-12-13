#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：token.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/13 16:26 
'''
from datetime import datetime

from backend.app.admin.schema.user import GetUserInfoNoRelationDetail
from backend.common.schema import SchemaBase


class GetSwaggerToken(SchemaBase):
    access_token: str
    token_type: str = 'Bearer'
    user: GetUserInfoNoRelationDetail


class AccessTokenBase(SchemaBase):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime


class GetNewToken(AccessTokenBase):
    pass


class GetLoginToken(AccessTokenBase):
    user: GetUserInfoNoRelationDetail
