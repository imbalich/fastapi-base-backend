#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：init_db.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/16 16:35 
'''

import asyncio
from typing import AsyncGenerator

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model import User, Role, Dept, Menu, Api
from backend.common.security.jwt import get_hash_password
from backend.database.db_mysql import async_db_session


async def init_test_data():
    """
    初始化测试数据
    """
    async with async_db_session() as db:
        async with db.begin():
            try:
                # 清空数据库
                # 删除所有表的数据
                tables = ['sys_user_role', 'sys_role_menu', 'sys_user', 'sys_role', 'sys_menu', 'sys_api', 'sys_dept']
                for table in tables:
                    await db.execute(text(f"DELETE FROM {table}"))
                    await db.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))

                # 1. 创建部门
                test_dept = Dept(
                    name="test",
                    level=0,
                    sort=0,
                    leader=None,
                    phone=None,
                    email=None,
                    status=1,
                    del_flag=False
                )
                db.add(test_dept)
                await db.flush()

                # 2. 创建API
                apis = [
                    Api(name="创建API", method="POST", path="/api/v1/apis", remark=None),
                    Api(name="删除API", method="DELETE", path="/api/v1/apis", remark=None),
                    Api(name="编辑API", method="PUT", path="/api/v1/apis/{pk}", remark=None)
                ]
                for api in apis:
                    db.add(api)
                await db.flush()

                # 3. 创建菜单
                menus = [
                    Menu(title="测试", name="test", level=0, sort=0, menu_type=0, status=0, show=0, cache=1, remark=None),
                    Menu(title="仪表盘", name="dashboard", level=0, sort=0, icon="IconDashboard", path="dashboard", menu_type=0, status=1, show=1, cache=1, remark=None),
                    Menu(title="工作台", name="Workplace", level=0, sort=0, path="workplace", menu_type=1, component="/dashboard/workplace/index.vue", status=1, show=1, cache=1, parent_id=2, remark=None),
                    Menu(title="系统管理", name="admin", level=0, sort=0, icon="IconSettings", path="admin", menu_type=0, status=1, show=1, cache=1, remark=None),
                    Menu(title="部门管理", name="SysDept", level=0, sort=0, path="sys-dept", menu_type=1, component="/admin/dept/index.vue", status=1, show=1, cache=1, parent_id=4, remark=None),
                    Menu(title="用户管理", name="SysUser", level=0, sort=0, path="sys-user", menu_type=1, component="/admin/user/index.vue", status=1, show=1, cache=1, parent_id=4, remark=None),
                    Menu(title="角色管理", name="SysRole", level=0, sort=0, path="sys-role", menu_type=1, component="/admin/role/index.vue", status=1, show=1, cache=1, parent_id=4, remark=None),
                    Menu(title="菜单管理", name="SysMenu", level=0, sort=0, path="sys-menu", menu_type=1, component="/admin/menu/index.vue", status=1, show=1, cache=1, parent_id=4, remark=None),
                    Menu(title="API 管理", name="SysApi", level=0, sort=0, path="sys-api", menu_type=1, component="/admin/api/index.vue", status=1, show=1, cache=1, parent_id=4, remark=None),
                    Menu(title="数据规则管理", name="SysDataRule", level=0, sort=0, path="sys-data-rule", menu_type=1, component="/admin/data-rule/index.vue", status=1, show=1, cache=1, parent_id=4, remark=None),
                    Menu(title="系统自动化", name="automation", level=0, sort=0, icon="IconCodeSquare", path="automation", menu_type=0, status=1, show=1, cache=1, remark=None),
                    Menu(title="代码生成", name="CodeGenerator", level=0, sort=0, path="code-generator", menu_type=1, component="/automation/generator/index.vue", status=1, show=1, cache=1, parent_id=11, remark=None),
                    Menu(title="系统监控", name="monitor", level=0, sort=0, icon="IconComputer", path="monitor", menu_type=0, status=1, show=1, cache=1, remark=None),
                    Menu(title="Redis 监控", name="Redis", level=0, sort=0, path="redis", menu_type=1, component="/monitor/redis/index.vue", perms="sys:monitor:redis", status=1, show=1, cache=1, parent_id=13, remark=None),
                    Menu(title="服务器监控", name="Server", level=0, sort=0, path="server", menu_type=1, component="/monitor/server/index.vue", perms="sys:monitor:server", status=1, show=1, cache=1, parent_id=13, remark=None),
                    Menu(title="日志", name="log", level=0, sort=0, icon="IconBug", path="log", menu_type=0, status=1, show=1, cache=1, remark=None),
                    Menu(title="登录日志", name="Login", level=0, sort=0, path="login", menu_type=1, component="/log/login/index.vue", status=1, show=1, cache=1, parent_id=16, remark=None),
                    Menu(title="操作日志", name="Opera", level=0, sort=0, path="opera", menu_type=1, component="/log/opera/index.vue", status=1, show=1, cache=1, parent_id=16, remark=None)
                ]
                for menu in menus:
                    db.add(menu)
                await db.flush()

                # 4. 创建角色
                test_role = Role(
                    name="test",
                    code="test",
                    data_scope=2,
                    status=1,
                    remark=None
                )
                db.add(test_role)
                await db.flush()

                # 5. 角色-菜单关联
                await db.execute(
                    text("INSERT INTO sys_role_menu (role_id, menu_id) VALUES (:role_id, :menu_id)"),
                    {"role_id": test_role.id, "menu_id": menus[0].id}
                )

                # 6. 创建用户
                test_user = User(
                    username="admin",
                    nickname="用户88888",
                    password="$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.",  # 密码: 123456
                    email="admin@example.com",
                    is_superuser=True,
                    is_staff=True,
                    status=1,
                    is_multi_login=False,
                    dept_id=test_dept.id
                )
                db.add(test_user)
                await db.flush()

                # 7. 用户-角色关联
                await db.execute(
                    text("INSERT INTO sys_user_role (user_id, role_id) VALUES (:user_id, :role_id)"),
                    {"user_id": test_user.id, "role_id": test_role.id}
                )

                print("初始化成功！")
                print("=== 测试用户信息 ===")
                print("账号：admin")
                print("密码：123456")

            except Exception as e:
                print(f"初始化失败：{str(e)}")
                raise


async def init_data():
    """
    初始化数据
    """
    try:
        # 初始化测试数据
        await init_test_data()
    except Exception as e:
        print(f"数据初始化失败：{str(e)}")


if __name__ == "__main__":
    asyncio.run(init_data())