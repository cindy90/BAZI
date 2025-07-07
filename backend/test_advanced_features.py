#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整的新框架功能测试
测试所有新增的高级功能
"""

import asyncio
from datetime import datetime
import sys
import os

# 设置路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

async def test_advanced_features():
    """测试高级功能"""
    print("=== 新八字框架高级功能测试 ===\n")
    
    try:
        # 导入所有新框架类
        from app.services.core import Bazi, StemBranch, FortuneModel
        from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
        from app.services.analyzers import AdvancedDayunAnalyzer, AdvancedEventEngine
        
        print("✅ 成功导入所有高级功能模块")
        
        # 创建测试命盘
        bazi = Bazi(
            year=StemBranch("甲", "子"),
            month=StemBranch("丙", "寅"), 
            day=StemBranch("戊", "午"),
            hour=StemBranch("丁", "巳"),
            gender="男",
            birth_time=datetime(1990, 5, 15, 10, 30)
        )
        
        print(f"\n测试命盘: {bazi.year} {bazi.month} {bazi.day} {bazi.hour}")
        print(f"日主: {bazi.get_day_master()} ({bazi.gender})")
        
        # 1. 测试高级五行计算
        print("\n=== 1. 高级五行计算测试 ===")
        five_elements_scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
        print("五行得分:")
        for element, score in five_elements_scores.items():
            print(f"  {element}: {score:.2f}")
        
        day_master_strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
        print(f"日主强弱: {day_master_strength}")
        
        balance_analysis = FiveElementsCalculator.analyze_five_elements_balance(bazi)
        print(f"五行平衡: {balance_analysis['balance']}")
        print(f"五行百分比: {balance_analysis['percentages']}")
        if balance_analysis['missing']:
            print(f"缺失五行: {balance_analysis['missing']}")
        if balance_analysis['excess']:
            print(f"过旺五行: {balance_analysis['excess']}")
        
        # 2. 测试大运计算和分析
        print("\n=== 2. 高级大运分析测试 ===")
        dayun_list = FortuneModel.calculate_da_yun(bazi)
        print(f"大运数量: {len(dayun_list)}")
        
        # 显示前5个大运
        for i, dayun in enumerate(dayun_list[:5]):
            print(f"第{i+1}步大运: {dayun.stem_branch} ({dayun.start_age}-{dayun.end_age}岁)")
        
        # 高级大运分析
        advanced_analysis = AdvancedDayunAnalyzer.analyze_dayun_fortune_trend(bazi, dayun_list)
        print(f"\n大运整体趋势: {advanced_analysis['overall_trend']}")
        
        if advanced_analysis['peak_periods']:
            print("运势高峰期:")
            for period in advanced_analysis['peak_periods']:
                print(f"  {period['period']} ({period['dayun']}): {period['description']}")
        
        if advanced_analysis['challenging_periods']:
            print("挑战期:")
            for period in advanced_analysis['challenging_periods']:
                print(f"  {period['period']} ({period['dayun']}): {period['description']}")
        
        if advanced_analysis['turning_points']:
            print("重要转折点:")
            for tp in advanced_analysis['turning_points']:
                print(f"  {tp['age']}岁: {tp['description']} (变化幅度: {tp['magnitude']})")
        
        # 3. 测试高级事件预测
        print("\n=== 3. 高级事件预测测试 ===")
        event_predictions = AdvancedEventEngine.predict_life_events(bazi, dayun_list)
        
        if event_predictions:
            print("预测重要事件:")
            for event_type, predictions in event_predictions.items():
                print(f"\n{event_type}:")
                for pred in predictions:
                    print(f"  {pred['age_range']}: {pred['description']}")
                    print(f"    概率: {pred['probability']}%, 建议: {pred['advice']}")
                    if pred['estimated_time']:
                        print(f"    预计时间: {pred['estimated_time']}年")
        else:
            print("未预测到显著事件")
        
        # 4. 测试神煞计算
        print("\n=== 4. 神煞计算测试 ===")
        shensha_calc = ShenShaCalculator()
        shensha_results = shensha_calc.calculate(bazi)
        
        print(f"神煞数量: {len(shensha_results)}")
        for key, shensha in shensha_results.items():
            status = "激活" if shensha.active else "未激活"
            print(f"  {shensha.name}: {shensha.position} ({status}, 强度: {shensha.strength:.2f})")
            if shensha.tags:
                print(f"    标签: {', '.join(shensha.tags)}")
        
        print("\n=== 高级功能测试完成 ===")
        print("✅ 所有高级功能运行正常!")
        
        # 5. 性能测试
        print("\n=== 5. 性能测试 ===")
        import time
        
        start_time = time.time()
        for i in range(100):
            # 批量计算测试
            test_bazi = Bazi(
                year=StemBranch("甲", "子"),
                month=StemBranch("丙", "寅"),
                day=StemBranch("戊", "午"), 
                hour=StemBranch("丁", "巳"),
                gender="男",
                birth_time=datetime(1990 + i % 50, 5, 15, 10, 30)
            )
            FiveElementsCalculator.calculate_comprehensive_scores(test_bazi)
        
        end_time = time.time()
        print(f"100次五行计算耗时: {(end_time - start_time):.3f}秒")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_advanced_features())
