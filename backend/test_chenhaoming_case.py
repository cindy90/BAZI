#!/usr/bin/env python3
"""
陈浩民案例测试 - 对比金标准验证
"""

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import json
import asyncio

async def test_chenhaoming_case():
    """测试陈浩民案例"""
    print("=== 陈浩民案例测试 ===")
    print("金标准数据:")
    print("姓名: 陈浩民")
    print("性别: 男")
    print("出生时间: 1994年11月6日 01:25（公历）")
    print("真太阳时: 1994年11月6日 01:15")
    print("出生地: 广东省广州市黄埔区")
    print("农历: 甲戌年十月初四丑时")
    print("八字: 甲戌 甲戌 丙申 己丑")
    print("生肖: 狗")
    print("日主: 丙火（阳火），生于戌月")
    print("旺衰: 身弱（异党75% vs 同党25%）")
    print("格局: 杂气伤官格")
    print("空亡: 申酉（年、月柱）")
    print("="*50)
    
    # 创建测试请求
    request_data = BaziCalculateRequest(
        name="陈浩民",
        gender="男",
        birth_datetime=datetime(1994, 11, 6, 1, 25, 0),
        is_solar_time=True,
        birth_place="广东省广州市黄埔区",
        longitude=113.4624,
        latitude=23.0998,
        timezone_offset=8.0
    )
    
    try:
        # 计算八字
        result = await calculate_bazi_data(request_data)
        result_dict = result.model_dump()
        
        print("=== 系统计算结果 ===")
        
        # 1. 验证基本信息
        print("1. 基本信息验证:")
        zodiac = result_dict.get('zodiac_sign', 'N/A')
        print(f"   生肖: {zodiac}")
        print(f"   金标准: 狗")
        print(f"   匹配情况: {'✓' if zodiac == '狗' else '✗'} {'匹配' if zodiac == '狗' else '不匹配'}")
        
        # 2. 验证四柱八字
        print("\n2. 四柱八字验证:")
        bazi_chars = result_dict.get('bazi_characters', {})
        calculated_bazi = f"{bazi_chars.get('year_stem', '')}{bazi_chars.get('year_branch', '')} {bazi_chars.get('month_stem', '')}{bazi_chars.get('month_branch', '')} {bazi_chars.get('day_stem', '')}{bazi_chars.get('day_branch', '')} {bazi_chars.get('hour_stem', '')}{bazi_chars.get('hour_branch', '')}"
        expected_bazi = "甲戌 甲戌 丙申 己丑"
        
        print(f"   系统计算: {calculated_bazi}")
        print(f"   金标准:   {expected_bazi}")
        print(f"   匹配情况: {'✓' if calculated_bazi == expected_bazi else '✗'} {'匹配' if calculated_bazi == expected_bazi else '不匹配'}")
        
        # 3. 验证日主
        print("\n3. 日主验证:")
        day_master_element = result_dict.get('day_master_element', 'N/A')
        print(f"   系统计算: {day_master_element}")
        print(f"   金标准:   火（丙火）")
        print(f"   匹配情况: {'✓' if day_master_element == '火' else '✗'} {'匹配' if day_master_element == '火' else '不匹配'}")
        
        # 4. 验证旺衰
        print("\n4. 旺衰验证:")
        strength = result_dict.get('day_master_strength', 'N/A')
        print(f"   系统计算: {strength}")
        print(f"   金标准:   身弱")
        is_weak = "弱" in strength or "偏弱" in strength or "极弱" in strength
        print(f"   匹配情况: {'✓' if is_weak else '✗'} {'匹配' if is_weak else '不匹配'}")
        
        # 5. 五行得分
        print("\n5. 五行得分:")
        five_elements = result_dict.get('five_elements_score', {})
        print(f"   系统计算: {five_elements}")
        
        # 6. 神煞验证
        print("\n6. 神煞验证:")
        shensha_list = result_dict.get('shen_sha_details', [])
        print(f"   系统计算神煞数量: {len(shensha_list)}")
        
        expected_shensha = ["国印贵人", "华盖", "文昌贵人", "天德", "月德", "驿马", "天乙贵人", "勾绞煞"]
        found_shensha = [s.get('name', '') for s in shensha_list]
        
        print(f"   金标准神煞: {expected_shensha}")
        print(f"   系统计算神煞: {found_shensha}")
        
        # 检查每个期望的神煞（允许天德/月德的别名）
        missing_shensha = []
        for expected in expected_shensha:
            if expected == "天德贵人" and "天德" in found_shensha:
                continue  # 天德 = 天德贵人
            elif expected == "月德贵人" and "月德" in found_shensha:
                continue  # 月德 = 月德贵人
            elif expected not in found_shensha:
                missing_shensha.append(expected)
        extra_shensha = [s for s in found_shensha if s not in expected_shensha]
        
        if missing_shensha:
            print(f"   缺失神煞: {missing_shensha}")
        if extra_shensha:
            print(f"   额外神煞: {extra_shensha}")
        
        # 7. 大运验证
        print("\n7. 大运验证:")
        major_cycles = result_dict.get('major_cycles', [])
        print(f"   系统计算大运数量: {len(major_cycles)}")
        
        if major_cycles:
            print("   前几步大运:")
            for i, cycle in enumerate(major_cycles[:5]):
                ten_god_info = f"{cycle.get('ten_gods_gan', 'N/A')}+{cycle.get('ten_gods_zhi', 'N/A')}"
                print(f"     {cycle.get('start_age', 'N/A')}-{cycle.get('end_age', 'N/A')}岁: {cycle.get('ganzhi', 'N/A')} ({ten_god_info})")
        
        # 金标准大运对比
        print("   金标准大运:")
        print("     1-10岁: 乙亥（正印+七杀）")
        print("     11-20岁: 丙子（比肩+正官）")
        print("     21-30岁: 丁丑（劫财+伤官）")
        print("     31-40岁: 戊寅（食神+偏印）")
        print("     41-50岁: 己卯（伤官+正印）")
        
        # 验证大运匹配
        expected_dayun = ["乙亥", "丙子", "丁丑", "戊寅", "己卯"]
        
        print("\n   大运匹配验证:")
        for i, exp_dayun in enumerate(expected_dayun):
            if i < len(major_cycles):
                cycle = major_cycles[i]
                actual_dayun = cycle.get('ganzhi', 'N/A')
                
                dayun_match = "✓" if actual_dayun == exp_dayun else "✗"
                print(f"     第{i+1}步: {actual_dayun} vs {exp_dayun} {dayun_match}")
            else:
                print(f"     第{i+1}步: 缺少数据")
        
        # 8. 流年分析
        print("\n8. 流年分析:")
        current_year = result_dict.get('current_year_fortune', {})
        if current_year:
            print(f"   当前年份: {current_year.get('year', 'N/A')}")
            print(f"   流年干支: {current_year.get('gan_zhi', 'N/A')}")
            print(f"   十神关系: {current_year.get('ten_god_relation', 'N/A')}")
        
        # 9. 纳音验证
        print("\n9. 纳音验证:")
        na_yin = result_dict.get('na_yin', {})
        print(f"   系统计算: {na_yin}")
        print("   金标准: 年柱-山头火, 月柱-山头火, 日柱-山下火, 时柱-霹雳火")
        
        # 10. 空亡验证
        print("\n10. 空亡验证:")
        gan_zhi_info = result_dict.get('gan_zhi_info', {})
        print(f"   干支信息: {gan_zhi_info}")
        print("   金标准: 申酉空亡（年、月柱）")
        
    except Exception as e:
        print(f"❌ 计算失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 分析可能的问题
    issues = []
    
    # 1. 八字计算问题
    if calculated_bazi != expected_bazi:
        issues.append(f"八字计算不准确: 系统={calculated_bazi}, 标准={expected_bazi}")
    
    # 2. 神煞计算问题
    if missing_shensha:
        issues.append(f"神煞计算不完整，缺失: {missing_shensha}")
    
    # 3. 大运计算问题
    if major_cycles:
        first_cycle = major_cycles[0]
        if first_cycle.get('ganzhi') != '乙亥':
            issues.append(f"大运计算可能有误: 第一步大运={first_cycle.get('ganzhi')}, 标准=乙亥")
    else:
        issues.append("大运计算失败: 没有返回大运数据")
    
    # 输出问题总结
    print("\n" + "="*50)
    print("=== 差异分析和问题诊断 ===")
    if issues:
        print("发现的问题:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("✓ 未发现明显问题")
    
    print("=== 修复建议 ===")
    print("1. 验证1994年节气数据的准确性")
    print("2. 检查戌月神煞规则的完整性")
    print("3. 确认男性大运起运算法")
    print("4. 验证丙火生于戌月的强弱判断")
    print("5. 检查伏吟（甲戌重复）的处理")

if __name__ == "__main__":
    asyncio.run(test_chenhaoming_case())
