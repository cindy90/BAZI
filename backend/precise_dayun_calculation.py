#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确计算大运时间差
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from major_solar_terms import load_major_solar_terms_flat

def precise_dayun_calculation():
    """精确计算大运时间差"""
    print("=== 精确大运时间计算 ===")
    
    # 高泽兮案例
    birth_time = datetime(2023, 9, 14, 0, 26)
    gender = "女"
    year_gan = "癸"
    
    print(f"出生时间: {birth_time}")
    print(f"性别: {gender}")
    print(f"年干: {year_gan} (阴年)")
    print(f"阴年女性: 顺排")
    
    # 加载12个主要节气
    major_terms = load_major_solar_terms_flat()
    
    # 找到出生前后最近的节气
    prev_term, next_term = None, None
    for term in major_terms:
        if term["year"] == 2023:
            term_dt = datetime.strptime(term["datetime"], "%Y-%m-%d %H:%M:%S")
            if term_dt <= birth_time:
                prev_term = term
            if term_dt > birth_time and not next_term:
                next_term = term
    
    print(f"\n上一个主要节气: {prev_term['name']} - {prev_term['datetime']}")
    print(f"下一个主要节气: {next_term['name']} - {next_term['datetime']}")
    
    # 精确计算时间差
    next_dt = datetime.strptime(next_term["datetime"], "%Y-%m-%d %H:%M:%S")
    time_diff = next_dt - birth_time
    
    total_seconds = time_diff.total_seconds()
    total_days = total_seconds / (24 * 3600)
    
    print(f"\n时间差: {time_diff}")
    print(f"总秒数: {total_seconds}")
    print(f"总天数: {total_days:.6f}")
    
    # 传统算法：3天折1年
    years = total_days / 3
    print(f"起运年龄: {years:.6f} 年")
    
    # 转换为年月日
    full_years = int(years)
    remaining_years = years - full_years
    months = remaining_years * 12
    full_months = int(months)
    remaining_months = months - full_months
    days = remaining_months * 30  # 近似，每月30天
    
    print(f"起运年龄: {full_years}年{full_months}个月{days:.1f}天")
    
    # 对比金标准
    print(f"\n=== 对比金标准 ===")
    print(f"系统计算: {full_years}年{full_months}个月{days:.1f}天")
    print(f"金标准: 8年3个月14天")
    
    # 分析差异
    gold_years = 8 + 3/12 + 14/365
    print(f"金标准年龄: {gold_years:.6f} 年")
    print(f"系统年龄: {years:.6f} 年")
    print(f"差异: {abs(gold_years - years):.6f} 年")
    
    # 分析可能的原因
    print(f"\n=== 差异分析 ===")
    print(f"系统使用的节气: {next_term['name']} ({next_term['datetime']})")
    print(f"时间差: {total_days:.1f} 天")
    print(f"可能原因:")
    print(f"1. 节气时间精度不同")
    print(f"2. 时辰计算方法不同")
    print(f"3. 起运计算规则差异")

if __name__ == "__main__":
    precise_dayun_calculation()
