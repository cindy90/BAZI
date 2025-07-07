#!/usr/bin/env python3
"""
简单测试流年神煞分析重构功能
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.core import Bazi, StemBranch
from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
from datetime import datetime

def test_simple_liunian_shensha():
    """简单测试流年神煞分析"""
    print("=" * 50)
    print("简单测试流年神煞分析重构功能")
    print("=" * 50)
    
    # 创建八字对象
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),  # 戊土日主，贵人在丑未
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    print(f"本命盘：{bazi.year.stem}{bazi.year.branch}年 {bazi.day.stem}{bazi.day.branch}日")
    print(f"日主：{bazi.day.stem} (戊土日主，天乙贵人在丑未)")
    
    # 创建神煞计算器
    shen_sha_calculator = ShenShaCalculator()
    
    # 测试流年辛未（应该有天乙贵人）
    liunian_gan = "辛"
    liunian_zhi = "未"
    print(f"流年：{liunian_gan}{liunian_zhi}")
    
    # 调用重构后的方法
    liunian_shensha = FiveElementsCalculator.analyze_liunian_shensha(
        bazi, liunian_gan, liunian_zhi, shen_sha_calculator
    )
    
    print(f"\n流年神煞分析结果：")
    if liunian_shensha:
        for i, shensha in enumerate(liunian_shensha, 1):
            print(f"{i}. {shensha['name']}")
            print(f"   强度：{shensha['strength']}")
            print(f"   描述：{shensha['description']}")
            print(f"   正面标签：{shensha['positive_tags']}")
            print(f"   负面标签：{shensha['negative_tags']}")
            
            # 显示触发信息
            if 'base_stem' in shensha:
                print(f"   基准天干：{shensha['base_stem']}")
            if 'trigger_zhi' in shensha:
                print(f"   触发地支：{shensha['trigger_zhi']}")
            print()
    else:
        print("   无特殊神煞")
    
    # 测试流年癸酉（子年生人遇酉，应该有桃花）
    print("\n" + "-" * 50)
    liunian_gan2 = "癸"
    liunian_zhi2 = "酉"
    print(f"流年：{liunian_gan2}{liunian_zhi2}")
    print(f"年支：{bazi.year.branch} (子年生人，桃花在酉)")
    
    liunian_shensha2 = FiveElementsCalculator.analyze_liunian_shensha(
        bazi, liunian_gan2, liunian_zhi2, shen_sha_calculator
    )
    
    print(f"\n流年神煞分析结果：")
    if liunian_shensha2:
        for i, shensha in enumerate(liunian_shensha2, 1):
            print(f"{i}. {shensha['name']}")
            print(f"   强度：{shensha['strength']}")
            print(f"   描述：{shensha['description']}")
            print(f"   正面标签：{shensha['positive_tags']}")
            print(f"   负面标签：{shensha['negative_tags']}")
            
            # 显示触发信息
            if 'base_zhi' in shensha:
                print(f"   基准地支：{shensha['base_zhi']}")
            if 'trigger_zhi' in shensha:
                print(f"   触发地支：{shensha['trigger_zhi']}")
            print()
    else:
        print("   无特殊神煞")

if __name__ == "__main__":
    test_simple_liunian_shensha()
