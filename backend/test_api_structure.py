#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试API结构和输出格式
"""

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import json
import asyncio

async def test_api_structure():
    """测试API结构"""
    print("=== 测试API结构 ===")
    
    # 测试数据
    request_data = BaziCalculateRequest(
        name="测试用户",
        gender="男",
        birth_datetime=datetime(1990, 3, 15, 14, 30, 0),
        is_solar_time=True,
        birth_place="北京",
        longitude=116.4074,
        latitude=39.9042,
        timezone_offset=8.0
    )
    
    try:
        # 计算八字
        result = await calculate_bazi_data(request_data)
        
        print(f"✓ API调用成功")
        print(f"返回类型: {type(result)}")
        
        # 将结果转换为字典
        result_dict = result.model_dump()
        print(f"主要字段: {list(result_dict.keys())}")
        
        # 检查八字信息
        if 'bazi_characters' in result_dict:
            print(f"✓ bazi_characters 字段存在")
            bazi_chars = result_dict['bazi_characters']
            print(f"  八字: {bazi_chars}")
        
        # 检查日主信息
        if 'day_master_element' in result_dict:
            print(f"✓ day_master_element 字段存在: {result_dict['day_master_element']}")
        
        if 'day_master_strength' in result_dict:
            print(f"✓ day_master_strength 字段存在: {result_dict['day_master_strength']}")
        
        # 检查神煞字段
        if 'shen_sha_details' in result_dict:
            print(f"✓ shen_sha_details 字段存在")
            shensha_list = result_dict['shen_sha_details']
            if shensha_list:
                print(f"  神煞数量: {len(shensha_list)}")
                
                # 检查每个神煞的结构
                for i, shensha in enumerate(shensha_list[:3]):  # 只检查前3个
                    print(f"  神煞 {i+1}: {shensha.get('name', 'N/A')}")
                    print(f"    位置: {shensha.get('positions', 'N/A')}")
                    print(f"    强度: {shensha.get('strength', 'N/A')}")
                    print(f"    吉凶等级: {shensha.get('auspicious_level', 'N/A')}")
                    print(f"    描述: {shensha.get('description', 'N/A')}")
                    if 'tags' in shensha:
                        print(f"    标签: {shensha['tags']}")
            else:
                print("  神煞列表为空")
        
        # 检查流年分析
        if 'current_year_fortune' in result_dict:
            print(f"✓ current_year_fortune 字段存在")
            current_year = result_dict['current_year_fortune']
            if current_year:
                print(f"  流年分析字段: {list(current_year.keys())}")
                
                if 'shensha_analysis' in current_year:
                    print(f"  流年神煞分析存在")
                    liunian_shensha = current_year['shensha_analysis']
                    print(f"  流年神煞类型: {type(liunian_shensha)}")
                    if isinstance(liunian_shensha, list):
                        print(f"  流年神煞数量: {len(liunian_shensha)}")
        
        # 检查五行分析
        if 'five_elements_score' in result_dict:
            print(f"✓ five_elements_score 字段存在")
            five_elements = result_dict['five_elements_score']
            print(f"  五行得分: {five_elements}")
        
        # 检查喜用神
        if 'favorable_elements' in result_dict:
            print(f"✓ favorable_elements 字段存在")
            favorable = result_dict['favorable_elements']
            print(f"  喜用神: {favorable}")
        
        print(f"\n=== API结构测试完成 ===")
        return True
        
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_api_structure())
