#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：crud_user.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/10 17:21 
'''
import bcrypt

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import User, Role
from backend.app.admin.schema.user import RegisterUserParam, AddUserParam
from backend.common.security.jwt import get_hash_password
from backend.utils.timezone import timezone


class CRUDUser(CRUDPlus[User]):
    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        """
        获取用户信息
        """
        return await self.select_model(db, user_id)

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """
        通过 username 获取用户
        """
        return await self.select_model_by_column(db, username=username)

    async def get_by_nickname(self, db: AsyncSession, nickname: str) -> User | None:
        """
        通过 nickname 获取用户
        """
        return await self.select_model_by_column(db, nickname=nickname)

    async def update_login_time(self, db: AsyncSession, username: str) -> int:
        """
        更新用户登录时间
        """
        return await self.update_model_by_column(db, {'last_login_time': timezone.now()}, username=username)

    async def create(self, db: AsyncSession, obj: RegisterUserParam, *, social: bool = False) -> None:
        """
        创建用户
        """
        if not social:
            obj.password = get_hash_password(obj.password)
        dict_obj = obj.model_dump()
        dict_obj.update({'is_staff': True})
        new_use = self.model(**dict_obj)
        db.add(new_use)

    async def add(self, db: AsyncSession, obj: AddUserParam) -> None:
        """
        后台添加用户
        """
        obj.password = get_hash_password(obj.password)
        dict_obj = obj.model_dump(exclude={'roles'})  # 先删除 roles 字段
        new_user = self.model(**dict_obj)
        role_list = []
        for role_id in obj.roles:
            role_list.append(await db.get(Role, role_id))
        new_user.roles.extend(role_list)
        db.add(new_user)

    async def get_with_relation(self, db: AsyncSession, *, user_id: int = None, username: str = None) -> User | None:
        """
        获取用户和（部门，角色，权限）
        """
        stmt = select(self.model).options(
            selectinload(self.model.dept),
            selectinload(self.model.roles).options(
                selectinload(Role.permissions)
                # TODO:后期可能添加数据权限
            ),
        )
        filters = []
        if user_id:
            filters.append(self.model.id == user_id)
        if username:
            filters.append(self.model.username == username)
        user = await db.execute(stmt.where(*filters))
        return user.scalars().first()


user_dao: CRUDUser = CRUDUser(User)
