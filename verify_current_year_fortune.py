#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证current_year_fortune字段的返回情况
"""
import requests
import json
import sys

def test_current_year_fortune():
    """测试current_year_fortune字段"""
    url = "http://localhost:8000/api/v1/bazi/test-full-response"
    
    data = {
        "birth_datetime": "1990-04-29T10:30:00",
        "gender": "男",
        "birth_place": "北京"
    }
    
    try:
        print("🚀 发送API请求...")
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API请求成功")
            
            # 检查current_year_fortune字段
            if "current_year_fortune" in result:
                current_year_fortune = result["current_year_fortune"]
                print("✅ current_year_fortune 字段存在")
                print(f"   年份: {current_year_fortune.get('year', 'N/A')}")
                print(f"   干支: {current_year_fortune.get('gan_zhi', 'N/A')}")
                print(f"   分析: {current_year_fortune.get('analysis', 'N/A')}")
                
                # 检查detailed_analysis
                if "detailed_analysis" in current_year_fortune:
                    detailed = current_year_fortune["detailed_analysis"]
                    print("✅ detailed_analysis 字段存在")
                    print(f"   整体运势: {detailed.get('overall_fortune', 'N/A')[:50]}...")
                    print(f"   事业财运: {detailed.get('career_wealth', 'N/A')}")
                    print(f"   感情婚姻: {detailed.get('love_marriage', 'N/A')}")
                    print(f"   健康方面: {detailed.get('health', 'N/A')}")
                else:
                    print("❌ detailed_analysis 字段缺失")
                
                # 检查special_combinations
                if "special_combinations" in current_year_fortune:
                    print("✅ special_combinations 字段存在")
                else:
                    print("❌ special_combinations 字段缺失")
                
                # 保存完整结果到文件
                with open("current_year_fortune_result.json", "w", encoding="utf-8") as f:
                    json.dump(current_year_fortune, f, ensure_ascii=False, indent=2)
                print("📁 完整结果已保存到 current_year_fortune_result.json")
                
            else:
                print("❌ current_year_fortune 字段缺失")
                # 列出所有可用字段
                print("可用字段:")
                for key in result.keys():
                    print(f"  - {key}")
                    
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("验证 current_year_fortune 字段")
    print("=" * 50)
    test_current_year_fortune()
    print("=" * 50)
    print("验证完成")
    print("=" * 50)
