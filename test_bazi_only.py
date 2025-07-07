#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接测试 Bazi 类的新增方法
"""

import sys
import os

# 直接添加路径
backend_services_path = os.path.join(os.path.dirname(__file__), 'backend', 'app', 'services')
sys.path.insert(0, backend_services_path)

# 只导入 core 和 constants
from core import Bazi, StemBranch
from datetime import datetime

def test_bazi_methods():
    """测试 Bazi 类的新增方法"""
    print("=== 测试 Bazi 类新增方法 ===")
    
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
    print(f"八字详情: {bazi.__repr__()}")
    
    # 测试基础信息获取
    print("\n--- 基础信息获取 ---")
    print(f"所有天干: {bazi.get_all_stems()}")
    print(f"所有地支: {bazi.get_all_branches()}")
    print(f"所有干支: {bazi.get_all_stem_branches()}")
    
    # 测试五行分析
    print("\n--- 五行分析 ---")
    try:
        elements_dist = bazi.get_elements_distribution()
        print(f"五行分布: {elements_dist}")
        
        dominant = bazi.get_dominant_element()
        print(f"主导五行: {dominant}")
        
        stem_elements = bazi.get_stem_elements()
        print(f"天干五行: {stem_elements}")
        
        branch_elements = bazi.get_branch_elements()
        print(f"地支五行: {branch_elements}")
        
        # 测试五行检查
        print(f"是否有木: {bazi.has_element('木')}")
        print(f"是否有金: {bazi.has_element('金')}")
        
    except Exception as e:
        print(f"五行分析错误: {e}")
    
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
    try:
        hidden_stems = bazi.get_hidden_stems_in_branches()
        print(f"各支藏干: {hidden_stems}")
    except Exception as e:
        print(f"藏干分析错误: {e}")
    
    # 测试关系分析
    print("\n--- 关系分析 ---")
    try:
        relationships = bazi.analyze_branch_relationships("申")
        print(f"申与命局关系: {relationships}")
    except Exception as e:
        print(f"关系分析错误: {e}")
    
    # 测试季节和强弱
    print("\n--- 季节和强弱 ---")
    print(f"月令季节: {bazi.get_month_season()}")
    print(f"日主强弱: {bazi.is_day_master_strong()}")
    
    # 测试组合检查
    print("\n--- 组合检查 ---")
    print(f"是否有甲寅组合: {bazi.has_stem_branch_combination('甲', '寅')}")
    print(f"是否有乙亥组合: {bazi.has_stem_branch_combination('乙', '亥')}")
    
    return bazi

if __name__ == "__main__":
    try:
        test_bazi_methods()
        print("\n✅ Bazi 类新增方法测试完成！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
