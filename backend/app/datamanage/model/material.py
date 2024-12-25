#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：material.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 14:19 
'''
from datetime import date
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Material(Base):
    """物料个数统计表"""

    __tablename__ = 'dm_material'

    id: Mapped[id_key] = mapped_column(init=False)

    product_model: Mapped[str] = mapped_column(String(100), comment='型号')
    material_code: Mapped[str] = mapped_column(String(100), comment='物料号')
    material_name: Mapped[str] = mapped_column(String(100), comment='物料名称')
    total_quantity: Mapped[int] = mapped_column(Integer, comment='物料总数量')
    load_time: Mapped[date] = mapped_column(Date, comment='物料数量计算时间')