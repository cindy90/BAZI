#!/usr/bin/env python3
"""
测试新的数据驱动神煞计算引擎
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.calculators import ShenShaCalculator
from app.services.core import StemBranch, Bazi
from datetime import datetime

def test_shensha_calculation():
    """测试神煞计算"""
    print("=" * 50)
    print("测试新的数据驱动神煞计算引擎")
    print("=" * 50)
    
    # 创建测试用例
    test_cases = [
        {
            "name": "甲子日主",
            "year": StemBranch("甲", "子"),
            "month": StemBranch("乙", "丑"),
            "day": StemBranch("甲", "子"),
            "hour": StemBranch("丙", "寅"),
            "gender": "男",
            "birth_time": datetime(1990, 4, 29, 10, 30)
        },
        {
            "name": "丙午日主",
            "year": StemBranch("庚", "午"),
            "month": StemBranch("戊", "寅"),
            "day": StemBranch("丙", "午"),
            "hour": StemBranch("己", "亥"),
            "gender": "女",
            "birth_time": datetime(1990, 4, 29, 10, 30)
        },
        {
            "name": "戊戌日主（魁罡）",
            "year": StemBranch("己", "未"),
            "month": StemBranch("丙", "寅"),
            "day": StemBranch("戊", "戌"),
            "hour": StemBranch("甲", "子"),
            "gender": "男",
            "birth_time": datetime(1990, 4, 29, 10, 30)
        }
    ]
    
    calculator = ShenShaCalculator()
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试用例: {case['name']}")
        print("-" * 30)
        
        # 创建八字
        bazi = Bazi(
            year=case["year"],
            month=case["month"],
            day=case["day"],
            hour=case["hour"],
            gender=case["gender"],
            birth_time=case["birth_time"]
        )
        
        # 计算神煞
        shensha_result = calculator.calculate(bazi)
        
        print(f"八字: {bazi.year} {bazi.month} {bazi.day} {bazi.hour}")
        print(f"性别: {case['gender']}")
        print(f"日主: {bazi.day_master}")
        print()
        
        # 打印神煞结果
        print("神煞计算结果:")
        if shensha_result:
            for key, shensha in shensha_result.items():
                if shensha.active:
                    print(f"  {shensha.name}: {shensha.position}")
                    print(f"    强度: {shensha.strength:.2f}")
                    print(f"    描述: {shensha.description}")
                    if shensha.positive_tags:
                        print(f"    正面标签: {', '.join(shensha.positive_tags)}")
                    if shensha.negative_tags:
                        print(f"    负面标签: {', '.join(shensha.negative_tags)}")
                    if shensha.tags:
                        print(f"    附加标签: {', '.join(shensha.tags)}")
                    print()
        else:
            print("  未发现活跃的神煞")
        
        print("=" * 50)

def test_specific_shensha():
    """测试特定神煞"""
    print("\n测试特定神煞计算")
    print("=" * 30)
    
    # 测试天乙贵人
    print("1. 测试天乙贵人（甲日主）")
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("乙", "丑"),  # 丑为甲日主天乙贵人
        day=StemBranch("甲", "子"),
        hour=StemBranch("丙", "未"),   # 未为甲日主天乙贵人
        gender="男"
    )
    
    calculator = ShenShaCalculator()
    shensha_result = calculator.calculate(bazi)
    
    if "tianyi_guiren" in shensha_result:
        tianyi = shensha_result["tianyi_guiren"]
        print(f"  {tianyi.name}: {tianyi.position}")
        print(f"  强度: {tianyi.strength:.2f}")
        print(f"  描述: {tianyi.description}")
        if tianyi.tags:
            print(f"  标签: {', '.join(tianyi.tags)}")
    
    # 测试桃花
    print("\n2. 测试桃花（子水见酉金）")
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("乙", "酉"),  # 酉为子年桃花
        day=StemBranch("丙", "子"),   # 子为桃花基础
        hour=StemBranch("丁", "卯"),
        gender="男"
    )
    
    shensha_result = calculator.calculate(bazi)
    
    if "tao_hua" in shensha_result:
        taohua = shensha_result["tao_hua"]
        print(f"  {taohua.name}: {taohua.position}")
        print(f"  强度: {taohua.strength:.2f}")
        print(f"  描述: {taohua.description}")
        if taohua.tags:
            print(f"  标签: {', '.join(taohua.tags)}")
    
    # 测试魁罡
    print("\n3. 测试魁罡（戊戌日）")
    bazi = Bazi(
        year=StemBranch("己", "亥"),
        month=StemBranch("乙", "亥"),
        day=StemBranch("戊", "戌"),  # 戊戌为魁罡
        hour=StemBranch("甲", "子"),
        gender="男"
    )
    
    shensha_result = calculator.calculate(bazi)
    
    if "kuigang" in shensha_result:
        kuigang = shensha_result["kuigang"]
        print(f"  {kuigang.name}: {kuigang.position}")
        print(f"  强度: {kuigang.strength:.2f}")
        print(f"  描述: {kuigang.description}")
        if kuigang.tags:
            print(f"  标签: {', '.join(kuigang.tags)}")

if __name__ == "__main__":
    test_shensha_calculation()
    test_specific_shensha()
