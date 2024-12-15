# fastapi-base-backend
借鉴（抄袭）自[FBA](https://github.com/fastapi-practices/fastapi_best_architecture)项目，用于构建个人未来开发的通用后台模板工程，基于FBA的基础上进行自定义的改进。

# 修改原则
该版本主要修改为了作为小范围/小团队使用的内部工具平台服务，故做出如下限制：
1. 不允许用户注册，只允许内部人员使用，账号只能由管理员注册和赋权（接口保留，配合前端去除此功能）
2. 所有操作必须有记录，不允许用户直接删除操作记录

# 修订记录
1. 24/12/8 #001： 更改mysql连接使用的异步操作引擎库为`aiomysql`,Windows环境下因为原`asyncmy`库存在某些问题，如需使用`asyncmy`请自行解决存在的问题。
2. 2024/12/15 #002： 去除模板生成模块
3. 2024/12/16 #003： 初步定版V1 FBB自改自用项目

# 项目构建
## 项目依赖
每次更新完项目后生成依赖`pip freeze > requirements.txt`

继续开发之前安装依赖`pip install -r requirements.txt`

# 注意事项
## 环境配置
1. 请复制环境变量文件，并将其中关键字段更改，尤其是token部分请重新生成并保密
2. `backend/core/conf.py`中的配置请按需更改
3. 在`backend/scripts/init_data.py`初始化数据脚本处xx行修改数据，启动`backend/pre_start.sh`脚本初始化迁移和插入初始数据