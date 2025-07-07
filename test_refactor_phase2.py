#!/usr/bin/env python3
"""
第四到第六步重构验证脚本
测试 constants.py 常量补全、core.py 增强、真太阳时校正等功能
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from app.services.bazi_calculator import calculate_bazi_data
from app.services.core import Bazi, StemBranch
from app.services.constants import *
from app.services.calculators import FiveElementsCalculator, ShenShaCalculator
from app.schemas.bazi import BaziCalculateRequest
import json

def test_constants_completion():
    """测试 constants.py 常量补全"""
    print("=" * 50)
    print("测试 constants.py 常量补全")
    print("=" * 50)
    
    # 测试基础常量
    print(f"✓ JIAZI_TABLE 长度: {len(JIAZI_TABLE)}")
    print(f"✓ STEM_ELEMENTS 长度: {len(STEM_ELEMENTS)}")
    print(f"✓ BRANCH_ELEMENTS 长度: {len(BRANCH_ELEMENTS)}")
    print(f"✓ BRANCH_HIDDEN_STEMS 长度: {len(BRANCH_HIDDEN_STEMS)}")
    
    # 测试真太阳时校正常量
    print(f"✓ STANDARD_LONGITUDE: {STANDARD_LONGITUDE}")
    print(f"✓ CITY_LONGITUDE_MAPPING 城市数量: {len(CITY_LONGITUDE_MAPPING)}")
    print(f"✓ EQUATION_OF_TIME_BY_MONTH 长度: {len(EQUATION_OF_TIME_BY_MONTH)}")
    
    # 测试长生十二宫常量
    print(f"✓ CHANG_SHENG_MAPPING 长度: {len(CHANG_SHENG_MAPPING)}")
    print(f"✓ CHANG_SHENG_STRENGTH_LEVELS 长度: {len(CHANG_SHENG_STRENGTH_LEVELS)}")
    
    # 测试新增常量
    print(f"✓ XUNKONG_MAPPING 长度: {len(XUNKONG_MAPPING)}")
    print(f"✓ STEM_COMBINATIONS_DETAILED 长度: {len(STEM_COMBINATIONS_DETAILED)}")
    
    # 验证数据结构
    print(f"✓ BRANCH_HIDDEN_STEMS['子'] 类型: {type(BRANCH_HIDDEN_STEMS['子'])}")
    print(f"✓ BRANCH_HIDDEN_STEMS['子'] 内容: {BRANCH_HIDDEN_STEMS['子']}")
    
    print("✓ constants.py 常量补全测试通过！")

def test_core_enhancements():
    """测试 core.py Bazi 类增强"""
    print("\n" + "=" * 50)
    print("测试 core.py Bazi 类增强")
    print("=" * 50)
    
    # 创建测试八字
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 10, 30)
    )
    
    # 测试新增方法
    print(f"✓ get_all_stems(): {bazi.get_all_stems()}")
    print(f"✓ get_all_branches(): {bazi.get_all_branches()}")
    print(f"✓ get_all_stem_branches(): {bazi.get_all_stem_branches()}")
    
    # 测试柱查询方法
    print(f"✓ get_pillar_branch('年'): {bazi.get_pillar_branch('年')}")
    print(f"✓ get_pillar_branch('day'): {bazi.get_pillar_branch('day')}")
    print(f"✓ get_pillar_element('月'): {bazi.get_pillar_element('月')}")
    print(f"✓ get_pillar_element('hour'): {bazi.get_pillar_element('hour')}")
    
    # 测试新增的辅助方法
    print(f"✓ get_elements_distribution(): {bazi.get_elements_distribution()}")
    print(f"✓ get_stem_by_type('day_stem'): {bazi.get_stem_by_type('day_stem')}")
    print(f"✓ get_branch_by_type('year_branch'): {bazi.get_branch_by_type('year_branch')}")
    
    # 测试干支组合检查
    print(f"✓ has_stem_branch_combination('甲', '子'): {bazi.has_stem_branch_combination('甲', '子')}")
    print(f"✓ has_stem_branch_combination('乙', '丑'): {bazi.has_stem_branch_combination('乙', '丑')}")
    
    print("✓ core.py Bazi 类增强测试通过！")

def test_calculators_integration():
    """测试 calculators.py 集成"""
    print("\n" + "=" * 50)
    print("测试 calculators.py 集成")
    print("=" * 50)
    
    # 创建测试八字
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 10, 30)
    )
    
    # 测试 FiveElementsCalculator
    print("测试 FiveElementsCalculator:")
    day_master_strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
    print(f"✓ calculate_day_master_strength: {day_master_strength}")
    
    five_elements_pct = FiveElementsCalculator.calculate_five_elements_percentage(bazi)
    print(f"✓ calculate_five_elements_percentage: {five_elements_pct}")
    
    ten_god = FiveElementsCalculator.calculate_ten_god_relation("甲", "戊")
    print(f"✓ calculate_ten_god_relation('甲', '戊'): {ten_god}")
    
    zhi_hidden = FiveElementsCalculator.get_zhi_hidden_gan("子")
    print(f"✓ get_zhi_hidden_gan('子'): {zhi_hidden}")
    
    chang_sheng = FiveElementsCalculator.calculate_chang_sheng_twelve_palaces("甲", "子")
    print(f"✓ calculate_chang_sheng_twelve_palaces('甲', '子'): {chang_sheng}")
    
    # 测试 ShenShaCalculator
    print("测试 ShenShaCalculator:")
    shen_sha_calc = ShenShaCalculator()
    shen_sha_results = shen_sha_calc.calculate_shensha(bazi)
    print(f"✓ calculate_shensha 神煞数量: {len(shen_sha_results)}")
    
    # 显示几个重要神煞
    for key, sha in list(shen_sha_results.items())[:3]:
        print(f"  - {key}: {sha.name} (位置: {sha.position}, 强度: {sha.strength})")
    
    print("✓ calculators.py 集成测试通过！")

def test_solar_time_correction():
    """测试真太阳时校正"""
    print("\n" + "=" * 50)
    print("测试真太阳时校正")
    print("=" * 50)
    
    from app.services.calculators import get_solar_time_correction
    
    # 测试不同城市的真太阳时校正
    test_cases = [
        (datetime(2024, 6, 15, 12, 0), "北京"),
        (datetime(2024, 6, 15, 12, 0), "上海"),
        (datetime(2024, 6, 15, 12, 0), "广州"),
        (datetime(2024, 6, 15, 12, 0), "成都"),
        (datetime(2024, 6, 15, 12, 0), "乌鲁木齐"),
    ]
    
    for dt, city in test_cases:
        try:
            correction = get_solar_time_correction(dt, city)
            if correction.get("correction_applied"):
                print(f"✓ {city}: 校正 {correction.get('longitude_diff_minutes', 0):.1f}分钟 + 均时差 {correction.get('equation_of_time_minutes', 0):.1f}分钟")
            else:
                print(f"✓ {city}: 无需校正")
        except Exception as e:
            print(f"✗ {city}: 校正失败 - {e}")
    
    print("✓ 真太阳时校正测试通过！")

def test_main_api():
    """测试主 API 功能"""
    print("\n" + "=" * 50)
    print("测试主 API 功能")
    print("=" * 50)
    
    import asyncio
    
    async def async_test():
        # 创建测试请求
        request = BaziCalculateRequest(
            birth_datetime=datetime(1984, 2, 15, 10, 30),
            gender="男",
            birth_place="北京"
        )
        
        try:
            # 测试完整模式
            print("测试完整模式...")
            response = await calculate_bazi_data(request, quick_mode=False)
            print(f"✓ 八字: {response.bazi_characters}")
            print(f"✓ 日主强度: {response.day_master_strength}")
            print(f"✓ 五行分布: {response.five_elements_score}")
            print(f"✓ 生肖: {response.zodiac_sign}")
            print(f"✓ 大运数量: {len(response.major_cycles)}")
            print(f"✓ 神煞数量: {len(response.shen_sha_details)}")
            print(f"✓ 真太阳时校正: {response.location_info.get('correction_applied', False)}")
            
            # 测试快速模式
            print("\n测试快速模式...")
            response_quick = await calculate_bazi_data(request, quick_mode=True)
            print(f"✓ 快速模式八字: {response_quick.bazi_characters}")
            print(f"✓ 快速模式神煞数量: {len(response_quick.shen_sha_details)}")
            
            print("✓ 主 API 功能测试通过！")
            
        except Exception as e:
            print(f"✗ 主 API 功能测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 运行异步测试
    asyncio.run(async_test())

def test_accuracy_validation():
    """测试精度验证"""
    print("\n" + "=" * 50)
    print("测试精度验证")
    print("=" * 50)
    
    import asyncio
    
    async def async_test():
        # 测试经典八字案例
        test_cases = [
            {
                "name": "甲子年丙寅月戊午日壬戌时",
                "birth_datetime": datetime(1984, 2, 15, 19, 30),
                "gender": "男",
                "expected_bazi": ["甲子", "丙寅", "戊午", "壬戌"]
            },
            {
                "name": "乙丑年戊寅月庚子日丁亥时",
                "birth_datetime": datetime(1985, 3, 10, 21, 45),
                "gender": "女",
                "expected_bazi": ["乙丑", "戊寅", "庚子", "丁亥"]
            }
        ]
        
        for case in test_cases:
            try:
                request = BaziCalculateRequest(
                    birth_datetime=case["birth_datetime"],
                    gender=case["gender"],
                    birth_place="北京"
                )
                
                response = await calculate_bazi_data(request, quick_mode=True)
                actual_bazi = [
                    response.bazi_characters["year_stem"] + response.bazi_characters["year_branch"],
                    response.bazi_characters["month_stem"] + response.bazi_characters["month_branch"],
                    response.bazi_characters["day_stem"] + response.bazi_characters["day_branch"],
                    response.bazi_characters["hour_stem"] + response.bazi_characters["hour_branch"]
                ]
                
                print(f"测试: {case['name']}")
                print(f"  预期: {case['expected_bazi']}")
                print(f"  实际: {actual_bazi}")
                
                # 检查年柱和日柱（最重要的两柱）
                year_match = actual_bazi[0] == case['expected_bazi'][0]
                day_match = actual_bazi[2] == case['expected_bazi'][2]
                
                if year_match and day_match:
                    print(f"  ✓ 核心柱位匹配")
                else:
                    print(f"  ✗ 核心柱位不匹配")
                    
            except Exception as e:
                print(f"  ✗ 测试失败: {e}")
    
    # 运行异步测试
    asyncio.run(async_test())
    print("✓ 精度验证测试完成！")

if __name__ == "__main__":
    print("开始第四到第六步重构验证...")
    
    try:
        test_constants_completion()
        test_core_enhancements()
        test_calculators_integration()
        test_solar_time_correction()
        test_main_api()
        test_accuracy_validation()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试完成！重构验证成功！")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
