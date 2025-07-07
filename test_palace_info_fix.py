#!/usr/bin/env python3
"""
测试 palace_info 字段修正后的宫位信息
验证身宫和胎息的计算是否正确
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from datetime import datetime
from backend.app.services.main import calculate_bazi_data
from backend.app.schemas.bazi import BaziCalculateRequest

async def test_palace_info():
    """测试 palace_info 字段的计算"""
    
    print("=== 测试 palace_info 字段修正 ===\n")
    
    # 测试用例：1990年1月1日8点出生的男性
    test_request = BaziCalculateRequest(
        name="测试用户",
        birth_datetime=datetime(1990, 1, 1, 8, 0, 0),
        gender="男",
        birth_place="北京",
        is_solar_time=True,
        longitude=116.4074,
        latitude=39.9042,
        timezone_offset=8
    )
    
    try:
        # 调用修正后的计算函数
        result = await calculate_bazi_data(test_request)
        
        print("1. 基础八字信息:")
        bazi = result.bazi_characters
        print(f"   年柱: {bazi['year_stem']}{bazi['year_branch']}")
        print(f"   月柱: {bazi['month_stem']}{bazi['month_branch']}")
        print(f"   日柱: {bazi['day_stem']}{bazi['day_branch']}")
        print(f"   时柱: {bazi['hour_stem']}{bazi['hour_branch']}")
        print(f"   日主: {result.day_master_element}")
        
        print("\n2. palace_info 宫位信息:")
        palace = result.palace_info
        
        print(f"   胎元: {palace['tai_yuan']}")
        print(f"   命宫: {palace['ming_gong']}")
        print(f"   身宫: {palace['shen_gong']}")
        print(f"   胎息: {palace['tai_xi']}")
        
        print("\n3. 验证结果:")
        
        # 检查是否还有"待计算"值
        pending_count = 0
        for field_name, field_value in palace.items():
            if field_value == '待计算':
                print(f"   ❌ {field_name} 仍为'待计算'")
                pending_count += 1
            elif field_value == '' or field_value is None:
                print(f"   ⚠️  {field_name} 为空值: '{field_value}'")
            else:
                print(f"   ✅ {field_name} 已正确计算: {field_value}")
        
        if pending_count == 0:
            print("   ✅ 所有宫位信息都已正确计算，无'待计算'占位符")
        else:
            print(f"   ❌ 仍有 {pending_count} 个字段未正确计算")
        
        # 特别验证身宫和胎息
        if palace['shen_gong'] != '待计算':
            print("   ✅ 身宫信息已正确获取")
        else:
            print("   ❌ 身宫信息仍未计算")
            
        if palace['tai_xi'] != '待计算':
            print("   ✅ 胎息信息已正确获取")
        else:
            print("   ❌ 胎息信息仍未计算")
        
        print("\n4. 宫位信息详细分析:")
        print(f"   胎元({palace['tai_yuan']}): 受胎之月的天干地支")
        print(f"   命宫({palace['ming_gong']}): 人生命运的核心宫位")
        print(f"   身宫({palace['shen_gong']}): 身体健康和性格特征的宫位")
        print(f"   胎息({palace['tai_xi']}): 胎儿在母体中的息养之所")
        
        print("\n=== 测试完成 ===")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_multiple_cases():
    """测试多个不同的出生时间案例"""
    print("\n=== 测试多个案例的宫位信息 ===\n")
    
    test_cases = [
        {"name": "案例1", "datetime": datetime(1985, 6, 15, 10, 30, 0), "gender": "女"},
        {"name": "案例2", "datetime": datetime(1995, 12, 25, 14, 0, 0), "gender": "男"},
        {"name": "案例3", "datetime": datetime(2000, 3, 8, 20, 45, 0), "gender": "女"},
    ]
    
    for case in test_cases:
        print(f"--- {case['name']} ---")
        test_request = BaziCalculateRequest(
            name=case['name'],
            birth_datetime=case['datetime'],
            gender=case['gender'],
            birth_place="北京",
            is_solar_time=True,
            longitude=116.4074,
            latitude=39.9042,
            timezone_offset=8
        )
        
        try:
            result = await calculate_bazi_data(test_request)
            palace = result.palace_info
            
            print(f"出生时间: {case['datetime']}, 性别: {case['gender']}")
            print(f"胎元: {palace['tai_yuan']}, 命宫: {palace['ming_gong']}")
            print(f"身宫: {palace['shen_gong']}, 胎息: {palace['tai_xi']}")
            
            # 检查是否有待计算的字段
            has_pending = any(v == '待计算' for v in palace.values())
            if has_pending:
                print("❌ 存在未计算的宫位信息")
            else:
                print("✅ 所有宫位信息都已正确计算")
                
        except Exception as e:
            print(f"❌ {case['name']} 计算失败: {e}")
        
        print()

if __name__ == "__main__":
    print("开始测试 palace_info 字段修正...")
    
    # 测试单个案例
    success1 = asyncio.run(test_palace_info())
    
    # 测试多个案例
    asyncio.run(test_multiple_cases())
    
    if success1:
        print("\n🎉 palace_info 字段修正测试通过！")
    else:
        print("\n❌ palace_info 字段修正测试失败！")
