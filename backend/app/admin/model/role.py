#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：role.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/9 16:03 
'''
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_user_role, sys_role_permission
from backend.common.model import Base, id_key


class Role(Base):
    """角色表"""

    __tablename__ = 'sys_role'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='角色名称')
    code: Mapped[str] = mapped_column(String(100), unique=True, comment='角色编码')
    data_scope: Mapped[int | None] = mapped_column(
        default=0,
        comment='数据权限范围（0: 全部数据，1: 自定义数据，2: 所在部门及以下数据，3: 所在部门数据，4: 仅本人数据）',
    )
    status: Mapped[int] = mapped_column(default=1, comment='角色状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')

    # 角色用户多对多
    users: Mapped[list['User']] = relationship(init=False, secondary=sys_user_role, back_populates='roles')

    # 角色菜单多对多
    permissions: Mapped[list['Permission']] = relationship(init=False, secondary=sys_role_permission,
                                                           back_populates='roles')

    # TODO:暂时不做数据权限的设计，先完成RBAC的功能，再做数据权限的设计
