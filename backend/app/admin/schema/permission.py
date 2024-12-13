#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：permission.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/12 15:39 
'''
from datetime import datetime
from pydantic import ConfigDict, Field
from backend.common.enums import PermissionType, StatusType, MethodType
from backend.common.schema import SchemaBase


# 基础权限模型
class PermissionBase(SchemaBase):
    """权限基础模型"""
    name: str = Field(..., description='权限名称')
    code: str = Field(..., description='权限标识码')
    type: PermissionType
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


# 前端权限模型
class FrontendPermissionBase(PermissionBase):
    """前端权限基础模型（目录/菜单/按钮）"""
    title: str = Field(..., description='显示名称')
    sort: int = Field(default=0, ge=0)
    show: StatusType = Field(default=StatusType.enable)
    parent_id: int | None = Field(default=None)

    # 可选字段
    icon: str | None = Field(default=None)
    path: str | None = Field(default=None)
    component: str | None = Field(default=None)
    cache: StatusType = Field(default=StatusType.enable)


class CreateFrontendPermissionParam(FrontendPermissionBase):
    """创建前端权限请求"""
    pass


class UpdateFrontendPermissionParam(FrontendPermissionBase):
    """更新前端权限请求"""
    pass


class GetFrontendPermissionDetails(FrontendPermissionBase):
    """前端权限详情"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None


# API权限模型
class APIPermissionBase(PermissionBase):
    """API权限基础模型"""
    api_path: str = Field(..., description='API路径')
    method: MethodType = Field(..., description='HTTP方法')


class CreateAPIPermissionParam(APIPermissionBase):
    """创建API权限请求"""
    pass


class UpdateAPIPermissionParam(APIPermissionBase):
    """更新API权限请求"""
    pass


class GetAPIPermissionDetails(APIPermissionBase):
    """API权限详情"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
