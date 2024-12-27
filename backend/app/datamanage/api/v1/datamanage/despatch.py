#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：despatch.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 16:40 
'''
from typing import Annotated

from fastapi import APIRouter, Query

from backend.app.datamanage.service.despatch_service import despatch_service
from backend.common.response.response_schema import response_base, ResponseModel
from backend.database.db import CurrentSession

router = APIRouter()

"""
接口需求:
1.获取发运数据中所有型号的接口：用于支持前端的下拉框选择
2.获取发运数据中所有修理级别的接口：用于支持前端的下拉框选择
3.（模糊条件）分页获取所有发运数据
"""


@router.get('/models', summary='获取发运数据中所有型号')
async def get_despatch_models() -> ResponseModel:
    models = await despatch_service.get_models()
    return response_base.success(data=models)
