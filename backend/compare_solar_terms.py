#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比不同节气数据源的差异
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from solar_terms_utils import load_solar_terms_flat

def compare_solar_terms():
    """对比不同节气数据源"""
    print("=== 对比节气数据源 ===")
    
    birth_time = datetime(2023, 9, 14, 0, 26)
    print(f"出生时间: {birth_time}")
    
    # 完整节气数据
    full_terms = load_solar_terms_flat()
    print(f"完整节气数据: {len(full_terms)} 个")
    
    # 找到出生前后的节气
    prev_term, next_term = None, None
    for term in full_terms:
        if term["year"] == 2023:
            term_dt = datetime.strptime(term["datetime"], "%Y-%m-%d %H:%M:%S")
            if term_dt <= birth_time:
                prev_term = term
            if term_dt > birth_time and not next_term:
                next_term = term
    
    print(f"完整数据 - 上一个节气: {prev_term['name']} ({prev_term['datetime']})")
    print(f"完整数据 - 下一个节气: {next_term['name']} ({next_term['datetime']})")
    
    # 计算天数
    next_dt = datetime.strptime(next_term["datetime"], "%Y-%m-%d %H:%M:%S")
    days_to_next = (next_dt - birth_time).days
    print(f"完整数据 - 距离下一节气: {days_to_next} 天")
    print(f"完整数据 - 起运年龄: {days_to_next / 3:.2f} 年")
    
    # 简化节气数据（只有12个主要节气）
    major_terms = {
        "立春": "2023-02-04 10:42:00",
        "惊蛰": "2023-03-06 04:36:00",
        "清明": "2023-04-05 09:13:00",
        "立夏": "2023-05-06 02:19:00",
        "芒种": "2023-06-06 06:18:00",
        "小暑": "2023-07-07 16:31:00",
        "立秋": "2023-08-08 02:23:00",
        "白露": "2023-09-08 05:27:00",
        "寒露": "2023-10-08 21:16:00",
        "立冬": "2023-11-08 00:36:00",
        "大雪": "2023-12-07 17:33:00",
        "小寒": "2024-01-06 04:49:00"
    }
    
    # 找到出生前后的主要节气
    prev_major, next_major = None, None
    for name, time_str in major_terms.items():
        term_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        if term_dt <= birth_time:
            prev_major = (name, time_str)
        if term_dt > birth_time and not next_major:
            next_major = (name, time_str)
    
    print(f"\n主要节气 - 上一个节气: {prev_major[0]} ({prev_major[1]})")
    print(f"主要节气 - 下一个节气: {next_major[0]} ({next_major[1]})")
    
    # 计算天数
    next_major_dt = datetime.strptime(next_major[1], "%Y-%m-%d %H:%M:%S")
    days_to_next_major = (next_major_dt - birth_time).days
    print(f"主要节气 - 距离下一节气: {days_to_next_major} 天")
    print(f"主要节气 - 起运年龄: {days_to_next_major / 3:.2f} 年")
    
    # 对比结果
    print(f"\n=== 对比结果 ===")
    print(f"完整数据计算: {days_to_next / 3:.2f} 年")
    print(f"主要节气计算: {days_to_next_major / 3:.2f} 年")
    print(f"金标准: 8.29 年")
    
    # 分析差异
    print(f"\n=== 差异分析 ===")
    print(f"完整数据使用的是: {next_term['name']} (24节气)")
    print(f"主要节气使用的是: {next_major[0]} (12节气)")
    print(f"金标准更接近: {'主要节气' if abs(days_to_next_major / 3 - 8.29) < abs(days_to_next / 3 - 8.29) else '完整数据'}")

if __name__ == "__main__":
    compare_solar_terms()
