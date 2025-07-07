#!/usr/bin/env python3
"""
检查API返回结果的大运结构
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.bazi_calculator import calculate_bazi_full

def check_api_response_structure():
    """检查API返回的大运结构"""
    print("=== 检查API响应结构 ===")
    
    # 高梦泽案例数据
    request_data = {
        "birth_time": "2020-07-29 13:26:00",
        "location": "北京市朝阳区",
        "gender": "女",
        "name": "高梦泽",
        "birth_type": "阳历",
        "timezone": "Asia/Shanghai",
        "calculate_mode": "complete"
    }
    
    try:
        result = calculate_bazi_full(request_data)
        
        print("=== 大运相关字段 ===")
        if 'major_cycles' in result:
            major_cycles = result['major_cycles']
            print(f"major_cycles 数量: {len(major_cycles)}")
            
            if major_cycles:
                print("\n第一个大运结构:")
                first_cycle = major_cycles[0]
                print(f"字段: {list(first_cycle.keys())}")
                print(f"完整内容: {first_cycle}")
                
                print("\n前5个大运:")
                for i, cycle in enumerate(major_cycles[:5]):
                    print(f"第{i+1}步: {cycle}")
        else:
            print("未找到 major_cycles 字段")
            
        print("\n=== 所有顶级字段 ===")
        for key in result.keys():
            if isinstance(result[key], list):
                print(f"{key}: List[{len(result[key])}]")
            elif isinstance(result[key], dict):
                print(f"{key}: Dict[{len(result[key])}]")
            else:
                print(f"{key}: {type(result[key])}")
                
    except Exception as e:
        print(f"API调用失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_api_response_structure()
