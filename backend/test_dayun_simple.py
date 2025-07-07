#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试大运计算功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.services.calculators import FiveElementsCalculator

def test_dayun_simple():
    """测试大运计算"""
    print("=== 测试大运计算 ===")
    
    # 高泽兮案例
    birth_time = datetime(2023, 9, 14, 0, 26)
    gender = "女"
    year_gan = "癸"
    month_pillar = "辛酉"
    
    try:
        result = FiveElementsCalculator.calculate_precise_dayun(
            birth_time, gender, year_gan, month_pillar
        )
        print(f"返回结果长度: {len(result)}")
        print(f"返回结果类型: {type(result)}")
        
        start_date, start_days, luck_pillars, start_age = result
        print(f"起运日期: {start_date}")
        print(f"起运天数: {start_days}")
        print(f"起运年龄: {start_age}")
        print(f"大运柱数: {len(luck_pillars)}")
        
        for i, dayun in enumerate(luck_pillars[:3]):
            print(f"第{i+1}步大运: {dayun.stem_branch.stem}{dayun.stem_branch.branch} ({dayun.start_age}-{dayun.end_age}岁)")
        
        return True
        
    except Exception as e:
        print(f"大运计算失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dayun_simple()
    if success:
        print("\n✓ 大运计算测试成功")
    else:
        print("\n✗ 大运计算测试失败")
