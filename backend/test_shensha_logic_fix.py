#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试神煞判定逻辑修复
验证官杀印绶和冲合计算的准确性
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.bazi_calculator import calculate_bazi_data
from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
from app.services.core import Bazi, StemBranch
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime


def test_ten_god_logic():
    """测试十神关系判断逻辑"""
    print("=== 测试十神关系判断逻辑 ===")
    
    # 创建测试八字：甲木日主
    bazi = Bazi(
        year=StemBranch("壬", "寅"),   # 壬水生甲木 -> 偏印
        month=StemBranch("庚", "申"),  # 庚金克甲木 -> 七杀
        day=StemBranch("甲", "子"),    # 甲木日主，子水生甲木 -> 正印(藏干癸水)
        hour=StemBranch("丁", "巳"),   # 丁火泄甲木 -> 伤官
        gender="男"
    )
    
    calculator = ShenShaCalculator()
    
    # 测试官杀印绶检查
    has_official_or_seal = calculator._check_with_official_or_seal(bazi)
    has_seal = calculator._check_with_seal(bazi)
    
    print(f"八字: {bazi.year} {bazi.month} {bazi.day} {bazi.hour}")
    print(f"日主: {bazi.day.stem}")
    print(f"检查官杀印绶: {has_official_or_seal}")
    print(f"检查印绶: {has_seal}")
    
    # 验证十神关系
    day_stem = bazi.day.stem
    test_cases = [
        ("壬", day_stem, "偏印"),
        ("庚", day_stem, "七杀"), 
        ("癸", day_stem, "正印"),  # 子水藏干
        ("丁", day_stem, "伤官")
    ]
    
    print("\n十神关系验证:")
    for other_stem, day_stem, expected in test_cases:
        actual = FiveElementsCalculator.calculate_ten_god_relation(other_stem, day_stem)
        print(f"{other_stem} -> {day_stem}: 期望={expected}, 实际={actual}, 匹配={actual == expected}")


def test_conflict_harmony_logic():
    """测试冲合计算逻辑"""
    print("\n=== 测试冲合计算逻辑 ===")
    
    # 创建测试八字：包含子午冲和丑未冲
    bazi = Bazi(
        year=StemBranch("甲", "子"),   
        month=StemBranch("丙", "午"),  # 子午冲
        day=StemBranch("戊", "丑"),    
        hour=StemBranch("庚", "未"),   # 丑未冲
        gender="男"
    )
    
    calculator = ShenShaCalculator()
    
    print(f"八字: {bazi.year} {bazi.month} {bazi.day} {bazi.hour}")
    
    # 测试冲合计算
    test_branches = ["子", "午", "丑", "未", "寅", "申"]
    
    print("\n冲合计算验证:")
    for branch in test_branches:
        conflicts = calculator._count_conflicts(bazi, branch)
        harmonies = calculator._count_harmonies(bazi, branch)
        print(f"地支{branch}: 冲={conflicts}次, 合={harmonies}次")


async def test_complete_shensha():
    """测试完整的神煞计算"""
    print("\n=== 测试完整神煞计算 ===")
    
    request = BaziCalculateRequest(
        birth_datetime=datetime(1990, 6, 15, 14, 30),
        birth_place='北京',
        gender='男',
        name=None,
        is_solar_time=True,
        longitude=None,
        latitude=None,
        timezone_offset=None
    )
    
    result = await calculate_bazi_data(request)
    
    print(f"八字: {result.bazi_characters}")
    print(f"日主: {result.day_master_element}")
    print(f"喜用神: {result.favorable_elements}")
    
    if result.shen_sha_details:
        print(f"神煞数量: {len(result.shen_sha_details)}")
        for i, shensha in enumerate(result.shen_sha_details):
            name = shensha.get('name', '')
            position = shensha.get('position', '')
            description = shensha.get('description', '')
            strength = shensha.get('strength', 0)
            print(f"  {i+1}. {name} ({position}): 强度={strength:.2f}, {description}")
    else:
        print("未找到神煞信息")


async def main():
    """主测试函数"""
    test_ten_god_logic()
    test_conflict_harmony_logic()
    await test_complete_shensha()


if __name__ == "__main__":
    asyncio.run(main())
