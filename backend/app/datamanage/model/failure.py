#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：failure.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 14:23 
'''
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key
from backend.database.db_mysql import uuid4_str


class Failure(Base):
    """国铁历史故障数据"""

    __tablename__ = 'dm_failure'

    report_id: Mapped[str] = mapped_column(String(100), primary_key=True, comment='报告编号（必填且唯一）')
    road_subdivision: Mapped[str] = mapped_column(String(255), comment='所属路局（一级配属）')
    discovery_location: Mapped[str] = mapped_column(String(255), comment='发现地点（二级配属）')
    product_lifetime_stage: Mapped[str] = mapped_column(String(255), comment='产品寿命阶段')
    discovery_date: Mapped[str] = mapped_column(String(30), comment='发现时间（日期）')
    response_time: Mapped[str] = mapped_column(String(255), comment='信息响应时间（h）')
    product_model: Mapped[str] = mapped_column(String(255), comment='产品型号')
    product_number: Mapped[str] = mapped_column(String(255), comment='产品编号')
    manufacturing_date: Mapped[str] = mapped_column(String(30), comment='新造出厂日期（日期）')
    last_maintenance_date: Mapped[str] = mapped_column(String(30), comment='最近检修出厂日期（日期）')
    train_type: Mapped[str] = mapped_column(String(255), comment='机车型号（车型）')
    train_number: Mapped[str] = mapped_column(String(255), comment='机车编号')
    car_number: Mapped[str] = mapped_column(String(255), comment='车厢号')
    axle_position: Mapped[str] = mapped_column(String(255), comment='轴位')
    total_mileage_and_consistent: Mapped[str] = mapped_column(String(255), comment='车组总运行里程和总运行里程是否一致')
    repair_after_mileage_and_consistent: Mapped[str] = mapped_column(String(255),
                                                                     comment='车组检修后运行里程和检修后运行里程是否一致')
    fault_location: Mapped[str] = mapped_column(String(255), comment='终判故障部位')
    fault_material_code: Mapped[str] = mapped_column(String(255), comment='终判故障部位物料编码')
    fault_type: Mapped[str] = mapped_column(String(255), comment='终判故障类型')
    fault_mode: Mapped[str] = mapped_column(String(255), comment='终判故障模式')
    fault_location_duplicate: Mapped[str] = mapped_column(String(255), comment='故障地点是否和发现地点重复？')
    fault_interval_start: Mapped[str] = mapped_column(String(255), comment='故障区间（起点）')
    fault_interval_end: Mapped[str] = mapped_column(String(255), comment='故障区间（终点）')
    train_run: Mapped[str] = mapped_column(String(255), comment='担当车次')
    run_circuit_start: Mapped[str] = mapped_column(String(255), comment='运行交路（起点）')
    run_circuit_end: Mapped[str] = mapped_column(String(255), comment='运行交路（终点）')
    fault_part_number: Mapped[str] = mapped_column(String(255), comment='故障件编号')
    fault_description: Mapped[str] = mapped_column(LONGTEXT, comment='故障描述')
    handling_method_and_unresolved_problems: Mapped[str] = mapped_column(String(2000), comment='处理方式及未解决问题')
    replacement_part_number: Mapped[str] = mapped_column(String(255), comment='更换件编号')
    handling_method: Mapped[str] = mapped_column(String(255), comment='处理方法')
    failure_date: Mapped[str] = mapped_column(String(30), comment='现场故障处理完成日期(日期)')
    accident_classification: Mapped[str] = mapped_column(String(255), comment='事故类别')
    severity: Mapped[str] = mapped_column(String(255), comment='严重度')
    maintenance_location: Mapped[str] = mapped_column(String(255), comment='检修地点')
    remark: Mapped[str] = mapped_column(String(255), comment='备注')
    maintenance_type: Mapped[str] = mapped_column(String(255), comment='检修类别')
    analysis_responsible_person: Mapped[str] = mapped_column(String(255), comment='分析负责人')
    fault_classification: Mapped[str] = mapped_column(LONGTEXT, comment='故障分类')
    cause_analysis: Mapped[str] = mapped_column(LONGTEXT, comment='原因分析')
    measures: Mapped[str] = mapped_column(LONGTEXT, comment='措施')
    analysis_status: Mapped[str] = mapped_column(String(255), comment='分析情况')
    final_fault_responsibility: Mapped[str] = mapped_column(String(255), comment='最终判责')
    supplier_name: Mapped[str] = mapped_column(String(255), comment='供方名称')
    months: Mapped[str] = mapped_column(String(255), comment='月份')
    unit_quantity: Mapped[str] = mapped_column(String(255), comment='单位量')
    product_series: Mapped[str] = mapped_column(String(255), comment='产品系列')
    locomotive_type: Mapped[str] = mapped_column(String(255), comment='机车类别车型类别')
    is_zero_distance: Mapped[str] = mapped_column(String(255), comment='是否零公里(是/否)')
    is_operating_fault: Mapped[str] = mapped_column(String(255), comment='是否运营故障(是/否)')
    product_type: Mapped[str] = mapped_column(String(255), comment='产品类型')
    is_source: Mapped[str] = mapped_column(String(255), comment='是否源头(是/否)')
    is_ours: Mapped[str] = mapped_column(String(128), comment='是否为永济公司产品(是/否)')
    is_closedloop: Mapped[str] = mapped_column(String(128), comment='是否闭环(是/否)')
    job_duration: Mapped[str] = mapped_column(String(20), comment='作业时长')
    tenant_id: Mapped[str] = mapped_column(String(128), comment='租户')
    statistic_end_time: Mapped[str] = mapped_column(String(32), comment='统计截至时间(算法运行时间)')
