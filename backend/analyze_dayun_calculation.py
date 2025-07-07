#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究大运计算规律
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from solar_terms_utils import load_solar_terms_flat

def analyze_dayun_calculation():
    """分析大运计算规律"""
    print("=== 大运计算分析 ===")
    
    # 高泽兮案例
    birth_time = datetime(2023, 9, 14, 0, 26)
    gender = "女"
    year_gan = "癸"  # 阴年
    
    print(f"出生时间: {birth_time}")
    print(f"性别: {gender}")
    print(f"年干: {year_gan} (阴年)")
    print(f"阴年女性: 顺排")
    
    # 加载节气
    solar_terms = load_solar_terms_flat()
    
    # 找到出生前后最近的节气
    prev_term, next_term = None, None
    for term in solar_terms:
        term_dt = datetime.strptime(term["datetime"], "%Y-%m-%d %H:%M:%S")
        if term_dt <= birth_time:
            prev_term = term
        if term_dt > birth_time and not next_term:
            next_term = term
    
    print(f"\n上一个节气: {prev_term['name']} - {prev_term['datetime']}")
    print(f"下一个节气: {next_term['name']} - {next_term['datetime']}")
    
    # 计算距离
    prev_dt = datetime.strptime(prev_term["datetime"], "%Y-%m-%d %H:%M:%S")
    next_dt = datetime.strptime(next_term["datetime"], "%Y-%m-%d %H:%M:%S")
    
    days_from_prev = (birth_time - prev_dt).days
    days_to_next = (next_dt - birth_time).days
    
    print(f"\n距离上一个节气: {days_from_prev} 天")
    print(f"距离下一个节气: {days_to_next} 天")
    
    # 顺排用下一个节气，逆排用上一个节气
    is_forward = True  # 阴年女性顺排
    ref_days = days_to_next if is_forward else days_from_prev
    
    print(f"\n顺排用下一个节气: {ref_days} 天")
    
    # 不同的计算方法
    print("\n=== 不同计算方法 ===")
    
    # 方法1: 传统三天折一年
    age1 = ref_days / 3
    print(f"方法1 (三天折一年): {age1:.2f} 年")
    
    # 方法2: 一天折四个月
    age2 = ref_days * 4 / 12
    print(f"方法2 (一天折四个月): {age2:.2f} 年")
    
    # 方法3: 看看金标准的逆推算法
    gold_age = 8 + 3/12 + 14/365  # 8年3个月14天
    print(f"金标准年龄: {gold_age:.2f} 年")
    
    # 逆推需要多少天
    needed_days = gold_age * 3
    print(f"金标准需要的天数: {needed_days:.2f} 天")
    
    # 看看是否是用的逆排（上一个节气）
    if days_from_prev > 0:
        age_reverse = days_from_prev / 3
        print(f"如果逆排算法: {age_reverse:.2f} 年")
    
    # 或者有其他计算方法
    print("\n=== 特殊情况分析 ===")
    # 可能是按月建计算？
    # 或者是从立春算起？
    
    # 查找立春
    lichun_2023 = None
    lichun_2024 = None
    for term in solar_terms:
        if term["name"] == "立春":
            if term["year"] == 2023:
                lichun_2023 = term
            elif term["year"] == 2024:
                lichun_2024 = term
    
    if lichun_2023:
        lichun_dt = datetime.strptime(lichun_2023["datetime"], "%Y-%m-%d %H:%M:%S")
        days_from_lichun = (birth_time - lichun_dt).days
        print(f"距离2023年立春: {days_from_lichun} 天")
    
    if lichun_2024:
        lichun_dt = datetime.strptime(lichun_2024["datetime"], "%Y-%m-%d %H:%M:%S")
        days_to_lichun = (lichun_dt - birth_time).days
        print(f"距离2024年立春: {days_to_lichun} 天")
        age_lichun = days_to_lichun / 3
        print(f"按立春计算年龄: {age_lichun:.2f} 年")

if __name__ == "__main__":
    analyze_dayun_calculation()
