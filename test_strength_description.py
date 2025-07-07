#!/usr/bin/env python3
"""
测试日主强度等级描述功能
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.services.calculators import FiveElementsCalculator

def test_strength_level_descriptions():
    """测试强度等级描述"""
    test_cases = [
        (0.1, "偏弱"),
        (0.2, "偏弱"),
        (0.3, "较弱"),
        (0.35, "较弱"),
        (0.4, "中和"),
        (0.5, "中和"),
        (0.6, "较强"),
        (0.65, "较强"),
        (0.7, "偏强"),
        (0.75, "偏强"),
        (0.8, "极强"),
        (0.9, "极强"),
    ]
    
    print("=== 日主强度等级描述测试 ===")
    print("强度值 -> 描述")
    print("-" * 25)
    
    for strength, expected in test_cases:
        result = FiveElementsCalculator.get_strength_level_description(strength)
        status = "✓" if result == expected else "✗"
        print(f"{strength:4.1f} -> {result:4s} {status}")
        
        if result != expected:
            print(f"  预期: {expected}, 实际: {result}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_strength_level_descriptions()
