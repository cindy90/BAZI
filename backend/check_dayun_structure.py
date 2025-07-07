#!/usr/bin/env python3
"""
检查大运数据结构专用脚本
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
import asyncio

def check_dayun_structure():
    """检查大运数据结构"""
    print("=== 检查大运数据结构 ===")
    
    # 高梦泽案例数据
    request_data = BaziCalculateRequest(
        name="高梦泽",
        gender="女",
        birth_date="2020-07-29",
        birth_time="13:26",
        birth_place="北京市朝阳区",
        calculation_type="complete"
    )
    
    try:
        result = asyncio.run(calculate_bazi_data(request_data))
        result_dict = result.dict()
        
        print("主要字段:")
        for key in result_dict.keys():
            print(f"  {key}: {type(result_dict[key])}")
        
        # 检查大运数据
        major_cycles = result_dict.get('major_cycles', [])
        print(f"\n大运数据 (major_cycles): {len(major_cycles)} 个")
        
        if major_cycles:
            print("\n第一个大运的字段:")
            first_cycle = major_cycles[0]
            for key, value in first_cycle.items():
                print(f"  {key}: {value}")
        
        # 检查其他可能的大运相关字段
        print("\n搜索包含 'dayun' 或 'cycle' 的字段:")
        for key, value in result_dict.items():
            if 'dayun' in key.lower() or 'cycle' in key.lower():
                print(f"  {key}: {type(value)}")
        
    except Exception as e:
        print(f"检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_dayun_structure()
