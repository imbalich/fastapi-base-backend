#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：crud_user.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/10 17:21 
'''

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import User
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


