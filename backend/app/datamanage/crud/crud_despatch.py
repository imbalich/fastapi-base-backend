#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：crud_despatch.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/26 16:51 
'''
from typing import Sequence

from sqlalchemy import Select, select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.datamanage.model import Despatch


class CRUDDespatch(CRUDPlus[Despatch]):

    async def get_models(self, db: AsyncSession) -> Sequence[Despatch.model] | None:
        """
        获取所有的model
        """
        stmt = select(distinct(self.model.model)).order_by(self.model.model)
        result = await db.execute(stmt)
        models = result.scalars().all()
        return models


despatch_dao: CRUDDespatch = CRUDDespatch(Despatch)
