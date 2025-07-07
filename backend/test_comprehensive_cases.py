#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
综合八字案例测试 - 高泽兮、高梦泽、陈梦三个金标准验证
"""

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import json
import asyncio

# 定义三个金标准案例
GOLD_STANDARDS = {
    "高泽兮": {
        "request": {
            "name": "高泽兮",
            "gender": "女",
            "birth_datetime": datetime(2023, 9, 14, 0, 26, 0),
            "is_solar_time": True,
            "birth_place": "北京市昌平区",
            "longitude": 116.2317,
            "latitude": 40.2206,
            "timezone_offset": 8.0
        },
        "standard": {
            "bazi": {
                "year": "癸卯",
                "month": "辛酉",
                "day": "乙亥",
                "hour": "丙子"
            },
            "zodiac": "兔",
            "day_master": "乙木",
            "strength": "平和",
            "nayin": {
                "year": "金箔金",
                "month": "石榴木",
                "day": "山头火",
                "hour": "涧下水"
            },
            "shensha": [
                "天乙贵人", "文昌贵人", "福星贵人", "禄神",
                "德秀贵人", "空亡", "灾煞", "国印贵人",
                "十灵日", "月德合", "天德合", "太极贵人",
                "童子煞", "桃花", "红鸾", "披麻"
            ],
            "dayun": [
                {"ganzhi": "壬戌", "start_age": 8, "end_age": 17},  # 癸卯年女命顺排
                {"ganzhi": "癸亥", "start_age": 18, "end_age": 27},
                {"ganzhi": "甲子", "start_age": 28, "end_age": 37},
                {"ganzhi": "乙丑", "start_age": 38, "end_age": 47},
                {"ganzhi": "丙寅", "start_age": 48, "end_age": 57},
                {"ganzhi": "丁卯", "start_age": 58, "end_age": 67}
            ],
            "kongwang": {
                "year": ["辰", "巳"],
                "month": ["子", "丑"],
                "day": ["申", "酉"],
                "hour": ["申", "酉"]
            },
            "pattern": "七杀格",
            "qiyun_info": {
                "age": "8岁",
                "year": "2031年壬戌年起运",
                "rule": "逢壬、丁年立春后换大运"
            }
        }
    },
    "陈梦": {
        "request": {
            "name": "陈梦",
            "gender": "女",
            "birth_datetime": datetime(1990, 4, 29, 10, 9, 0),
            "is_solar_time": True,
            "birth_place": "广东省韶关市新丰县",
            "longitude": 114.2056,  # 新丰县经度
            "latitude": 24.0578,    # 新丰县纬度
            "timezone_offset": 8.0
        },
        "standard": {
            "bazi": {
                "year": "庚午",
                "month": "庚辰",
                "day": "甲子",
                "hour": "己巳"
            },
            "zodiac": "马",
            "day_master": "甲木",
            "strength": "极弱",
            "nayin": {
                "year": "路旁土",
                "month": "白腊金",
                "day": "海中金",
                "hour": "大林木"
            },
            "shensha": [
                "福星贵人", "太极贵人", "红艳煞",  # 年柱
                "国印贵人", "金舆", "寡宿", "吊客", "华盖",  # 月柱
                "太极贵人", "福星贵人", "德秀贵人", "童子煞", "灾煞",  # 日柱
                "文昌贵人", "天厨贵人", "德秀贵人", "童子煞", "金神", "亡神", "劫煞"  # 时柱
            ],
            "dayun": [
                {"ganzhi": "己卯", "start_age": 8, "end_age": 17},
                {"ganzhi": "戊寅", "start_age": 18, "end_age": 27},
                {"ganzhi": "丁丑", "start_age": 28, "end_age": 37},
                {"ganzhi": "丙子", "start_age": 38, "end_age": 47},
                {"ganzhi": "乙亥", "start_age": 48, "end_age": 57},
                {"ganzhi": "甲戌", "start_age": 58, "end_age": 67}
            ],
            "kongwang": {
                "year": ["戌", "亥"],
                "month": ["申", "酉"],
                "day": ["戌", "亥"],
                "hour": ["戌", "亥"]
            },
            "pattern": "杂气正财格",
            "qiyun_info": {
                "age": "8岁0个月4天",
                "year": "1998年己卯年起运",
                "rule": "逢戊、癸年清明后28天交大运"
            }
        }
    }
}

async def test_single_case(case_name: str, case_data: dict):
    """测试单个案例"""
    print(f"\n=== {case_name}案例测试 ===")
    
    request_data = BaziCalculateRequest(**case_data["request"])
    gold_standard = case_data["standard"]
    
    print(f"姓名: {request_data.name}")
    print(f"性别: {request_data.gender}")
    print(f"出生时间: {request_data.birth_datetime}")
    print(f"出生地: {request_data.birth_place}")
    print(f"八字: {gold_standard['bazi']['year']} {gold_standard['bazi']['month']} {gold_standard['bazi']['day']} {gold_standard['bazi']['hour']}")
    print(f"生肖: {gold_standard['zodiac']}")
    print(f"日主: {gold_standard['day_master']}")
    print(f"旺衰: {gold_standard['strength']}")
    print(f"格局: {gold_standard['pattern']}")
    print("="*50)
    
    try:
        # 计算八字
        result = await calculate_bazi_data(request_data)
        result_dict = result.model_dump()
        
        print("=== 系统计算结果 ===")
        
        # 1. 验证八字
        print("1. 八字验证:")
        bazi_result = result_dict.get('bazi_characters', {})
        
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
        
        # 2. 验证纳音
        print("\n2. 纳音验证:")
        nayin_result = result_dict.get('na_yin', {})
        
        system_nayin = {}
        for pillar in ["year", "month", "day", "hour"]:
            nayin_key = f"{pillar}_na_yin"
            if nayin_key in nayin_result:
                nayin_value = nayin_result[nayin_key]
                if isinstance(nayin_value, list) and len(nayin_value) > 0:
                    system_nayin[pillar] = nayin_value[0]
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
        
        # 3. 验证旺衰
        print("\n3. 旺衰验证:")
        from app.services.calculators import FiveElementsCalculator
        from app.services.core import Bazi, StemBranch
        
        # 构建八字对象
        bazi_obj = Bazi(
            year=StemBranch(gold_standard['bazi']['year'][0], gold_standard['bazi']['year'][1]),
            month=StemBranch(gold_standard['bazi']['month'][0], gold_standard['bazi']['month'][1]),
            day=StemBranch(gold_standard['bazi']['day'][0], gold_standard['bazi']['day'][1]),
            hour=StemBranch(gold_standard['bazi']['hour'][0], gold_standard['bazi']['hour'][1]),
            gender=request_data.gender
        )
        
        direct_strength = FiveElementsCalculator.calculate_day_master_strength(bazi_obj)
        api_strength = result_dict.get('day_master_strength', 'N/A')
        
        print(f"   系统计算: {direct_strength}")
        print(f"   API返回: {api_strength}")
        print(f"   金标准: {gold_standard['strength']}")
        
        strength_match = (direct_strength == gold_standard['strength'])
        print(f"   匹配情况: {'✓ 匹配' if strength_match else '❌ 不匹配'}")
        
        # 4. 验证神煞
        print("\n4. 神煞验证:")
        shensha_list = result_dict.get('shen_sha_details', [])
        system_shensha = [s.get('name', '') for s in shensha_list]
        
        print(f"   系统计算神煞数量: {len(system_shensha)}")
        print(f"   金标准神煞数量: {len(gold_standard['shensha'])}")
        
        # 神煞匹配分析
        shensha_aliases = {
            "天乙贵人": ["天乙贵人", "贵人"],
            "文昌贵人": ["文昌贵人", "文昌"],
            "福星贵人": ["福星贵人", "福星"],
            "太极贵人": ["太极贵人", "太极"],
            "德秀贵人": ["德秀贵人", "德秀"],
            "国印贵人": ["国印贵人", "国印"],
            "天厨贵人": ["天厨贵人", "天厨"],
            "童子煞": ["童子煞", "童子"],
            "灾煞": ["灾煞"],
            "空亡": ["空亡", "旬空"],
            "红艳煞": ["红艳煞", "红艳"],
            "金舆": ["金舆"],
            "寡宿": ["寡宿"],
            "吊客": ["吊客"],
            "华盖": ["华盖"],
            "金神": ["金神"],
            "亡神": ["亡神"],
            "劫煞": ["劫煞"],
            "桃花": ["桃花", "咸池"],
            "红鸾": ["红鸾"],
            "披麻": ["披麻"]
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
        
        print(f"   匹配神煞: {len(matched_shensha)}/{len(normalized_gold)}")
        if missing_shensha:
            print(f"   缺失神煞: {missing_shensha}")
        if extra_shensha:
            print(f"   额外神煞: {extra_shensha}")
        
        shensha_match_rate = len(matched_shensha) / len(normalized_gold) * 100 if normalized_gold else 0
        print(f"   神煞匹配率: {shensha_match_rate:.1f}%")
        
        # 5. 验证大运
        print("\n5. 大运验证:")
        dayun_list = result_dict.get('major_cycles', [])
        
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
            age_match = abs(gold_start - system_start) <= 1
            
            if ganzhi_match and age_match:
                dayun_matches += 1
                print(f"   大运{i+1}: ✓ {gold_ganzhi} 匹配")
            else:
                print(f"   大运{i+1}: ❌ {gold_ganzhi} vs {system_ganzhi}")
        
        dayun_match_rate = dayun_matches / len(gold_standard['dayun']) * 100 if gold_standard['dayun'] else 0
        print(f"   大运匹配率: {dayun_match_rate:.1f}%")
        
        # 6. 验证空亡
        print("\n6. 空亡验证:")
        xunkong_info = FiveElementsCalculator.calculate_all_pillar_xunkong(bazi_obj)
        
        all_gold_kongwang = []
        for kw_list in gold_standard['kongwang'].values():
            all_gold_kongwang.extend(kw_list)
        all_gold_kongwang = list(set(all_gold_kongwang))
        
        all_system_kongwang = []
        for kw_list in xunkong_info.values():
            all_system_kongwang.extend(kw_list)
        all_system_kongwang = list(set(all_system_kongwang))
        
        kongwang_match = set(all_system_kongwang) == set(all_gold_kongwang)
        print(f"   空亡匹配: {'✓ 匹配' if kongwang_match else '❌ 不匹配'}")
        
        # 7. 综合评分
        print("\n7. 综合评分:")
        
        total_score = 0
        max_score = 0
        
        # 八字评分 (40分)
        max_score += 40
        if bazi_match:
            total_score += 40
            print("   ✓ 八字匹配: 40/40")
        else:
            print("   ❌ 八字不匹配: 0/40")
        
        # 纳音评分 (15分)
        max_score += 15
        if nayin_match:
            total_score += 15
            print("   ✓ 纳音匹配: 15/15")
        else:
            print("   ❌ 纳音不匹配: 0/15")
        
        # 旺衰评分 (10分)
        max_score += 10
        if strength_match:
            total_score += 10
            print("   ✓ 旺衰匹配: 10/10")
        else:
            print("   ❌ 旺衰不匹配: 0/10")
        
        # 神煞评分 (15分)
        max_score += 15
        shensha_score = int(15 * shensha_match_rate / 100)
        total_score += shensha_score
        print(f"   神煞匹配: {shensha_score}/15 ({shensha_match_rate:.1f}%)")
        
        # 大运评分 (15分)
        max_score += 15
        dayun_score = int(15 * dayun_match_rate / 100)
        total_score += dayun_score
        print(f"   大运匹配: {dayun_score}/15 ({dayun_match_rate:.1f}%)")
        
        # 空亡评分 (5分)
        max_score += 5
        if kongwang_match:
            total_score += 5
            print("   ✓ 空亡匹配: 5/5")
        else:
            print("   ❌ 空亡不匹配: 0/5")
        
        final_score = total_score / max_score * 100
        print(f"\n   {case_name}总分: {total_score}/{max_score} ({final_score:.1f}%)")
        
        return {
            "case_name": case_name,
            "total_score": total_score,
            "max_score": max_score,
            "percentage": final_score,
            "details": {
                "bazi_match": bazi_match,
                "nayin_match": nayin_match,
                "strength_match": strength_match,
                "shensha_match_rate": shensha_match_rate,
                "dayun_match_rate": dayun_match_rate,
                "kongwang_match": kongwang_match
            }
        }
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return {
            "case_name": case_name,
            "total_score": 0,
            "max_score": 100,
            "percentage": 0,
            "error": str(e)
        }

async def test_comprehensive_cases():
    """综合测试所有案例"""
    print("=== 八字排盘系统综合测试 ===")
    print("测试案例：高泽兮、陈梦")
    print("="*60)
    
    results = []
    
    # 测试每个案例
    for case_name, case_data in GOLD_STANDARDS.items():
        result = await test_single_case(case_name, case_data)
        results.append(result)
    
    # 综合统计
    print("\n" + "="*60)
    print("=== 综合测试统计 ===")
    
    total_cases = len(results)
    total_score = sum(r['total_score'] for r in results)
    total_max = sum(r['max_score'] for r in results)
    average_percentage = total_score / total_max * 100
    
    print(f"测试案例总数: {total_cases}")
    print(f"总得分: {total_score}/{total_max} ({average_percentage:.1f}%)")
    
    print("\n各案例得分详情:")
    for result in results:
        case_name = result['case_name']
        percentage = result['percentage']
        
        if 'error' in result:
            print(f"  {case_name}: 测试失败 - {result['error']}")
        else:
            status = "优秀" if percentage >= 90 else "良好" if percentage >= 80 else "一般" if percentage >= 60 else "不合格"
            print(f"  {case_name}: {result['total_score']}/{result['max_score']} ({percentage:.1f}%) - {status}")
    
    # 详细分析
    print("\n=== 详细分析 ===")
    successful_results = [r for r in results if 'error' not in r]
    
    if successful_results:
        # 八字匹配统计
        bazi_matches = sum(1 for r in successful_results if r['details']['bazi_match'])
        print(f"八字匹配率: {bazi_matches}/{len(successful_results)} ({bazi_matches/len(successful_results)*100:.1f}%)")
        
        # 纳音匹配统计
        nayin_matches = sum(1 for r in successful_results if r['details']['nayin_match'])
        print(f"纳音匹配率: {nayin_matches}/{len(successful_results)} ({nayin_matches/len(successful_results)*100:.1f}%)")
        
        # 旺衰匹配统计
        strength_matches = sum(1 for r in successful_results if r['details']['strength_match'])
        print(f"旺衰匹配率: {strength_matches}/{len(successful_results)} ({strength_matches/len(successful_results)*100:.1f}%)")
        
        # 神煞平均匹配率
        shensha_avg = sum(r['details']['shensha_match_rate'] for r in successful_results) / len(successful_results)
        print(f"神煞平均匹配率: {shensha_avg:.1f}%")
        
        # 大运平均匹配率
        dayun_avg = sum(r['details']['dayun_match_rate'] for r in successful_results) / len(successful_results)
        print(f"大运平均匹配率: {dayun_avg:.1f}%")
        
        # 空亡匹配统计
        kongwang_matches = sum(1 for r in successful_results if r['details']['kongwang_match'])
        print(f"空亡匹配率: {kongwang_matches}/{len(successful_results)} ({kongwang_matches/len(successful_results)*100:.1f}%)")
    
    # 优化建议
    print("\n=== 优化建议 ===")
    if average_percentage >= 90:
        print("🎉 系统表现优秀，与金标准高度匹配！")
    elif average_percentage >= 80:
        print("👍 系统表现良好，基本符合金标准。")
        print("建议继续优化大运算法和神煞规则。")
    elif average_percentage >= 60:
        print("⚠️ 系统表现一般，需要重点优化。")
        print("建议优先修复八字排盘和旺衰判断算法。")
    else:
        print("❌ 系统存在重大问题，需要全面检查。")
        print("建议从基础算法开始重新验证。")
    
    return {
        "total_cases": total_cases,
        "average_percentage": average_percentage,
        "results": results
    }

if __name__ == "__main__":
    asyncio.run(test_comprehensive_cases())
