#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：router.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/13 16:42 
'''
from fastapi import APIRouter

from backend.app.admin.api.router import v1 as admin_v1
from backend.app.task.api.router import v1 as task_v1
from backend.app.datamanage.api.router import v1 as datamanage_v1
from backend.core.conf import settings

route = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

route.include_router(admin_v1)
route.include_router(task_v1)
route.include_router(datamanage_v1)
