#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试优化后的八字计算系统
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import asyncio
import json

async def test_bazi_calculation():
    """测试八字计算"""
    print("=" * 50)
    print("测试优化后的八字计算系统")
    print("=" * 50)
    
    # 测试数据
    test_request = BaziCalculateRequest(
        name="测试用户",
        gender="男",
        birth_datetime=datetime(1990, 5, 15, 14, 30, 0),
        is_solar_time=True,
        birth_place="北京",
        longitude=116.4,
        latitude=39.9,
        timezone_offset=8.0
    )
    
    try:
        print(f"测试八字计算: {test_request.birth_datetime}, {test_request.gender}, {test_request.birth_place}")
        
        # 计算八字
        result = await calculate_bazi_data(test_request)
        
        print(f"✓ 八字计算成功")
        print(f"八字干支: {result.bazi_characters}")
        print(f"日主: {result.day_master_element}")
        print(f"性别: {test_request.gender}")
        print(f"生肖: {result.zodiac_sign}")
        print(f"五行得分: {result.five_elements_score}")
        print(f"日主强度: {result.day_master_strength}")
        print(f"大运数量: {len(result.major_cycles)}")
        print(f"interactions字段: {type(result.interactions)}")
        print(f"location_info字段: {type(result.location_info)}")
        
        # 测试快速模式
        print("\n" + "=" * 30)
        print("测试快速模式")
        print("=" * 30)
        
        result_quick = await calculate_bazi_data(test_request, quick_mode=True)
        print(f"✓ 快速模式计算成功")
        print(f"八字干支: {result_quick.bazi_characters}")
        
        print("\n" + "=" * 50)
        print("测试完成 - 所有功能正常")
        print("=" * 50)
        
    except Exception as e:
        print(f"✗ 八字计算失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_bazi_calculation())
