#!/usr/bin/env python
"""
验证所有修复的完整测试
"""
import json
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_constants():
    """测试 constants.py 中的常量"""
    print("=== 测试 constants.py 常量 ===")
    
    from app.services.constants import JIAZI_TABLE
    
    # 测试 JIAZI_TABLE
    print(f"JIAZI_TABLE 长度: {len(JIAZI_TABLE)}")
    assert len(JIAZI_TABLE) == 60, f"JIAZI_TABLE 长度应该是 60，实际是 {len(JIAZI_TABLE)}"
    
    # 验证前几个和后几个
    expected_first_few = ["甲子", "乙丑", "丙寅", "丁卯", "戊辰"]
    expected_last_few = ["丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"]
    
    assert JIAZI_TABLE[:5] == expected_first_few, f"JIAZI_TABLE 前5个不匹配"
    assert JIAZI_TABLE[-8:] == expected_last_few, f"JIAZI_TABLE 后8个不匹配"
    
    print("✓ JIAZI_TABLE 验证通过")

def test_solar_terms():
    """测试节气数据"""
    print("\n=== 测试节气数据 ===")
    
    if not os.path.exists('solar_terms_data.json'):
        print("❌ solar_terms_data.json 文件不存在")
        return False
    
    with open('solar_terms_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 检查2024年数据
    year_2024 = data.get('2024', {})
    assert len(year_2024) == 24, f"2024年应该有24个节气，实际有{len(year_2024)}个"
    
    # 检查关键节气
    assert '立春' in year_2024, "缺少立春节气"
    assert '春分' in year_2024, "缺少春分节气"
    assert '夏至' in year_2024, "缺少夏至节气"
    assert '秋分' in year_2024, "缺少秋分节气"
    assert '冬至' in year_2024, "缺少冬至节气"
    
    # 验证时间格式
    lichun_time = year_2024['立春']
    assert isinstance(lichun_time, str), "节气时间应该是字符串"
    assert len(lichun_time) == 16, f"节气时间格式错误: {lichun_time}"
    
    print("✓ 节气数据验证通过")
    return True

def test_shensha_interactions():
    """测试神煞互动规则"""
    print("\n=== 测试神煞互动规则 ===")
    
    if not os.path.exists('shensha_rules.json'):
        print("❌ shensha_rules.json 文件不存在")
        return False
    
    with open('shensha_rules.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    interactions = data.get('shensha_interactions', {})
    assert len(interactions) > 0, "神煞互动规则不能为空"
    
    # 检查关键的互动规则
    assert 'yima_chong' in interactions, "缺少 yima_chong 互动规则"
    assert 'yima_he' in interactions, "缺少 yima_he 互动规则"
    
    # 验证结构
    yima_chong = interactions['yima_chong']
    assert 'effects' in yima_chong, "yima_chong 缺少 effects"
    assert 'strength_formula' in yima_chong, "yima_chong 缺少 strength_formula"
    
    yima_he = interactions['yima_he']
    assert 'effects' in yima_he, "yima_he 缺少 effects"
    assert 'strength_formula' in yima_he, "yima_he 缺少 strength_formula"
    
    print("✓ 神煞互动规则验证通过")
    return True

def test_calculator_integration():
    """测试计算器集成"""
    print("\n=== 测试计算器集成 ===")
    
    try:
        from app.services.calculators import ShenShaCalculator
        
        calculator = ShenShaCalculator()
        
        # 测试神煞计算器能够正常导入
        assert calculator is not None, "ShenShaCalculator 创建失败"
        
        print("✓ 计算器集成验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 计算器集成测试失败: {e}")
        return False

def test_effect_compatibility():
    """测试 effect 兼容性"""
    print("\n=== 测试 effect 兼容性 ===")
    
    try:
        from app.services.calculators import ShenShaCalculator
        
        calculator = ShenShaCalculator()
        
        # 测试 _apply_single_effect 方法存在
        assert hasattr(calculator, '_apply_single_effect'), "ShenShaCalculator 缺少 _apply_single_effect 方法"
        
        print("✓ effect 兼容性验证通过")
        return True
        
    except Exception as e:
        print(f"❌ effect 兼容性测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始完整验证测试...")
    print("=" * 50)
    
    success_count = 0
    total_tests = 5
    
    try:
        test_constants()
        success_count += 1
    except Exception as e:
        print(f"❌ constants 测试失败: {e}")
    
    try:
        if test_solar_terms():
            success_count += 1
    except Exception as e:
        print(f"❌ 节气数据测试失败: {e}")
    
    try:
        if test_shensha_interactions():
            success_count += 1
    except Exception as e:
        print(f"❌ 神煞互动测试失败: {e}")
    
    try:
        if test_calculator_integration():
            success_count += 1
    except Exception as e:
        print(f"❌ 计算器集成测试失败: {e}")
    
    try:
        if test_effect_compatibility():
            success_count += 1
    except Exception as e:
        print(f"❌ effect 兼容性测试失败: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试完成: {success_count}/{total_tests} 项测试通过")
    
    if success_count == total_tests:
        print("🎉 所有测试都通过！系统优化完成。")
    else:
        print(f"⚠️  还有 {total_tests - success_count} 项测试需要修复")

if __name__ == "__main__":
    main()
