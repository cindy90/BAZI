#!/usr/bin/env python3
"""
简化的综合分析测试脚本
演示新的综合分析功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from backend.app.schemas.bazi import BaziCalculateRequest
from backend.app.services.bazi_calculator import calculate_bazi_data
import json
import asyncio

async def demo_comprehensive_analysis():
    """演示综合分析功能"""
    print("=== 八字综合分析功能演示 ===\n")
    
    # 测试案例
    test_cases = [
        {
            "name": "示例1 - 甲子年丙寅月己卯日辛未时",
            "birth_datetime": datetime(1984, 2, 15, 14, 30),
            "gender": "男",
            "birth_place": "北京"
        },
        {
            "name": "示例2 - 庚申年戊子月癸酉日甲寅时",
            "birth_datetime": datetime(1980, 12, 25, 8, 15),
            "gender": "女",
            "birth_place": "上海"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"{i}. {case['name']}")
        print("-" * 50)
        
        try:
            # 创建请求
            request = BaziCalculateRequest(
                name=case['name'],
                birth_datetime=case['birth_datetime'],
                gender=case['gender'],
                birth_place=case['birth_place'],
                is_solar_time=True,
                longitude=116.4 if case['birth_place'] == "北京" else 121.5,
                latitude=39.9 if case['birth_place'] == "北京" else 31.2,
                timezone_offset=8
            )
            
            # 计算八字
            result = await calculate_bazi_data(request)
            
            # 显示基本信息
            print(f"八字: {result.bazi_characters['year_stem']}{result.bazi_characters['year_branch']} "
                  f"{result.bazi_characters['month_stem']}{result.bazi_characters['month_branch']} "
                  f"{result.bazi_characters['day_stem']}{result.bazi_characters['day_branch']} "
                  f"{result.bazi_characters['hour_stem']}{result.bazi_characters['hour_branch']}")
            
            print(f"日主强弱: {result.day_master_strength}")
            print(f"基础喜用神: {', '.join(result.favorable_elements)}")
            
            # 显示综合分析结果
            if result.comprehensive_favorable_analysis:
                comp = result.comprehensive_favorable_analysis
                
                print("\n【综合分析结果】")
                print(f"• 基础分析: {comp['basic_analysis']['analysis']}")
                print(f"• 命局格局: {comp['pattern_analysis']['primary_pattern']} - {comp['pattern_analysis']['pattern_description']}")
                print(f"• 季节调候: {comp['season_analysis']['season']} - {comp['season_analysis']['adjustment_needed']}")
                print(f"• 主要喜用神: {', '.join(comp['final_prognosis']['primary_favorable'])}")
                print(f"• 次要喜用神: {', '.join(comp['final_prognosis']['secondary_favorable'])}")
                print(f"• 综合评分: {comp['final_prognosis']['overall_rating']:.1f}/10")
                
                if comp['final_prognosis']['life_advice']:
                    print(f"• 生活建议: {comp['final_prognosis']['life_advice'][0]}")
                
                if comp['pathology_analysis']['primary_issues']:
                    print(f"• 主要问题: {', '.join(comp['pathology_analysis']['primary_issues'])}")
                
                if comp['pathology_analysis']['remedies']:
                    print(f"• 调节方法: {', '.join(comp['pathology_analysis']['remedies'])}")
            
            # 显示当年运势（综合分析增强版）
            if result.current_year_fortune:
                fortune = result.current_year_fortune
                print(f"\n【{fortune['year']}年运势分析】")
                print(f"• 流年干支: {fortune['gan_zhi']}")
                print(f"• 十神关系: {fortune['ten_god_relation']}")
                
                if 'comprehensive_rating' in fortune:
                    print(f"• 综合评分: {fortune['comprehensive_rating']:.1f}/10")
                
                if 'five_elements_analysis' in fortune:
                    elem_analysis = fortune['five_elements_analysis']
                    if 'favorable_match' in elem_analysis:
                        match_status = "有利" if elem_analysis['favorable_match'] else "不利" if elem_analysis.get('unfavorable_match') else "中性"
                        print(f"• 五行匹配: {match_status}")
                
                if 'detailed_analysis' in fortune:
                    detailed = fortune['detailed_analysis']
                    print(f"• 整体运势: {detailed.get('overall_fortune', '').split('：')[1][:50]}...")
                    print(f"• 实用建议: {detailed.get('practical_advice', '').split('：')[1][:50]}...")
            
            print("\n" + "="*80 + "\n")
            
        except Exception as e:
            print(f"计算失败: {e}")
            print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(demo_comprehensive_analysis())
