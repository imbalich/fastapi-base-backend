#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : crud_user_social.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 21:19
'''
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import UserSocial
from backend.app.admin.schema.user_social import CreateUserSocialParam
from backend.common.enums import UserSocialType


class CRUDOUserSocial(CRUDPlus[UserSocial]):
    async def get(self, db: AsyncSession, pk: int, source: UserSocialType) -> UserSocial | None:
        """
        获取用户社交账号绑定
        """
        return await self.select_model_by_column(db, user_id=pk, source=source)

    async def create(self, db: AsyncSession, obj_in: CreateUserSocialParam) -> None:
        """
        创建用户社交账号绑定
        """
        await self.create_model(db, obj_in)

    async def delete(self, db: AsyncSession, social_id: int) -> int:
        """
        删除用户社交账号绑定
        """
        return await self.delete_model(db, social_id)


user_social_dao: CRUDOUserSocial = CRUDOUserSocial(UserSocial)
