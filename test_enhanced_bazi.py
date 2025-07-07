#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试增强版 Bazi 类和优化后的 calculators 模块
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.services.core import Bazi, StemBranch
from backend.app.services.calculators import FiveElementsCalculator, ShenShaCalculator
from backend.app.services.constants import *
import json
from datetime import datetime

def test_enhanced_bazi_methods():
    """测试增强版 Bazi 类的方法"""
    print("=== 测试增强版 Bazi 类方法 ===")
    
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
    
    # 测试新增方法
    print("\n--- 基础信息获取 ---")
    print(f"所有天干: {bazi.get_all_stems()}")
    print(f"所有地支: {bazi.get_all_branches()}")
    print(f"所有干支: {bazi.get_all_stem_branches()}")
    
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
    
    return bazi

def test_optimized_calculators(bazi):
    """测试优化后的计算器"""
    print("\n=== 测试优化后的计算器 ===")
    
    # 测试五行计算
    print("\n--- 五行计算 ---")
    scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
    print(f"五行得分: {scores}")
    
    strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
    print(f"日主强度: {strength:.2f}")
    
    favorable = FiveElementsCalculator.get_favorable_elements(bazi)
    print(f"喜用神: {favorable}")
    
    percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi)
    print(f"五行百分比: {percentages}")
    
    # 测试综合分析
    print("\n--- 综合分析 ---")
    comprehensive = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
    print(f"综合分析评分: {comprehensive['final_prognosis']['overall_rating']}")
    print(f"主要喜用神: {comprehensive['final_prognosis']['primary_favorable']}")
    print(f"生活建议: {comprehensive['final_prognosis']['life_advice'][:2]}")
    
    # 测试神煞计算
    print("\n--- 神煞计算 ---")
    shensha_calc = ShenShaCalculator()
    shensha_result = shensha_calc.calculate_shensha(bazi)
    print(f"神煞数量: {len(shensha_result)}")
    for name, shensha in list(shensha_result.items())[:3]:
        print(f"  {shensha.name}: {shensha.position}, 强度: {shensha.strength:.2f}")

def test_integration():
    """测试完整集成"""
    print("\n=== 完整集成测试 ===")
    
    # 创建测试八字
    bazi = test_enhanced_bazi_methods()
    
    # 测试计算器
    test_optimized_calculators(bazi)
    
    # 测试流年分析
    print("\n--- 流年分析测试 ---")
    current_year = 2025
    current_year_gan = "乙"
    current_year_zhi = "巳"
    
    # 分析流年互动
    interactions = FiveElementsCalculator.analyze_liunian_interactions(
        bazi, current_year_gan, current_year_zhi
    )
    print(f"流年互动评估: {interactions['overall_assessment']}")
    print(f"冲突关系: {interactions['conflicts']}")
    print(f"和谐关系: {interactions['harmonies']}")
    
    # 分析流年神煞
    shensha_calc = ShenShaCalculator()
    liunian_shensha = FiveElementsCalculator.analyze_liunian_shensha(
        bazi, current_year_gan, current_year_zhi, shensha_calc
    )
    print(f"流年神煞数量: {len(liunian_shensha)}")
    
    # 生成详细预测
    ten_god = FiveElementsCalculator.calculate_ten_god_relation(current_year_gan, bazi.day.stem)
    comprehensive_analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
    
    predictions = FiveElementsCalculator.generate_detailed_predictions(
        ten_god, 
        STEM_ELEMENTS.get(current_year_gan, ""),
        BRANCH_ELEMENTS.get(current_year_zhi, ""),
        interactions,
        liunian_shensha,
        comprehensive_analysis
    )
    
    print(f"\n流年{current_year_gan}{current_year_zhi}({ten_god})详细预测:")
    for category, events in predictions.items():
        print(f"  {category}: {len(events)}条预测")
        for event in events[:2]:  # 显示前两条
            print(f"    - {event}")

def main():
    """主测试函数"""
    print("开始测试增强版 Bazi 类和优化后的计算器...")
    
    try:
        test_integration()
        print("\n✅ 所有测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
