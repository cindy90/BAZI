#!/usr/bin/env python3
"""
简化的八字流年分析集成测试
验证增强版 special_combinations 和 predicted_events 功能
"""

import sys
import os
import asyncio
import json
from datetime import datetime, timezone, timedelta

# 添加路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.bazi_calculator import calculate_bazi_data
from backend.app.schemas.bazi import BaziCalculateRequest

async def test_enhanced_liunian_api():
    """测试增强版流年分析API"""
    print("=== 测试增强版流年分析API ===")
    
    # 准备测试数据 - 使用正确的API结构
    beijing_tz = timezone(timedelta(hours=8))
    test_request = BaziCalculateRequest(
        name="测试用户",
        gender="男",
        birth_datetime=datetime(1984, 2, 15, 14, 30, tzinfo=beijing_tz),
        is_solar_time=True,
        birth_place="北京市",
        longitude=116.4074,
        latitude=39.9042,
        timezone_offset=8.0
    )
    
    print(f"测试请求:")
    print(f"  姓名: {test_request.name}")
    print(f"  生日: {test_request.birth_datetime}")
    print(f"  性别: {test_request.gender}")
    print(f"  出生地: {test_request.birth_place}")
    
    try:
        # 调用完整的计算API
        result = await calculate_bazi_data(test_request)
        
        print(f"\n=== 基本信息 ===")
        bazi_chars = result.bazi_characters
        bazi_str = f"{bazi_chars['year_stem']}{bazi_chars['year_branch']} {bazi_chars['month_stem']}{bazi_chars['month_branch']} {bazi_chars['day_stem']}{bazi_chars['day_branch']} {bazi_chars['hour_stem']}{bazi_chars['hour_branch']}"
        print(f"八字四柱: {bazi_str}")
        print(f"日主五行: {result.day_master_element}")
        print(f"日主强度: {result.day_master_strength}")
        print(f"生肖: {result.zodiac_sign}")
        
        print(f"\n=== 五行得分 ===")
        for element, score in result.five_elements_score.items():
            print(f"  {element}: {score}")
        
        print(f"\n=== 喜用神分析 ===")
        print(f"喜用神: {', '.join(result.favorable_elements)}")
        
        # 检查是否有综合分析结果
        if result.comprehensive_favorable_analysis:
            print(f"\n=== 综合分析 ===")
            comp_analysis = result.comprehensive_favorable_analysis
            if 'final_prognosis' in comp_analysis:
                final_prognosis = comp_analysis['final_prognosis']
                print(f"综合评分: {final_prognosis.get('overall_rating', 'N/A')}")
                print(f"主要喜用神: {final_prognosis.get('primary_favorable', [])}")
                print(f"次要喜用神: {final_prognosis.get('secondary_favorable', [])}")
                print(f"主要忌神: {final_prognosis.get('primary_unfavorable', [])}")
        
        print(f"\n=== 流年分析 ===")
        if result.current_year_fortune:
            current_year_fortune = result.current_year_fortune
            print(f"流年: {current_year_fortune.get('year', 'N/A')}年 {current_year_fortune.get('gan_zhi', 'N/A')}")
            print(f"流年十神: {current_year_fortune.get('ten_god_relation', 'N/A')}")
            print(f"当前大运: {current_year_fortune.get('current_dayun', 'N/A')}")
            print(f"综合评分: {current_year_fortune.get('comprehensive_rating', 'N/A')}")
            
            # 检查特殊组合
            if 'special_combinations' in current_year_fortune:
                special_combinations = current_year_fortune['special_combinations']
                print(f"\n=== 特殊组合分析 ===")
                print(f"岁运并临: {special_combinations.get('sui_yun_bing_lin', False)}")
                print(f"天克地冲: {special_combinations.get('tian_ke_di_chong', False)}")
                print(f"岁运相冲: {special_combinations.get('sui_yun_xiang_chong', False)}")
                
                favorable_combinations = special_combinations.get('favorable_combinations', [])
                if favorable_combinations:
                    print(f"\n有利组合:")
                    for i, combo in enumerate(favorable_combinations, 1):
                        print(f"  {i}. {combo}")
                
                special_warnings = special_combinations.get('special_warnings', [])
                if special_warnings:
                    print(f"\n特殊警示:")
                    for i, warning in enumerate(special_warnings, 1):
                        print(f"  {i}. {warning}")
                
                # 检查新增的个性化分析
                personalized_insights = special_combinations.get('personalized_insights', [])
                if personalized_insights:
                    print(f"\n个性化洞察:")
                    for i, insight in enumerate(personalized_insights, 1):
                        print(f"  {i}. {insight}")
                
                timing_analysis = special_combinations.get('timing_analysis', [])
                if timing_analysis:
                    print(f"\n时机分析:")
                    for i, timing in enumerate(timing_analysis, 1):
                        print(f"  {i}. {timing}")
                
                risk_assessment = special_combinations.get('risk_assessment', [])
                if risk_assessment:
                    print(f"\n风险评估:")
                    for i, risk in enumerate(risk_assessment, 1):
                        print(f"  {i}. {risk}")
                
                critical_analysis = special_combinations.get('critical_analysis', '')
                if critical_analysis:
                    print(f"\n关键分析: {critical_analysis}")
            
            # 检查预测事件
            if 'predicted_events' in current_year_fortune:
                predicted_events = current_year_fortune['predicted_events']
                print(f"\n=== 详细预测事件 ===")
                
                for category, events in predicted_events.items():
                    if events:
                        print(f"\n{category.upper()}:")
                        for i, event in enumerate(events, 1):
                            print(f"  {i}. {event}")
            
            # 检查流年互动
            if 'liunian_interactions' in current_year_fortune:
                interactions = current_year_fortune['liunian_interactions']
                print(f"\n=== 流年互动分析 ===")
                print(f"整体评估: {interactions.get('overall_assessment', 'N/A')}")
                
                harmonies = interactions.get('harmonies', [])
                if harmonies:
                    print(f"和合关系: {', '.join(harmonies)}")
                
                conflicts = interactions.get('conflicts', [])
                if conflicts:
                    print(f"冲突关系: {', '.join(conflicts)}")
                
                punishments = interactions.get('punishments', [])
                if punishments:
                    print(f"刑害关系: {', '.join(punishments)}")
                
                special_combs = interactions.get('special_combinations', [])
                if special_combs:
                    print(f"特殊组合: {', '.join(special_combs)}")
            
            # 检查流年神煞
            if 'liunian_shensha' in current_year_fortune:
                shensha_list = current_year_fortune['liunian_shensha']
                if shensha_list:
                    print(f"\n=== 流年神煞 ===")
                    for shensha in shensha_list:
                        print(f"  {shensha.get('name', 'N/A')} (位置: {shensha.get('position', 'N/A')}, 强度: {shensha.get('strength', 0):.1f})")
        
        # 保存测试结果
        result_dict = {
            "test_info": {
                "test_name": "增强版流年分析API测试",
                "test_time": datetime.now().isoformat(),
                "bazi": bazi_str,
                "day_master": result.day_master_element,
                "strength": result.day_master_strength
            },
            "five_elements_score": result.five_elements_score,
            "favorable_elements": result.favorable_elements,
            "current_year_fortune": result.current_year_fortune,
            "comprehensive_analysis": result.comprehensive_favorable_analysis
        }
        
        with open("enhanced_api_test_result.json", "w", encoding="utf-8") as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=2)
        
        print(f"\n测试结果已保存到: enhanced_api_test_result.json")
        print("✓ 增强版流年分析API测试完成")
        
        return result
        
    except Exception as e:
        print(f"API测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    try:
        print("开始增强版流年分析API测试...")
        result = asyncio.run(test_enhanced_liunian_api())
        
        if result:
            print("\n🎉 测试成功！增强版流年分析功能正常工作")
        else:
            print("\n❌ 测试失败")
            
    except Exception as e:
        print(f"测试程序异常: {e}")
        import traceback
        traceback.print_exc()
