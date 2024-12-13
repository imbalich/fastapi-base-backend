#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：crud_role.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/13 14:31 
'''
from typing import Sequence

from sqlalchemy import Select, desc, select
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Menu, Role, User
from backend.app.admin.schema.role import (
    CreateRoleParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
)


class CRUDRole(CRUDPlus[Role]):
    async def get(self, db, role_id: int) -> Role | None:
        """
        获取角色
        """
        return await self.select_model(db, role_id)

    async def get_with_relation(self, db, role_id: int) -> Role | None:
        """
        获取角色和菜单
        """
        # TODO:暂时去除数据规则部分
        stmt = (
            select(self.model)
            .options(selectinload(self.model.menus))
            .where(self.model.id == role_id)
        )
        role = await db.execute(stmt)
        return role.scalars().first()

    async def get_all(self, db) -> Sequence[Role]:
        """
        获取所有角色
        """
        return await self.select_models(db)

    async def get_by_user(self, db, user_id: int) -> Sequence[Role]:
        """
        获取用户所有角色
        """
        stmt = select(self.model).join(self.model.users).where(User.id == user_id)
        roles = await db.execute(stmt)
        return roles.scalars().all()

    async def get_list(self, name: str = None, data_scope: int = None, status: int = None) -> Select:
        """
        获取角色列表
        """
        # TODO:暂时去除数据规则部分
        stmt = (
            select(self.model)
            .options(selectinload(self.model.menus))
            .order_by(desc(self.model.created_time))
        )
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if data_scope:
            where_list.append(self.model.data_scope == data_scope)
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            stmt = stmt.where(*where_list)
        return stmt

    async def get_by_name(self, db, name: str) -> Role | None:
        """
        通过 name 获取角色
        """
        return await self.select_model_by_column(db, name=name)

    async def create(self, db, obj_in: CreateRoleParam) -> None:
        """
        创建角色
        """
        await self.create_model(db, obj_in)

    async def update(self, db, role_id: int, obj_in: UpdateRoleParam) -> int:
        """
        更新角色
        """
        return await self.update_model(db, role_id, obj_in)

    async def update_menus(self, db, role_id: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        更新角色菜单
        """
        current_role = await self.get_with_relation(db, role_id)
        # 更新菜单
        stmt = select(Menu).where(Menu.id.in_(menu_ids.menus))
        menus = await db.execute(stmt)
        current_role.menus = menus.scalars().all()
        return len(current_role.menus)

    async def delete(self, db, role_id: list[int]) -> int:
        """
        删除角色
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=role_id)


role_dao: CRUDRole = CRUDRole(Role)
