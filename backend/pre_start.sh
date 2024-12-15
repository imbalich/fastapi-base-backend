#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : pre_start.sh.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 22:51
'''
#!/usr/bin/env bash

alembic revision --autogenerate -m "Initial migration"

alembic upgrade head

python3 ./scripts/init_data.py
