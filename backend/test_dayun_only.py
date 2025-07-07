#!/usr/bin/env python3
"""
测试大运计算专用脚本
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.services.calculators import FiveElementsCalculator

def test_dayun_calculation():
    """测试大运计算"""
    print("=== 测试大运计算 ===")
    
    # 高梦泽案例数据
    birth_time = datetime(2020, 7, 29, 13, 26)
    gender = "女"
    year_gan = "庚"
    month_pillar = "癸未"
    
    try:
        start_date, start_days, luck_pillars, start_age = FiveElementsCalculator.calculate_precise_dayun(
            birth_time, gender, year_gan, month_pillar
        )
        
        print(f"起运日期: {start_date}")
        print(f"起运天数: {start_days}")
        print(f"起运年龄: {start_age}")
        print(f"大运数量: {len(luck_pillars)}")
        
        print("\n前5步大运:")
        for i, dayun in enumerate(luck_pillars[:5]):
            if hasattr(dayun, 'stem_branch'):
                print(f"第{i+1}步: {dayun.start_age}-{dayun.end_age}岁 {dayun.stem_branch.stem}{dayun.stem_branch.branch}")
            else:
                print(f"第{i+1}步: {dayun}")
        
        # 测试格式化
        formatted_dayun = FiveElementsCalculator.format_dayun_info(start_age, luck_pillars, birth_time, "癸")
        print(f"\n格式化大运数量: {len(formatted_dayun)}")
        
        print("\n格式化前5步大运:")
        for i, dayun_info in enumerate(formatted_dayun[:5]):
            print(f"第{i+1}步: {dayun_info}")
        
        # 金标准对比
        print("\n=== 金标准对比 ===")
        expected = ["壬午", "辛巳", "庚辰", "己卯", "戊寅"]
        print("期望大运:", expected)
        actual = []
        for dayun in luck_pillars[:5]:
            if hasattr(dayun, 'stem_branch'):
                actual.append(dayun.stem_branch.stem + dayun.stem_branch.branch)
            else:
                actual.append(str(dayun))
        print("实际大运:", actual)
        
        # 检查匹配
        for i, (exp, act) in enumerate(zip(expected, actual)):
            status = "✓" if exp == act else "✗"
            print(f"第{i+1}步: 期望{exp}, 实际{act} {status}")
            
    except Exception as e:
        print(f"大运计算失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dayun_calculation()
