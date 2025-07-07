#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试高级大运计算器
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from advanced_dayun_calculator import AdvancedDayunCalculator

def test_advanced_dayun():
    """测试高级大运计算器"""
    print("=== 测试高级大运计算器 ===")
    
    # 高泽兮案例
    birth_time = datetime(2023, 9, 14, 0, 26)
    gender = "女"
    year_gan = "癸"
    
    print(f"出生时间: {birth_time}")
    print(f"性别: {gender}")
    print(f"年干: {year_gan}")
    
    try:
        calculator = AdvancedDayunCalculator()
        
        # 计算起运年龄
        qiyun_age, explanation = calculator.calculate_qiyun_age(birth_time, year_gan, gender)
        print(f"\n起运年龄: {qiyun_age:.2f} 岁")
        print(f"计算说明: {explanation}")
        
        # 计算完整大运
        dayun_result = calculator.calculate_dayun(birth_time, year_gan, gender, "辛酉")
        print(f"\n大运计算结果:")
        print(f"起运年龄: {dayun_result['qiyun_age']:.2f} 岁")
        print(f"大运数量: {len(dayun_result['dayun_pillars'])}")
        
        for i, pillar in enumerate(dayun_result['dayun_pillars'][:5]):
            print(f"第{i+1}步大运: {pillar['ganzhi']} ({pillar['start_age']}-{pillar['end_age']}岁)")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_advanced_dayun()
    if success:
        print("\n✓ 高级大运计算器测试成功")
    else:
        print("\n✗ 高级大运计算器测试失败")
