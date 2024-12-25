#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：repair.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 14:24 
'''
from datetime import date
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Repair(Base):
    """造修阶段表"""

    __tablename__ = 'dm_repair'

    id: Mapped[id_key] = mapped_column(init=False)

    id_repair: Mapped[int] = mapped_column(Integer, comment='修级顺序')
    repair_levels: Mapped[str] = mapped_column(String(255), comment='造修阶段')
    model: Mapped[str] = mapped_column(String(255), comment='产品型号')
    creator: Mapped[str] = mapped_column(String(255), comment='创建人')
    create_time: Mapped[date] = mapped_column(Date, comment='创建时间')