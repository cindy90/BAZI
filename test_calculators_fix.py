#!/usr/bin/env python3
"""
测试修复后的 calculators.py 导入
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=== 测试 calculators.py 修复 ===")

try:
    print("1. 测试导入 calculators 模块...")
    from app.services.calculators import FiveElementsCalculator
    print("✓ 成功导入 FiveElementsCalculator")
    
    print("2. 测试创建实例...")
    calc = FiveElementsCalculator()
    print("✓ 成功创建实例")
    
    print("3. 测试常量访问...")
    from app.services.calculators import STEM_ELEMENTS
    print(f"✓ STEM_ELEMENTS: {list(STEM_ELEMENTS.keys())[:5]}")
    
    print("4. 测试藏干数据...")
    from app.services.calculators import BRANCH_HIDDEN_STEMS
    print(f"✓ BRANCH_HIDDEN_STEMS['子']: {BRANCH_HIDDEN_STEMS.get('子', {})}")
    
    print("\n=== 所有测试通过 ===")
    
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
