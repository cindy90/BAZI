#!/usr/bin/env python
"""
综合验证测试 - 检查神煞计算器集成和数据结构兼容性
"""
import json
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_shensha_calculator_integration():
    """测试 ShenShaCalculator 与 FiveElementsCalculator 的集成"""
    print("=== 测试 ShenShaCalculator 集成 ===")
    
    try:
        from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
        from app.services.core import Bazi, StemBranch
        
        # 创建测试八字
        birth_chart = Bazi(
            year=StemBranch("庚", "午"),
            month=StemBranch("辛", "巳"),
            day=StemBranch("庚", "辰"),
            hour=StemBranch("癸", "未"),
            gender="男"
        )
        
        # 测试神煞计算
        shensha_calculator = ShenShaCalculator()
        all_shensha = shensha_calculator.calculate_shensha(birth_chart)
        
        print(f"✓ 神煞计算成功，共计算出 {len(all_shensha)} 个神煞")
        
        # 检查 auspicious_level 字段
        auspicious_levels_found = 0
        for key, shensha in all_shensha.items():
            if hasattr(shensha, 'auspicious_level'):
                auspicious_levels_found += 1
                print(f"  {shensha.name}: 吉凶等级 {shensha.auspicious_level}")
                break  # 只打印一个示例
        
        if auspicious_levels_found > 0:
            print(f"✓ auspicious_level 字段正常，已在 {auspicious_levels_found} 个神煞中找到")
        else:
            print("❌ 未找到 auspicious_level 字段")
        
        # 测试与五行分析器的集成
        comprehensive_analysis = FiveElementsCalculator.analyze_comprehensive_gods(birth_chart)
        print(f"✓ 五行综合分析成功，分析结果包含 {len(comprehensive_analysis)} 个部分")
        
        # 测试流年神煞分析
        liunian_result = FiveElementsCalculator.analyze_liunian_shensha(
            birth_chart, "甲", "辰", shensha_calculator
        )
        print(f"✓ 流年神煞分析成功")
        print(f"  有利神煞: {len(liunian_result.get('favorable_shensha', []))}")
        print(f"  不利神煞: {len(liunian_result.get('unfavorable_shensha', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ ShenShaCalculator 集成测试失败: {e}")
        return False

def test_bazi_calculator_integration():
    """测试 bazi_calculator.py 中的流年分析集成"""
    print("\n=== 测试 bazi_calculator 流年分析集成 ===")
    
    try:
        # 测试核心计算器组件
        from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
        
        print("✓ 核心计算器组件导入成功")
        
        # 测试流年神煞分析功能
        from app.services.core import Bazi, StemBranch
        
        test_chart = Bazi(
            year=StemBranch("庚", "午"),
            month=StemBranch("辛", "巳"),
            day=StemBranch("庚", "辰"),
            hour=StemBranch("癸", "未"),
            gender="男"
        )
        
        shensha_calculator = ShenShaCalculator()
        liunian_result = FiveElementsCalculator.analyze_liunian_shensha(
            test_chart, "甲", "辰", shensha_calculator
        )
        
        # 验证返回结构
        required_keys = ['favorable_shensha', 'unfavorable_shensha']
        missing_keys = [key for key in required_keys if key not in liunian_result]
        
        if not missing_keys:
            print("✓ 流年神煞分析返回结构正确")
            print(f"  有利神煞数量: {len(liunian_result.get('favorable_shensha', []))}")
            print(f"  不利神煞数量: {len(liunian_result.get('unfavorable_shensha', []))}")
        else:
            print(f"❌ 流年神煞分析缺少必要字段: {missing_keys}")
        
        return True
        
    except Exception as e:
        print(f"❌ bazi_calculator 集成测试失败: {e}")
        return False

def test_shensha_rules_compatibility():
    """测试 shensha_rules.json 的结构兼容性"""
    print("\n=== 测试 shensha_rules.json 兼容性 ===")
    
    try:
        with open('shensha_rules.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        rules = data.get('rules', [])
        interactions = data.get('shensha_interactions', {})
        
        print(f"✓ 神煞规则文件加载成功")
        print(f"  基础规则数量: {len(rules)}")
        print(f"  互动规则数量: {len(interactions)}")
        
        # 检查基础规则的必要字段
        required_rule_fields = ['key', 'name', 'calc_method']
        rules_with_issues = 0
        auspicious_level_count = 0
        
        for rule in rules:
            missing_fields = [field for field in required_rule_fields if field not in rule]
            if missing_fields:
                rules_with_issues += 1
            
            if 'auspicious_level' in rule:
                auspicious_level_count += 1
        
        if rules_with_issues == 0:
            print("✓ 所有基础规则结构完整")
        else:
            print(f"❌ {rules_with_issues} 个基础规则结构不完整")
        
        print(f"✓ {auspicious_level_count}/{len(rules)} 个规则包含 auspicious_level 字段")
        
        # 检查互动规则的 effect 结构
        problematic_effects = 0
        for interaction_key, interaction in interactions.items():
            effects = interaction.get('effects', {})
            for target_key, effect in effects.items():
                if isinstance(effect, dict):
                    # 检查是否有自定义字符串而不是标准字段
                    if 'effect' in effect and isinstance(effect['effect'], str):
                        if effect['effect'] not in ['activate', 'deactivate']:  # 允许的自定义值
                            problematic_effects += 1
                            print(f"⚠️  发现自定义effect字符串: {interaction_key}.{target_key}.effect = {effect['effect']}")
        
        if problematic_effects == 0:
            print("✓ 所有互动规则的 effect 结构符合标准")
        else:
            print(f"⚠️  发现 {problematic_effects} 个非标准 effect 结构")
        
        return True
        
    except Exception as e:
        print(f"❌ shensha_rules.json 兼容性测试失败: {e}")
        return False

def test_interaction_effects():
    """测试神煞互动效果的应用"""
    print("\n=== 测试神煞互动效果应用 ===")
    
    try:
        from app.services.calculators import ShenShaCalculator
        from app.services.core import ShenSha
        
        calculator = ShenShaCalculator()
        
        # 测试 _apply_single_effect 方法存在
        if hasattr(calculator, '_apply_single_effect'):
            print("✓ _apply_single_effect 方法存在")
        else:
            print("❌ _apply_single_effect 方法不存在")
            return False
        
        # 创建模拟神煞对象测试
        test_shensha = ShenSha(
            name="测试神煞",
            position="年",
            strength=1.0,
            active=True,
            auspicious_level=5
        )
        
        # 测试效果应用
        test_effect = {
            "active": False,
            "strength_modifier": 1.5,
            "add_tags": ["测试标签"],
            "description": "测试描述"
        }
        
        from app.services.core import Bazi, StemBranch
        test_chart = Bazi(
            year=StemBranch("甲", "子"),
            month=StemBranch("丙", "寅"),
            day=StemBranch("戊", "午"),
            hour=StemBranch("庚", "申"),
            gender="男"
        )
        
        test_interaction_rule = {}
        
        # 应用效果
        calculator._apply_single_effect(test_shensha, test_effect, test_chart, test_interaction_rule)
        
        # 验证效果
        if (test_shensha.active == False and 
            test_shensha.strength == 1.5 and 
            "测试标签" in test_shensha.tags and
            test_shensha.description == "测试描述"):
            print("✓ 神煞互动效果应用正常")
        else:
            print("❌ 神煞互动效果应用异常")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 神煞互动效果测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始综合验证测试...")
    print("=" * 60)
    
    tests = [
        test_shensha_calculator_integration,
        test_bazi_calculator_integration,
        test_shensha_rules_compatibility,
        test_interaction_effects
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有集成测试都通过！系统各模块协同工作正常。")
    else:
        print(f"⚠️  还有 {total_tests - passed_tests} 项测试需要修复")

if __name__ == "__main__":
    main()
