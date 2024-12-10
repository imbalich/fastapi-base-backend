#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：user.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/10 16:04 
'''
from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field, HttpUrl, model_validator
from typing_extensions import Self

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase, CustomPhoneNumber


class AuthSchemaBase(SchemaBase):
    username: str
    password: str | None


class AuthLoginParam(AuthSchemaBase):
    captcha: str


class RegisterUserParam(AuthSchemaBase):
    """
    注册用户:需要填写邮箱地址
    """
    nickname: str | None = None
    email: EmailStr = Field(examples=['user@example.com'])


class RegisterUserParamWithoutEmail(AuthSchemaBase):
    """
    注册用户:邮箱地址选填
    """
    nickname: str | None = None
    email: EmailStr | None = Field(examples=['user@example.com'])


class UserInfoSchemaBase(SchemaBase):
    dept_id: int | None = None
    username: str
    nickname: str
    email: EmailStr = Field(examples=['user@example.com'])
    phone: CustomPhoneNumber | None = None


class UpdateUserParam(UserInfoSchemaBase):
    pass


class UpdateUserRoleParam(SchemaBase):
    roles: list[int]


class AvatarParam(SchemaBase):
    url: HttpUrl = Field(description='头像 http 地址')


class GetUserInfoNoRelationDetail(UserInfoSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    dept_id: int | None = None
    id: int
    uuid: str
    avatar: str | None = None
    status: StatusType = Field(default=StatusType.enable)
    is_superuser: bool
    is_staff: bool
    is_multi_login: bool
    join_time: datetime = None
    last_login_time: datetime | None = None


class GetUserInfoListDetails(GetUserInfoNoRelationDetail):
    """
    获取用户列表详细信息
    """
    # TODO:后续补充关联关系
    model_config = ConfigDict(from_attributes=True)


class GetCurrentUserInfoDetail(GetUserInfoListDetails):
    """
    获取当前用户详细信息
    """
    model_config = ConfigDict(from_attributes=True)

    # TODO:后续补充关联关系


class CurrentUserIns(GetUserInfoListDetails):
    model_config = ConfigDict(from_attributes=True)


class ResetPasswordParam(SchemaBase):
    old_password: str
    new_password: str
    confirm_password: str
