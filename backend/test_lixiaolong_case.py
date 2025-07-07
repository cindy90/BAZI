#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
李小龙案例测试 - 对比金标准验证
"""

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import json
import asyncio

async def test_lixiaolong_case():
    """测试李小龙案例"""
    print("=== 李小龙案例测试 ===")
    print("金标准数据:")
    print("姓名: 李小龙")
    print("性别: 男")
    print("出生时间: 1940年11月27日 8:00（当地时间）")
    print("出生地: 美国旧金山")
    print("八字: 庚辰 丁亥 丁酉 甲辰")
    print("生肖: 龙")
    print("日主: 丁火（阴火），生于亥月")
    print("旺衰: 丁火偏弱")
    print("纳音: 白蜡金 屋上土 山下火 佛灯火")
    print("="*50)
    
    # 定义金标准数据
    gold_standard = {
        "bazi": {
            "year": "庚辰",
            "month": "丁亥", 
            "day": "丁酉",
            "hour": "甲辰"
        },
        "zodiac": "龙",
        "day_master": "丁火",
        "strength": "丁火偏弱",
        "nayin": {
            "year": "白蜡金",
            "month": "屋上土",
            "day": "山下火",
            "hour": "佛灯火"
        },
        "shensha": [
            "天乙贵人", "太极贵人", "天德贵人", "月德贵人", "金神", 
            "华盖", "学堂", "国印", "桃花", "天喜", "红鸾", "孤辰",
            "寡宿", "勾煞", "绞煞", "天罗", "地网", "十恶大败"
        ],
        "dayun": [
            {"ganzhi": "丙戌", "start_age": 3, "end_age": 12},
            {"ganzhi": "乙酉", "start_age": 13, "end_age": 22},
            {"ganzhi": "甲申", "start_age": 23, "end_age": 32},
            {"ganzhi": "癸未", "start_age": 33, "end_age": 42},
            {"ganzhi": "壬午", "start_age": 43, "end_age": 52},
            {"ganzhi": "辛巳", "start_age": 53, "end_age": 62}
        ],
        "kongwang": ["申", "酉"]  # 月柱、时柱空亡
    }
    
    # 创建测试请求
    request_data = BaziCalculateRequest(
        name="李小龙",
        gender="男",
        birth_datetime=datetime(1940, 11, 27, 8, 0, 0),
        is_solar_time=True,
        birth_place="旧金山",
        longitude=-122.4194,  # 旧金山经度
        latitude=37.7749,     # 旧金山纬度
        timezone_offset=-8.0   # 旧金山时区（PST）
    )
    
    try:
        # 计算八字
        result = await calculate_bazi_data(request_data)
        result_dict = result.model_dump()
        
        print("=== 系统计算结果 ===")
        
        # 1. 验证基本信息
        print("1. 基本信息验证:")
        print(f"   姓名: {request_data.name}")
        print(f"   性别: {request_data.gender}")
        print(f"   生肖: {result_dict.get('zodiac_sign', 'N/A')}")
        print(f"   日主: {result_dict.get('day_master_element', 'N/A')}")
        
        # 2. 验证八字
        print("\n2. 八字验证:")
        bazi_result = result_dict.get('bazi_characters', {})
        
        # 组合八字显示
        year_ganzhi = bazi_result.get('year_stem', '') + bazi_result.get('year_branch', '')
        month_ganzhi = bazi_result.get('month_stem', '') + bazi_result.get('month_branch', '')
        day_ganzhi = bazi_result.get('day_stem', '') + bazi_result.get('day_branch', '')
        hour_ganzhi = bazi_result.get('hour_stem', '') + bazi_result.get('hour_branch', '')
        
        print(f"   系统计算: {year_ganzhi} {month_ganzhi} {day_ganzhi} {hour_ganzhi}")
        print(f"   金标准:   {gold_standard['bazi']['year']} {gold_standard['bazi']['month']} {gold_standard['bazi']['day']} {gold_standard['bazi']['hour']}")
        
        system_bazi = {
            "year": year_ganzhi,
            "month": month_ganzhi,
            "day": day_ganzhi,
            "hour": hour_ganzhi
        }
        
        bazi_match = True
        for pillar in ["year", "month", "day", "hour"]:
            system_value = system_bazi.get(pillar, 'N/A')
            gold_value = gold_standard["bazi"][pillar]
            match = system_value == gold_value
            print(f"   {pillar.upper()}柱: {system_value} vs {gold_value} {'✓' if match else '❌'}")
            if not match:
                bazi_match = False
        
        print(f"   八字整体匹配: {'✓ 匹配' if bazi_match else '❌ 不匹配'}")
        
        # 3. 验证纳音
        print("\n3. 纳音验证:")
        nayin_result = result_dict.get('na_yin', {})
        print(f"   系统计算: {nayin_result}")
        print(f"   金标准:   {gold_standard['nayin']}")
        
        # 提取纳音名称
        system_nayin = {}
        for pillar in ["year", "month", "day", "hour"]:
            nayin_key = f"{pillar}_na_yin"
            if nayin_key in nayin_result:
                nayin_value = nayin_result[nayin_key]
                if isinstance(nayin_value, list) and len(nayin_value) > 0:
                    system_nayin[pillar] = nayin_value[0]  # 取名称部分
                else:
                    system_nayin[pillar] = str(nayin_value)
            else:
                system_nayin[pillar] = 'N/A'
        
        nayin_match = True
        for pillar in ["year", "month", "day", "hour"]:
            system_value = system_nayin.get(pillar, 'N/A')
            gold_value = gold_standard["nayin"][pillar]
            match = system_value == gold_value
            print(f"   {pillar.upper()}柱: {system_value} vs {gold_value} {'✓' if match else '❌'}")
            if not match:
                nayin_match = False
        
        print(f"   纳音整体匹配: {'✓ 匹配' if nayin_match else '❌ 不匹配'}")
        
        # 4. 验证旺衰
        print("\n4. 旺衰验证:")
        strength = result_dict.get('day_master_strength', 'N/A')
        print(f"   系统计算: {strength}")
        print(f"   金标准:   {gold_standard['strength']}")
        strength_match = '偏弱' in strength or '弱' in strength
        print(f"   匹配情况: {'✓ 匹配' if strength_match else '❌ 不匹配'}")
        
        # 5. 验证神煞
        print("\n5. 神煞验证:")
        shensha_list = result_dict.get('shen_sha_details', [])
        system_shensha = [s.get('name', '') for s in shensha_list]
        print(f"   系统计算神煞数量: {len(system_shensha)}")
        print(f"   金标准神煞数量: {len(gold_standard['shensha'])}")
        
        print("   金标准神煞:")
        for i, shensha in enumerate(gold_standard['shensha'], 1):
            print(f"     {i:2d}. {shensha}")
        
        print("   系统计算神煞:")
        for i, shensha in enumerate(system_shensha, 1):
            print(f"     {i:2d}. {shensha}")
        
        # 神煞匹配分析（支持别名）
        shensha_aliases = {
            "天乙贵人": ["天乙贵人", "贵人"],
            "太极贵人": ["太极贵人", "太极"],
            "天德贵人": ["天德贵人", "天德"],
            "月德贵人": ["月德贵人", "月德"],
            "金神": ["金神"],
            "华盖": ["华盖"],
            "学堂": ["学堂", "学馆"],
            "国印": ["国印", "国印贵人"],
            "桃花": ["桃花", "咸池"],
            "天喜": ["天喜"],
            "红鸾": ["红鸾"],
            "孤辰": ["孤辰"],
            "寡宿": ["寡宿"],
            "勾煞": ["勾煞", "勾绞煞"],
            "绞煞": ["绞煞", "勾绞煞"],
            "天罗": ["天罗"],
            "地网": ["地网"],
            "十恶大败": ["十恶大败"]
        }
        
        def normalize_shensha_name(name):
            """标准化神煞名称"""
            for standard, aliases in shensha_aliases.items():
                if name in aliases:
                    return standard
            return name
        
        normalized_system = [normalize_shensha_name(s) for s in system_shensha]
        normalized_gold = [normalize_shensha_name(s) for s in gold_standard['shensha']]
        
        matched_shensha = []
        missing_shensha = []
        extra_shensha = []
        
        for gold_shensha in normalized_gold:
            if gold_shensha in normalized_system:
                matched_shensha.append(gold_shensha)
            else:
                missing_shensha.append(gold_shensha)
        
        for system_shensha in normalized_system:
            if system_shensha not in normalized_gold:
                extra_shensha.append(system_shensha)
        
        print(f"\n   匹配神煞 ({len(matched_shensha)}):")
        for shensha in matched_shensha:
            print(f"     ✓ {shensha}")
        
        if missing_shensha:
            print(f"\n   缺失神煞 ({len(missing_shensha)}):")
            for shensha in missing_shensha:
                print(f"     ❌ {shensha}")
        
        if extra_shensha:
            print(f"\n   额外神煞 ({len(extra_shensha)}):")
            for shensha in extra_shensha:
                print(f"     ➕ {shensha}")
        
        shensha_match_rate = len(matched_shensha) / len(normalized_gold) * 100
        print(f"\n   神煞匹配率: {shensha_match_rate:.1f}%")
        
        # 6. 验证大运
        print("\n6. 大运验证:")
        dayun_list = result_dict.get('major_cycles', [])
        print(f"   系统计算大运数量: {len(dayun_list)}")
        print(f"   金标准大运数量: {len(gold_standard['dayun'])}")
        
        print("   金标准大运:")
        for i, dayun in enumerate(gold_standard['dayun'], 1):
            print(f"     {i}. {dayun['ganzhi']} ({dayun['start_age']}-{dayun['end_age']}岁)")
        
        print("   系统计算大运:")
        for i, dayun in enumerate(dayun_list, 1):
            # 从系统结果中提取大运信息
            ganzhi = dayun.get('gan_zhi', 'N/A')
            start_age = dayun.get('start_age', 'N/A')
            end_age = dayun.get('end_age', 'N/A')
            print(f"     {i}. {ganzhi} ({start_age}-{end_age}岁)")
        
        # 大运匹配分析
        dayun_matches = 0
        min_compare_count = min(len(gold_standard['dayun']), len(dayun_list))
        for i in range(min_compare_count):
            gold_dayun = gold_standard['dayun'][i]
            system_dayun = dayun_list[i]
            
            gold_ganzhi = gold_dayun['ganzhi']
            system_ganzhi = system_dayun.get('gan_zhi', 'N/A')
            gold_start = gold_dayun['start_age']
            system_start = system_dayun.get('start_age', 0)
            
            ganzhi_match = gold_ganzhi == system_ganzhi
            age_match = abs(gold_start - system_start) <= 1  # 允许1岁误差
            
            if ganzhi_match and age_match:
                dayun_matches += 1
                print(f"   大运{i+1}: ✓ {gold_ganzhi} 匹配")
            else:
                print(f"   大运{i+1}: ❌ {gold_ganzhi} vs {system_ganzhi} ({'干支' if not ganzhi_match else '年龄'}不匹配)")
        
        if len(gold_standard['dayun']) > 0:
            dayun_match_rate = dayun_matches / len(gold_standard['dayun']) * 100
        else:
            dayun_match_rate = 0
        print(f"\n   大运匹配率: {dayun_match_rate:.1f}%")
        
        # 7. 验证空亡
        print("\n7. 空亡验证:")
        # 从interactions中查找空亡信息
        interactions = result_dict.get('interactions', {})
        kongwang_result = []
        if 'kong_wang' in interactions:
            kongwang_result = interactions['kong_wang']
        elif 'special_combinations' in interactions:
            special_combinations = interactions['special_combinations']
            if 'kong_wang' in special_combinations:
                kongwang_result = special_combinations['kong_wang']
        
        print(f"   系统计算: {kongwang_result}")
        print(f"   金标准:   {gold_standard['kongwang']}")
        
        kongwang_match = set(kongwang_result) == set(gold_standard['kongwang'])
        print(f"   匹配情况: {'✓ 匹配' if kongwang_match else '❌ 不匹配'}")
        
        # 8. 综合评估
        print("\n" + "="*50)
        print("综合评估:")
        
        total_score = 0
        max_score = 0
        
        # 八字评分
        max_score += 40
        if bazi_match:
            total_score += 40
            print("✓ 八字匹配: 40/40")
        else:
            print("❌ 八字不匹配: 0/40")
        
        # 纳音评分
        max_score += 20
        if nayin_match:
            total_score += 20
            print("✓ 纳音匹配: 20/20")
        else:
            print("❌ 纳音不匹配: 0/20")
        
        # 旺衰评分
        max_score += 10
        if strength_match:
            total_score += 10
            print("✓ 旺衰匹配: 10/10")
        else:
            print("❌ 旺衰不匹配: 0/10")
        
        # 神煞评分
        max_score += 20
        shensha_score = int(20 * shensha_match_rate / 100)
        total_score += shensha_score
        print(f"神煞匹配: {shensha_score}/20 ({shensha_match_rate:.1f}%)")
        
        # 大运评分
        max_score += 20
        dayun_score = int(20 * dayun_match_rate / 100)
        total_score += dayun_score
        print(f"大运匹配: {dayun_score}/20 ({dayun_match_rate:.1f}%)")
        
        # 空亡评分
        max_score += 10
        if kongwang_match:
            total_score += 10
            print("✓ 空亡匹配: 10/10")
        else:
            print("❌ 空亡不匹配: 0/10")
        
        final_score = total_score / max_score * 100
        print(f"\n总分: {total_score}/{max_score} ({final_score:.1f}%)")
        
        if final_score >= 90:
            print("🎉 优秀！系统与金标准高度匹配")
        elif final_score >= 70:
            print("👍 良好！系统基本符合金标准")
        elif final_score >= 50:
            print("⚠️ 一般！系统需要进一步优化")
        else:
            print("❌ 不合格！系统存在重大问题")
        
        return final_score
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    asyncio.run(test_lixiaolong_case())
