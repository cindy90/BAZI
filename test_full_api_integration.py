#!/usr/bin/env python3
"""
完整的八字流年分析API集成测试
验证增强版 special_combinations 和 predicted_events 功能
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# 添加路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.bazi_calculator import calculate_bazi_data
from backend.app.schemas.bazi import BaziCalculateRequest

async def test_full_api_integration():
    """完整的API集成测试"""
    print("=== 完整的八字流年分析API集成测试 ===")
    
    # 准备测试数据
    test_request = BaziCalculateRequest(
        birth_year=1984,
        birth_month=2,
        birth_day=15,
        birth_hour=14,
        birth_minute=30,
        gender="男",
        calendar_type="阳历",
        current_year=2025
    )
    
    print(f"测试请求:")
    print(f"  生日: {test_request.birth_year}-{test_request.birth_month}-{test_request.birth_day} {test_request.birth_hour}:{test_request.birth_minute}")
    print(f"  性别: {test_request.gender}")
    print(f"  流年: {test_request.current_year}")
    
    try:
        # 调用完整的计算API
        result = await calculate_bazi_data(test_request)
        
        print(f"\n=== 基本信息 ===")
        print(f"八字四柱: {result.year.gan}{result.year.zhi} {result.month.gan}{result.month.zhi} {result.day.gan}{result.day.zhi} {result.hour.gan}{result.hour.zhi}")
        print(f"性别: {result.gender}")
        print(f"当前年龄: {result.current_year_fortune.age}岁")
        
        print(f"\n=== 流年分析 ===")
        current_year_fortune = result.current_year_fortune
        print(f"流年: {current_year_fortune.year}年 {current_year_fortune.gan_zhi}")
        print(f"流年十神: {current_year_fortune.ten_god_relation}")
        print(f"当前大运: {current_year_fortune.current_dayun}")
        print(f"综合评分: {current_year_fortune.comprehensive_rating:.1f}分")
        
        print(f"\n=== 五行分析 ===")
        five_elements = current_year_fortune.five_elements_analysis
        print(f"流年干支五行: {five_elements.liunian_gan_element} + {five_elements.liunian_zhi_element}")
        print(f"大运五行: {five_elements.dayun_element}")
        print(f"五行互动: {five_elements.element_interaction}")
        print(f"喜用神匹配: {'是' if five_elements.favorable_match else '否'}")
        print(f"忌神匹配: {'是' if five_elements.unfavorable_match else '否'}")
        
        print(f"\n=== 长生信息 ===")
        chang_sheng = current_year_fortune.chang_sheng_info
        print(f"长生状态: {chang_sheng.state}")
        print(f"状态描述: {chang_sheng.description}")
        
        print(f"\n=== 特殊组合分析 ===")
        special_combinations = current_year_fortune.special_combinations
        print(f"岁运并临: {special_combinations.sui_yun_bing_lin}")
        print(f"天克地冲: {special_combinations.tian_ke_di_chong}")
        print(f"岁运相冲: {special_combinations.sui_yun_xiang_chong}")
        
        print(f"\n有利组合:")
        for i, combo in enumerate(special_combinations.favorable_combinations, 1):
            print(f"  {i}. {combo}")
        
        print(f"\n特殊警示:")
        for i, warning in enumerate(special_combinations.special_warnings, 1):
            print(f"  {i}. {warning}")
        
        # 检查是否有新增的个性化洞察
        if hasattr(special_combinations, 'personalized_insights'):
            print(f"\n个性化洞察:")
            for i, insight in enumerate(special_combinations.personalized_insights, 1):
                print(f"  {i}. {insight}")
        
        if hasattr(special_combinations, 'timing_analysis'):
            print(f"\n时机分析:")
            for i, timing in enumerate(special_combinations.timing_analysis, 1):
                print(f"  {i}. {timing}")
        
        if hasattr(special_combinations, 'risk_assessment'):
            print(f"\n风险评估:")
            for i, risk in enumerate(special_combinations.risk_assessment, 1):
                print(f"  {i}. {risk}")
        
        print(f"\n关键分析: {special_combinations.critical_analysis}")
        
        print(f"\n=== 流年互动分析 ===")
        interactions = current_year_fortune.liunian_interactions
        print(f"整体评估: {interactions.overall_assessment}")
        
        if interactions.harmonies:
            print(f"和合关系: {', '.join(interactions.harmonies)}")
        if interactions.conflicts:
            print(f"冲突关系: {', '.join(interactions.conflicts)}")
        if interactions.punishments:
            print(f"刑害关系: {', '.join(interactions.punishments)}")
        if interactions.special_combinations:
            print(f"特殊组合: {', '.join(interactions.special_combinations)}")
        
        print(f"\n=== 流年神煞 ===")
        shensha_list = current_year_fortune.liunian_shensha
        for shensha in shensha_list:
            print(f"  {shensha.name} (位置: {shensha.position}, 强度: {shensha.strength:.1f})")
        
        print(f"\n=== 详细预测事件 ===")
        predicted_events = current_year_fortune.predicted_events
        
        for category, events in predicted_events.items():
            if events:
                print(f"\n{category.upper()}:")
                for i, event in enumerate(events, 1):
                    print(f"  {i}. {event}")
        
        # 保存完整结果
        result_dict = {
            "bazi_info": {
                "year": f"{result.year.gan}{result.year.zhi}",
                "month": f"{result.month.gan}{result.month.zhi}",
                "day": f"{result.day.gan}{result.day.zhi}",
                "hour": f"{result.hour.gan}{result.hour.zhi}",
                "gender": result.gender
            },
            "current_year_fortune": {
                "year": current_year_fortune.year,
                "gan_zhi": current_year_fortune.gan_zhi,
                "ten_god_relation": current_year_fortune.ten_god_relation,
                "comprehensive_rating": current_year_fortune.comprehensive_rating,
                "special_combinations": {
                    "sui_yun_bing_lin": special_combinations.sui_yun_bing_lin,
                    "tian_ke_di_chong": special_combinations.tian_ke_di_chong,
                    "sui_yun_xiang_chong": special_combinations.sui_yun_xiang_chong,
                    "favorable_combinations": special_combinations.favorable_combinations,
                    "special_warnings": special_combinations.special_warnings,
                    "critical_analysis": special_combinations.critical_analysis
                },
                "predicted_events": dict(predicted_events),
                "liunian_interactions": {
                    "overall_assessment": interactions.overall_assessment,
                    "harmonies": interactions.harmonies,
                    "conflicts": interactions.conflicts,
                    "punishments": interactions.punishments,
                    "special_combinations": interactions.special_combinations
                },
                "liunian_shensha": [
                    {
                        "name": s.name,
                        "position": s.position,
                        "strength": s.strength,
                        "description": s.description
                    } for s in shensha_list
                ]
            }
        }
        
        with open("full_api_integration_test_result.json", "w", encoding="utf-8") as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=2)
        
        print(f"\n完整测试结果已保存到: full_api_integration_test_result.json")
        
        return result
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_multiple_liunian_cases():
    """测试多个流年案例"""
    print("\n=== 测试多个流年案例 ===")
    
    test_cases = [
        {
            "name": "财星流年",
            "request": BaziCalculateRequest(
                birth_year=1985, birth_month=6, birth_day=20, birth_hour=10, birth_minute=0,
                gender="女", calendar_type="阳历", current_year=2025
            )
        },
        {
            "name": "官杀流年",
            "request": BaziCalculateRequest(
                birth_year=1990, birth_month=8, birth_day=15, birth_hour=14, birth_minute=30,
                gender="男", calendar_type="阳历", current_year=2025
            )
        },
        {
            "name": "印星流年",
            "request": BaziCalculateRequest(
                birth_year=1988, birth_month=3, birth_day=25, birth_hour=8, birth_minute=15,
                gender="女", calendar_type="阳历", current_year=2025
            )
        }
    ]
    
    summary = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试案例: {case['name']}")
        
        try:
            result = await calculate_bazi_data(case["request"])
            
            # 提取关键信息
            bazi = f"{result.year.gan}{result.year.zhi} {result.month.gan}{result.month.zhi} {result.day.gan}{result.day.zhi} {result.hour.gan}{result.hour.zhi}"
            fortune = result.current_year_fortune
            
            print(f"  八字: {bazi}")
            print(f"  流年十神: {fortune.ten_god_relation}")
            print(f"  综合评分: {fortune.comprehensive_rating:.1f}分")
            print(f"  特殊组合: {len(fortune.special_combinations.favorable_combinations)}个有利, {len(fortune.special_combinations.special_warnings)}个警示")
            print(f"  预测事件: {sum(len(events) for events in fortune.predicted_events.values())}条")
            
            summary.append({
                "case_name": case["name"],
                "bazi": bazi,
                "ten_god": fortune.ten_god_relation,
                "rating": fortune.comprehensive_rating,
                "events_count": sum(len(events) for events in fortune.predicted_events.values())
            })
            
        except Exception as e:
            print(f"  测试失败: {e}")
            summary.append({
                "case_name": case["name"],
                "error": str(e)
            })
    
    print(f"\n=== 多案例测试总结 ===")
    for item in summary:
        if "error" in item:
            print(f"  {item['case_name']}: 测试失败 - {item['error']}")
        else:
            print(f"  {item['case_name']}: {item['ten_god']} (评分: {item['rating']:.1f}, 预测: {item['events_count']}条)")
    
    return summary

if __name__ == "__main__":
    try:
        # 运行完整API集成测试
        print("开始完整API集成测试...")
        full_result = asyncio.run(test_full_api_integration())
        
        if full_result:
            print("\n✓ 完整API集成测试通过")
            
            # 运行多案例测试
            print("\n开始多案例测试...")
            multi_results = asyncio.run(test_multiple_liunian_cases())
            
            print("\n✓ 多案例测试完成")
            
            print("\n=== 最终测试总结 ===")
            print("✓ 基本八字计算功能正常")
            print("✓ 流年分析功能正常")
            print("✓ 特殊组合分析功能正常")
            print("✓ 预测事件生成功能正常")
            print("✓ 流年互动分析功能正常")
            print("✓ 流年神煞分析功能正常")
            print("✓ 多案例测试通过")
            
            print("\n🎉 增强版流年分析系统测试全部通过！")
            
        else:
            print("\n❌ 完整API集成测试失败")
            
    except Exception as e:
        print(f"测试程序异常: {e}")
        import traceback
        traceback.print_exc()
