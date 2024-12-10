#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：jwt.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/10 16:16 
'''
from datetime import timedelta

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic_core import from_json
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.dataclasses import RefreshToken, AccessToken, NewToken
from backend.common.exception.errors import TokenError
from backend.core.conf import settings
from backend.database.db_redis import redis_client
from backend.utils.timezone import timezone

# JWT authorizes dependency injection
DependsJwtAuth = Depends(HTTPBearer())

# 创建 CryptContext 实例
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    """
    使用 bcrypt 算法加密密码

    :param password: 原始密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码

    :param plain_password: 待验证的明文密码
    :param hashed_password: 存储的哈希密码
    :return: 验证是否成功
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(sub: str, multi_login: bool) -> AccessToken:
    """
    生成加密的访问令牌

    :param sub: JWT 的主题/用户ID
    :param multi_login: 用户是否允许多点登录
    :return: AccessToken 对象，包含访问令牌和其过期时间
    """
    # 计算访问令牌的过期时间
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
    expire_seconds = settings.TOKEN_EXPIRE_SECONDS

    # 准备要编码到 JWT 中的数据
    to_encode = {'exp': expire, 'sub': sub}

    # 使用 JWT 库创建访问令牌
    access_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)

    # 如果不允许多点登录，删除该用户之前的所有访问令牌
    if multi_login is False:
        key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{sub}'
        await redis_client.delete_prefix(key_prefix)

    # 在 Redis 中存储新的访问令牌
    key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{access_token}'
    await redis_client.setex(key, expire_seconds, access_token)

    # 返回 AccessToken 对象
    return AccessToken(access_token=access_token, access_token_expire_time=expire)


async def create_refresh_token(sub: str, multi_login: bool) -> RefreshToken:
    """
    生成加密的刷新令牌，仅用于创建新的访问令牌

    :param sub: JWT 的主题/用户ID
    :param multi_login: 用户是否允许多点登录
    :return: RefreshToken 对象，包含刷新令牌和其过期时间
    """
    # 计算刷新令牌的过期时间
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    expire_seconds = settings.TOKEN_REFRESH_EXPIRE_SECONDS

    # 准备要编码到 JWT 中的数据
    to_encode = {'exp': expire, 'sub': sub}

    # 使用 JWT 库创建刷新令牌
    refresh_token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)

    # 如果不允许多点登录，删除该用户之前的所有刷新令牌
    if multi_login is False:
        key_prefix = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}'
        await redis_client.delete_prefix(key_prefix)

    # 在 Redis 中存储新的刷新令牌
    key = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}'
    await redis_client.setex(key, expire_seconds, refresh_token)

    # 返回 RefreshToken 对象
    return RefreshToken(refresh_token=refresh_token, refresh_token_expire_time=expire)


async def create_new_token(sub: str, token: str, refresh_token: str, multi_login: bool) -> NewToken:
    """
    生成新的令牌对（新的访问令牌和刷新令牌）

    :param sub: JWT 的主题/用户ID
    :param token: 当前的访问令牌
    :param refresh_token: 当前的刷新令牌
    :param multi_login: 用户是否允许多点登录
    :return: NewToken 对象，包含新的访问令牌和刷新令牌及其过期时间
    """
    # 验证刷新令牌是否存在且有效
    redis_refresh_token = await redis_client.get(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}')
    if not redis_refresh_token or redis_refresh_token != refresh_token:
        raise TokenError(msg='Refresh Token 已过期')

    # 创建新的访问令牌
    new_access_token = await create_access_token(sub, multi_login)
    # 创建新的刷新令牌
    new_refresh_token = await create_refresh_token(sub, multi_login)

    # 删除旧的访问令牌和刷新令牌
    token_key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}'
    refresh_token_key = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}'
    await redis_client.delete(token_key)
    await redis_client.delete(refresh_token_key)

    # 返回新的令牌对
    return NewToken(
        new_access_token=new_access_token.access_token,
        new_access_token_expire_time=new_access_token.access_token_expire_time,
        new_refresh_token=new_refresh_token.refresh_token,
        new_refresh_token_expire_time=new_refresh_token.refresh_token_expire_time,
    )


def get_token(request: Request) -> str:
    """
    从请求头中获取 Bearer 令牌

    :param request: FastAPI 的 Request 对象
    :return: 提取的令牌字符串
    :raises TokenError: 如果令牌格式不正确或不存在
    """
    # 从请求头中获取 Authorization 字段
    authorization = request.headers.get('Authorization')

    # 解析 Authorization 头，分离出认证方案和令牌
    scheme, token = get_authorization_scheme_param(authorization)

    # 验证认证方案是否为 Bearer
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError(msg='Token 无效')

    # 返回提取的令牌
    return token


def jwt_decode(token: str) -> int:
    """
    解码 JWT 令牌并提取用户 ID

    :param token: JWT 令牌字符串
    :return: 解码后的用户 ID
    :raises TokenError: 如果令牌无效、过期或解码失败
    """
    try:
        # 解码 JWT 令牌
        payload = jwt.decode(
            token,
            settings.TOKEN_SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM]
        )

        # 从解码后的载荷中提取用户 ID
        user_id = int(payload.get('sub'))

        # 验证用户 ID 是否存在
        if not user_id:
            raise TokenError(msg='Token 无效')

    except ExpiredSignatureError:
        # 捕获令牌过期异常
        raise TokenError(msg='Token 已过期')

    except (JWTError, Exception):
        # 捕获其他 JWT 相关错误或一般异常
        raise TokenError(msg='Token 无效')

    # 返回解码后的用户 ID
    return user_id


async def get_current_user(db: AsyncSession, pk: int) -> User:
    """
    通过用户ID获取当前用户信息并进行验证

    :param db: 异步数据库会话
    :param pk: 用户ID
    :return: 用户对象
    :raises TokenError: 如果用户不存在
    :raises AuthorizationError: 如果用户或其关联实体（部门、角色）状态异常
    """
    from backend.app.admin.crud.crud_user import user_dao

    # 获取用户信息及其关联数据
    user = await user_dao.get_with_relation(db, user_id=pk)

    # 验证用户是否存在
    if not user:
        raise TokenError(msg='Token 无效')

    # 检查用户状态
    if not user.status:
        raise AuthorizationError(msg='用户已被锁定，请联系系统管理员')

    # 检查用户部门状态
    if user.dept_id:
        if not user.dept.status:
            raise AuthorizationError(msg='用户所属部门已被锁定，请联系系统管理员')
        if user.dept.del_flag:
            raise AuthorizationError(msg='用户所属部门已被删除，请联系系统管理员')

    # 检查用户角色状态
    if user.roles:
        role_status = [role.status for role in user.roles]
        if all(status == 0 for status in role_status):
            raise AuthorizationError(msg='用户所属角色已被锁定，请联系系统管理员')

    return user
