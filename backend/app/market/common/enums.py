#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : enums.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/24 20:58
'''
from backend.common.enums import IntEnum


class StockMarketType(IntEnum):
    """股票市场类型"""
    nasdaq = 1
    sp = 2
    dow = 3
    nyse = 4
    other = 5
