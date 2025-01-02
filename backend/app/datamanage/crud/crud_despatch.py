#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：crud_despatch.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/26 16:51 
'''
from typing import Sequence, Any

from sqlalchemy import Select, select, distinct, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.datamanage.model import Despatch


class CRUDDespatch(CRUDPlus[Despatch]):

    async def get_distinct_column_values(self, db: AsyncSession, column_name: str) -> Sequence[Any]:
        """
        获取指定列的所有唯一值
        :param db: 数据库会话
        :param column_name: 列名
        :return: 唯一值列表
        """
        # 确保列名存在于模型中
        if not hasattr(self.model, column_name):
            raise ValueError(f"Column {column_name} does not exist in model {self.model.__name__}")

        # 构建查询
        column = getattr(self.model, column_name)
        stmt = select(distinct(column)).order_by(column)
        # 执行查询
        result = await db.execute(stmt)

        # 返回结果
        return result.scalars().all()

    async def get_list(self, model: str = None, identifier: str = None, repair_level: str = None,
                       time_range: list[str] = None) -> Select:
        stmt = select(self.model).order_by(desc(self.model.model))
        where_list = []
        if model:
            where_list.append(self.model.model == model)
        if identifier is not None:
            where_list.append(self.model.identifier == identifier)
        if repair_level is not None:
            where_list.append(self.model.repair_level == repair_level)
        if time_range:
            where_list.append(self.model.life_cycle_time.between(time_range[0], time_range[1]))
        if where_list:
            stmt = stmt.where(*where_list)
        return stmt


despatch_dao: CRUDDespatch = CRUDDespatch(Despatch)
