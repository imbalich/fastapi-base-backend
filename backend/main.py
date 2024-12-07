#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/7 16:44 
'''
from pathlib import Path

import uvicorn

from backend.core.registrar import register_app

app = register_app()

if __name__ == '__main__':
    # 如果你喜欢在 IDE 中进行 DEBUG，main 启动方法会很有帮助
    # 如果你喜欢通过 print 方式进行调试，建议使用 fastapi cli 方式启动服务
    try:
        config = uvicorn.Config(app=f'{Path(__file__).stem}:app', reload=True)
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
