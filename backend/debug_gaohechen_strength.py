#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试高赫辰的五行强弱计算
"""
from app.services.calculators import FiveElementsCalculator
from app.services.core import Bazi, StemBranch
from app.services.constants import *

def debug_gaohechen_strength():
    """调试高赫辰五行强弱计算"""
    print("=== 高赫辰五行强弱计算调试 ===")
    
    # 创建八字对象
    bazi = Bazi(
        year=StemBranch("己", "巳"),
        month=StemBranch("丁", "卯"),
        day=StemBranch("丁", "丑"),
        hour=StemBranch("辛", "亥"),
        gender="男"
    )
    
    print(f"八字: {bazi.year.stem}{bazi.year.branch} {bazi.month.stem}{bazi.month.branch} {bazi.day.stem}{bazi.day.branch} {bazi.hour.stem}{bazi.hour.branch}")
    print(f"日主: {bazi.day.stem} ({STEM_ELEMENTS[bazi.day.stem]})")
    
    # 详细计算过程
    day_stem = bazi.day.stem
    day_element = STEM_ELEMENTS[day_stem]
    
    print(f"\n日主五行: {day_element}")
    
    # 统计同党（帮身、生身）和异党（克身、泄身）的力量
    same_party_score = 0.0  # 同党得分
    different_party_score = 0.0  # 异党得分
    
    print("\n=== 天干分析 ===")
    stems = [bazi.year.stem, bazi.month.stem, bazi.day.stem, bazi.hour.stem]
    stem_names = ["年干", "月干", "日干", "时干"]
    stem_weights = [1.0, 1.5, 2.0, 1.0]  # 年月日时的权重
    
    for i, stem in enumerate(stems):
        element = STEM_ELEMENTS[stem]
        weight = stem_weights[i]
        
        if element == day_element:
            same_party_score += weight  # 同类，帮身
            print(f"{stem_names[i]}: {stem}({element}) - 同类帮身 +{weight}")
        elif element in FIVE_ELEMENTS_GENERATION and FIVE_ELEMENTS_GENERATION[element] == day_element:
            same_party_score += weight * 0.8  # 生身
            print(f"{stem_names[i]}: {stem}({element}) - 生身 +{weight * 0.8}")
        elif element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[element] == day_element:
            different_party_score += weight  # 克身
            print(f"{stem_names[i]}: {stem}({element}) - 克身 +{weight}")
        elif day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == element:
            different_party_score += weight * 0.7  # 泄身
            print(f"{stem_names[i]}: {stem}({element}) - 泄身 +{weight * 0.7}")
        else:
            print(f"{stem_names[i]}: {stem}({element}) - 其他关系 +0")
    
    print(f"天干同党得分: {same_party_score}")
    print(f"天干异党得分: {different_party_score}")
    
    print("\n=== 地支分析 ===")
    branches = [bazi.year.branch, bazi.month.branch, bazi.day.branch, bazi.hour.branch]
    branch_names = ["年支", "月支", "日支", "时支"]
    branch_weights = [0.8, 2.5, 1.5, 0.8]  # 年月日时的权重，月支权重最大
    
    for i, branch in enumerate(branches):
        element = BRANCH_ELEMENTS[branch]
        weight = branch_weights[i]
        
        if element == day_element:
            same_party_score += weight  # 同类，帮身
            print(f"{branch_names[i]}: {branch}({element}) - 同类帮身 +{weight}")
        elif element in FIVE_ELEMENTS_GENERATION and FIVE_ELEMENTS_GENERATION[element] == day_element:
            same_party_score += weight * 0.8  # 生身
            print(f"{branch_names[i]}: {branch}({element}) - 生身 +{weight * 0.8}")
        elif element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[element] == day_element:
            different_party_score += weight  # 克身
            print(f"{branch_names[i]}: {branch}({element}) - 克身 +{weight}")
        elif day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == element:
            different_party_score += weight * 0.7  # 泄身
            print(f"{branch_names[i]}: {branch}({element}) - 泄身 +{weight * 0.7}")
        else:
            print(f"{branch_names[i]}: {branch}({element}) - 其他关系 +0")
    
    print(f"地支同党得分: {same_party_score - 4.5}")  # 减去天干的得分
    print(f"地支异党得分: {different_party_score - 0.7}")  # 减去天干的得分
    
    # 计算同党vs异党的比例
    total_score = same_party_score + different_party_score
    same_party_ratio = same_party_score / total_score
    
    print(f"\n=== 最终计算 ===")
    print(f"同党总得分: {same_party_score}")
    print(f"异党总得分: {different_party_score}")
    print(f"总得分: {total_score}")
    print(f"同党占比: {same_party_ratio:.3f} ({same_party_ratio*100:.1f}%)")
    
    # 使用判断标准
    if same_party_ratio >= 0.75:
        strength = "极强"
    elif same_party_ratio >= 0.58:
        strength = "身强"
    elif same_party_ratio >= 0.45:
        strength = "平和"
    elif same_party_ratio >= 0.40:
        strength = "身弱"
    else:
        strength = "极弱"
    
    print(f"判断结果: {strength}")
    print(f"金标准: 身强")
    
    # 计算需要调整的阈值
    print(f"\n=== 阈值分析 ===")
    print(f"当前同党占比: {same_party_ratio:.3f}")
    print(f"需要调整极强阈值到: {same_party_ratio + 0.01:.2f} 以上")
    print(f"或调整身强阈值到: {same_party_ratio - 0.01:.2f} 以下")
    
    return same_party_ratio

if __name__ == "__main__":
    debug_gaohechen_strength()
