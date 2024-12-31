#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：replace.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 14:24 
'''
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Replace(Base):
    """必换件表"""

    __tablename__ = 'dm_replace'

    id: Mapped[id_key] = mapped_column(init=False)
    model: Mapped[str] = mapped_column(String(30), comment='型号')
    material_name: Mapped[str] = mapped_column(String(50), comment='零部件名称')
    material_code: Mapped[str] = mapped_column(String(50), comment='零部件物料编码')
    replace_level: Mapped[str] = mapped_column(String(50), comment='修造级别')
    replace_cycle: Mapped[float] = mapped_column(Float, comment='必换周期')
