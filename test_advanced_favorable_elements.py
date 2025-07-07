#!/usr/bin/env python3
"""
测试新的高级喜用神分析功能
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.calculators import FiveElementsCalculator
from app.services.core import StemBranch, Bazi
from datetime import datetime

def test_advanced_favorable_elements():
    """测试高级喜用神分析"""
    print("=" * 60)
    print("测试高级喜用神分析功能")
    print("=" * 60)
    
    # 创建测试用例
    test_cases = [
        {
            "name": "春季甲木日主（需调候）",
            "year": StemBranch("甲", "子"),
            "month": StemBranch("丁", "卯"),  # 春季
            "day": StemBranch("甲", "寅"),
            "hour": StemBranch("乙", "亥"),
            "gender": "男",
            "birth_time": datetime(1990, 3, 15, 10, 30)  # 春季
        },
        {
            "name": "夏季丙火日主（需润燥）",
            "year": StemBranch("庚", "午"),
            "month": StemBranch("癸", "未"),  # 夏季
            "day": StemBranch("丙", "午"),
            "hour": StemBranch("己", "亥"),
            "gender": "女",
            "birth_time": datetime(1990, 7, 15, 14, 30)  # 夏季
        },
        {
            "name": "冬季壬水日主（需暖局）",
            "year": StemBranch("壬", "子"),
            "month": StemBranch("壬", "子"),  # 冬季
            "day": StemBranch("壬", "子"),
            "hour": StemBranch("辛", "亥"),
            "gender": "男",
            "birth_time": datetime(1990, 12, 15, 8, 30)  # 冬季
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试用例: {case['name']}")
        print("-" * 40)
        
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
        print(f"生于: {case['birth_time'].strftime('%Y年%m月%d日 %H时')}")
        print(f"日主: {bazi.day_master}")
        print()
        
        # 基础五行分析
        scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
        print("五行得分:")
        for element, score in scores.items():
            print(f"  {element}: {score:.2f}")
        print()
        
        # 基础喜用神
        basic_favorable = FiveElementsCalculator.get_favorable_elements(bazi)
        print(f"基础喜用神: {', '.join(basic_favorable)}")
        
        # 高级喜用神分析
        advanced_analysis = FiveElementsCalculator.get_advanced_favorable_elements(bazi)
        print(f"主要喜用神: {', '.join(advanced_analysis['primary_favorable'])}")
        print(f"次要喜用神: {', '.join(advanced_analysis['secondary_favorable'])}")
        print(f"调候用神: {', '.join(advanced_analysis['seasonal_priority'])}")
        print(f"通关用神: {', '.join(advanced_analysis['mediation_gods'])}")
        print(f"季节: {advanced_analysis['season']}")
        if advanced_analysis['conflicts_detected']:
            print(f"五行冲突: {', '.join(advanced_analysis['conflicts_detected'])}")
        print(f"分析摘要: {advanced_analysis['analysis_summary']}")
        print()
        
        # 病药用神分析
        disease_medicine = FiveElementsCalculator.analyze_disease_medicine_gods(bazi)
        print("病药用神分析:")
        print(f"  命局病症: {', '.join(disease_medicine['diseases'])}")
        print(f"  治病用神: {', '.join(disease_medicine['medicines'])}")
        print(f"  日主占比: {disease_medicine['day_master_ratio']:.1%}")
        print(f"  病药分析: {disease_medicine['analysis']}")
        print()
        
        # 格局分析
        pattern_analysis = FiveElementsCalculator.analyze_pattern_and_gods(bazi)
        print("格局分析:")
        print(f"  格局: {pattern_analysis['pattern']}")
        print(f"  格局描述: {pattern_analysis['pattern_description']}")
        print(f"  格局喜神: {', '.join(pattern_analysis['favorable_gods'])}")
        print(f"  格局忌神: {', '.join(pattern_analysis['avoid_gods'])}")
        print()
        
        # 综合用神分析
        comprehensive = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
        print("综合用神分析:")
        print(f"  最终主要用神: {', '.join(comprehensive['primary_gods'])}")
        print(f"  最终次要用神: {', '.join(comprehensive['secondary_gods'])}")
        print(f"  综合权重排序:")
        for god, weight in list(comprehensive['all_weights'].items())[:5]:
            print(f"    {god}: {weight:.3f}")
        print(f"  综合分析摘要: {comprehensive['comprehensive_summary']}")
        
        print("=" * 60)

def test_seasonal_adjustment():
    """测试季节调候用神"""
    print("\n专项测试：季节调候用神")
    print("=" * 40)
    
    # 同一日主在不同季节的调候需求
    day_stem = "甲"
    seasons = [
        (datetime(1990, 3, 15), "春季"),
        (datetime(1990, 6, 15), "夏季"),
        (datetime(1990, 9, 15), "秋季"),
        (datetime(1990, 12, 15), "冬季")
    ]
    
    for birth_time, season_name in seasons:
        print(f"\n{season_name} - {day_stem}日主:")
        
        bazi = Bazi(
            year=StemBranch("甲", "子"),
            month=StemBranch("丁", "卯"),
            day=StemBranch("甲", "寅"),
            hour=StemBranch("乙", "亥"),
            gender="男",
            birth_time=birth_time
        )
        
        advanced_analysis = FiveElementsCalculator.get_advanced_favorable_elements(bazi)
        print(f"  调候用神: {', '.join(advanced_analysis['seasonal_priority'])}")
        print(f"  调候权重: {advanced_analysis['seasonal_weight']:.2f}")

def test_element_conflicts():
    """测试五行战克检测"""
    print("\n专项测试：五行战克检测")
    print("=" * 40)
    
    # 构造五行战克的八字
    bazi = Bazi(
        year=StemBranch("甲", "寅"),  # 木
        month=StemBranch("戊", "辰"), # 土
        day=StemBranch("甲", "寅"),   # 木
        hour=StemBranch("戊", "戌"),  # 土
        gender="男",
        birth_time=datetime(1990, 4, 15, 10, 30)
    )
    
    print(f"八字: {bazi.year} {bazi.month} {bazi.day} {bazi.hour}")
    
    scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
    print("五行得分:")
    for element, score in scores.items():
        print(f"  {element}: {score:.2f}")
    
    conflicts = FiveElementsCalculator._detect_element_conflicts(scores)
    print(f"检测到的五行冲突: {conflicts}")
    
    advanced_analysis = FiveElementsCalculator.get_advanced_favorable_elements(bazi)
    print(f"通关用神: {', '.join(advanced_analysis['mediation_gods'])}")

if __name__ == "__main__":
    test_advanced_favorable_elements()
    test_seasonal_adjustment()
    test_element_conflicts()
