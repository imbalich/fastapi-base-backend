#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : role.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 21:48
'''
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.role import (
    CreateRoleParam,
    GetRoleListDetails,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleRuleParam,
)
from backend.app.admin.service.data_rule_service import data_rule_service
from backend.app.admin.service.menu_service import menu_service
from backend.app.admin.service.role_service import role_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession
from backend.utils.serializers import select_as_dict, select_list_serialize

router = APIRouter()


@router.get('/all', summary='获取所有角色', dependencies=[DependsJwtAuth])
async def get_all_roles() -> ResponseModel:
    roles = await role_service.get_all()
    data = select_list_serialize(roles)
    return response_base.success(data=data)


@router.get('/{pk}/all', summary='获取用户所有角色', dependencies=[DependsJwtAuth])
async def get_user_all_roles(pk: Annotated[int, Path(...)]) -> ResponseModel:
    roles = await role_service.get_by_user(pk=pk)
    data = select_list_serialize(roles)
    return response_base.success(data=data)


@router.get('/{pk}/menus', summary='获取角色所有菜单', dependencies=[DependsJwtAuth])
async def get_role_all_menus(pk: Annotated[int, Path(...)]) -> ResponseModel:
    menu = await menu_service.get_role_menu_tree(pk=pk)
    return response_base.success(data=menu)


@router.get('/{pk}/rules', summary='获取角色所有数据规则', dependencies=[DependsJwtAuth])
async def get_role_all_rules(pk: Annotated[int, Path(...)]) -> ResponseModel:
    rule = await data_rule_service.get_role_rules(pk=pk)
    return response_base.success(data=rule)


@router.get('/{pk}', summary='获取角色详情', dependencies=[DependsJwtAuth])
async def get_role(pk: Annotated[int, Path(...)]) -> ResponseModel:
    role = await role_service.get(pk=pk)
    data = GetRoleListDetails(**select_as_dict(role))
    return response_base.success(data=data)


@router.get(
    '',
    summary='（模糊条件）分页获取所有角色',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_roles(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    data_scope: Annotated[int | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    role_select = await role_service.get_select(name=name, data_scope=data_scope, status=status)
    page_data = await paging_data(db, role_select, GetRoleListDetails)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建角色',
    dependencies=[
        Depends(RequestPermission('sys:role:add')),
        DependsRBAC,
    ],
)
async def create_role(obj: CreateRoleParam) -> ResponseModel:
    await role_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新角色',
    dependencies=[
        Depends(RequestPermission('sys:role:edit')),
        DependsRBAC,
    ],
)
async def update_role(pk: Annotated[int, Path(...)], obj: UpdateRoleParam) -> ResponseModel:
    count = await role_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/menu',
    summary='更新角色菜单',
    dependencies=[
        Depends(RequestPermission('sys:role:menu:edit')),
        DependsRBAC,
    ],
)
async def update_role_menus(
    request: Request, pk: Annotated[int, Path(...)], menu_ids: UpdateRoleMenuParam
) -> ResponseModel:
    count = await role_service.update_role_menu(request=request, pk=pk, menu_ids=menu_ids)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/rule',
    summary='更新角色数据权限规则',
    dependencies=[
        Depends(RequestPermission('sys:role:rule:edit')),
        DependsRBAC,
    ],
)
async def update_role_rules(
    request: Request, pk: Annotated[int, Path(...)], rule_ids: UpdateRoleRuleParam
) -> ResponseModel:
    count = await role_service.update_role_rule(request=request, pk=pk, rule_ids=rule_ids)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='（批量）删除角色',
    dependencies=[
        Depends(RequestPermission('sys:role:del')),
        DependsRBAC,
    ],
)
async def delete_role(request: Request, pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await role_service.delete(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()