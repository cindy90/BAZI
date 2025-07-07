#!/usr/bin/env python3
"""
测试综合优化效果
验证喜用神忌神分析的统一性和流年互动分析的常量化
"""

import sys
import os
import json
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入必要的模块
from app.services.calculators import FiveElementsCalculator, ShenShaCalculator
from app.services.core import Bazi, StemBranch

def test_unified_gods_analysis():
    """测试统一的喜用神忌神分析"""
    print("=== 测试统一的喜用神忌神分析 ===")
    
    # 创建测试八字对象
    test_cases = [
        {
            "name": "身弱测试",
            "year": StemBranch("乙", "丑"),
            "month": StemBranch("戊", "午"),
            "day": StemBranch("甲", "寅"),
            "hour": StemBranch("丁", "未"),
            "gender": "男"
        },
        {
            "name": "身强测试",
            "year": StemBranch("甲", "子"),
            "month": StemBranch("丙", "寅"),
            "day": StemBranch("甲", "午"),
            "hour": StemBranch("甲", "戌"),
            "gender": "男"
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"\n--- {test_case['name']} ---")
            
            # 创建八字对象
            bazi_obj = Bazi(
                year=test_case["year"],
                month=test_case["month"],
                day=test_case["day"],
                hour=test_case["hour"],
                gender=test_case["gender"]
            )
            
            print(f"四柱：{test_case['year'].stem}{test_case['year'].branch} "
                  f"{test_case['month'].stem}{test_case['month'].branch} "
                  f"{test_case['day'].stem}{test_case['day'].branch} "
                  f"{test_case['hour'].stem}{test_case['hour'].branch}")
            
            # 测试统一的喜用神分析
            gods_analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi_obj)
            
            basic = gods_analysis["basic_analysis"]
            print(f"日主：{basic['day_element']}")
            print(f"日主强度：{basic['day_strength']:.3f}")
            print(f"喜用神：{basic['favorable_elements']}")
            print(f"忌神：{basic['unfavorable_elements']}")
            
            prognosis = gods_analysis["final_prognosis"]
            print(f"综合评价：{prognosis['overall_rating']}")
            print(f"建议：{prognosis['life_advice']}")
            
            # 验证逻辑一致性
            if basic['day_strength'] < 0.4:
                expected_favorable = basic['day_element'] in basic['favorable_elements']
                print(f"身弱逻辑验证：{'✓' if expected_favorable else '✗'}")
            elif basic['day_strength'] > 0.6:
                expected_unfavorable = basic['day_element'] in basic['unfavorable_elements']
                print(f"身强逻辑验证：{'✓' if expected_unfavorable else '✗'}")
            else:
                print("中和状态")
                
        except Exception as e:
            print(f"测试异常：{e}")
    
    print("\n=== 喜用神忌神分析测试完成 ===\n")

def test_liunian_interactions():
    """测试流年互动分析的常量化"""
    print("=== 测试流年互动分析的常量化 ===")
    
    # 创建测试八字对象
    bazi_obj = Bazi(
        year=StemBranch("乙", "丑"),
        month=StemBranch("戊", "午"),
        day=StemBranch("甲", "寅"),
        hour=StemBranch("丁", "未"),
        gender="男"
    )
    
    print(f"命局四柱：乙丑 戊午 甲寅 丁未")
    
    # 测试不同的流年
    test_liunian = [
        ("甲", "子", "2024年流年"),
        ("乙", "丑", "2025年流年"),
        ("丙", "寅", "2026年流年")
    ]
    
    for liunian_gan, liunian_zhi, description in test_liunian:
        try:
            print(f"\n--- {description} ({liunian_gan}{liunian_zhi}) ---")
            
            # 测试流年互动分析
            interactions = FiveElementsCalculator.analyze_liunian_interactions(
                bazi_obj, liunian_gan, liunian_zhi, "戊", "戌"  # 假设大运
            )
            
            print(f"天干互动：{interactions['stem_interactions']}")
            print(f"地支互动：{interactions['branch_interactions']}")
            print(f"大运互动：{interactions['dayun_interactions']}")
            if interactions['special_patterns']:
                print(f"特殊格局：{interactions['special_patterns']}")
            
            # 验证互动分析的完整性
            total_interactions = (len(interactions['stem_interactions']) + 
                                len(interactions['branch_interactions']) + 
                                len(interactions['dayun_interactions']))
            print(f"总互动数量：{total_interactions}")
            
        except Exception as e:
            print(f"测试异常：{e}")
    
    print("\n=== 流年互动分析测试完成 ===\n")

def test_five_elements_percentage():
    """测试五行能量百分比的精确计算"""
    print("=== 测试五行能量百分比的精确计算 ===")
    
    # 创建测试八字对象
    bazi_obj = Bazi(
        year=StemBranch("乙", "丑"),
        month=StemBranch("戊", "午"),
        day=StemBranch("甲", "寅"),
        hour=StemBranch("丁", "未"),
        gender="男"
    )
    
    print(f"四柱：乙丑 戊午 甲寅 丁未")
    
    try:
        # 测试五行能量精确计算
        energy_scores = FiveElementsCalculator.calculate_comprehensive_five_elements_energy(bazi_obj)
        print(f"五行能量分数：{energy_scores}")
        
        # 测试五行百分比
        percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi_obj)
        print(f"五行能量百分比：{percentages}")
        
        # 验证百分比总和
        total_percentage = sum(percentages.values())
        print(f"百分比总和：{total_percentage:.1f}%")
        print(f"百分比验证：{'✓' if abs(total_percentage - 100.0) < 0.1 else '✗'}")
        
        # 验证能量分数与百分比的一致性
        total_energy = sum(energy_scores.values())
        consistency_check = True
        for element in energy_scores:
            expected_percentage = (energy_scores[element] / total_energy) * 100
            actual_percentage = percentages[element]
            if abs(expected_percentage - actual_percentage) > 0.1:
                consistency_check = False
                break
        
        print(f"能量分数与百分比一致性：{'✓' if consistency_check else '✗'}")
        
    except Exception as e:
        print(f"测试异常：{e}")
    
    print("\n=== 五行能量百分比测试完成 ===\n")

def main():
    """主测试函数"""
    print("开始综合优化测试...")
    print("=" * 50)
    
    # 运行所有测试
    test_unified_gods_analysis()
    test_liunian_interactions()
    test_five_elements_percentage()
    
    print("=" * 50)
    print("综合优化测试完成！")

if __name__ == "__main__":
    main()
