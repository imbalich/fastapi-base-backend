#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：permission_middleware.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/11 17:37 
'''
# backend/middleware/permission_middleware.py
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.core.conf import settings
from backend.common.exception.errors import ForbiddenError
from backend.utils.serializers import MsgSpecJSONResponse


class PermissionMiddleware(BaseHTTPMiddleware):
    """权限验证中间件"""

    async def dispatch(self, request: Request, call_next) -> Response:
        # 白名单路径直接放行
        if request.url.path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
            return await call_next(request)

        # 获取当前用户
        user = request.state.user
        if not user:
            return await call_next(request)

        # 超级管理员直接放行
        if user.is_superuser:
            return await call_next(request)

        try:
            # 验证权限
            if not await self._check_permission(request, user):
                raise ForbiddenError(msg="没有访问权限")

            # 设置数据权限范围
            request.state.data_scope = await self._get_data_scope(user)

            return await call_next(request)

        except ForbiddenError as e:
            return MsgSpecJSONResponse(
                content={"code": e.code, "msg": e.msg, "data": None},
                status_code=e.code
            )

    async def _check_permission(self, request: Request, user) -> bool:
        """检查用户是否有权限访问当前路径"""
        path = request.url.path
        method = request.method.lower()

        # 获取用户所有权限
        perms = set()
        for role in user.roles:
            if role.status != 1:  # 角色未启用
                continue
            for perm in role.permissions:
                if perm.status != 1:  # 权限未启用
                    continue
                if perm.type == 'A':  # API权限
                    perms.add(perm.code)

        # 检查是否有权限
        required_perm = f"{path}:{method}"
        return required_perm in perms

    async def _get_data_scope(self, user) -> dict:
        """获取用户数据权限范围"""
        if not user.roles:
            return {"type": "self"}

        # 获取最大数据权限范围
        scopes = [role.data_scope for role in user.roles if role.status == 1]
        if not scopes:
            return {"type": "self"}

        max_scope = min(scopes)  # 数字越小，权限范围越大

        if max_scope == 0:  # 全部数据
            return {"type": "all"}
        elif max_scope == 1:  # 自定义数据
            # TODO: 实现自定义数据权限
            return {"type": "custom", "dept_ids": []}
        elif max_scope == 2:  # 本部门及以下
            # TODO: 获取部门及其所有子部门
            return {"type": "dept_and_below", "dept_id": user.dept_id}
        elif max_scope == 3:  # 本部门
            return {"type": "dept", "dept_id": user.dept_id}
        else:  # 仅本人
            return {"type": "self"}
