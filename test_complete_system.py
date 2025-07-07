#!/usr/bin/env python3
"""
测试完整的数据驱动神煞计算引擎和高级喜用神分析
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.bazi_calculator import calculate_bazi_data
from app.services.core import StemBranch, Bazi
from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
from datetime import datetime

def test_comprehensive_system():
    """测试完整系统的集成"""
    print("=" * 60)
    print("测试完整的八字分析系统")
    print("=" * 60)
    
    # 创建测试用例 - 具有多种神煞和复杂五行关系的八字
    test_cases = [
        {
            "name": "甲子日主（天乙贵人在年月）",
            "year": StemBranch("甲", "子"),
            "month": StemBranch("乙", "丑"),  # 丑为甲日主天乙贵人
            "day": StemBranch("甲", "子"),
            "hour": StemBranch("丙", "未"),   # 未为甲日主天乙贵人
            "gender": "男",
            "birth_time": datetime(1990, 4, 29, 10, 30)  # 春季
        },
        {
            "name": "丙午日主（桃花+驿马）",
            "year": StemBranch("庚", "午"),   # 午为桃花基础
            "month": StemBranch("戊", "寅"),  # 寅为申子辰驿马
            "day": StemBranch("丙", "午"),
            "hour": StemBranch("己", "卯"),   # 卯为午的桃花
            "gender": "女",
            "birth_time": datetime(1990, 7, 15, 14, 30)  # 夏季
        },
        {
            "name": "戊戌日主（魁罡+空亡）",
            "year": StemBranch("己", "未"),
            "month": StemBranch("丙", "寅"),
            "day": StemBranch("戊", "戌"),   # 戊戌魁罡
            "hour": StemBranch("甲", "子"),
            "gender": "男",
            "birth_time": datetime(1990, 11, 20, 8, 30)   # 冬季
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
        print(f"性别: {case['gender']}, 日主: {bazi.day_master}")
        
        # 1. 测试神煞计算
        print(f"\n📿 神煞分析:")
        shensha_calc = ShenShaCalculator()
        shensha_result = shensha_calc.calculate(bazi)
        
        active_shensha = [s for s in shensha_result.values() if s.active]
        if active_shensha:
            for shensha in active_shensha:
                print(f"  ✨ {shensha.name}: {shensha.position}")
                print(f"     强度: {shensha.strength:.2f}")
                print(f"     描述: {shensha.description}")
                if shensha.positive_tags:
                    print(f"     正面: {', '.join(shensha.positive_tags)}")
                if shensha.negative_tags:
                    print(f"     负面: {', '.join(shensha.negative_tags)}")
                if shensha.tags:
                    print(f"     特征: {', '.join(shensha.tags)}")
                print()
        else:
            print("  未发现活跃的神煞")
        
        # 2. 测试五行分析
        print(f"🔥 五行分析:")
        scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
        percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi)
        strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
        
        print(f"  五行分布: {dict(percentages)}")
        print(f"  日主强弱: {strength}")
        
        # 3. 测试高级喜用神分析
        print(f"\n🌟 高级喜用神分析:")
        advanced_analysis = FiveElementsCalculator.get_advanced_favorable_elements(bazi)
        
        print(f"  主要喜用神: {advanced_analysis.get('primary_favorable', [])}")
        print(f"  次要喜用神: {advanced_analysis.get('secondary_favorable', [])}")
        print(f"  调候用神: {advanced_analysis.get('seasonal_priority', [])}")
        print(f"  通关用神: {advanced_analysis.get('mediation_gods', [])}")
        print(f"  季节: {advanced_analysis.get('season', '未知')}")
        print(f"  冲突: {advanced_analysis.get('conflicts_detected', [])}")
        
        analysis_summary = advanced_analysis.get('analysis_summary', '')
        if analysis_summary:
            print(f"\n  📋 分析摘要:")
            print(f"     {analysis_summary}")
        
        # 4. 测试病药用神分析
        print(f"\n🏥 病药用神分析:")
        disease_medicine = FiveElementsCalculator.analyze_disease_medicine_gods(bazi)
        
        diseases = disease_medicine.get('diseases', [])
        medicines = disease_medicine.get('medicines', [])
        
        if diseases:
            print(f"  病症: {', '.join(diseases)}")
        if medicines:
            print(f"  药神: {', '.join(medicines)}")
        
        disease_analysis = disease_medicine.get('analysis', '')
        if disease_analysis:
            print(f"  分析: {disease_analysis}")
        
        # 5. 测试格局分析
        print(f"\n👑 格局分析:")
        pattern_analysis = FiveElementsCalculator.analyze_pattern_and_gods(bazi)
        
        print(f"  格局: {pattern_analysis.get('pattern', '未知')}")
        print(f"  格局用神: {pattern_analysis.get('favorable_gods', [])}")
        print(f"  格局忌神: {pattern_analysis.get('avoid_gods', [])}")
        
        pattern_desc = pattern_analysis.get('pattern_description', '')
        if pattern_desc:
            print(f"  说明: {pattern_desc}")
        
        # 6. 测试综合用神分析
        print(f"\n🎯 综合用神分析:")
        comprehensive = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
        
        print(f"  最终喜用神: {comprehensive.get('primary_gods', [])}")
        print(f"  次要用神: {comprehensive.get('secondary_gods', [])}")
        
        comprehensive_summary = comprehensive.get('comprehensive_summary', '')
        if comprehensive_summary:
            print(f"  综合分析: {comprehensive_summary}")
        
        print("=" * 60)

def test_error_handling():
    """测试错误处理机制"""
    print("\n" + "=" * 40)
    print("测试错误处理机制")
    print("=" * 40)
    
    # 测试无效日期的八字
    try:
        bazi = Bazi(
            year=StemBranch("甲", "子"),
            month=StemBranch("乙", "丑"),
            day=StemBranch("无效干", "子"),  # 无效天干
            hour=StemBranch("丙", "寅"),
            gender="男"
        )
        
        shensha_calc = ShenShaCalculator()
        result = shensha_calc.calculate(bazi)
        print("✅ 错误处理测试通过：系统能够处理无效输入")
        
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")

def test_performance():
    """测试性能"""
    print("\n" + "=" * 40)
    print("测试系统性能")
    print("=" * 40)
    
    import time
    
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("乙", "丑"),
        day=StemBranch("丙", "寅"),
        hour=StemBranch("丁", "卯"),
        gender="男",
        birth_time=datetime(1990, 4, 29, 10, 30)
    )
    
    # 测试神煞计算性能
    start_time = time.time()
    shensha_calc = ShenShaCalculator()
    for _ in range(100):
        shensha_calc.calculate(bazi)
    shensha_time = time.time() - start_time
    
    # 测试五行分析性能
    start_time = time.time()
    for _ in range(100):
        FiveElementsCalculator.analyze_comprehensive_gods(bazi)
    wuxing_time = time.time() - start_time
    
    print(f"神煞计算 100次耗时: {shensha_time:.3f}秒 (平均: {shensha_time/100*1000:.1f}ms/次)")
    print(f"五行分析 100次耗时: {wuxing_time:.3f}秒 (平均: {wuxing_time/100*1000:.1f}ms/次)")
    
    if shensha_time < 1.0 and wuxing_time < 2.0:
        print("✅ 性能测试通过：系统响应速度良好")
    else:
        print("⚠️  性能测试警告：系统响应可能较慢")

if __name__ == "__main__":
    test_comprehensive_system()
    test_error_handling()
    test_performance()
