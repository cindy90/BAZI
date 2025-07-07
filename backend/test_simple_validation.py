#!/usr/bin/env python
"""
简化的验证测试
"""
import json
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    print("=== 简化验证测试 ===")
    
    # 1. 测试 constants.py 导入
    try:
        from app.services.constants import JIAZI_TABLE
        print(f"✓ JIAZI_TABLE 导入成功，长度: {len(JIAZI_TABLE)}")
        if len(JIAZI_TABLE) == 60:
            print("✓ JIAZI_TABLE 长度正确")
        else:
            print(f"❌ JIAZI_TABLE 长度错误，期望60，实际{len(JIAZI_TABLE)}")
    except Exception as e:
        print(f"❌ constants.py 导入失败: {e}")
    
    # 2. 测试节气数据
    try:
        if os.path.exists('solar_terms_data.json'):
            with open('solar_terms_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            year_2024 = data.get('2024', {})
            print(f"✓ 节气数据加载成功，2024年有{len(year_2024)}个节气")
            if len(year_2024) == 24:
                print("✓ 节气数据数量正确")
            else:
                print(f"❌ 节气数据数量错误，期望24，实际{len(year_2024)}")
        else:
            print("❌ solar_terms_data.json 不存在")
    except Exception as e:
        print(f"❌ 节气数据测试失败: {e}")
    
    # 3. 测试神煞规则
    try:
        if os.path.exists('shensha_rules.json'):
            with open('shensha_rules.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            interactions = data.get('shensha_interactions', {})
            print(f"✓ 神煞规则加载成功，有{len(interactions)}个互动规则")
            if len(interactions) > 0:
                print("✓ 神煞互动规则数量正确")
            else:
                print("❌ 神煞互动规则为空")
        else:
            print("❌ shensha_rules.json 不存在")
    except Exception as e:
        print(f"❌ 神煞规则测试失败: {e}")
    
    # 4. 测试计算器导入
    try:
        from app.services.calculators import ShenShaCalculator
        calculator = ShenShaCalculator()
        print("✓ ShenShaCalculator 导入成功")
        
        if hasattr(calculator, '_apply_single_effect'):
            print("✓ _apply_single_effect 方法存在")
        else:
            print("❌ _apply_single_effect 方法不存在")
    except Exception as e:
        print(f"❌ 计算器导入失败: {e}")
    
    print("\n=== 验证完成 ===")

if __name__ == "__main__":
    main()
