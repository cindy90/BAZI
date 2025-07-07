#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
在 services 目录中直接测试 Bazi 类增强功能
"""

import sys
import os

# 直接在 services 目录中运行
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入相关模块
import core
import constants
from datetime import datetime

def test_bazi_enhancements():
    """测试 Bazi 类的增强功能"""
    print("=== 测试 Bazi 类增强功能 ===")
    
    # 创建测试八字
    bazi = core.Bazi(
        year=core.StemBranch("甲", "子"),
        month=core.StemBranch("丙", "寅"), 
        day=core.StemBranch("戊", "申"),
        hour=core.StemBranch("甲", "寅"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    print(f"测试八字: {bazi}")
    print(f"详细表示: {bazi.__repr__()}")
    
    # 测试基础信息获取
    print("\n--- 基础信息获取 ---")
    print(f"所有天干: {bazi.get_all_stems()}")
    print(f"所有地支: {bazi.get_all_branches()}")
    print(f"所有干支: {bazi.get_all_stem_branches()}")
    
    # 测试五行分析
    print("\n--- 五行分析 ---")
    elements_dist = bazi.get_elements_distribution()
    print(f"五行分布: {elements_dist}")
    print(f"主导五行: {bazi.get_dominant_element()}")
    print(f"天干五行: {bazi.get_stem_elements()}")
    print(f"地支五行: {bazi.get_branch_elements()}")
    
    # 测试统计分析
    print("\n--- 统计分析 ---")
    print(f"甲出现次数: {bazi.count_stem_occurrences('甲')}")
    print(f"寅出现次数: {bazi.count_branch_occurrences('寅')}")
    print(f"甲的位置: {bazi.find_stem_positions('甲')}")
    print(f"寅的位置: {bazi.find_branch_positions('寅')}")
    
    # 测试位置查询
    print("\n--- 位置查询 ---")
    print(f"日支元素: {bazi.get_position_element('日')}")
    print(f"月支: {bazi.get_position_branch('月')}")
    print(f"时干: {bazi.get_position_stem('时')}")
    
    # 测试藏干分析
    print("\n--- 藏干分析 ---")
    hidden_stems = bazi.get_hidden_stems_in_branches()
    print(f"各支藏干: {hidden_stems}")
    
    # 测试关系分析
    print("\n--- 关系分析 ---")
    relationships = bazi.analyze_branch_relationships("申")
    print(f"申与命局关系: {relationships}")
    
    # 测试季节和强弱
    print("\n--- 季节和强弱 ---")
    print(f"月令季节: {bazi.get_month_season()}")
    print(f"日主强弱: {bazi.is_day_master_strong()}")
    
    # 测试组合检查
    print("\n--- 组合检查 ---")
    print(f"是否有甲寅组合: {bazi.has_stem_branch_combination('甲', '寅')}")
    print(f"是否有乙亥组合: {bazi.has_stem_branch_combination('乙', '亥')}")
    
    print("\n✅ 所有测试完成！")

if __name__ == "__main__":
    try:
        test_bazi_enhancements()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
