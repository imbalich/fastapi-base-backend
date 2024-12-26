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

from backend.database.db import CurrentSession

router = APIRouter()


@router.post('', summary='（模糊条件）分页获取所有发运数据')
async def get_pagination_despatch(
        db: CurrentSession,
        model: Annotated[int | None, Query()] = None,  # 产品型号
        identifier: Annotated[str | None, Query()] = None,  # 产品编码
        repair_level: Annotated[str | None, Query()] = None,  # 修理级别
        repair_level_num: Annotated[int | None, Query()] = None,  # 修级序号
        life_cycle_time: Annotated[list[str] | None, Query(None, description="出厂日期范围，格式：[YYYY-MM-DD, YYYY-MM-DD]")] = None
):
    pass