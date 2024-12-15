#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : api.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 22:20
'''
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import MethodType
from backend.common.schema import SchemaBase


class ApiSchemaBase(SchemaBase):
    name: str
    method: MethodType = Field(default=MethodType.GET, description='请求方法')
    path: str = Field(description='api路径')
    remark: str | None = None


class CreateApiParam(ApiSchemaBase):
    pass


class UpdateApiParam(ApiSchemaBase):
    pass


class GetApiListDetails(ApiSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
