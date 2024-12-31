#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 16:39 
'''
from fastapi import APIRouter

from backend.app.datamanage.api.v1.datamanage.despatch import router as despatch_router

router = APIRouter(prefix="/datamanage")

router.include_router(despatch_router, prefix="/despatch", tags=["发运数据"])
