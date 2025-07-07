#!/usr/bin/env python
"""
验证神煞 auspicious_level 和 effect 字段修复
"""
import json
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_auspicious_level():
    """测试 auspicious_level 字段"""
    print("=== 测试 auspicious_level 字段 ===")
    
    try:
        from app.services.calculators import ShenShaCalculator
        from app.services.core import ShenSha, Bazi, StemBranch
        
        # 创建测试八字
        birth_chart = Bazi(
            year=StemBranch("甲", "子"),
            month=StemBranch("丙", "寅"),
            day=StemBranch("戊", "午"),
            hour=StemBranch("庚", "申"),
            gender="男",
            birth_time=datetime(1984, 2, 15, 14, 30)
        )
        
        calculator = ShenShaCalculator()
        all_shensha = calculator.calculate_shensha(birth_chart)
        
        print(f"计算出的神煞数量: {len(all_shensha)}")
        
        # 检查神煞是否有 auspicious_level 字段
        for key, shensha in all_shensha.items():
            if shensha.active:
                print(f"神煞: {shensha.name}")
                print(f"  位置: {shensha.position}")
                print(f"  强度: {shensha.strength}")
                print(f"  吉凶等级: {shensha.auspicious_level}")
                print(f"  描述: {shensha.description}")
                print()
                
                # 验证 auspicious_level 是否存在
                assert hasattr(shensha, 'auspicious_level'), f"神煞 {shensha.name} 缺少 auspicious_level 字段"
                assert isinstance(shensha.auspicious_level, int), f"神煞 {shensha.name} 的 auspicious_level 不是整数"
                assert 1 <= shensha.auspicious_level <= 10, f"神煞 {shensha.name} 的 auspicious_level 不在 1-10 范围内"
        
        print("✓ auspicious_level 字段测试通过")
        return True
        
    except Exception as e:
        print(f"❌ auspicious_level 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_effect_deactivate():
    """测试 effect 字段不再有自定义字符串"""
    print("\n=== 测试 effect 字段格式 ===")
    
    try:
        with open('shensha_rules.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查神煞规则中的 interactions
        deactivate_found = False
        for rule in data.get("rules", []):
            interactions = rule.get("interactions", {})
            for interaction_name, interaction in interactions.items():
                if "effect" in interaction and interaction["effect"] == "deactivate":
                    deactivate_found = True
                    print(f"❌ 发现自定义字符串 'deactivate' 在 {rule['name']} -> {interaction_name}")
        
        # 检查 shensha_interactions 中的 effects
        for interaction_name, interaction in data.get("shensha_interactions", {}).items():
            effects = interaction.get("effects", {})
            for effect_key, effect in effects.items():
                if "effect" in effect and effect["effect"] == "deactivate":
                    deactivate_found = True
                    print(f"❌ 发现自定义字符串 'deactivate' 在 {interaction_name} -> {effect_key}")
        
        if not deactivate_found:
            print("✓ 没有发现 'deactivate' 自定义字符串")
            print("✓ effect 字段格式测试通过")
            return True
        else:
            print("❌ 仍有 'deactivate' 自定义字符串需要修复")
            return False
            
    except Exception as e:
        print(f"❌ effect 字段测试失败: {e}")
        return False

def test_shensha_output():
    """测试神煞输出包含 auspicious_level"""
    print("\n=== 测试神煞输出格式 ===")
    
    try:
        from app.services.calculators import ShenShaCalculator
        from app.services.core import Bazi, StemBranch
        
        # 创建测试八字
        birth_chart = Bazi(
            year=StemBranch("甲", "子"),
            month=StemBranch("丙", "寅"),
            day=StemBranch("戊", "午"),
            hour=StemBranch("庚", "申"),
            gender="男",
            birth_time=datetime(1984, 2, 15, 14, 30)
        )
        
        calculator = ShenShaCalculator()
        result = calculator.analyze_interactions(birth_chart)
        
        # 检查输出格式
        for shensha_info in result.get("favorable_shensha", []) + result.get("unfavorable_shensha", []):
            print(f"检查神煞输出: {shensha_info['name']}")
            
            # 验证必要字段
            assert "name" in shensha_info, "缺少 name 字段"
            assert "position" in shensha_info, "缺少 position 字段"
            assert "strength" in shensha_info, "缺少 strength 字段"
            assert "description" in shensha_info, "缺少 description 字段"
            assert "auspicious_level" in shensha_info, "缺少 auspicious_level 字段"
            
            print(f"  吉凶等级: {shensha_info['auspicious_level']}")
        
        print("✓ 神煞输出格式测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 神煞输出测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始验证 auspicious_level 和 effect 字段修复...")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    if test_auspicious_level():
        success_count += 1
    
    if test_effect_deactivate():
        success_count += 1
    
    if test_shensha_output():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"测试完成: {success_count}/{total_tests} 项测试通过")
    
    if success_count == total_tests:
        print("🎉 所有修复验证通过！")
    else:
        print(f"⚠️  还有 {total_tests - success_count} 项需要检查")

if __name__ == "__main__":
    main()
