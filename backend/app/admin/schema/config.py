#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : config.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 22:20
'''
from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class SaveConfigParam(SchemaBase):
    name: str
    key: str
    value: str


class AnyConfigSchemaBase(SchemaBase):
    name: str
    type: str | None
    key: str
    value: str
    is_frontend: bool
    remark: str | None


class CreateAnyConfigParam(AnyConfigSchemaBase):
    pass


class UpdateAnyConfigParam(AnyConfigSchemaBase):
    pass


class GetAnyConfigListDetails(AnyConfigSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
