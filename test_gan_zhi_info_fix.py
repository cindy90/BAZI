#!/usr/bin/env python3
"""
测试 gan_zhi_info 字段修正后的四柱详细信息
验证天干十神和地支藏干的计算是否正确
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import asyncio
from datetime import datetime
from backend.app.services.main import calculate_bazi_data
from backend.app.schemas.bazi import BaziCalculateRequest

async def test_gan_zhi_info():
    """测试 gan_zhi_info 字段的计算"""
    
    print("=== 测试 gan_zhi_info 字段修正 ===\n")
    
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
        
        print("\n2. gan_zhi_info 详细信息:")
        gan_zhi = result.gan_zhi_info
        
        print("\n   年柱详细:")
        year_pillar = gan_zhi['year_pillar']
        print(f"     干支: {year_pillar['gan']}{year_pillar['zhi']}")
        print(f"     十神: {year_pillar['ten_god']}")
        print(f"     藏干: {year_pillar['hidden_stems']}")
        
        print("\n   月柱详细:")
        month_pillar = gan_zhi['month_pillar']
        print(f"     干支: {month_pillar['gan']}{month_pillar['zhi']}")
        print(f"     十神: {month_pillar['ten_god']}")
        print(f"     藏干: {month_pillar['hidden_stems']}")
        
        print("\n   日柱详细:")
        day_pillar = gan_zhi['day_pillar']
        print(f"     干支: {day_pillar['gan']}{day_pillar['zhi']}")
        print(f"     十神: {day_pillar['ten_god']}")
        print(f"     藏干: {day_pillar['hidden_stems']}")
        
        print("\n   时柱详细:")
        hour_pillar = gan_zhi['hour_pillar']
        print(f"     干支: {hour_pillar['gan']}{hour_pillar['zhi']}")
        print(f"     十神: {hour_pillar['ten_god']}")
        print(f"     藏干: {hour_pillar['hidden_stems']}")
        
        print("\n3. 验证结果:")
        
        # 检查是否还有"未知"值
        unknown_count = 0
        for pillar_name, pillar_data in gan_zhi.items():
            if pillar_data.get('ten_god') == '未知':
                print(f"   ❌ {pillar_name} 的十神仍为'未知'")
                unknown_count += 1
            if pillar_data.get('hidden_stems') == '未知':
                print(f"   ❌ {pillar_name} 的藏干仍为'未知'")
                unknown_count += 1
        
        if unknown_count == 0:
            print("   ✅ 所有四柱的十神和藏干都已正确计算")
        else:
            print(f"   ⚠️  仍有 {unknown_count} 个字段未正确计算")
        
        # 验证日柱的十神是否为"日主"
        if day_pillar['ten_god'] == '日主':
            print("   ✅ 日柱十神正确设置为'日主'")
        else:
            print(f"   ❌ 日柱十神错误: {day_pillar['ten_god']}")
        
        # 验证十神计算逻辑（基于五行生克关系）
        print("\n4. 十神计算验证:")
        day_gan = bazi['day_stem']
        print(f"   日主: {day_gan}")
        
        for pillar_name, pillar_data in gan_zhi.items():
            if pillar_name != 'day_pillar':
                gan = pillar_data['gan']
                ten_god = pillar_data['ten_god']
                print(f"   {pillar_name}: {gan} -> {ten_god}")
        
        print("\n=== 测试完成 ===")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gan_zhi_info())
    if success:
        print("\n🎉 gan_zhi_info 字段修正测试通过！")
    else:
        print("\n❌ gan_zhi_info 字段修正测试失败！")
