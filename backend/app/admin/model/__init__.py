#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/9 15:57 
'''
from backend.app.admin.model.user import User
from backend.app.admin.model.role import Role
from backend.app.admin.model.menu import Menu
from backend.app.admin.model.dept import Dept
from backend.app.admin.model.user_social import UserSocial
from backend.app.admin.model.data_rule import DataRule
from backend.app.admin.model.casbin_rule import CasbinRule
from backend.app.admin.model.config import Config
from backend.app.admin.model.api import Api
from backend.app.admin.model.login_log import LoginLog
from backend.app.admin.model.opera_log import OperaLog
