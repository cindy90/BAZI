#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12个主要节气（月令）数据，用于大运计算
"""

# 12个主要节气，每个月的"节"，用于月令和大运计算
MAJOR_SOLAR_TERMS = [
    "立春", "惊蛰", "清明", "立夏", "芒种", "小暑", 
    "立秋", "白露", "寒露", "立冬", "大雪", "小寒"
]

def load_major_solar_terms_flat(json_path=None):
    """
    加载12个主要节气数据（月令）并转换为扁平list
    只取每个月的"节"，不取"气"
    """
    from solar_terms_utils import load_solar_terms_flat
    
    # 加载所有节气
    all_terms = load_solar_terms_flat(json_path)
    
    # 过滤出12个主要节气
    major_terms = []
    for term in all_terms:
        if term["name"] in MAJOR_SOLAR_TERMS:
            major_terms.append(term)
    
    # 按时间排序
    from datetime import datetime
    major_terms.sort(key=lambda x: datetime.strptime(x["datetime"], "%Y-%m-%d %H:%M:%S"))
    
    return major_terms
