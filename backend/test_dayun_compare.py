#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
大运算法与金标准对比分析脚本
"""
from app.services.calculators import FiveElementsCalculator
from app.services.core import StemBranch
from solar_terms_utils import load_solar_terms_flat
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 金标准案例（可扩展）
GOLD_CASES = [
    {
        "name": "高泽兮",
        "gender": "女",
        "birth": datetime(2023, 9, 14, 0, 26),
        "year_gan": "癸",
        "month_pillar": "辛酉",
        "gold_dayun": [
            {"ganzhi": "壬戌", "start_age": 8},
            {"ganzhi": "癸亥", "start_age": 18},
            {"ganzhi": "甲子", "start_age": 28},
            {"ganzhi": "乙丑", "start_age": 38},
            {"ganzhi": "丙寅", "start_age": 48},
            {"ganzhi": "丁卯", "start_age": 58},
        ]
    },
    {
        "name": "高赫辰",
        "gender": "男",
        "birth": datetime(1989, 3, 18, 21, 20),
        "year_gan": "己",
        "month_pillar": "丁卯",
        "gold_dayun": [
            {"ganzhi": "丙寅", "start_age": 8},
            {"ganzhi": "乙丑", "start_age": 18},
            {"ganzhi": "甲子", "start_age": 28},
            {"ganzhi": "癸亥", "start_age": 38},
            {"ganzhi": "壬戌", "start_age": 48},
            {"ganzhi": "辛酉", "start_age": 58},
        ]
    },
    # 可继续添加其他金标准案例
]

def compare_dayun(case, solar_terms):
    print(f"\n=== {case['name']} 大运对比 ===")
    sys_start, sys_start_age, sys_luck, sys_start_age2, forward_str = FiveElementsCalculator.calculate_precise_dayun(
        case["birth"], case["gender"], case["year_gan"], case["month_pillar"], solar_terms)
    print(f"顺逆排: {forward_str}")
    print(f"系统起运年龄: {sys_start_age}")
    print(f"金标准起运年龄: {case['gold_dayun'][0]['start_age']}")
    print("\n金标准大运:")
    for d in case["gold_dayun"]:
        print(f"  {d['ganzhi']} ({d['start_age']}岁)")
    print("\n系统大运:")
    for i, d in enumerate(sys_luck[:len(case['gold_dayun'])]):
        print(f"  {d.stem_branch.stem}{d.stem_branch.branch} ({d.start_age}岁)")
    # 差异分析
    print("\n差异分析:")
    for i, gold in enumerate(case["gold_dayun"]):
        sys = sys_luck[i]
        match = (gold["ganzhi"] == sys.stem_branch.stem + sys.stem_branch.branch) and (gold["start_age"] == sys.start_age)
        print(f"  {i+1}. {gold['ganzhi']}({gold['start_age']}) vs {sys.stem_branch.stem}{sys.stem_branch.branch}({sys.start_age}) {'✓' if match else '❌'}")
    print("-"*40)

def main():
    solar_terms = load_solar_terms_flat()
    for case in GOLD_CASES:
        compare_dayun(case, solar_terms)

if __name__ == "__main__":
    main()
