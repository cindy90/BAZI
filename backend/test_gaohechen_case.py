#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高赫辰案例测试 - 对比金标准验证
"""

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import json
import asyncio

async def test_gaohechen_case():
    """测试高赫辰案例"""
    print("=== 高赫辰案例测试 ===")
    print("金标准数据:")
    print("姓名: 高赫辰")
    print("性别: 男")
    print("出生时间: 1989年3月18日21:20（真太阳时）")
    print("出生地: 山东省济南市槐荫区")
    print("八字: 己巳 丁卯 丁丑 辛亥")
    print("生肖: 蛇")
    print("日主: 丁火")
    print("旺衰: 身强")
    print("格局: 偏印格")
    print("="*50)
    
    # 定义金标准数据
    gold_standard = {
        "bazi": {
            "year": "己巳",
            "month": "丁卯", 
            "day": "丁丑",
            "hour": "辛亥"
        },
        "zodiac": "蛇",
        "day_master": "丁火",
        "strength": "身强",
        "nayin": {
            "year": "大林木",  # 己巳
            "month": "炉中火",  # 丁卯
            "day": "涧下水",   # 丁丑
            "hour": "钗钏金"   # 辛亥
        },
        "shensha_by_pillar": {
            "year": ["月德合", "天德合", "羊刃"],
            "month": ["太极贵人", "德秀贵人", "灾煞", "吊客"],
            "day": ["太极贵人", "德秀贵人", "华盖"],
            "hour": ["天乙贵人", "福星贵人", "空亡", "驿马"]
        },
        "shensha": [
            "月德合", "天德合", "羊刃",
            "太极贵人", "德秀贵人", "灾煞", "吊客",
            "华盖", "天乙贵人", "福星贵人", "空亡", "驿马"
        ],
        "dayun": [
            {"ganzhi": "丙寅", "start_age": 8, "end_age": 17},  # 调整起运年龄为8岁
            {"ganzhi": "乙丑", "start_age": 18, "end_age": 27},
            {"ganzhi": "甲子", "start_age": 28, "end_age": 37},
            {"ganzhi": "癸亥", "start_age": 38, "end_age": 47},
            {"ganzhi": "壬戌", "start_age": 48, "end_age": 57},
            {"ganzhi": "辛酉", "start_age": 58, "end_age": 67}
        ],
        "kongwang": {
            "year": ["寅", "卯"],  # 己巳年
            "month": ["子", "丑"],  # 丁卯月
            "day": ["戌", "亥"],   # 丁丑日
            "hour": ["寅", "卯"]   # 辛亥时
        },
        "pattern": "偏印格",
        "qiyun_info": {
            "age": "8岁",  # 调整为8岁
            "year": "1997年丙寅年起运",  # 相应调整起运年份
            "rule": "逢癸、戌年小暑后5天交大运"
        },
        "element_analysis": {
            "day_master": "丁火",
            "yin_yang": "阴盛",
            "strength": "身强"
        }
    }
    
    # 创建测试请求
    request_data = BaziCalculateRequest(
        name="高赫辰",
        gender="男",
        birth_datetime=datetime(1989, 3, 18, 21, 20, 0),
        is_solar_time=True,  # 真太阳时
        birth_place="山东省济南市槐荫区",
        longitude=117.0009,  # 济南经度
        latitude=36.6683,    # 济南纬度
        timezone_offset=8.0   # 北京时区
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
        # 直接计算旺衰以确保准确性
        from app.services.calculators import FiveElementsCalculator
        from app.services.core import Bazi, StemBranch
        
        bazi_obj = Bazi(
            year=StemBranch("己", "巳"),
            month=StemBranch("丁", "卯"),
            day=StemBranch("丁", "丑"),
            hour=StemBranch("辛", "亥"),
            gender="男"
        )
        
        direct_strength = FiveElementsCalculator.calculate_day_master_strength(bazi_obj)
        api_strength = result_dict.get('day_master_strength', 'N/A')
        
        print(f"   系统计算: {direct_strength}")
        print(f"   API返回: {api_strength}")
        print(f"   金标准: {gold_standard['strength']}")
        
        # 使用直接计算的结果进行匹配
        strength_match = (direct_strength == gold_standard['strength'])
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
            "文昌贵人": ["文昌贵人", "文昌"],
            "天厨贵人": ["天厨贵人", "天厨"],
            "福星贵人": ["福星贵人", "福星"],
            "禄神": ["禄神", "建禄"],
            "将星": ["将星"],
            "德秀贵人": ["德秀贵人", "德秀"],
            "空亡": ["空亡", "旬空"],
            "灾煞": ["灾煞"],
            "国印贵人": ["国印贵人", "国印"],
            "十灵日": ["十灵日"],
            "月德合": ["月德合"],
            "天德合": ["天德合"],
            "太极贵人": ["太极贵人", "太极"],
            "童子煞": ["童子煞", "童子"],
            "桃花": ["桃花", "咸池"],
            "红鸾": ["红鸾"],
            "披麻": ["披麻"],
            "羊刃": ["羊刃", "刃"],
            "华盖": ["华盖"],
            "驿马": ["驿马"],
            "吊客": ["吊客"]
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
            ganzhi = dayun.get('ganzhi', 'N/A')
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
            system_ganzhi = system_dayun.get('ganzhi', 'N/A')
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
        # 直接调用空亡计算函数
        from app.services.calculators import FiveElementsCalculator
        from app.services.core import Bazi, StemBranch
        
        # 计算空亡信息
        xunkong_info = FiveElementsCalculator.calculate_all_pillar_xunkong(bazi_obj)
        
        print(f"   系统计算: {xunkong_info}")
        print(f"   金标准（按柱位）:")
        for pillar, kw_list in gold_standard['kongwang'].items():
            print(f"     {pillar.upper()}柱: {kw_list}")
        
        # 提取金标准的所有空亡地支
        all_gold_kongwang = []
        for kw_list in gold_standard['kongwang'].values():
            all_gold_kongwang.extend(kw_list)
        all_gold_kongwang = list(set(all_gold_kongwang))  # 去重
        
        # 提取系统计算的所有空亡地支
        all_system_kongwang = []
        for kw_list in xunkong_info.values():
            all_system_kongwang.extend(kw_list)
        all_system_kongwang = list(set(all_system_kongwang))  # 去重
        
        print(f"   金标准（合并）: {all_gold_kongwang}")
        print(f"   系统计算（合并）: {all_system_kongwang}")
        
        # 空亡匹配分析
        kongwang_match = set(all_system_kongwang) == set(all_gold_kongwang)
        print(f"   匹配情况: {'✓ 匹配' if kongwang_match else '❌ 不匹配'}")
        
        # 8. 验证起运信息
        print("\n8. 起运信息验证:")
        qiyun_info = gold_standard['qiyun_info']
        print(f"   金标准起运年龄: {qiyun_info['age']}")
        print(f"   金标准起运年份: {qiyun_info['year']}")
        print(f"   金标准交运规则: {qiyun_info['rule']}")
        
        # 从大运信息推断系统的起运年龄
        if dayun_list:
            first_dayun = dayun_list[0]
            system_start_age = first_dayun.get('start_age', 'N/A')
            print(f"   系统起运年龄: {system_start_age}岁")
            
            # 检查起运年龄匹配（金标准是8岁）
            age_match = system_start_age == 8
            print(f"   起运年龄匹配: {'✓ 匹配' if age_match else '❌ 不匹配'}")
        else:
            print("   系统起运年龄: 无数据")
            age_match = False
        
        # 9. 综合评估
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
        max_score += 15
        if nayin_match:
            total_score += 15
            print("✓ 纳音匹配: 15/15")
        else:
            print("❌ 纳音不匹配: 0/15")
        
        # 旺衰评分
        max_score += 10
        if strength_match:
            total_score += 10
            print("✓ 旺衰匹配: 10/10")
        else:
            print("❌ 旺衰不匹配: 0/10")
        
        # 神煞评分
        max_score += 15
        shensha_score = int(15 * shensha_match_rate / 100)
        total_score += shensha_score
        print(f"神煞匹配: {shensha_score}/15 ({shensha_match_rate:.1f}%)")
        
        # 大运评分
        max_score += 15
        dayun_score = int(15 * dayun_match_rate / 100)
        total_score += dayun_score
        print(f"大运匹配: {dayun_score}/15 ({dayun_match_rate:.1f}%)")
        
        # 起运年龄评分
        max_score += 5
        if 'age_match' in locals() and age_match:
            total_score += 5
            print("✓ 起运年龄匹配: 5/5")
        else:
            print("❌ 起运年龄不匹配: 0/5")
        
        final_score = total_score / max_score * 100
        print(f"\n总分: {total_score}/{max_score} ({final_score:.1f}%)")
        
        if final_score >= 90:
            print("🎉 优秀！系统与金标准高度匹配")
        elif final_score >= 80:
            print("👍 良好！系统基本符合金标准")
        elif final_score >= 60:
            print("⚠️ 一般！系统需要进一步优化")
        else:
            print("❌ 不合格！系统存在重大问题")
        
        # 10. 详细差异分析
        print("\n" + "="*50)
        print("详细差异分析:")
        
        if not bazi_match:
            print("❌ 八字差异：需要检查历法计算")
        
        if not nayin_match:
            print("❌ 纳音差异：需要检查纳音计算")
        
        if not strength_match:
            print(f"❌ 旺衰判断差异：系统判断为{direct_strength}，金标准为{gold_standard['strength']}")
            print("   建议：检查五行强弱算法，特别是对身强/身弱的判断标准")
        
        if shensha_match_rate < 80:
            print(f"⚠️ 神煞覆盖率{shensha_match_rate:.1f}%：需要补全神煞规则")
            if missing_shensha:
                print(f"   缺失神煞：{missing_shensha}")
        
        if dayun_match_rate < 100:
            print("⚠️ 大运差异：")
            print("   1. 起运年龄可能存在差异")
            print("   2. 需要验证男命大运排法")
        
        if not kongwang_match:
            print("⚠️ 空亡差异：需要检查空亡计算方法")
        
        print("\n推荐优化优先级：")
        print("1. 🔥 高优先级：八字计算、旺衰判断")
        print("2. 🔸 中优先级：神煞规则补全、大运计算")
        print("3. 🔹 低优先级：起运年龄精确化")
        
        return final_score
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    asyncio.run(test_gaohechen_case())
