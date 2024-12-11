#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：user.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/9 15:57 
'''

from datetime import datetime
from typing import Union

from sqlalchemy import VARBINARY, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_user_role
from backend.common.model import Base, id_key
from backend.database.db_mysql import uuid4_str
from backend.utils.timezone import timezone


class User(Base):
    """用户表"""

    __tablename__ = 'sys_user'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String(50), init=False, default_factory=uuid4_str, unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='用户名')
    # 作为通用后台考虑，昵称最好不可重复，但是作为内部工具平台，内部人员姓名存在重复的情况，故改为可重复
    nickname: Mapped[str] = mapped_column(String(20), unique=False, comment='昵称')
    password: Mapped[str | None] = mapped_column(String(255), comment='密码')
    # 作为通用平台，邮箱不可重复必须（用于注册，或邮件通知），作为内部工具平台，如果没有企业内部邮箱则做保留并不在业务逻辑中使用！
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment='邮箱')
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='超级权限(0否 1是)')
    is_staff: Mapped[bool] = mapped_column(default=False, comment='后台管理登陆(0否 1是)')
    status: Mapped[int] = mapped_column(default=1, comment='用户账号状态(0停用 1正常)')
    is_multi_login: Mapped[bool] = mapped_column(default=False, comment='是否重复登陆(0否 1是)')
    # 用户头像，作为一种静态资源，使用场景不确定，故作保留
    avatar: Mapped[str | None] = mapped_column(String(255), default=None, comment='头像')
    # 手机号，具有通用使用意义，不适用可在业务逻辑或schema中去除此项，数据库部分建议保留
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='手机号')
    join_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='注册时间')
    last_login_time: Mapped[datetime | None] = mapped_column(init=False, onupdate=timezone.now, comment='上次登录')

    # 部门用户一对多
    dept_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None, comment='所属部门ID'
    )
    dept: Mapped[Union['Dept', None]] = relationship(init=False, back_populates='users')

    # 用户社交信息一对多
    socials: Mapped[list['UserSocial']] = relationship(init=False, back_populates='user')

    # 用户角色多对多
    roles: Mapped[list['Role']] = relationship(init=False, secondary=sys_user_role, back_populates='users')
