#!/usr/bin/env python3
"""
简单集成测试 - 验证核心功能
"""
import sys
import os
sys.path.append('.')

from app.services.core import Bazi, StemBranch
from app.services.calculators import ShenShaCalculator, FiveElementsCalculator

def test_core_functions():
    print("🎯 开始核心功能测试")
    
    # 创建测试八字
    year_sb = StemBranch("庚", "午")
    month_sb = StemBranch("庚", "辰") 
    day_sb = StemBranch("甲", "子")
    hour_sb = StemBranch("庚", "午")
    
    bazi = Bazi(year_sb, month_sb, day_sb, hour_sb, "男")
    
    print(f"✅ 八字对象创建成功: {bazi.get_bazi_characters()}")
    print(f"✅ 日主: {bazi.get_day_master()}")
    print(f"✅ 生肖: {bazi.get_zodiac()}")
    
    # 测试神煞计算器
    calculator = ShenShaCalculator()
    
    # 测试纳音功能
    nayin_name, nayin_index = calculator.get_nayin_name_and_element("甲", "子")
    print(f"✅ 纳音测试: 甲子 = {nayin_name} (索引: {nayin_index})")
    
    # 测试干支互动分析
    interactions = calculator.analyze_interactions(bazi)
    print(f"✅ 干支互动分析: {len(interactions)} 类别")
    for key, value in interactions.items():
        print(f"   - {key}: {len(value)} 个")
    
    # 测试五行计算
    five_elements = FiveElementsCalculator.calculate_five_elements_percentage(bazi)
    print(f"✅ 五行百分比: {five_elements}")
    
    day_strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
    print(f"✅ 日主强弱: {day_strength}")
    
    print("🎉 所有核心功能测试通过!")

if __name__ == "__main__":
    test_core_functions()
