#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend
@File    ：stock.py
@IDE     ：PyCharm
@Author  ：imbalich
@Date    ：2024/12/24
'''
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Stock(Base):
    """股票基础信息"""
    __tablename__ = 'market_stock'

    id: Mapped[id_key] = mapped_column(init=False)

    # 基础信息 (很少/不变)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='股票代码')
    name: Mapped[str] = mapped_column(String(100), comment='股票名称')
    market: Mapped[int] = mapped_column(default=1, comment='交易市场(1:NASDAQ 2:SP500 3:DOW 4:NYSE)')
    sector: Mapped[str | None] = mapped_column(String(100), index=True, comment='板块')
    industry: Mapped[str | None] = mapped_column(String(100), index=True, comment='行业')

    # 状态
    status: Mapped[int] = mapped_column(default=1, comment='状态(0:停用 1:正常)')
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

