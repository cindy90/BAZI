#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查不完整案例的原始数据
"""

import csv
import json

def check_incomplete_cases():
    """检查不完整案例的原始数据"""
    
    # 从验证报告中获取不完整案例的ID
    incomplete_cases = ['19', '41', '46', '47', '48', '49', '50']
    
    print("=" * 80)
    print("🔍 检查不完整案例的原始数据")
    print("=" * 80)
    
    try:
        with open('八字命理案例数据.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, 1):
                if str(i) in incomplete_cases:
                    print(f"\n📋 案例 {i}: {row.get('姓名', 'Unknown')}")
                    print("-" * 40)
                    
                    # 检查四柱信息
                    pillars = ['年柱', '月柱', '日柱', '时柱']
                    for pillar in pillars:
                        col = f'标准_{pillar}'
                        value = row.get(col, '缺失')
                        print(f"  {pillar}: {value}")
                    
                    # 检查五行得分
                    elements = ['木', '火', '土', '金', '水']
                    print(f"  五行得分:")
                    for elem in elements:
                        col = f'标准_五行得分_{elem}'
                        value = row.get(col, '缺失')
                        print(f"    {elem}: {value}")
                    
                    # 检查旺衰
                    strength = row.get('标准_日主旺衰', '缺失')
                    print(f"  日主旺衰: {strength}")
                    
                    # 检查出生信息
                    birth_fields = ['阳历生日_年', '阳历生日_月', '阳历生日_日', '阳历生日_时']
                    print(f"  出生信息:")
                    for field in birth_fields:
                        value = row.get(field, '缺失')
                        print(f"    {field}: {value}")
                    
                    print()
                    
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")

if __name__ == "__main__":
    check_incomplete_cases()
