#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：product.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 14:00 
'''
from datetime import date

from sqlalchemy import String, Date, Float
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Product(Base):
    """产品信息表"""

    __tablename__ = 'dm_product'

    id: Mapped[id_key] = mapped_column(init=False)
    large_class: Mapped[str] = mapped_column(String(255), comment='产品大类')
    product_type: Mapped[str] = mapped_column(String(255), comment='产品类型')
    apply_area: Mapped[str] = mapped_column(String(255), comment='应用领域')
    apply_area_desc: Mapped[str] = mapped_column(String(255), comment='应用领域（细分）')
    product_sub: Mapped[str] = mapped_column(String(255), comment='产品子类')
    sub_name: Mapped[str] = mapped_column(String(255), comment='产品名称')
    sub_saet: Mapped[str] = mapped_column(String(255), comment='产品系列')
    model: Mapped[str] = mapped_column(String(255), comment='产品型号')
    industry_unit: Mapped[str] = mapped_column(String(255), comment='产业单元')
    repair_priot: Mapped[str] = mapped_column(String(255), comment='维修周期')
    attach_train: Mapped[str] = mapped_column(String(255), comment='配属车型')
    attach_convert: Mapped[str] = mapped_column(String(255), comment='配套变流器')
    attach_module_num: Mapped[str] = mapped_column(String(255), comment='配套模块数量')
    cooling_mode: Mapped[str] = mapped_column(String(255), comment='冷却方式')
    voltage_level: Mapped[str] = mapped_column(String(255), comment='电压等级')
    structure: Mapped[str] = mapped_column(String(255), comment='轴承结构')
    repair_times: Mapped[int] = mapped_column(comment='修级间隔天数')
    avg_worktime: Mapped[int] = mapped_column(comment='日均工作小时')
    avg_speed: Mapped[float] = mapped_column(Float, comment='平均时速')
    year_days: Mapped[int] = mapped_column(comment='年运行天数')
    update_time: Mapped[date] = mapped_column(Date, comment='变更时间')
    mark: Mapped[str] = mapped_column(String(255), comment='备注')
    prd_big_type: Mapped[str] = mapped_column(String(200), comment='自定义类别')