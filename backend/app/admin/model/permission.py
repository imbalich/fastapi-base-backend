#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：permission.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/11 15:52 
'''
from typing import Union

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_role_permission
from backend.common.enums import PermissionType, StatusType
from backend.common.model import Base, id_key


class Permission(Base):
    """权限表"""

    __tablename__ = 'sys_permission'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='权限名称')
    code: Mapped[str] = mapped_column(String(100), unique=True, comment='权限标识码')
    type: Mapped[int] = mapped_column(default=PermissionType.directory, comment='权限类型（0目录 1菜单 2按钮 9后端接口）')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    status: Mapped[int] = mapped_column(default=1, comment='权限状态（0停用 1正常）')

    # 前端权限特有字段
    title: Mapped[str | None] = mapped_column(String(50), comment='显示名称')
    icon: Mapped[str | None] = mapped_column(String(100), default=None, comment='图标')
    path: Mapped[str | None] = mapped_column(String(200), default=None, comment='路由地址')
    component: Mapped[str | None] = mapped_column(String(255), default=None, comment='组件路径')
    show: Mapped[int] = mapped_column(default=1, comment='是否显示（0否 1是）')
    cache: Mapped[int] = mapped_column(default=1, comment='是否缓存（0否 1是）')

    # API权限特有字段
    api_path: Mapped[str | None] = mapped_column(String(200), default=None, comment='API路径')
    method: Mapped[str | None] = mapped_column(String(20), default=None, comment='HTTP方法')

    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')

    # 父级权限一对多（仅前端权限使用）
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_permission.id', ondelete='SET NULL'), default=None, index=True, comment='父权限ID'
    )
    parent: Mapped[Union['Permission', None]] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list['Permission'] | None] = relationship(init=False, back_populates='parent')

    # 权限角色多对多
    roles: Mapped[list['Role']] = relationship(init=False, secondary=sys_role_permission, back_populates='permissions')
