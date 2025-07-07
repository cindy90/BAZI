#!/usr/bin/env python
"""
检查 shensha_rules.json 结构
"""
import json

def check_shensha_rules():
    """检查 shensha_rules.json 结构"""
    try:
        with open('shensha_rules.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Top level keys: {list(data.keys())}")
        
        interactions = data.get('shensha_interactions', {})
        print(f"Shensha interactions count: {len(interactions)}")
        
        if interactions:
            print("Sample interaction keys:")
            for key in list(interactions.keys())[:3]:
                print(f"  - {key}")
            
            # 检查一个具体的互动规则
            first_key = list(interactions.keys())[0]
            first_interaction = interactions[first_key]
            print(f"\nSample interaction '{first_key}' structure:")
            for key, value in first_interaction.items():
                print(f"  {key}: {type(value).__name__}")
                if key == 'effects':
                    for effect_key, effect_value in value.items():
                        print(f"    {effect_key}: {type(effect_value).__name__}")
                        if isinstance(effect_value, dict):
                            print(f"      keys: {list(effect_value.keys())}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_shensha_rules()
