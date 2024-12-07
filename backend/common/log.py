#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：log.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/7 17:11 
'''
import inspect
import logging
import os

from sys import stderr, stdout

from asgi_correlation_id import correlation_id
from loguru import logger

from backend.core import path_conf
from backend.core.conf import settings


class InterceptHandler(logging.Handler):
    """
    默认处理程序，来自 loguru 文档中的示例。
    参见 https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    这个处理程序用于拦截标准 logging 模块的日志，并将其重定向到 loguru。
    """

    def emit(self, record: logging.LogRecord):
        """
        处理日志记录的方法。
        当一个日志事件发生时，logging 系统会调用这个方法。

        :param record: logging.LogRecord 对象，包含了所有的日志信息
        """
        # 尝试将 logging 的日志级别名称转换为 loguru 的对应级别
        try:
            # 使用 record.levelname（如 'INFO', 'ERROR' 等）获取 loguru 的级别名称
            level = logger.level(record.levelname).name
        except ValueError:
            # 如果转换失败（例如自定义级别），则使用原始的日志级别数值
            level = record.levelno

        # 查找发起日志消息的调用者（即实际调用 logger.xxx() 的代码位置）
        frame, depth = inspect.currentframe(), 0
        # 从当前帧开始，向上查找直到找到非 logging 模块的帧
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back  # 移动到上一帧
            depth += 1  # 增加深度计数

        # 使用 loguru 记录日志
        # opt() 方法用于设置日志记录的额外选项
        # depth: 确保日志记录显示正确的调用位置
        # exception: 如果存在异常信息，将其包含在日志中
        # log(): 使用动态级别记录日志消息
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,  # 日志级别
            record.getMessage()  # 日志消息内容
        )


def setup_logging():
    """
    设置日志系统
    From https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
    https://github.com/pawamoy/pawamoy.github.io/issues/17
    """
    # 拦截根日志记录器的所有输出
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_ROOT_LEVEL)

    # 移除所有日志处理器并将日志传播到根日志记录器
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        # 对于 uvicorn.access 和 watchfiles.main，禁止日志传播
        if 'uvicorn.access' in name or 'watchfiles.main' in name:
            logging.getLogger(name).propagate = False
        else:
            logging.getLogger(name).propagate = True

        # 调试日志处理器（已注释）
        # logging.debug(f'{logging.getLogger(name)}, {logging.getLogger(name).propagate}')

    # 移除 loguru 的所有现有处理器
    logger.remove()

    # 定义相关 ID 过滤函数
    # https://github.com/snok/asgi-correlation-id?tab=readme-ov-file#configure-logging
    # https://github.com/snok/asgi-correlation-id/issues/7
    def correlation_id_filter(record) -> bool:
        # 获取相关 ID，如果不存在则使用默认值
        cid = correlation_id.get(settings.LOG_CID_DEFAULT_VALUE)
        # 将相关 ID 截断到指定长度并添加到日志记录中
        record['correlation_id'] = cid[: settings.LOG_CID_UUID_LENGTH]
        return True

    # 配置 loguru 日志记录器
    logger.configure(
        handlers=[
            {
                'sink': stdout,  # 输出到标准输出
                'level': settings.LOG_STDOUT_LEVEL,  # 设置日志级别
                'filter': lambda record: correlation_id_filter(record) and record['level'].no <= 25,  # 过滤条件
                'format': settings.LOG_STD_FORMAT,  # 日志格式
            },
            {
                'sink': stderr,  # 输出到标准错误
                'level': settings.LOG_STDERR_LEVEL,  # 设置日志级别
                'filter': lambda record: correlation_id_filter(record) and record['level'].no >= 30,  # 过滤条件
                'format': settings.LOG_STD_FORMAT,  # 日志格式
            },
        ]
    )


def set_customize_logfile():
    # 获取日志文件存储路径
    log_path = path_conf.LOG_DIR
    # 如果日志目录不存在，则创建它
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    # 定义标准输出和标准错误日志文件的完整路径
    log_stdout_file = os.path.join(log_path, settings.LOG_STDOUT_FILENAME)
    log_stderr_file = os.path.join(log_path, settings.LOG_STDERR_FILENAME)

    # 配置 loguru 日志记录器
    # 参考文档：https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
    log_config = {
        'rotation': '10 MB',  # 当日志文件达到10MB时进行轮转
        'retention': '15 days',  # 保留最近15天的日志
        'compression': 'tar.gz',  # 使用tar.gz格式压缩旧日志
        'enqueue': True,  # 启用异步写入，提高性能
        'format': settings.LOG_FILE_FORMAT,  # 使用预定义的日志格式
    }

    # 配置标准输出日志文件
    logger.add(
        str(log_stdout_file),  # 日志文件路径
        level=settings.LOG_STDOUT_LEVEL,  # 日志级别
        **log_config,  # 使用上面定义的配置
        backtrace=False,  # 不包含异常回溯
        diagnose=False,  # 不包含诊断信息
    )

    # 配置标准错误日志文件
    logger.add(
        str(log_stderr_file),  # 日志文件路径
        level=settings.LOG_STDERR_LEVEL,  # 日志级别
        **log_config,  # 使用上面定义的配置
        backtrace=True,  # 包含异常回溯
        diagnose=True,  # 包含诊断信息
    )


log = logger
