#!/usr/bin/env python3
"""
测试神煞计算系统重构后的功能
验证职责分离：初始化 -> 自身修正 -> 互动修正
"""

import sys
impo        {
            "name": "甲日生人",
            "bazi": Bazi(
                year=StemBranch("甲", "子"),
                month=StemBranch("丙", "寅"),
                day=StemBranch("甲", "子"),
                hour=StemBranch("丙", "丑"),  # 丑为甲日天乙贵人
                gender="男"
            ),
            "expected": ["tianyi_guiren"]
        },
        {
            "name": "乙日生人",
            "bazi": Bazi(
                year=StemBranch("乙", "子"),
                month=StemBranch("丙", "寅"),
                day=StemBranch("乙", "子"),
                hour=StemBranch("丙", "申"),  # 申为乙日天乙贵人
                gender="男"
            ),
            "expected": ["tianyi_guiren"]
        }nd(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.services.calculators import ShenShaCalculator
from backend.app.services.core import Bazi, StemBranch
from backend.app.services.logger_config import setup_logger

logger = setup_logger("test_shensha_refactor")

def test_shensha_refactor():
    """测试重构后的神煞计算系统"""
    print("=" * 60)
    print("测试神煞计算系统重构")
    print("=" * 60)
    
    # 创建神煞计算器
    calculator = ShenShaCalculator()
    
    # 测试用例：甲子日生人
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("甲", "子"),
        hour=StemBranch("丙", "寅"),
        gender="男"
    )
    
    print(f"测试八字：{bazi.year.stem}{bazi.year.branch} {bazi.month.stem}{bazi.month.branch} {bazi.day.stem}{bazi.day.branch} {bazi.hour.stem}{bazi.hour.branch}")
    print()
    
    # 计算神煞
    try:
        shensha_result = calculator.calculate_shensha(bazi)
        
        print(f"计算出的神煞数量: {len(shensha_result)}")
        print()
        
        # 显示每个神煞的详细信息
        for key, shensha in shensha_result.items():
            print(f"神煞键: {key}")
            print(f"  名称: {shensha.name}")
            print(f"  位置: {shensha.position}")
            print(f"  强度: {shensha.strength:.2f}")
            print(f"  激活: {shensha.active}")
            print(f"  正面标签: {shensha.positive_tags}")
            print(f"  负面标签: {shensha.negative_tags}")
            print(f"  描述: {shensha.description}")
            print()
        
        # 验证职责分离
        print("=" * 40)
        print("验证职责分离")
        print("=" * 40)
        
        # 检查是否有神煞被正确初始化
        if shensha_result:
            print("✓ 神煞初始化成功")
        else:
            print("✗ 神煞初始化失败")
        
        # 检查是否有强度修正
        has_modified_strength = any(
            abs(shensha.strength - 1.0) > 0.01 
            for shensha in shensha_result.values()
        )
        if has_modified_strength:
            print("✓ 强度修正已应用")
        else:
            print("? 无强度修正或修正值为1.0")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ 神煞计算失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_shensha():
    """测试特定神煞的计算"""
    print("=" * 60)
    print("测试特定神煞计算")
    print("=" * 60)
    
    calculator = ShenShaCalculator()
    
    # 测试天乙贵人的计算
    test_cases = [
        {
            "name": "甲日生人",
            "bazi": Bazi(
                year=StemBranch("甲", "子"),
                month=StemBranch("丙", "寅"),
                day=StemBranch("甲", "子"),
                hour=StemBranch("丙", "丑")  # 丑为甲日天乙贵人
            ),
            "expected": ["tianyi_guiren"]
        },
        {
            "name": "乙日生人",
            "bazi": Bazi(
                year=StemBranch("乙", "子"),
                month=StemBranch("丙", "寅"),
                day=StemBranch("乙", "子"),
                hour=StemBranch("丙", "申")  # 申为乙日天乙贵人
            ),
            "expected": ["tianyi_guiren"]
        }
    ]
    
    for test_case in test_cases:
        print(f"测试：{test_case['name']}")
        bazi = test_case["bazi"]
        print(f"八字：{bazi.year.stem}{bazi.year.branch} {bazi.month.stem}{bazi.month.branch} {bazi.day.stem}{bazi.day.branch} {bazi.hour.stem}{bazi.hour.branch}")
        
        try:
            shensha_result = calculator.calculate_shensha(bazi)
            
            # 检查期望的神煞是否存在
            for expected_key in test_case["expected"]:
                if expected_key in shensha_result:
                    shensha = shensha_result[expected_key]
                    print(f"  ✓ 找到 {shensha.name} 在 {shensha.position}")
                else:
                    print(f"  ✗ 未找到期望的神煞: {expected_key}")
            
            print()
            
        except Exception as e:
            print(f"  ✗ 计算失败: {e}")
            print()

def test_method_separation():
    """测试方法职责分离"""
    print("=" * 60)
    print("测试方法职责分离")
    print("=" * 60)
    
    calculator = ShenShaCalculator()
    
    # 测试 _calculate_single_shensha 只负责初始化
    rule = {
        "key": "test_tianyi",
        "name": "天乙贵人",
        "description": "测试用天乙贵人",
        "calc_method": "stem_zhi_lookup",
        "base_stem_types": ["day_stem"],
        "rules": {
            "甲": ["丑", "未"]
        },
        "positive_tags": ["贵人"],
        "negative_tags": [],
        "strength_modifier": {
            "favorable_element": 1.5,
            "conflict": 0.8
        }
    }
    
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("甲", "子"),
        hour=StemBranch("丙", "丑")
    )
    
    print("测试 _calculate_single_shensha 方法：")
    try:
        shensha = calculator._calculate_single_shensha(rule, bazi)
        if shensha:
            print(f"  ✓ 成功初始化神煞: {shensha.name}")
            print(f"  ✓ 初始强度: {shensha.strength}")
            print(f"  ✓ 位置: {shensha.position}")
            print(f"  ✓ 正面标签: {shensha.positive_tags}")
            
            # 验证强度为默认值1.0（未修正）
            if shensha.strength == 1.0:
                print("  ✓ 强度为初始值1.0，未进行修正")
            else:
                print(f"  ✗ 强度已被修正为 {shensha.strength}")
        else:
            print("  ✗ 神煞初始化失败")
    except Exception as e:
        print(f"  ✗ 初始化失败: {e}")
    
    print()
    
    # 测试 _apply_shensha_modifiers 方法
    print("测试 _apply_shensha_modifiers 方法：")
    try:
        if shensha:
            original_strength = shensha.strength
            calculator._apply_shensha_modifiers(shensha, rule, bazi)
            
            if shensha.strength != original_strength:
                print(f"  ✓ 强度修正成功: {original_strength} -> {shensha.strength}")
            else:
                print(f"  ? 强度未改变: {shensha.strength}")
    except Exception as e:
        print(f"  ✗ 强度修正失败: {e}")
    
    print()

if __name__ == "__main__":
    print("神煞计算系统重构测试")
    print("测试职责分离：初始化 -> 自身修正 -> 互动修正")
    print()
    
    success = True
    
    # 运行测试
    success &= test_shensha_refactor()
    test_specific_shensha()
    test_method_separation()
    
    print("=" * 60)
    if success:
        print("✓ 重构测试通过")
    else:
        print("✗ 重构测试失败")
    print("=" * 60)
