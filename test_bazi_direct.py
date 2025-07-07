#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接测试 Bazi 类的增强功能
"""

import sys
import os

# 直接添加路径到具体模块
backend_services_path = os.path.join(os.path.dirname(__file__), 'backend', 'app', 'services')
sys.path.insert(0, backend_services_path)

# 导入模块
from core import Bazi, StemBranch
from calculators import FiveElementsCalculator, ShenShaCalculator
from constants import *
from datetime import datetime

def test_enhanced_bazi():
    """测试增强版 Bazi 类"""
    print("=== 测试增强版 Bazi 类 ===")
    
    # 创建测试八字: 甲子年 丙寅月 戊申日 甲寅时
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "申"),
        hour=StemBranch("甲", "寅"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    print(f"测试八字: {bazi}")
    
    # 测试新增的方法
    print("\n--- 基础信息获取 ---")
    print(f"所有天干: {bazi.get_all_stems()}")
    print(f"所有地支: {bazi.get_all_branches()}")
    
    print("\n--- 五行分析 ---")
    print(f"五行分布: {bazi.get_elements_distribution()}")
    print(f"主导五行: {bazi.get_dominant_element()}")
    print(f"天干五行: {bazi.get_stem_elements()}")
    print(f"地支五行: {bazi.get_branch_elements()}")
    
    print("\n--- 统计分析 ---")
    print(f"甲出现次数: {bazi.count_stem_occurrences('甲')}")
    print(f"寅出现次数: {bazi.count_branch_occurrences('寅')}")
    print(f"甲的位置: {bazi.find_stem_positions('甲')}")
    print(f"寅的位置: {bazi.find_branch_positions('寅')}")
    
    print("\n--- 位置查询 ---")
    print(f"日支元素: {bazi.get_position_element('日')}")
    print(f"月支: {bazi.get_position_branch('月')}")
    print(f"时干: {bazi.get_position_stem('时')}")
    
    print("\n--- 藏干分析 ---")
    hidden_stems = bazi.get_hidden_stems_in_branches()
    print(f"各支藏干: {hidden_stems}")
    
    print("\n--- 关系分析 ---")
    relationships = bazi.analyze_branch_relationships("申")
    print(f"申与命局关系: {relationships}")
    
    print("\n--- 季节和强弱 ---")
    print(f"月令季节: {bazi.get_month_season()}")
    print(f"日主强弱: {bazi.is_day_master_strong()}")
    
    print("\n--- 组合检查 ---")
    print(f"是否有甲寅组合: {bazi.has_stem_branch_combination('甲', '寅')}")
    print(f"是否有乙亥组合: {bazi.has_stem_branch_combination('乙', '亥')}")
    
    # 测试五行计算
    print("\n--- 五行计算测试 ---")
    scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
    print(f"五行得分: {scores}")
    
    strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
    print(f"日主强度: {strength:.2f}")
    
    favorable = FiveElementsCalculator.get_favorable_elements(bazi)
    print(f"喜用神: {favorable}")
    
    percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi)
    print(f"五行百分比: {percentages}")
    
    return bazi

if __name__ == "__main__":
    try:
        test_enhanced_bazi()
        print("\n✅ 测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
