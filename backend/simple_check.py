#!/usr/bin/env python3
"""
简单检查大运数据结构
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import json
import asyncio

async def check_structure():
    """简单检查结构"""
    print("=== 检查大运数据结构 ===")
    
    request_data = BaziCalculateRequest(
        name="高梦泽",
        gender="女",
        birth_datetime=datetime(2020, 7, 29, 13, 26, 0),
        is_solar_time=True,
        birth_place="北京市朝阳区",
        longitude=116.4074,
        latitude=39.9042,
        timezone_offset=8.0
    )
    
    try:
        result = await calculate_bazi_data(request_data)
        result_dict = result.model_dump()
        
        # 检查大运数据
        major_cycles = result_dict.get('major_cycles', [])
        print(f"大运数量: {len(major_cycles)}")
        
        if major_cycles:
            print("\n第一个大运的字段:")
            first_cycle = major_cycles[0]
            for key, value in first_cycle.items():
                print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"检查失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_structure())
