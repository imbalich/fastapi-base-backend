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

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_role_permission
from backend.common.model import Base, id_key


class Permission(Base):
    """权限表"""
    __tablename__ = 'sys_permission'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(50), comment='菜单标题')
    name: Mapped[str] = mapped_column(String(50), comment='权限名称')
    type: Mapped[str] = mapped_column(default=0, comment='权限类型（0目录 1菜单 2功能按钮 9后端接口）')
    code: Mapped[str] = mapped_column(String(100), unique=True, comment='权限代码')
    icon: Mapped[str | None] = mapped_column(String(100), default=None, comment='菜单图标')
    path: Mapped[str | None] = mapped_column(String(200), comment='路由地址')
    component: Mapped[str | None] = mapped_column(String(255), comment='组件路径')
    perms: Mapped[str | None] = mapped_column(String(100), comment='权限标识')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    visible: Mapped[bool] = mapped_column(default=True, comment='是否显示（0隐藏 1显示）')
    status: Mapped[int] = mapped_column(default=1, comment='状态（0停用 1正常）')
    cache: Mapped[int] = mapped_column(default=1, comment='是否缓存（0否 1是）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_permission.id', ondelete='SET NULL'), default=None, index=True, comment='父权限ID'
    )
    parent: Mapped[Union['Permission', None]] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list['Permission'] | None] = relationship(init=False, back_populates='parent')

    # 权限角色多对多关联关系
    roles: Mapped[list['Role']] = relationship(init=False, secondary=sys_role_permission, back_populates='permissions')
