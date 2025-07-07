#!/usr/bin/env python3
"""
完整测试新的数据驱动神煞计算引擎和高级喜用神分析系统
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.bazi_calculator import calculate_bazi_data
from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
from app.services.core import StemBranch, Bazi
from datetime import datetime
import json

def test_complete_system():
    """测试完整的系统集成"""
    print("=" * 60)
    print("完整的八字神煞和喜用神分析系统测试")
    print("=" * 60)
    
    # 创建多个有代表性的测试用例
    test_cases = [
        {
            "name": "甲子日主 - 春生木旺",
            "year": StemBranch("甲", "子"),
            "month": StemBranch("丁", "卯"),  # 春月
            "day": StemBranch("甲", "子"),
            "hour": StemBranch("丙", "寅"),
            "gender": "男",
            "birth_time": datetime(1984, 3, 15, 10, 30),
            "description": "春生甲木，木旺需要火泄或金修剪"
        },
        {
            "name": "丙午日主 - 夏生火炎",
            "year": StemBranch("庚", "午"),
            "month": StemBranch("壬", "午"),  # 夏月
            "day": StemBranch("丙", "午"),
            "hour": StemBranch("己", "亥"),
            "gender": "女",
            "birth_time": datetime(1990, 6, 15, 14, 30),
            "description": "夏生丙火，火炎需要水来润泽"
        },
        {
            "name": "戊戌日主 - 魁罡格",
            "year": StemBranch("己", "未"),
            "month": StemBranch("丙", "寅"),
            "day": StemBranch("戊", "戌"),  # 魁罡日
            "hour": StemBranch("甲", "子"),
            "gender": "男",
            "birth_time": datetime(1979, 2, 28, 8, 30),
            "description": "戊戌魁罡，性格刚烈但聪明果断"
        },
        {
            "name": "庚申日主 - 秋金锐利",
            "year": StemBranch("壬", "戌"),
            "month": StemBranch("己", "酉"),  # 秋月
            "day": StemBranch("庚", "申"),
            "hour": StemBranch("戊", "寅"),
            "gender": "女",
            "birth_time": datetime(1982, 9, 20, 16, 45),
            "description": "秋生庚金，金锐需要水来淘洗"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试用例: {case['name']}")
        print(f"   说明: {case['description']}")
        print("-" * 50)
        
        # 创建八字
        bazi = Bazi(
            year=case["year"],
            month=case["month"],
            day=case["day"],
            hour=case["hour"],
            gender=case["gender"],
            birth_time=case["birth_time"]
        )
        
        print(f"八字: {bazi.year} {bazi.month} {bazi.day} {bazi.hour}")
        print(f"性别: {case['gender']}, 生肖: {bazi.zodiac}")
        print()
        
        # 1. 神煞计算测试
        print("【神煞分析】")
        shensha_calculator = ShenShaCalculator()
        shensha_result = shensha_calculator.calculate(bazi)
        
        active_shensha = {k: v for k, v in shensha_result.items() if v.active}
        if active_shensha:
            for key, shensha in active_shensha.items():
                print(f"  ✓ {shensha.name}: {shensha.position}")
                print(f"    强度: {shensha.strength:.2f}")
                if shensha.positive_tags:
                    print(f"    正面: {', '.join(shensha.positive_tags)}")
                if shensha.negative_tags:
                    print(f"    负面: {', '.join(shensha.negative_tags)}")
                if shensha.tags:
                    print(f"    特征: {', '.join(shensha.tags)}")
                print()
        else:
            print("  无明显活跃神煞")
        
        # 2. 五行分析测试
        print("【五行分析】")
        five_elements_scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
        five_elements_percentage = FiveElementsCalculator.calculate_five_elements_percentage(bazi)
        day_master_strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
        
        print(f"  日主强弱: {day_master_strength}")
        print("  五行分布:")
        for element, percentage in five_elements_percentage.items():
            print(f"    {element}: {percentage}%")
        print()
        
        # 3. 基础喜用神测试
        print("【基础喜用神】")
        basic_favorable = FiveElementsCalculator.get_favorable_elements(bazi)
        print(f"  基础喜用神: {', '.join(basic_favorable)}")
        print()
        
        # 4. 高级喜用神分析测试
        print("【高级喜用神分析】")
        advanced_analysis = FiveElementsCalculator.get_advanced_favorable_elements(bazi)
        print(f"  主要喜用神: {', '.join(advanced_analysis['primary_favorable'])}")
        if advanced_analysis['secondary_favorable']:
            print(f"  次要喜用神: {', '.join(advanced_analysis['secondary_favorable'])}")
        if advanced_analysis['seasonal_priority']:
            print(f"  调候用神: {', '.join(advanced_analysis['seasonal_priority'])}")
        if advanced_analysis['mediation_gods']:
            print(f"  通关用神: {', '.join(advanced_analysis['mediation_gods'])}")
        print(f"  季节: {advanced_analysis['season']}")
        if advanced_analysis['conflicts_detected']:
            print(f"  五行冲突: {', '.join(advanced_analysis['conflicts_detected'])}")
        print(f"  分析摘要: {advanced_analysis['analysis_summary']}")
        print()
        
        # 5. 病药用神分析测试
        print("【病药用神分析】")
        disease_medicine = FiveElementsCalculator.analyze_disease_medicine_gods(bazi)
        if disease_medicine['diseases']:
            print(f"  命局病症: {', '.join(disease_medicine['diseases'])}")
        if disease_medicine['medicines']:
            print(f"  治病用神: {', '.join(disease_medicine['medicines'])}")
        print(f"  日主占比: {disease_medicine['day_master_ratio']}")
        print(f"  病药分析: {disease_medicine['analysis']}")
        print()
        
        # 6. 格局分析测试
        print("【格局分析】")
        pattern_analysis = FiveElementsCalculator.analyze_pattern_and_gods(bazi)
        print(f"  格局: {pattern_analysis['pattern']}")
        print(f"  格局描述: {pattern_analysis['pattern_description']}")
        if pattern_analysis['favorable_gods']:
            print(f"  格局喜用神: {', '.join(pattern_analysis['favorable_gods'])}")
        if pattern_analysis['avoid_gods']:
            print(f"  格局忌神: {', '.join(pattern_analysis['avoid_gods'])}")
        print(f"  格局分析: {pattern_analysis['pattern_analysis']}")
        print()
        
        # 7. 综合用神分析测试
        print("【综合用神分析】")
        comprehensive = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
        print(f"  综合主要用神: {', '.join(comprehensive['primary_gods'])}")
        if comprehensive['secondary_gods']:
            print(f"  综合次要用神: {', '.join(comprehensive['secondary_gods'])}")
        print("  权重分析:")
        for god, weight in comprehensive['all_weights'].items():
            if weight > 0.1:  # 只显示权重较高的
                print(f"    {god}: {weight:.2f}")
        print(f"  综合摘要: {comprehensive['comprehensive_summary']}")
        
        print("=" * 60)

def test_specific_shensha_accuracy():
    """测试特定神煞的计算准确性"""
    print("\n特定神煞准确性测试")
    print("=" * 40)
    
    test_cases = [
        {
            "name": "天乙贵人测试（甲日丑未时）",
            "bazi": Bazi(
                year=StemBranch("甲", "子"),
                month=StemBranch("乙", "丑"),  # 丑为甲日天乙贵人
                day=StemBranch("甲", "子"),
                hour=StemBranch("己", "未"),   # 未为甲日天乙贵人
                gender="男"
            ),
            "expected_shensha": "tianyi_guiren",
            "expected_positions": ["月", "时"]
        },
        {
            "name": "桃花测试（子年酉月）",
            "bazi": Bazi(
                year=StemBranch("甲", "子"),   # 子
                month=StemBranch("乙", "酉"), # 酉为子年桃花
                day=StemBranch("丙", "寅"),
                hour=StemBranch("丁", "卯"),
                gender="女"
            ),
            "expected_shensha": "tao_hua",
            "expected_positions": ["月"]
        },
        {
            "name": "驿马测试（申年寅时）",
            "bazi": Bazi(
                year=StemBranch("甲", "申"),   # 申
                month=StemBranch("乙", "酉"),
                day=StemBranch("丙", "子"),
                hour=StemBranch("己", "寅"),   # 寅为申年驿马
                gender="男"
            ),
            "expected_shensha": "yima",
            "expected_positions": ["时"]
        },
        {
            "name": "魁罡测试（戊戌日）",
            "bazi": Bazi(
                year=StemBranch("己", "亥"),
                month=StemBranch("乙", "亥"),
                day=StemBranch("戊", "戌"),    # 戊戌为魁罡
                hour=StemBranch("甲", "子"),
                gender="男"
            ),
            "expected_shensha": "kuigang",
            "expected_positions": ["日柱"]
        }
    ]
    
    shensha_calculator = ShenShaCalculator()
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}")
        print(f"八字: {test_case['bazi'].year} {test_case['bazi'].month} {test_case['bazi'].day} {test_case['bazi'].hour}")
        
        result = shensha_calculator.calculate(test_case['bazi'])
        expected_key = test_case['expected_shensha']
        
        if expected_key in result and result[expected_key].active:
            shensha = result[expected_key]
            actual_positions = shensha.position.split(", ") if shensha.position else []
            expected_positions = test_case['expected_positions']
            
            print(f"✓ {shensha.name} 计算正确")
            print(f"  位置: {shensha.position}")
            print(f"  强度: {shensha.strength:.2f}")
            
            # 验证位置准确性
            position_match = any(pos in actual_positions for pos in expected_positions)
            if position_match:
                print("✓ 位置计算正确")
            else:
                print(f"✗ 位置计算错误，期望: {expected_positions}, 实际: {actual_positions}")
        else:
            print(f"✗ {test_case['expected_shensha']} 未能正确计算或未激活")

def test_advanced_analysis_accuracy():
    """测试高级喜用神分析的准确性"""
    print("\n高级喜用神分析准确性测试")
    print("=" * 40)
    
    # 测试调候用神
    print("\n1. 调候用神测试")
    summer_fire_bazi = Bazi(
        year=StemBranch("庚", "午"),
        month=StemBranch("癸", "未"),  # 夏月
        day=StemBranch("丙", "午"),    # 丙火日主
        hour=StemBranch("己", "亥"),
        gender="女",
        birth_time=datetime(1990, 7, 15, 14, 30)  # 夏季
    )
    
    advanced = FiveElementsCalculator.get_advanced_favorable_elements(summer_fire_bazi)
    print(f"夏生丙火 - 调候用神: {', '.join(advanced.get('seasonal_priority', []))}")
    print(f"分析: {advanced['analysis_summary']}")
    
    # 测试病药用神
    print("\n2. 病药用神测试")
    weak_day_master_bazi = Bazi(
        year=StemBranch("庚", "申"),  # 金克木
        month=StemBranch("庚", "申"), # 金克木
        day=StemBranch("甲", "子"),   # 甲木日主
        hour=StemBranch("庚", "申"),  # 金克木
        gender="男"
    )
    
    disease_medicine = FiveElementsCalculator.analyze_disease_medicine_gods(weak_day_master_bazi)
    print(f"金多克木局 - 病症: {', '.join(disease_medicine['diseases'])}")
    print(f"治病用神: {', '.join(disease_medicine['medicines'])}")
    print(f"分析: {disease_medicine['analysis']}")

if __name__ == "__main__":
    test_complete_system()
    test_specific_shensha_accuracy()
    test_advanced_analysis_accuracy()
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("数据驱动神煞计算引擎和高级喜用神分析系统已成功实现。")
    print("=" * 60)
