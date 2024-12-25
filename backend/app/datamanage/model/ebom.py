#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：ebom.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/25 14:08 
'''
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key
from backend.database.db_mysql import uuid4_str
from backend.utils.timezone import timezone


class Ebom(Base):
    """dm_ebom 表"""

    __tablename__ = 'dm_ebom'

    id: Mapped[id_key] = mapped_column(init=False)
    partid: Mapped[str] = mapped_column(String(100), comment='父节点')
    level1: Mapped[str] = mapped_column(String(10), comment='层级序号')
    sync_time: Mapped[str] = mapped_column(String(100), comment='数据解析入库时间')
    file_name1: Mapped[str] = mapped_column(String(200), comment='源文件名称')
    prd_no: Mapped[str] = mapped_column(String(100), comment='产品型号')
    prd_code: Mapped[str] = mapped_column(String(100), comment='产品配置码Header')
    prd_name: Mapped[str] = mapped_column(String(100), comment='产品名称')
    prd_level: Mapped[str] = mapped_column(String(100), comment='修造级别')
    prd_vision: Mapped[str] = mapped_column(String(100), comment='产品总成版本号')
    prd_proxh: Mapped[str] = mapped_column(String(100), comment='产品型号')
    prd_link: Mapped[str] = mapped_column(String(100), comment='检修全字段')
    cn_no: Mapped[str] = mapped_column(String(200), comment='变更单号')
    cn_rels_time: Mapped[str] = mapped_column(String(200), comment='变更发布时间')
    cn_item_id: Mapped[str] = mapped_column(String(200), comment='变更图号')
    process_id: Mapped[str] = mapped_column(String(255), comment='发布流程ID')
    y8_hasmetal: Mapped[str] = mapped_column(String(200), comment='是否含有非金属材料')
    y8_weight: Mapped[str] = mapped_column(String(200), comment='重量')
    y8_matisdesc: Mapped[str] = mapped_column(String(100), comment='工业标准描述')
    bl_sequence_no: Mapped[str] = mapped_column(String(100), comment='序号')
    y8_gylx: Mapped[str] = mapped_column(String(255), comment='工艺分工')
    y8_wxsccj: Mapped[str] = mapped_column(String(100), comment='生产厂家技术状态')
    last_mod_date: Mapped[str] = mapped_column(String(100), comment='日期')
    y8_gx: Mapped[str] = mapped_column(String(100), comment='工序')
    y8_gypzl: Mapped[str] = mapped_column(String(200), comment='工艺偏置量')
    y8_grupdesc: Mapped[str] = mapped_column(String(255), comment='物料组描述')
    y8_qtgw: Mapped[str] = mapped_column(String(200), comment='其他区域工位')
    y8_cllyl: Mapped[str] = mapped_column(String(200), comment='材料利用率')
    y8_matdel: Mapped[str] = mapped_column(String(100), comment='已删除')
    y8_gyde: Mapped[str] = mapped_column(String(200), comment='工艺定额')
    y8_wxpc: Mapped[str] = mapped_column(String(100), comment='批次号')
    y8_knowledgeno: Mapped[str] = mapped_column(String(100), comment='结构树编码')
    y8_gjxd: Mapped[str] = mapped_column(String(255), comment='关键项点')
    y8_materialcode: Mapped[str] = mapped_column(String(200), comment='材料编码/规格')
    y8_beizhu: Mapped[str] = mapped_column(String(200), comment='备注')
    y8_configurationcode: Mapped[str] = mapped_column(String(200), comment='构型编码')
    y8_cldekly: Mapped[str] = mapped_column(String(200), comment='交出定额')
    y8_gysccd: Mapped[str] = mapped_column(String(255), comment='生产厂地')
    y8_cldekhs: Mapped[str] = mapped_column(String(200), comment='可回收废料')
    y8_guige: Mapped[str] = mapped_column(String(100), comment='材料规格')
    y8_sjcn: Mapped[str] = mapped_column(String(100), comment='临时更改单编号')
    y8_wwyy: Mapped[str] = mapped_column(String(200), comment='委外原因')
    y8_sjjszt: Mapped[str] = mapped_column(String(100), comment='是否技术状态项')
    bl_quantity: Mapped[str] = mapped_column(String(100), comment='bl_quantity')
    y8_isbh: Mapped[str] = mapped_column(String(200), comment='比偶换件')
    y8_wxcn: Mapped[str] = mapped_column(String(100), comment='临时更改单')
    y8_proxh: Mapped[str] = mapped_column(String(100), comment='产品型号')
    y8_zczms: Mapped[str] = mapped_column(String(200), comment='材质&供应状态')
    y8_sjpc: Mapped[str] = mapped_column(String(100), comment='批次号')
    y8_sjsccj: Mapped[str] = mapped_column(String(255), comment='生产厂家')
    y8_lldw: Mapped[str] = mapped_column(String(200), comment='领料代码')
    y8_grupcode: Mapped[str] = mapped_column(String(100), comment='物料组代码')
    y8_matdescc: Mapped[str] = mapped_column(String(255), comment='物料描述')
    y8_zpsgw: Mapped[str] = mapped_column(String(200), comment='工位代码')
    y8_wlgxmc: Mapped[str] = mapped_column(String(100), comment='工序名称')
    y8_zzjszt: Mapped[str] = mapped_column(String(100), comment='是否技术状态项')
    y8_typecode: Mapped[str] = mapped_column(String(100), comment='物料类型代码')
    y8_bsyq: Mapped[str] = mapped_column(String(200), comment='标识要求')
    item_revision_id: Mapped[str] = mapped_column(String(100), comment='版本')
    y8_glth: Mapped[str] = mapped_column(String(200), comment='关联新造图号')
    y8_configurationcodedesc: Mapped[str] = mapped_column(String(200), comment='构型')
    y8_zzpc: Mapped[str] = mapped_column(String(100), comment='批次号')
    y8_sjggxh: Mapped[str] = mapped_column(String(100), comment='规格号')
    y8_matdescs: Mapped[str] = mapped_column(String(200), comment='物料简称')
    y8_zzjx2: Mapped[str] = mapped_column(String(100), comment='制造基线图号版本号')
    y8_material2: Mapped[str] = mapped_column(String(200), comment='材料编码')
    y8_zzjx1: Mapped[str] = mapped_column(String(100), comment='制造基线工艺文件编号版本号')
    y8_zzwx: Mapped[str] = mapped_column(String(200), comment='自制/外协')
    y8_clmc: Mapped[str] = mapped_column(String(200), comment='材料名称')
    y8_guide: Mapped[str] = mapped_column(String(200), comment='规格')
    y8_gxdm: Mapped[str] = mapped_column(String(100), comment='y8_gxdm')
    object_name1: Mapped[str] = mapped_column(String(255), comment='产品名称')
    y8_soft: Mapped[str] = mapped_column(String(100), comment='软件')
    y8_sjgycj: Mapped[str] = mapped_column(String(100), comment='供应商厂家')
    y8_matbunit: Mapped[str] = mapped_column(String(200), comment='基本计量单位')
    y8_materialtype: Mapped[str] = mapped_column(String(200), comment='材料类型')
    y8_mat_provis: Mapped[str] = mapped_column(String(200), comment='外协自买料')
    y8_cllx: Mapped[str] = mapped_column(String(100), comment='材料类型')
    y8_gyfg: Mapped[str] = mapped_column(String(200))
    y8_sjjx2: Mapped[str] = mapped_column(String(100), comment='设计基线图号版本号')
    y8_xlcc: Mapped[str] = mapped_column(String(200), comment='下料尺寸')
    y8_sjjx1: Mapped[str] = mapped_column(String(100), comment='设计基线技术协议')
    y8_sjjx4: Mapped[str] = mapped_column(String(100), comment='设计基线图号版本号')
    y8_sjjx3: Mapped[str] = mapped_column(String(100), comment='设计基线采购规范号版本号采用的标准')
    y8_wxjszt: Mapped[str] = mapped_column(String(100), comment='是否技术状态项')
    object_type: Mapped[str] = mapped_column(String(200), comment='自制件/外购件')
    item_id: Mapped[str] = mapped_column(String(100), comment='产品id')
    y8_no: Mapped[str] = mapped_column(String(100), comment='y8_no')
    y8_zpsfs: Mapped[str] = mapped_column(String(200), comment='领料方式')
    y8_matname: Mapped[str] = mapped_column(String(255), comment='物料名称')
    y8_sb: Mapped[str] = mapped_column(String(100), comment='设备')
    y8_glbm: Mapped[str] = mapped_column(String(200), comment='关联新造料号')
    y8_typedesc: Mapped[str] = mapped_column(String(255), comment='物料类型描述')
    y8_scbmbm: Mapped[str] = mapped_column(String(200), comment='工艺路线情况')
    y8_zzsccj: Mapped[str] = mapped_column(String(100), comment='生产厂家')
    y8_gycn: Mapped[str] = mapped_column(String(100), comment='临时更改单编号')
    y8_werk: Mapped[str] = mapped_column(String(200), comment='工厂')
    y8_itemtype: Mapped[str] = mapped_column(String(100), comment='零部件类型')
    y8_wxggxh: Mapped[str] = mapped_column(String(100), comment='规格号')
    y8_matbnum1: Mapped[str] = mapped_column(String(100), comment='y8_matbnum1')
    y8_guide2: Mapped[str] = mapped_column(String(200), comment='材料规格')
    y8_sjjx6: Mapped[str] = mapped_column(String(100), comment='设计基线图号版本号')
    y8_gzmj: Mapped[str] = mapped_column(String(100), comment='工装模具')
    y8_wxgycj: Mapped[str] = mapped_column(String(100), comment='供应商厂家')
    y8_sjjx5: Mapped[str] = mapped_column(String(100), comment='设计基线采购规范号版本号采用的标准')
    y8_gb: Mapped[str] = mapped_column(String(100), comment='工步')
    y8_bsnr: Mapped[str] = mapped_column(String(255), comment='标识内容')
    state_now: Mapped[str] = mapped_column(String(10), comment='当前是否启用，1启用；0未启用,默认为1')