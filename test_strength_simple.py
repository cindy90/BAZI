#!/usr/bin/env python3
"""
测试日主强度等级描述功能 - 简化版
"""

def get_strength_level_description(strength: float) -> str:
    """将浮点强度转换为文本描述"""
    if strength < 0.3:
        return "偏弱"
    elif strength < 0.4:
        return "较弱"
    elif strength < 0.6:
        return "中和"
    elif strength < 0.7:
        return "较强"
    elif strength < 0.8:
        return "偏强"
    else:
        return "极强"

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
    
    all_pass = True
    for strength, expected in test_cases:
        result = get_strength_level_description(strength)
        status = "✓" if result == expected else "✗"
        print(f"{strength:4.1f} -> {result:4s} {status}")
        
        if result != expected:
            print(f"  预期: {expected}, 实际: {result}")
            all_pass = False
    
    print(f"\n=== 测试完成 {'✓ 全部通过' if all_pass else '✗ 有失败'} ===")

if __name__ == "__main__":
    test_strength_level_descriptions()
