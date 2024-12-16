#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：init_db.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/16 16:35 
'''


# 数据初始化脚本

import asyncio
from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model import User, Role, Dept
from backend.common.security.jwt import get_hash_password
from backend.database.db_mysql import async_db_session, create_table


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话
    """
    async with async_db_session() as session:
        yield session


async def init_super_user():
    """
    初始化超级管理员
    """
    async for db in get_db():
        try:
            # 检查是否已存在超级管理员
            stmt = select(User).where(User.is_superuser == True)
            result = await db.execute(stmt)
            super_user = result.scalar_one_or_none()

            if super_user:
                print("超级管理员已存在，跳过初始化")
                return

            # 创建开发部门结构
            dev_dept = Dept(
                name="开发组",
                level=0,
                sort=0,
                leader="admin",
                phone="13800138000",
                email="dev@example.com",
                status=1,
                del_flag=False
            )
            db.add(dev_dept)
            await db.flush()

            # 创建子部门：后端组
            backend_dept = Dept(
                name="后端组",
                level=1,
                sort=1,
                leader="admin",
                phone="13800138001",
                email="backend@example.com",
                status=1,
                del_flag=False,
                parent_id=dev_dept.id
            )
            db.add(backend_dept)

            # 创建子部门：前端组
            frontend_dept = Dept(
                name="前端组",
                level=1,
                sort=2,
                leader="admin",
                phone="13800138002",
                email="frontend@example.com",
                status=1,
                del_flag=False,
                parent_id=dev_dept.id
            )
            db.add(frontend_dept)
            await db.flush()

            # 创建超级管理员角色
            super_role = Role(
                name="超级管理员",
                code="superadmin",
                status=1,
                data_scope=0,  # 全部数据权限
                remark="超级管理员角色"
            )
            db.add(super_role)
            await db.flush()

            # 创建超级管理员用户
            super_user = User(
                username="admin",
                nickname="超级管理员",
                password=get_hash_password("admin123"),
                email="admin@example.com",
                is_superuser=True,
                is_staff=True,
                status=1,
                dept_id=dev_dept.id  # 将超级管理员放在开发组
            )

            # 关联角色
            super_user.roles.append(super_role)

            db.add(super_user)
            await db.commit()

            print("初始化成功！")
            print("=== 超级管理员信息 ===")
            print("账号：admin")
            print("密码：admin123")
            print("\n=== 部门结构 ===")
            print("开发组")
            print("├── 后端组")
            print("└── 前端组")

        except Exception as e:
            await db.rollback()
            print(f"初始化失败：{str(e)}")
            raise


async def init_data():
    """
    初始化数据
    """
    try:
        # 创建数据库表
        await create_table()
        print("数据库表创建成功！")

        # 初始化超级管理员
        await init_super_user()
    except Exception as e:
        print(f"数据初始化失败：{str(e)}")


if __name__ == "__main__":
    asyncio.run(init_data())