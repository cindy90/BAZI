#!/usr/bin/env python3
"""
综合API测试脚本 - 测试所有优化后的功能
"""

import asyncio
import json
from datetime import datetime
from app.services.bazi_calculator import calculate_bazi_data
from app.models.requests import BaziCalculateRequest

async def test_api_comprehensive():
    """全面测试API功能"""
    print("=" * 50)
    print("八字API综合测试")
    print("=" * 50)
    
    # 测试数据
    test_cases = [
        {
            "name": "测试案例1: 庚午年",
            "birth_time": "1990-05-15T14:30:00",
            "gender": "男",
            "city": "北京",
            "enable_solar_time": False
        },
        {
            "name": "测试案例2: 女命",
            "birth_time": "1985-08-20T09:15:00",
            "gender": "女",
            "city": "上海",
            "enable_solar_time": True
        },
        {
            "name": "测试案例3: 子时出生",
            "birth_time": "1995-12-01T00:30:00",
            "gender": "男",
            "city": "广州",
            "enable_solar_time": False
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   出生时间: {test_case['birth_time']}")
        print(f"   性别: {test_case['gender']}")
        print(f"   城市: {test_case['city']}")
        print(f"   真太阳时: {test_case['enable_solar_time']}")
        
        try:
            # 创建请求对象
            request = BaziCalculateRequest(
                birth_time=test_case['birth_time'],
                gender=test_case['gender'],
                city=test_case['city'],
                enable_solar_time=test_case['enable_solar_time']
            )
            
            # 调用API
            result = await calculate_bazi_data(request)
            
            # 验证结果
            assert result["status"] == "success", "计算状态应为成功"
            assert "bazi" in result, "结果应包含八字信息"
            assert "five_elements" in result, "结果应包含五行信息"
            assert "day_master_analysis" in result, "结果应包含日主分析"
            assert "dayun" in result, "结果应包含大运信息"
            assert "interactions" in result, "结果应包含神煞互动信息"
            assert "location_info" in result, "结果应包含地理位置信息"
            
            # 验证八字
            bazi = result["bazi"]
            for pillar in ["year_stem", "year_branch", "month_stem", "month_branch", 
                          "day_stem", "day_branch", "hour_stem", "hour_branch"]:
                assert pillar in bazi, f"八字应包含{pillar}"
                assert len(bazi[pillar]) == 1, f"{pillar}应为单个字符"
            
            # 验证五行
            five_elements = result["five_elements"]
            assert "percentages" in five_elements, "五行应包含百分比"
            percentages = five_elements["percentages"]
            total = sum(float(p.replace('%', '')) for p in percentages.values())
            assert abs(total - 100.0) < 0.01, f"五行百分比总和应为100%，实际为{total}%"
            
            # 验证日主分析
            day_master = result["day_master_analysis"]
            assert "element" in day_master, "日主分析应包含五行"
            assert "strength" in day_master, "日主分析应包含强度"
            assert "strength_description" in day_master, "日主分析应包含强度描述"
            
            # 验证大运
            dayun = result["dayun"]
            assert isinstance(dayun, list), "大运应为列表"
            assert len(dayun) > 0, "大运列表不应为空"
            for cycle in dayun:
                assert "pillar" in cycle, "大运周期应包含干支"
                assert "age_start" in cycle, "大运周期应包含起始年龄"
                assert "ten_god" in cycle, "大运周期应包含十神"
            
            # 验证神煞互动
            interactions = result["interactions"]
            assert isinstance(interactions, dict), "神煞互动应为字典"
            assert "total_shensha" in interactions, "神煞互动应包含总数"
            
            # 验证地理位置
            location_info = result["location_info"]
            assert "city" in location_info, "地理位置应包含城市"
            assert "longitude" in location_info, "地理位置应包含经度"
            assert "latitude" in location_info, "地理位置应包含纬度"
            
            print(f"   ✓ 测试通过")
            print(f"   八字: {bazi['year_stem']}{bazi['year_branch']} {bazi['month_stem']}{bazi['month_branch']} {bazi['day_stem']}{bazi['day_branch']} {bazi['hour_stem']}{bazi['hour_branch']}")
            print(f"   日主: {day_master['element']} ({day_master['strength']})")
            print(f"   大运数量: {len(dayun)}")
            print(f"   神煞总数: {interactions['total_shensha']}")
            
        except Exception as e:
            print(f"   ✗ 测试失败: {e}")
            import traceback
            traceback.print_exc()

async def test_constants_usage():
    """测试常量使用情况"""
    print("\n" + "=" * 50)
    print("常量使用测试")
    print("=" * 50)
    
    try:
        from app.services.constants import (
            DAY_MASTER_STRENGTH_WEIGHTS,
            DAY_MASTER_STRENGTH_THRESHOLDS,
            FIVE_ELEMENTS_ENERGY_WEIGHTS,
            BRANCH_SIX_CONFLICTS,
            BRANCH_SIX_COMBINATIONS
        )
        
        print("✓ 成功导入所有新增常量")
        print(f"  - 日主强度权重配置: {len(DAY_MASTER_STRENGTH_WEIGHTS)} 项")
        print(f"  - 日主强度阈值配置: {len(DAY_MASTER_STRENGTH_THRESHOLDS)} 项")
        print(f"  - 五行能量权重配置: {len(FIVE_ELEMENTS_ENERGY_WEIGHTS)} 项")
        print(f"  - 地支六冲: {len(BRANCH_SIX_CONFLICTS)} 对")
        print(f"  - 地支六合: {len(BRANCH_SIX_COMBINATIONS)} 对")
        
    except ImportError as e:
        print(f"✗ 常量导入失败: {e}")

async def test_static_methods():
    """测试静态方法调用"""
    print("\n" + "=" * 50)
    print("静态方法测试")
    print("=" * 50)
    
    try:
        from app.services.calculators import FiveElementsCalculator
        from app.services.core import Bazi, StemBranch
        from datetime import datetime
        
        # 创建测试八字
        bazi = Bazi(
            StemBranch('庚', '午'), StemBranch('辛', '巳'), 
            StemBranch('庚', '辰'), StemBranch('癸', '未'), 
            '男', datetime(1990, 5, 15, 14, 30)
        )
        
        # 测试各种静态方法
        strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
        percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi)
        scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
        analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
        
        print("✓ 所有静态方法调用成功")
        print(f"  - 日主强度: {strength}")
        print(f"  - 五行百分比总和: {sum(percentages.values()):.1f}%")
        print(f"  - 五行分数总和: {sum(scores.values()):.2f}")
        print(f"  - 喜用神分析包含字段: {list(analysis.keys())}")
        
    except Exception as e:
        print(f"✗ 静态方法测试失败: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主测试函数"""
    await test_api_comprehensive()
    await test_constants_usage()
    await test_static_methods()
    
    print("\n" + "=" * 50)
    print("综合测试完成")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
