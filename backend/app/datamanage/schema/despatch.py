#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：despatch.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 14:56 
'''
from datetime import date
from typing import Optional

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class DespatchSchemaBase(SchemaBase):
    model: Optional[str] = Field(None, description='model')
    identifier: Optional[str] = Field(None, description='identifier')
    attach_company: Optional[str] = Field(None, description='配属路局')
    attach_dept: Optional[str] = Field(None, description='配属路段')
    cust_name: Optional[str] = Field(None, description='客户名称')
    dopt_name: Optional[str] = Field(None, description='库房名称')
    factory_name: Optional[str] = Field(None, description='工厂名称')
    repair_level: Optional[str] = Field(None, description='修理级别')
    life_cycle_time: Optional[date] = Field(None, description='出厂日期')
    repair_level_num: Optional[int] = Field(None, description='修级序号')
    date_source: Optional[str] = Field(None, description='数据来源')
    sync_time: Optional[date] = Field(None, description='生成时间')


class CreateDespatchParam(DespatchSchemaBase):
    pass


class GetDespatchParam(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model: str = Field(..., description='产品型号')
    identifier: str = Field(..., description='产品编号')
    repair_level: str = Field(..., description='修理级别')
    life_cycle_time: date = Field(..., description='出厂日期')
    repair_level_num: int = Field(..., description='修级序号')


class GetDespatchDetails(GetDespatchParam):
    model_config = ConfigDict(from_attributes=True)

    attach_company: Optional[str] = Field(None, description='配属路局')
    attach_dept: Optional[str] = Field(None, description='配属路段')
    cust_name: Optional[str] = Field(None, description='客户名称')
    dopt_name: Optional[str] = Field(None, description='库房名称')
    factory_name: Optional[str] = Field(None, description='工厂名称')
    date_source: Optional[str] = Field(None, description='数据来源')
    sync_time: Optional[date] = Field(None, description='生成时间')


class GetDespatchListResponse(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    items: list[GetDespatchDetails] = Field(default_factory=list, description="查询结果列表")
    total: int = Field(default=0, ge=0, description="总记录数")
