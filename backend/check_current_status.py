#!/usr/bin/env python
"""
检查当前系统状态
"""
import json
import os

def check_jiazi_table():
    """检查JIAZI_TABLE"""
    print("=== 检查 JIAZI_TABLE ===")
    from app.services.constants import JIAZI_TABLE
    print(f"JIAZI_TABLE 长度: {len(JIAZI_TABLE)}")
    print(f"前10个: {JIAZI_TABLE[:10]}")
    print(f"后10个: {JIAZI_TABLE[-10:]}")
    print(f"第30个: {JIAZI_TABLE[30]}")
    print(f"第59个: {JIAZI_TABLE[59]}")
    print()

def check_solar_terms():
    """检查节气数据精度"""
    print("=== 检查节气数据精度 ===")
    if os.path.exists('solar_terms_data.json'):
        with open('solar_terms_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        year_data = data.get('2024', {})
        print(f"2024年节气数据前5个:")
        for i, (term, time_str) in enumerate(year_data.items()):
            print(f"  {term}: {time_str}")
            if i >= 4:
                break
        
        # 检查是否有 00:00:00 的时间
        zero_times = []
        for term, time_str in year_data.items():
            if time_str.endswith('00:00:00'):
                zero_times.append(f"{term}: {time_str}")
        
        if zero_times:
            print(f"\n发现 {len(zero_times)} 个 00:00:00 的时间:")
            for zt in zero_times[:5]:
                print(f"  {zt}")
        else:
            print("\n✓ 没有发现 00:00:00 的时间，数据精度良好")
    else:
        print("solar_terms_data.json 文件不存在")
    print()

def check_shensha_interactions():
    """检查神煞互动规则"""
    print("=== 检查神煞互动规则 ===")
    if os.path.exists('shensha_rules.json'):
        with open('shensha_rules.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        interactions = data.get('interactions', {})
        print(f"神煞互动规则数量: {len(interactions)}")
        
        # 检查effect结构
        sample_count = 0
        for interaction_name, interaction_data in interactions.items():
            if sample_count >= 3:
                break
            
            effects = interaction_data.get('effects', [])
            for effect in effects:
                if isinstance(effect, dict):
                    print(f"  {interaction_name} effect 结构:")
                    for key in effect.keys():
                        print(f"    - {key}")
                    sample_count += 1
                    break
    else:
        print("shensha_rules.json 文件不存在")
    print()

def main():
    print("=== 系统状态检查 ===")
    check_jiazi_table()
    check_solar_terms()
    check_shensha_interactions()

if __name__ == "__main__":
    main()
