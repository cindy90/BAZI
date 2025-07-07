#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
大运计算对比分析 - 高级计算器 vs 金标准案例
"""

from advanced_dayun_calculator import AdvancedDayunCalculator
from app.services.core import Bazi, StemBranch
from datetime import datetime
import asyncio
from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest

async def comprehensive_dayun_comparison():
    """全面的大运计算对比分析"""
    print("=== 大运计算对比分析 ===")
    print("高级计算器 vs 金标准案例")
    print("="*60)
    
    calculator = AdvancedDayunCalculator()
    
    # 定义测试案例
    test_cases = [
        {
            "name": "高泽兮",
            "gender": "女",
            "birth_datetime": datetime(2023, 9, 14, 0, 26, 0),
            "birth_place": "北京市昌平区",
            "bazi": {
                "year": ("癸", "卯"),
                "month": ("辛", "酉"),
                "day": ("乙", "亥"),
                "hour": ("丙", "子")
            },
            "gold_standard_dayun": [
                {"ganzhi": "壬戌", "start_age": 8, "end_age": 17},
                {"ganzhi": "癸亥", "start_age": 18, "end_age": 27},
                {"ganzhi": "甲子", "start_age": 28, "end_age": 37},
                {"ganzhi": "乙丑", "start_age": 38, "end_age": 47},
                {"ganzhi": "丙寅", "start_age": 48, "end_age": 57},
                {"ganzhi": "丁卯", "start_age": 58, "end_age": 67}
            ]
        },
        {
            "name": "高赫辰",
            "gender": "男",
            "birth_datetime": datetime(1989, 3, 18, 21, 20, 0),
            "birth_place": "山东省济南市槐荫区",
            "bazi": {
                "year": ("己", "巳"),
                "month": ("丁", "卯"),
                "day": ("丁", "丑"),
                "hour": ("辛", "亥")
            },
            "gold_standard_dayun": [
                {"ganzhi": "丙寅", "start_age": 8, "end_age": 17},
                {"ganzhi": "乙丑", "start_age": 18, "end_age": 27},
                {"ganzhi": "甲子", "start_age": 28, "end_age": 37},
                {"ganzhi": "癸亥", "start_age": 38, "end_age": 47},
                {"ganzhi": "壬戌", "start_age": 48, "end_age": 57},
                {"ganzhi": "辛酉", "start_age": 58, "end_age": 67}
            ]
        }
    ]
    
    # 添加两个新的理论测试案例
    test_cases.extend([
        {
            "name": "理论案例A（阳年男）",
            "gender": "男", 
            "birth_datetime": datetime(2024, 6, 15, 14, 30, 0),  # 甲辰年
            "birth_place": "北京",
            "bazi": {
                "year": ("甲", "辰"),  # 阳年
                "month": ("庚", "午"),
                "day": ("乙", "酉"),
                "hour": ("癸", "未")
            },
            "gold_standard_dayun": []  # 无金标准，仅做理论计算
        },
        {
            "name": "理论案例B（阳年女）",
            "gender": "女",
            "birth_datetime": datetime(2024, 12, 1, 10, 15, 0),  # 甲辰年
            "birth_place": "上海",
            "bazi": {
                "year": ("甲", "辰"),  # 阳年
                "month": ("乙", "亥"),
                "day": ("丙", "寅"),
                "hour": ("己", "巳")
            },
            "gold_standard_dayun": []  # 无金标准，仅做理论计算
        }
    ])
    
    # 对每个案例进行分析
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['name']} 分析")
        print("-" * 40)
        
        # 构建八字对象
        bazi = Bazi(
            year=StemBranch(case['bazi']['year'][0], case['bazi']['year'][1]),
            month=StemBranch(case['bazi']['month'][0], case['bazi']['month'][1]),
            day=StemBranch(case['bazi']['day'][0], case['bazi']['day'][1]),
            hour=StemBranch(case['bazi']['hour'][0], case['bazi']['hour'][1]),
            gender=case['gender']
        )
        
        print(f"基本信息: {case['name']} ({case['gender']})")
        print(f"出生时间: {case['birth_datetime']}")
        print(f"八字: {bazi.year.stem}{bazi.year.branch} {bazi.month.stem}{bazi.month.branch} {bazi.day.stem}{bazi.day.branch} {bazi.hour.stem}{bazi.hour.branch}")
        
        # 使用高级计算器计算
        advanced_result = calculator.calculate_complete_dayun(bazi, case['birth_datetime'])
        
        print(f"\n高级计算器结果:")
        print(f"  年干属性: {bazi.year.stem}干 ({'阳' if bazi.year.stem in ['甲','丙','戊','庚','壬'] else '阴'})")
        print(f"  排列方向: {advanced_result['direction']}")
        print(f"  起运年龄: {advanced_result['qiyun_age']:.1f}岁 (整数: {advanced_result['qiyun_age_int']}岁)")
        print(f"  计算说明: {advanced_result['qiyun_explanation']}")
        
        print("  大运序列:")
        for j, dayun in enumerate(advanced_result['dayun_list'][:6], 1):
            print(f"    {j}. {dayun['ganzhi']} ({dayun['start_age']}-{dayun['end_age']}岁)")
        
        # 如果有金标准，进行对比
        if case['gold_standard_dayun']:
            print(f"\n金标准对比:")
            print("  金标准大运:")
            for j, gold_dayun in enumerate(case['gold_standard_dayun'], 1):
                print(f"    {j}. {gold_dayun['ganzhi']} ({gold_dayun['start_age']}-{gold_dayun['end_age']}岁)")
            
            # 详细对比分析
            print("\n对比分析:")
            
            # 起运年龄对比
            gold_start_age = case['gold_standard_dayun'][0]['start_age']
            advanced_start_age = advanced_result['qiyun_age_int']
            age_diff = abs(gold_start_age - advanced_start_age)
            
            print(f"  起运年龄: 高级计算器 {advanced_start_age}岁 vs 金标准 {gold_start_age}岁 (差异: {age_diff}岁)")
            
            # 大运干支对比
            ganzhi_matches = 0
            age_matches = 0
            
            for j in range(min(len(advanced_result['dayun_list']), len(case['gold_standard_dayun']))):
                adv_dayun = advanced_result['dayun_list'][j]
                gold_dayun = case['gold_standard_dayun'][j]
                
                ganzhi_match = adv_dayun['ganzhi'] == gold_dayun['ganzhi']
                age_match = adv_dayun['start_age'] == gold_dayun['start_age']
                
                if ganzhi_match:
                    ganzhi_matches += 1
                if age_match:
                    age_matches += 1
                
                status = "✓" if (ganzhi_match and age_match) else ("⚠" if ganzhi_match else "❌")
                print(f"  大运{j+1}: {status} {adv_dayun['ganzhi']}({adv_dayun['start_age']}岁) vs {gold_dayun['ganzhi']}({gold_dayun['start_age']}岁)")
            
            # 计算匹配率
            total_compared = min(len(advanced_result['dayun_list']), len(case['gold_standard_dayun']))
            ganzhi_match_rate = (ganzhi_matches / total_compared * 100) if total_compared > 0 else 0
            age_match_rate = (age_matches / total_compared * 100) if total_compared > 0 else 0
            
            print(f"\n  匹配率统计:")
            print(f"    干支匹配率: {ganzhi_match_rate:.1f}% ({ganzhi_matches}/{total_compared})")
            print(f"    年龄匹配率: {age_match_rate:.1f}% ({age_matches}/{total_compared})")
            
            # 差异分析
            if ganzhi_match_rate < 100 or age_match_rate < 100:
                print(f"\n  差异原因分析:")
                if age_diff > 0:
                    print(f"    - 起运年龄差异: 可能由于节气计算方法或精度不同")
                if ganzhi_match_rate < 100:
                    print(f"    - 干支序列差异: 可能由于顺逆判断或月柱起点不同")
        
        # 获取当前系统的计算结果做参考
        try:
            request_data = BaziCalculateRequest(
                name=case['name'],
                gender=case['gender'],
                birth_datetime=case['birth_datetime'],
                is_solar_time=True,
                birth_place=case['birth_place'],
                longitude=116.4074,
                latitude=39.9042,
                timezone_offset=8.0
            )
            
            system_result = await calculate_bazi_data(request_data)
            system_dict = system_result.model_dump()
            system_dayun = system_dict.get('major_cycles', [])
            
            if system_dayun:
                print(f"\n当前系统计算结果:")
                for j, dayun in enumerate(system_dayun[:6], 1):
                    ganzhi = dayun.get('ganzhi', 'N/A')
                    start_age = dayun.get('start_age', 'N/A')
                    end_age = dayun.get('end_age', 'N/A')
                    print(f"    {j}. {ganzhi} ({start_age}-{end_age}岁)")
                
                # 与高级计算器对比
                print(f"\n高级计算器 vs 当前系统:")
                for j in range(min(len(advanced_result['dayun_list']), len(system_dayun))):
                    adv_dayun = advanced_result['dayun_list'][j]
                    sys_dayun = system_dayun[j]
                    
                    adv_ganzhi = adv_dayun['ganzhi']
                    sys_ganzhi = sys_dayun.get('ganzhi', 'N/A')
                    adv_age = adv_dayun['start_age']
                    sys_age = sys_dayun.get('start_age', 0)
                    
                    match = (adv_ganzhi == sys_ganzhi) and (adv_age == sys_age)
                    status = "✓" if match else "❌"
                    print(f"    大运{j+1}: {status} 高级:{adv_ganzhi}({adv_age}岁) vs 系统:{sys_ganzhi}({sys_age}岁)")
            
        except Exception as e:
            print(f"\n当前系统计算失败: {e}")
    
    # 总结分析
    print("\n" + "="*60)
    print("总结分析:")
    print("1. 高级计算器实现了基于节气的精确起运年龄计算")
    print("2. 采用了标准的阳年男/阴年女顺排，阴年男/阳年女逆排规则")
    print("3. 起运年龄计算公式: 距节气天数 ÷ 3 = 起运岁数")
    print("4. 与金标准的差异主要来源于:")
    print("   - 节气时间的精确度")
    print("   - 起运年龄的取整方式")
    print("   - 不同传统流派的细微差异")
    print("5. 建议:")
    print("   - 可以根据实际需求调整起运年龄的计算精度")
    print("   - 考虑提供多种计算模式（精确模式vs简化模式）")
    print("   - 建议以高级计算器的逻辑为准，因为它更符合传统理论")

if __name__ == "__main__":
    asyncio.run(comprehensive_dayun_comparison())
