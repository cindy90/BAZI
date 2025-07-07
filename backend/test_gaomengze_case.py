#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高梦泽案例测试 - 对比金标准验证
"""

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import json
import asyncio

async def test_gaomengze_case():
    """测试高梦泽案例"""
    print("=== 高梦泽案例测试 ===")
    print("金标准数据:")
    print("姓名: 高梦泽")
    print("性别: 女")
    print("出生时间: 2020年7月29日 13:26（北京时间）")
    print("出生地: 北京市朝阳区")
    print("八字: 庚子 癸未 癸酉 己未")
    print("生肖: 鼠")
    print("日主: 癸水（阴水），生于未月")
    print("旺衰: 癸水偏弱")
    print("格局: 杂气七杀格")
    print("="*50)
    
    # 创建测试请求
    request_data = BaziCalculateRequest(
        name="高梦泽",
        gender="女",
        birth_datetime=datetime(2020, 7, 29, 13, 26, 0),
        is_solar_time=True,
        birth_place="北京市朝阳区",
        longitude=116.4074,
        latitude=39.9042,
        timezone_offset=8.0
    )
    
    try:
        # 计算八字
        result = await calculate_bazi_data(request_data)
        result_dict = result.model_dump()
        
        print("=== 系统计算结果 ===")
        
        # 1. 验证基本信息
        print("1. 基本信息验证:")
        print(f"   姓名: {result_dict.get('name', 'N/A')}")
        print(f"   性别: {result_dict.get('gender', 'N/A')}")
        print(f"   生肖: {result_dict.get('zodiac_sign', 'N/A')}")
        print(f"   金标准: 鼠")
        
        # 2. 验证四柱八字
        print("\n2. 四柱八字验证:")
        bazi_chars = result_dict.get('bazi_characters', {})
        calculated_bazi = f"{bazi_chars.get('year_stem', '')}{bazi_chars.get('year_branch', '')} {bazi_chars.get('month_stem', '')}{bazi_chars.get('month_branch', '')} {bazi_chars.get('day_stem', '')}{bazi_chars.get('day_branch', '')} {bazi_chars.get('hour_stem', '')}{bazi_chars.get('hour_branch', '')}"
        print(f"   系统计算: {calculated_bazi}")
        print(f"   金标准:   庚子 癸未 癸酉 己未")
        print(f"   匹配情况: {'✓ 匹配' if calculated_bazi == '庚子 癸未 癸酉 己未' else '❌ 不匹配'}")
        
        # 3. 验证日主
        print("\n3. 日主验证:")
        day_master = result_dict.get('day_master_element', 'N/A')
        print(f"   系统计算: {day_master}")
        print(f"   金标准:   水（癸水）")
        print(f"   匹配情况: {'✓ 匹配' if day_master == '水' else '❌ 不匹配'}")
        
        # 4. 验证旺衰
        print("\n4. 旺衰验证:")
        strength = result_dict.get('day_master_strength', 'N/A')
        print(f"   系统计算: {strength}")
        print(f"   金标准:   癸水偏弱")
        print(f"   匹配情况: {'✓ 匹配' if '偏弱' in strength or '弱' in strength else '❌ 不匹配'}")
        
        # 5. 验证五行得分
        print("\n5. 五行得分:")
        five_elements = result_dict.get('five_elements_score', {})
        print(f"   系统计算: {five_elements}")
        
        # 6. 验证神煞
        print("\n6. 神煞验证:")
        shensha_list = result_dict.get('shen_sha_details', [])
        print(f"   系统计算神煞数量: {len(shensha_list)}")
        print("   金标准神煞: 禄神、天乙贵人、金神、桃花、天喜、披麻、血刃、天德合、月德合、童子煞")
        
        expected_shensha = ['禄神', '天乙贵人', '金神', '桃花', '天喜', '披麻', '血刃', '天德合', '月德合', '童子煞']
        found_shensha = [s.get('name', '') for s in shensha_list]
        print(f"   系统计算神煞: {found_shensha}")
        
        missing_shensha = [s for s in expected_shensha if s not in found_shensha]
        extra_shensha = [s for s in found_shensha if s not in expected_shensha]
        
        if missing_shensha:
            print(f"   缺失神煞: {missing_shensha}")
        if extra_shensha:
            print(f"   额外神煞: {extra_shensha}")
        
        # 7. 验证大运
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
        print("     1-10岁: 壬午（劫财+偏财）")
        print("     11-20岁: 辛巳（偏印+正财）")
        print("     21-30岁: 庚辰（正印+正官）")
        print("     31-40岁: 己卯（七杀+食神）")
        
        # 验证大运匹配
        expected_dayun = ["壬午", "辛巳", "庚辰", "己卯"]
        expected_ages = [(2, 11), (12, 21), (22, 31), (32, 41)]
        
        print("\n   大运匹配验证:")
        for i, (exp_dayun, exp_age) in enumerate(zip(expected_dayun, expected_ages)):
            if i < len(major_cycles):
                cycle = major_cycles[i]
                actual_dayun = cycle.get('ganzhi', 'N/A')
                actual_age = (cycle.get('start_age', 0), cycle.get('end_age', 0))
                
                dayun_match = "✓" if actual_dayun == exp_dayun else "✗"
                age_match = "✓" if actual_age == exp_age else "✗"
                
                print(f"     第{i+1}步: {actual_dayun} vs {exp_dayun} {dayun_match}, {actual_age} vs {exp_age} {age_match}")
            else:
                print(f"     第{i+1}步: 缺少数据")
        
        # 8. 验证流年分析
        print("\n8. 流年分析:")
        current_year = result_dict.get('current_year_fortune', {})
        if current_year:
            print(f"   当前年份: {current_year.get('year', 'N/A')}")
            print(f"   流年干支: {current_year.get('gan_zhi', 'N/A')}")
            print(f"   十神关系: {current_year.get('ten_god', 'N/A')}")
        
        # 9. 验证纳音
        print("\n9. 纳音验证:")
        na_yin = result_dict.get('na_yin', {})
        print(f"   系统计算: {na_yin}")
        print("   金标准: 年柱-壁上土, 月柱-杨柳木, 日柱-剑锋金, 时柱-天上火")
        
        # 10. 验证空亡
        print("\n10. 空亡验证:")
        # 检查是否有空亡相关信息
        if 'gan_zhi_info' in result_dict:
            ganzhi_info = result_dict['gan_zhi_info']
            print(f"   干支信息: {ganzhi_info}")
        
        return result_dict
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

async def analyze_discrepancies(result_dict):
    """分析差异和可能的问题"""
    print("\n" + "="*50)
    print("=== 差异分析和问题诊断 ===")
    
    if not result_dict:
        print("❌ 无法获取计算结果，请检查服务状态")
        return
    
    # 分析可能的问题
    issues = []
    
    # 1. 八字计算问题
    bazi_chars = result_dict.get('bazi_characters', {})
    calculated_bazi = f"{bazi_chars.get('year_stem', '')}{bazi_chars.get('year_branch', '')} {bazi_chars.get('month_stem', '')}{bazi_chars.get('month_branch', '')} {bazi_chars.get('day_stem', '')}{bazi_chars.get('day_branch', '')} {bazi_chars.get('hour_stem', '')}{bazi_chars.get('hour_branch', '')}"
    
    if calculated_bazi != '庚子 癸未 癸酉 己未':
        issues.append(f"八字计算不准确: 系统={calculated_bazi}, 标准=庚子 癸未 癸酉 己未")
    
    # 2. 神煞计算问题
    shensha_list = result_dict.get('shen_sha_details', [])
    found_shensha = [s.get('name', '') for s in shensha_list]
    expected_shensha = ['禄神', '天乙贵人', '金神', '桃花', '天喜', '披麻', '血刃', '天德合', '月德合', '童子煞']
    
    missing_shensha = [s for s in expected_shensha if s not in found_shensha]
    if missing_shensha:
        issues.append(f"神煞计算不完整，缺失: {missing_shensha}")
    
    # 3. 大运计算问题
    major_cycles = result_dict.get('major_cycles', [])
    if major_cycles:
        first_cycle = major_cycles[0]
        if first_cycle.get('ganzhi') != '壬午':
            issues.append(f"大运计算可能有误: 第一步大运={first_cycle.get('ganzhi')}, 标准=壬午")
    else:
        issues.append("大运计算失败: 没有返回大运数据")
    
    # 输出问题总结
    if issues:
        print("发现的问题:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("✓ 未发现明显问题")
    
    # 提供修复建议
    print("\n=== 修复建议 ===")
    print("1. 检查节气数据的准确性")
    print("2. 验证神煞规则的完整性")
    print("3. 确认大运起运算法")
    print("4. 检查真太阳时校正")
    print("5. 验证五行旺衰判断逻辑")

if __name__ == "__main__":
    async def main():
        result = await test_gaomengze_case()
        await analyze_discrepancies(result)
    
    asyncio.run(main())
