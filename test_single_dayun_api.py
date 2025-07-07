#!/usr/bin/env python3
"""
测试单个大运分析API修正
"""

import requests
import json
from datetime import datetime

def test_single_dayun_analysis():
    """测试单个大运分析API"""
    
    # API端点
    url = "http://localhost:8000/api/v1/bazi/single-dayun-analysis"
    
    # 请求体数据
    request_data = {
        "name": "测试",
        "gender": "女", 
        "birth_datetime": "2025-07-01T09:13:01+08:00",
        "is_solar_time": True
    }
    
    # 查询参数
    params = {
        "cycle_gan_zhi": "乙酉",
        "cycle_start_year": "2045", 
        "cycle_end_year": "2054"
    }
    
    try:
        print("🚀 测试单个大运分析API...")
        print(f"请求体: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
        print(f"查询参数: {params}")
        
        response = requests.post(url, json=request_data, params=params)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            print(f"返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 检查关键字段
            if 'cycle_analysis' in result and 'trend' in result['cycle_analysis']:
                print("✅ 包含 trend 字段")
                print(f"趋势: {result['cycle_analysis']['trend']}")
            else:
                print("❌ 缺少 trend 字段")
                
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_single_dayun_analysis()
