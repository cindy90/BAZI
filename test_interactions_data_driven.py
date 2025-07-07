#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试重构后的 calculators.py 中的 _check_shensha_interactions 方法
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from app.services.calculators import ShenShaCalculator
from app.services.core import Bazi, StemBranch
from datetime import datetime

def test_shensha_interactions():
    """测试神煞互动功能"""
    print("=" * 50)
    print("测试神煞互动功能")
    print("=" * 50)
    
    # 创建测试八字
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("壬", "午"),
        hour=StemBranch("庚", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    print(f"测试八字: {bazi.year.stem}{bazi.year.branch} {bazi.month.stem}{bazi.month.branch} {bazi.day.stem}{bazi.day.branch} {bazi.hour.stem}{bazi.hour.branch}")
    
    # 创建神煞计算器
    calculator = ShenShaCalculator()
    
    # 计算神煞
    shensha_result = calculator.calculate_shensha(bazi)
    
    print(f"\n发现神煞 {len(shensha_result)} 个:")
    for key, shensha in shensha_result.items():
        print(f"  {key}: {shensha.name}")
        print(f"    位置: {shensha.position}")
        print(f"    强度: {shensha.strength:.2f}")
        print(f"    激活: {shensha.active}")
        print(f"    标签: {shensha.tags}")
        print(f"    描述: {shensha.description}")
        print()
    
    # 测试互动规则
    print("=" * 50)
    print("测试互动规则加载")
    print("=" * 50)
    
    interactions = calculator.shensha_data.get("shensha_interactions", {})
    print(f"加载的互动规则数量: {len(interactions)}")
    
    for rule_name, rule_data in interactions.items():
        print(f"  {rule_name}: {rule_data.get('name', '未命名')}")
        print(f"    条件: {rule_data.get('condition', '未设置')}")
        print(f"    神煞键: {rule_data.get('shensha_keys', [])}")
        print()
    
    print("测试完成！")

if __name__ == "__main__":
    test_shensha_interactions()
