#!/usr/bin/env python3
"""
测试增强版流年分析功能
验证 special_combinations 和 predicted_events 的优化效果
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app.services.bazi_calculator import calculate_bazi_data
from backend.app.schemas.bazi import BaziCalculateRequest
from datetime import datetime
import json

def test_enhanced_liunian_analysis():
    """测试增强版流年分析功能"""
    print("=== 测试增强版流年分析功能 ===\n")
    
    # 测试用例1: 男命 1990-06-15 10:30
    test_case_1 = {
        "birth_year": 1990,
        "birth_month": 6,
        "birth_day": 15,
        "birth_hour": 10,
        "birth_minute": 30,
        "gender": "男",
        "current_year": 2025,
        "name": "测试案例1"
    }
    
    # 测试用例2: 女命 1985-03-22 14:45
    test_case_2 = {
        "birth_year": 1985,
        "birth_month": 3,
        "birth_day": 22,
        "birth_hour": 14,
        "birth_minute": 45,
        "gender": "女",
        "current_year": 2025,
        "name": "测试案例2"
    }
    
    test_cases = [test_case_1, test_case_2]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"测试案例 {i}: {test_case['name']}")
        print(f"生日: {test_case['birth_year']}-{test_case['birth_month']}-{test_case['birth_day']} {test_case['birth_hour']}:{test_case['birth_minute']}")
        print(f"性别: {test_case['gender']}")
        print(f"流年: {test_case['current_year']}")
        print(f"{'='*50}")
        
        try:
            # 创建请求对象
            request = BaziCalculateRequest(**test_case)
            
            # 计算八字数据
            result = calculate_bazi_data(request)
            
            if result:
                print(f"\n✓ 八字计算成功")
                print(f"四柱: {result.year_pillar} {result.month_pillar} {result.day_pillar} {result.hour_pillar}")
                print(f"当前年龄: {result.current_age}")
                print(f"当前大运: {result.current_dayun}")
                
                # 重点测试流年分析
                current_year_fortune = result.current_year_fortune
                print(f"\n--- 流年分析 ({current_year_fortune['year']}年{current_year_fortune['gan_zhi']}) ---")
                print(f"流年十神: {current_year_fortune['ten_god_relation']}")
                print(f"长生状态: {current_year_fortune['chang_sheng_info']['state']}")
                print(f"综合评分: {current_year_fortune['comprehensive_rating']:.1f}")
                
                # 测试特殊组合分析
                special_combinations = current_year_fortune.get("special_combinations", {})
                print(f"\n--- 特殊组合分析 ---")
                print(f"岁运并临: {special_combinations.get('sui_yun_bing_lin', False)}")
                print(f"天克地冲: {special_combinations.get('tian_ke_di_chong', False)}")
                print(f"岁运相冲: {special_combinations.get('sui_yun_xiang_chong', False)}")
                
                print(f"\n有利组合 ({len(special_combinations.get('favorable_combinations', []))}):")
                for combo in special_combinations.get('favorable_combinations', []):
                    print(f"  • {combo}")
                
                print(f"\n特殊警示 ({len(special_combinations.get('special_warnings', []))}):")
                for warning in special_combinations.get('special_warnings', []):
                    print(f"  • {warning}")
                
                # 新增字段测试
                if 'personalized_insights' in special_combinations:
                    print(f"\n个性化洞察 ({len(special_combinations['personalized_insights'])}):")
                    for insight in special_combinations['personalized_insights']:
                        print(f"  • {insight}")
                
                if 'timing_analysis' in special_combinations:
                    print(f"\n时机分析 ({len(special_combinations['timing_analysis'])}):")
                    for timing in special_combinations['timing_analysis']:
                        print(f"  • {timing}")
                
                if 'risk_assessment' in special_combinations:
                    print(f"\n风险评估 ({len(special_combinations['risk_assessment'])}):")
                    for risk in special_combinations['risk_assessment']:
                        print(f"  • {risk}")
                
                # 测试预测事件
                predicted_events = current_year_fortune.get("predicted_events", {})
                print(f"\n--- 预测事件 ---")
                
                categories = ["career", "wealth", "health", "relationship", "timing", "strategy", "warning"]
                for category in categories:
                    if category in predicted_events:
                        events = predicted_events[category]
                        print(f"\n{category.upper()} ({len(events)}):")
                        for event in events:
                            print(f"  • {event}")
                
                # 测试流年互动分析
                liunian_interactions = current_year_fortune.get("liunian_interactions", {})
                print(f"\n--- 流年互动分析 ---")
                print(f"整体评估: {liunian_interactions.get('overall_assessment', '未知')}")
                
                if liunian_interactions.get('conflicts'):
                    print(f"冲突 ({len(liunian_interactions['conflicts'])}):")
                    for conflict in liunian_interactions['conflicts']:
                        print(f"  • {conflict}")
                
                if liunian_interactions.get('harmonies'):
                    print(f"和谐 ({len(liunian_interactions['harmonies'])}):")
                    for harmony in liunian_interactions['harmonies']:
                        print(f"  • {harmony}")
                
                if liunian_interactions.get('special_combinations'):
                    print(f"特殊组合 ({len(liunian_interactions['special_combinations'])}):")
                    for combo in liunian_interactions['special_combinations']:
                        print(f"  • {combo}")
                
                # 测试流年神煞
                liunian_shensha = current_year_fortune.get("liunian_shensha", [])
                print(f"\n--- 流年神煞 ({len(liunian_shensha)}) ---")
                for shensha in liunian_shensha:
                    print(f"  • {shensha['name']}: {shensha['description']}")
                    if shensha.get('positive_tags'):
                        print(f"    正面标签: {', '.join(shensha['positive_tags'])}")
                    if shensha.get('negative_tags'):
                        print(f"    负面标签: {', '.join(shensha['negative_tags'])}")
                
                print(f"\n✅ 案例 {i} 分析完成")
                
            else:
                print(f"\n❌ 案例 {i} 计算失败")
                
        except Exception as e:
            print(f"\n❌ 案例 {i} 出错: {e}")
            import traceback
            traceback.print_exc()

def save_test_results():
    """保存测试结果到文件"""
    print("\n=== 保存测试结果 ===")
    
    test_case = {
        "birth_year": 1990,
        "birth_month": 6,
        "birth_day": 15,
        "birth_hour": 10,
        "birth_minute": 30,
        "gender": "男",
        "current_year": 2025,
        "name": "详细测试案例"
    }
    
    try:
        request = BaziCalculateRequest(**test_case)
        result = calculate_bazi_data(request)
        
        if result:
            # 提取关键信息
            test_result = {
                "basic_info": {
                    "四柱": f"{result.year_pillar} {result.month_pillar} {result.day_pillar} {result.hour_pillar}",
                    "当前年龄": result.current_age,
                    "当前大运": result.current_dayun,
                    "流年": f"{result.current_year_fortune['year']}年{result.current_year_fortune['gan_zhi']}"
                },
                "current_year_fortune": result.current_year_fortune,
                "comprehensive_analysis": result.comprehensive_favorable_analysis,
                "test_timestamp": datetime.now().isoformat()
            }
            
            # 保存到文件
            filename = f"enhanced_liunian_analysis_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(test_result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 测试结果已保存到: {filename}")
            
        else:
            print("❌ 计算失败，无法保存结果")
            
    except Exception as e:
        print(f"❌ 保存测试结果时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_liunian_analysis()
    save_test_results()
    print("\n=== 测试完成 ===")
