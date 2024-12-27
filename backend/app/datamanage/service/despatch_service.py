#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：despatch_service.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/26 16:52 
'''
from typing import Sequence

from fastapi import Request

from backend.app.datamanage.crud.crud_despatch import despatch_dao
from backend.app.datamanage.model import Despatch
from backend.common.exception import errors
from backend.database.db import async_db_session


class DespatchService:

    @staticmethod
    async def get_models() -> Sequence[Despatch.model]:
        async with async_db_session() as db:
            models = await despatch_dao.get_models(db)
            if not models:
                raise errors.NotFoundError(msg='发运数据中未找到型号')
            return models


despatch_service: DespatchService = DespatchService()
