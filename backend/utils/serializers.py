#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：serializers.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/7 16:51 
'''
from decimal import Decimal
from typing import Any, Sequence, TypeVar

from fastapi.encoders import decimal_encoder
from msgspec import json
from sqlalchemy import Row, RowMapping
from sqlalchemy.orm import ColumnProperty, SynonymProperty, class_mapper
from starlette.responses import JSONResponse

RowData = Row | RowMapping | Any

R = TypeVar('R', bound=RowData)


def select_columns_serialize(row: R) -> dict:
    """
    序列化 SQLAlchemy 选择的表列，不包含关系列

    :param row: 行数据
    :return: 序列化后的字典
    """
    result = {}
    for column in row.__table__.columns.keys():
        v = getattr(row, column)
        if isinstance(v, Decimal):
            v = decimal_encoder(v)
        result[column] = v
    return result


def select_list_serialize(row: Sequence[R]) -> list:
    """
    序列化 SQLAlchemy 选择列表

    :param row: 行数据序列
    :return: 序列化后的列表
    """
    result = [select_columns_serialize(_) for _ in row]
    return result


def select_as_dict(row: R, use_alias: bool = False) -> dict:
    """
    将 SQLAlchemy 选择转换为字典，可以包含关系数据，
    取决于选择对象本身的属性

    如果设置 use_alias 为 True，列名将作为别名返回，
    如果列中不存在别名，我们不建议将其设置为 True

    :param row: 行数据
    :param use_alias: 是否使用别名
    :return: 转换后的字典
    """
    if not use_alias:
        result = row.__dict__
        if '_sa_instance_state' in result:
            del result['_sa_instance_state']
    else:
        result = {}
        mapper = class_mapper(row.__class__)
        for prop in mapper.iterate_properties:
            if isinstance(prop, (ColumnProperty, SynonymProperty)):
                key = prop.key
                result[key] = getattr(row, key)

    return result


class MsgSpecJSONResponse(JSONResponse):
    """使用高性能 msgspec 库将数据序列化为 JSON 的 JSON 响应。"""

    def render(self, content: Any) -> bytes:
        return json.encode(content)