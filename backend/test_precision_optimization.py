#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试八字精度优化后的系统
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime


async def test_bazi_accuracy():
    """测试八字计算精度"""
    
    # 测试用例
    test_cases = [
        {
            "name": "测试1: 1985年9月22日 10:15 上海",
            "birth_datetime": datetime(1985, 9, 22, 10, 15),
            "birth_place": "上海",
            "gender": "女"
        },
        {
            "name": "测试2: 1990年6月15日 14:30 北京",
            "birth_datetime": datetime(1990, 6, 15, 14, 30),
            "birth_place": "北京",
            "gender": "男"
        },
        {
            "name": "测试3: 2000年1月1日 12:00 深圳",
            "birth_datetime": datetime(2000, 1, 1, 12, 0),
            "birth_place": "深圳",
            "gender": "女"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"{test_case['name']}")
        print(f"{'='*50}")
        
        request = BaziCalculateRequest(
            birth_datetime=test_case["birth_datetime"],
            birth_place=test_case["birth_place"],
            gender=test_case["gender"],
            name=None,
            is_solar_time=True,
            longitude=None,
            latitude=None,
            timezone_offset=None
        )
        
        try:
            result = await calculate_bazi_data(request)
            
            print(f"原始时间: {test_case['birth_datetime']}")
            print(f"出生地点: {test_case['birth_place']}")
            print(f"性别: {test_case['gender']}")
            print(f"八字: {result.bazi_characters}")
            print(f"日主: {result.day_master_element}")
            print(f"喜用神: {result.favorable_elements}")
            
            # 检查真太阳时校正信息
            if result.location_info:
                print(f"经度: {result.location_info.get('longitude', '未知')}")
                print(f"经度时差: {result.location_info.get('longitude_diff_minutes', 0):.2f}分钟")
                print(f"均时差: {result.location_info.get('equation_of_time_minutes', 0):.2f}分钟")
                if result.location_info.get('corrected_time'):
                    print(f"校正后时间: {result.location_info.get('corrected_time')}")
            
            # 检查神煞信息
            if result.shen_sha_details:
                print(f"神煞数量: {len(result.shen_sha_details)}")
                for i, shensha in enumerate(result.shen_sha_details[:3]):
                    name = shensha.get('name', '')
                    desc = shensha.get('description', '')
                    position = shensha.get('position', '')
                    print(f"  {i+1}. {name} ({position}): {desc}")
            else:
                print("未找到神煞信息")
                
        except Exception as e:
            print(f"计算失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_bazi_accuracy())
