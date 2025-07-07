#!/usr/bin/env python3
"""
直接测试增强版流年分析API
"""
import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api/v1"

def test_enhanced_liunian_api():
    """测试增强版流年分析API"""
    print("=== 测试增强版流年分析API ===\n")
    
    # 测试数据
    test_data = {
        "birth_year": 1990,
        "birth_month": 6,
        "birth_day": 15,
        "birth_hour": 10,
        "birth_minute": 30,
        "gender": "男",
        "current_year": 2025,
        "name": "测试用户"
    }
    
    try:
        # 发送请求
        response = requests.post(f"{API_BASE_URL}/bazi/calculate", json=test_data)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ API请求成功")
            print(f"八字: {data['year_pillar']} {data['month_pillar']} {data['day_pillar']} {data['hour_pillar']}")
            print(f"当前年龄: {data['current_age']}")
            print(f"当前大运: {data['current_dayun']}")
            
            # 测试流年分析
            current_year_fortune = data["current_year_fortune"]
            print(f"\n--- 流年分析 ({current_year_fortune['year']}年{current_year_fortune['gan_zhi']}) ---")
            print(f"流年十神: {current_year_fortune['ten_god_relation']}")
            print(f"长生状态: {current_year_fortune['chang_sheng_info']['state']}")
            
            # 测试特殊组合分析
            special_combinations = current_year_fortune["special_combinations"]
            print(f"\n--- 特殊组合分析 ---")
            print(f"有利组合数量: {len(special_combinations['favorable_combinations'])}")
            print(f"特殊警示数量: {len(special_combinations['special_warnings'])}")
            
            # 测试新增字段
            if 'personalized_insights' in special_combinations:
                print(f"个性化洞察数量: {len(special_combinations['personalized_insights'])}")
            if 'timing_analysis' in special_combinations:
                print(f"时机分析数量: {len(special_combinations['timing_analysis'])}")
            if 'risk_assessment' in special_combinations:
                print(f"风险评估数量: {len(special_combinations['risk_assessment'])}")
            
            # 展示部分内容
            print(f"\n有利组合前3条:")
            for i, combo in enumerate(special_combinations['favorable_combinations'][:3]):
                print(f"  {i+1}. {combo}")
            
            if special_combinations.get('personalized_insights'):
                print(f"\n个性化洞察前3条:")
                for i, insight in enumerate(special_combinations['personalized_insights'][:3]):
                    print(f"  {i+1}. {insight}")
            
            # 测试预测事件
            predicted_events = current_year_fortune["predicted_events"]
            print(f"\n--- 预测事件 ---")
            
            categories = ["career", "wealth", "health", "relationship", "timing", "strategy", "warning"]
            for category in categories:
                if category in predicted_events:
                    events = predicted_events[category]
                    print(f"{category.upper()}: {len(events)}条")
                    for event in events[:2]:  # 显示前2条
                        print(f"  • {event}")
            
            # 测试流年互动分析
            liunian_interactions = current_year_fortune["liunian_interactions"]
            print(f"\n--- 流年互动分析 ---")
            print(f"整体评估: {liunian_interactions['overall_assessment']}")
            print(f"冲突: {len(liunian_interactions.get('conflicts', []))}")
            print(f"和谐: {len(liunian_interactions.get('harmonies', []))}")
            print(f"特殊组合: {len(liunian_interactions.get('special_combinations', []))}")
            
            # 测试流年神煞
            liunian_shensha = current_year_fortune["liunian_shensha"]
            print(f"\n--- 流年神煞 ({len(liunian_shensha)}) ---")
            for shensha in liunian_shensha[:3]:  # 显示前3个
                print(f"  • {shensha['name']}: {shensha['description']}")
            
            # 保存完整结果
            filename = f"enhanced_liunian_api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ 完整结果已保存到: {filename}")
            return True
            
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

def test_multiple_cases():
    """测试多个案例"""
    print("\n=== 测试多个案例 ===\n")
    
    test_cases = [
        {
            "birth_year": 1985,
            "birth_month": 3,
            "birth_day": 22,
            "birth_hour": 14,
            "birth_minute": 45,
            "gender": "女",
            "current_year": 2025,
            "name": "中年女性"
        },
        {
            "birth_year": 1995,
            "birth_month": 12,
            "birth_day": 8,
            "birth_hour": 20,
            "birth_minute": 15,
            "gender": "男",
            "current_year": 2025,
            "name": "年轻男性"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"--- 案例{i}: {test_case['name']} ---")
        
        try:
            response = requests.post(f"{API_BASE_URL}/bazi/calculate", json=test_case)
            
            if response.status_code == 200:
                data = response.json()
                
                current_year_fortune = data["current_year_fortune"]
                special_combinations = current_year_fortune["special_combinations"]
                predicted_events = current_year_fortune["predicted_events"]
                
                print(f"✅ 案例{i}计算成功")
                print(f"八字: {data['year_pillar']} {data['month_pillar']} {data['day_pillar']} {data['hour_pillar']}")
                print(f"流年十神: {current_year_fortune['ten_god_relation']}")
                print(f"有利组合: {len(special_combinations['favorable_combinations'])}条")
                print(f"预测事件: 事业{len(predicted_events.get('career', []))}条, 财运{len(predicted_events.get('wealth', []))}条")
                
                # 显示一条个性化预测
                if predicted_events.get('career'):
                    print(f"事业预测示例: {predicted_events['career'][0]}")
                
            else:
                print(f"❌ 案例{i}计算失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 案例{i}出错: {e}")

def main():
    """主函数"""
    print("=== 增强版流年分析API测试 ===")
    print("测试服务器: http://localhost:8000")
    print("="*50)
    
    # 测试基本功能
    success = test_enhanced_liunian_api()
    
    if success:
        # 测试多个案例
        test_multiple_cases()
        print("\n✅ 所有测试完成")
    else:
        print("\n❌ 基本测试失败，跳过其他测试")

if __name__ == "__main__":
    main()
