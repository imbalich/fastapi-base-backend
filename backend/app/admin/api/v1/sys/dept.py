#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : dept.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 20:50
'''
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.dept import GetDeptListDetails
from backend.app.admin.service.dept_service import dept_service
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/{pk}', summary='获取部门详情', dependencies=[DependsJwtAuth])
async def get_dept(pk: Annotated[int, Path(...)]) -> ResponseModel:
    """
    获取部门详情
    :param pk: 部门id
    :return: 部门详情
    """
    dept = await dept_service.get(pk=pk)
    data = GetDeptListDetails(**select_as_dict(dept))
    return response_base.success(data=data)


@router.get('', summary='获取所有部门展示树', dependencies=[DependsJwtAuth])
async def get_all_depts_tree(
        name: Annotated[str | None, Query()] = None,
        leader: Annotated[str | None, Query()] = None,
        phone: Annotated[str | None, Query()] = None,
        status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    dept = await dept_service.get_dept_tree(name=name, leader=leader, phone=phone, status=status)
    return response_base.success(data=dept)


@router.post(
    '',
    summary='创建部门',
    dependencies=[
        Depends(RequestPermission('sys:dept:add')),
        DependsRBAC,
    ],
)
async def create_dept(obj: CreateDeptParam) -> ResponseModel:
    await dept_service.create(obj=obj)
    return response_base.success()
