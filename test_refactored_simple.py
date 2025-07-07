#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单测试重构后的函数
验证函数移动和常量统一是否成功
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'app', 'services'))

# 直接导入模块
from calculators import FiveElementsCalculator
from core import Bazi, StemBranch
from datetime import datetime

def test_refactored_functions():
    """测试重构后的函数"""
    print("🧪 测试重构后的计算器函数")
    print("=" * 60)
    
    # 创建测试八字
    test_bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    print(f"测试八字: {test_bazi.year.stem}{test_bazi.year.branch} {test_bazi.month.stem}{test_bazi.month.branch} {test_bazi.day.stem}{test_bazi.day.branch} {test_bazi.hour.stem}{test_bazi.hour.branch}")
    print()
    
    # 1. 测试十神关系计算
    print("1. 测试十神关系计算:")
    try:
        ten_god_year = FiveElementsCalculator.calculate_ten_god_relation(test_bazi.year.stem, test_bazi.day.stem)
        ten_god_month = FiveElementsCalculator.calculate_ten_god_relation(test_bazi.month.stem, test_bazi.day.stem)
        ten_god_hour = FiveElementsCalculator.calculate_ten_god_relation(test_bazi.hour.stem, test_bazi.day.stem)
        
        print(f"   年干 {test_bazi.year.stem} 与日主 {test_bazi.day.stem} 的关系: {ten_god_year}")
        print(f"   月干 {test_bazi.month.stem} 与日主 {test_bazi.day.stem} 的关系: {ten_god_month}")
        print(f"   时干 {test_bazi.hour.stem} 与日主 {test_bazi.day.stem} 的关系: {ten_god_hour}")
        print("   ✅ 十神关系计算成功")
    except Exception as e:
        print(f"   ❌ 十神关系计算失败: {e}")
    print()
    
    # 2. 测试地支藏干
    print("2. 测试地支藏干:")
    try:
        hidden_stems_year = FiveElementsCalculator.get_zhi_hidden_gan(test_bazi.year.branch)
        hidden_stems_month = FiveElementsCalculator.get_zhi_hidden_gan(test_bazi.month.branch)
        hidden_stems_day = FiveElementsCalculator.get_zhi_hidden_gan(test_bazi.day.branch)
        hidden_stems_hour = FiveElementsCalculator.get_zhi_hidden_gan(test_bazi.hour.branch)
        
        print(f"   年支 {test_bazi.year.branch} 藏干: {hidden_stems_year}")
        print(f"   月支 {test_bazi.month.branch} 藏干: {hidden_stems_month}")
        print(f"   日支 {test_bazi.day.branch} 藏干: {hidden_stems_day}")
        print(f"   时支 {test_bazi.hour.branch} 藏干: {hidden_stems_hour}")
        print("   ✅ 地支藏干计算成功")
    except Exception as e:
        print(f"   ❌ 地支藏干计算失败: {e}")
    print()
    
    # 3. 测试长生十二宫
    print("3. 测试长生十二宫:")
    try:
        chang_sheng_year = FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(test_bazi.day.stem, test_bazi.year.branch)
        chang_sheng_month = FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(test_bazi.day.stem, test_bazi.month.branch)
        chang_sheng_day = FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(test_bazi.day.stem, test_bazi.day.branch)
        chang_sheng_hour = FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(test_bazi.day.stem, test_bazi.hour.branch)
        
        print(f"   日主 {test_bazi.day.stem} 在年支 {test_bazi.year.branch}: {chang_sheng_year}")
        print(f"   日主 {test_bazi.day.stem} 在月支 {test_bazi.month.branch}: {chang_sheng_month}")
        print(f"   日主 {test_bazi.day.stem} 在日支 {test_bazi.day.branch}: {chang_sheng_day}")
        print(f"   日主 {test_bazi.day.stem} 在时支 {test_bazi.hour.branch}: {chang_sheng_hour}")
        print("   ✅ 长生十二宫计算成功")
    except Exception as e:
        print(f"   ❌ 长生十二宫计算失败: {e}")
    print()
    
    # 4. 测试长生十二宫强度
    print("4. 测试长生十二宫强度:")
    try:
        strength_year = FiveElementsCalculator.get_chang_sheng_strength_level(chang_sheng_year)
        strength_month = FiveElementsCalculator.get_chang_sheng_strength_level(chang_sheng_month)
        strength_day = FiveElementsCalculator.get_chang_sheng_strength_level(chang_sheng_day)
        strength_hour = FiveElementsCalculator.get_chang_sheng_strength_level(chang_sheng_hour)
        
        print(f"   {chang_sheng_year} 的强度等级: {strength_year}")
        print(f"   {chang_sheng_month} 的强度等级: {strength_month}")
        print(f"   {chang_sheng_day} 的强度等级: {strength_day}")
        print(f"   {chang_sheng_hour} 的强度等级: {strength_hour}")
        print("   ✅ 长生十二宫强度计算成功")
    except Exception as e:
        print(f"   ❌ 长生十二宫强度计算失败: {e}")
    print()
    
    # 5. 测试人生阶段分析
    print("5. 测试人生阶段分析:")
    try:
        for age in [8, 18, 28, 38, 48, 58, 68, 78]:
            phase = FiveElementsCalculator.analyze_dayun_phase(age)
            print(f"   {age}岁: {phase}")
        print("   ✅ 人生阶段分析成功")
    except Exception as e:
        print(f"   ❌ 人生阶段分析失败: {e}")
    print()
    
    print("✅ 重构后的函数测试完成！")

if __name__ == "__main__":
    test_refactored_functions()
