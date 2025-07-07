#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys

def test_bazi_api():
    """测试修复后的八字计算API"""
    url = "http://localhost:8000/api/v1/bazi/test-calculate"
    
    data = {
        "birth_datetime": "1990-04-29T10:30:00",
        "gender": "男",
        "birth_place": "北京"
    }
    
    print(f"🚀 测试API: {url}")
    print(f"📝 请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            
            # 检查关键字段
            key_fields = [
                "bazi_characters", "major_cycles", "current_year_fortune", 
                "na_yin", "palace_info", "five_elements_score"
            ]
            
            print("\n🔍 关键字段检查:")
            for field in key_fields:
                if field in result:
                    print(f"  ✅ {field}: 存在")
                    if field == "major_cycles" and isinstance(result[field], list):
                        print(f"      - 大运数量: {len(result[field])}")
                    elif field == "current_year_fortune" and isinstance(result[field], dict):
                        print(f"      - 流年: {result[field].get('year', 'N/A')}")
                        print(f"      - 干支: {result[field].get('gan_zhi', 'N/A')}")
                    elif field == "na_yin" and isinstance(result[field], dict):
                        print(f"      - 纳音字段数: {len(result[field])}")
                    elif field == "palace_info" and isinstance(result[field], dict):
                        print(f"      - 宫位字段数: {len(result[field])}")
                else:
                    print(f"  ❌ {field}: 缺失")
            
            # 保存详细结果
            with open("test_fixed_api_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n📁 详细结果已保存到: test_fixed_api_result.json")
            
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误详情: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"💥 网络请求失败: {e}")
    except Exception as e:
        print(f"💥 未知错误: {e}")

if __name__ == "__main__":
    test_bazi_api()
