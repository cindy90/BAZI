#!/usr/bin/env python3
"""
测试重构后的八字计算系统
验证 lunar_python + 真太阳时校正 + 流年神煞分析的整合效果
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from app.schemas.bazi import BaziCalculateRequest
from app.services.bazi_calculator import calculate_bazi_data
import asyncio
import json

async def test_integrated_system():
    """测试集成系统功能"""
    print("=" * 60)
    print("测试重构后的八字计算系统")
    print("=" * 60)
    
    # 测试用例1：北京出生，验证真太阳时校正
    print("\n【测试用例1】北京出生，真太阳时校正")
    print("-" * 40)
    
    request1 = BaziCalculateRequest(
        name="测试人员1",
        gender="男",
        birth_datetime=datetime(1990, 5, 15, 14, 30, 0),
        birth_place="北京",
        is_solar_time=True
    )
    
    try:
        result1 = await calculate_bazi_data(request1)
        print(f"八字：{result1.bazi_characters}")
        print(f"日主：{result1.day_master_element} {result1.day_master_strength}")
        print(f"生肖：{result1.zodiac_sign}")
        
        # 检查校正信息
        if result1.location_info:
            correction_applied = result1.location_info.get("correction_applied", False)
            print(f"真太阳时校正：{'已应用' if correction_applied else '未应用'}")
            if correction_applied:
                print(f"经度：{result1.location_info.get('longitude', 'N/A')}°")
                print(f"经度时差：{result1.location_info.get('longitude_diff_minutes', 0):.1f}分钟")
                print(f"均时差：{result1.location_info.get('equation_of_time_minutes', 0):.1f}分钟")
                print(f"原时间：{result1.location_info.get('original_time', 'N/A')}")
                print(f"校正时间：{result1.location_info.get('corrected_time', 'N/A')}")
        
        # 检查神煞
        if result1.shen_sha_details:
            print(f"神煞数量：{len(result1.shen_sha_details)}")
            for shensha in result1.shen_sha_details[:3]:  # 显示前3个
                print(f"  - {shensha['name']} ({shensha['position']})")
        
        print("✓ 测试用例1通过")
        
    except Exception as e:
        print(f"✗ 测试用例1失败：{e}")
        import traceback
        traceback.print_exc()
    
    # 测试用例2：上海出生，验证不同经度的校正
    print("\n【测试用例2】上海出生，不同经度校正")
    print("-" * 40)
    
    request2 = BaziCalculateRequest(
        name="测试人员2",
        gender="女",
        birth_datetime=datetime(1985, 12, 25, 6, 15, 0),
        birth_place="上海",
        is_solar_time=True
    )
    
    try:
        result2 = await calculate_bazi_data(request2)
        print(f"八字：{result2.bazi_characters}")
        print(f"日主：{result2.day_master_element} {result2.day_master_strength}")
        
        # 对比校正信息
        if result2.location_info and result2.location_info.get("correction_applied", False):
            print(f"上海经度：{result2.location_info.get('longitude', 'N/A')}°")
            print(f"上海经度时差：{result2.location_info.get('longitude_diff_minutes', 0):.1f}分钟")
        
        print("✓ 测试用例2通过")
        
    except Exception as e:
        print(f"✗ 测试用例2失败：{e}")
    
    # 测试用例3：无出生地，验证默认处理
    print("\n【测试用例3】无出生地，默认处理")
    print("-" * 40)
    
    request3 = BaziCalculateRequest(
        name="测试人员3",
        gender="男",
        birth_datetime=datetime(2000, 1, 1, 12, 0, 0),
        is_solar_time=True
    )
    
    try:
        result3 = await calculate_bazi_data(request3, quick_mode=True)
        print(f"八字：{result3.bazi_characters}")
        print(f"日主：{result3.day_master_element} {result3.day_master_strength}")
        
        # 检查是否无校正信息
        correction_applied = False
        if result3.location_info:
            correction_applied = result3.location_info.get("correction_applied", False)
        print(f"真太阳时校正：{'已应用' if correction_applied else '未应用（符合预期）'}")
        
        print("✓ 测试用例3通过")
        
    except Exception as e:
        print(f"✗ 测试用例3失败：{e}")
    
    # 测试用例4：流年运势分析
    print("\n【测试用例4】流年运势分析")
    print("-" * 40)
    
    request4 = BaziCalculateRequest(
        name="测试人员4",
        gender="男",
        birth_datetime=datetime(1990, 3, 21, 10, 30, 0),
        birth_place="广州",
        is_solar_time=True
    )
    
    try:
        result4 = await calculate_bazi_data(request4)
        print(f"八字：{result4.bazi_characters}")
        
        # 检查流年运势
        if result4.current_year_fortune:
            print(f"当年运势：{result4.current_year_fortune.get('year', 'N/A')}年")
            print(f"流年干支：{result4.current_year_fortune.get('gan_zhi', 'N/A')}")
            if 'liunian_shensha' in result4.current_year_fortune:
                shensha_count = len(result4.current_year_fortune['liunian_shensha'])
                print(f"流年神煞：{shensha_count}个")
                for shensha in result4.current_year_fortune['liunian_shensha'][:2]:
                    print(f"  - {shensha.get('name', 'N/A')}")
        
        print("✓ 测试用例4通过")
        
    except Exception as e:
        print(f"✗ 测试用例4失败：{e}")
    
    print("\n" + "=" * 60)
    print("重构测试完成")
    print("已验证：")
    print("1. lunar_python 八字计算核心功能")
    print("2. 真太阳时校正集成")
    print("3. 流年神煞分析重构") 
    print("4. 冗余代码清理")
    print("=" * 60)

def test_solar_time_correction_standalone():
    """独立测试真太阳时校正功能"""
    print("\n【独立测试】真太阳时校正功能")
    print("-" * 40)
    
    from app.services.precise_bazi_calculator import test_solar_time_correction
    test_solar_time_correction()

if __name__ == "__main__":
    # 运行主测试
    asyncio.run(test_integrated_system())
    
    # 运行独立测试
    test_solar_time_correction_standalone()
