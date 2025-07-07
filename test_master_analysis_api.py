#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的命理大师级分析功能
"""

import requests
import json

def test_master_fortune_analysis():
    """测试命理大师级全面运势分析"""
    
    url = "http://localhost:8000/api/v1/bazi/master-fortune-analysis"
    
    data = {
        "name": "测试用户",
        "gender": "女",
        "birth_datetime": "1990-04-29T10:30:00+08:00",
        "is_solar_time": True,
        "birth_place": "北京市",
        "target_year": 2025
    }
    
    try:
        print("Testing master fortune analysis...")
        
        response = requests.post(url, json=data, params={"target_year": 2025})
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("API call successful!")
            print(f"Analysis type: {result.get('analysis_type', 'unknown')}")
            
            if 'fortune_analysis' in result:
                fortune = result['fortune_analysis']
                
                if 'overall_fortune' in fortune:
                    overall = fortune['overall_fortune']
                    print(f"Overall fortune summary: {overall.get('summary', '')}")
                    print(f"Score: {overall.get('score', '')} points")
                
                print("Master analysis structure complete!")
            else:
                print("Missing fortune_analysis field")
                
        else:
            print(f"API call failed: {response.status_code}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_master_fortune_analysis()

def test_dayun_deep_analysis():
    """测试大运深度分析"""
    
    url = "http://localhost:8000/api/v1/bazi/dayun-deep-analysis"
    
    # 请求体数据
    request_data = {
        "name": "测试用户",
        "gender": "女",
        "birth_datetime": "1990-04-29T10:30:00+08:00",
        "is_solar_time": True
    }
    
    # 查询参数
    params = {
        "dayun_gan_zhi": "乙酉",
        "start_age": 20,
        "end_age": 30
    }
    
    try:
        print("\n🔮 测试大运深度分析...")
        print(f"请求体: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
        print(f"查询参数: {params}")
        
        response = requests.post(url, json=request_data, params=params)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            print(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if 'dayun_analysis' in result:
                analysis = result['dayun_analysis']
                
                if 'cycle_overview' in analysis:
                    overview = analysis['cycle_overview']
                    print(f"\n📈 大运概览:")
                    print(f"  性质: {overview.get('nature', '')}")
                    print(f"  主题: {overview.get('theme', '')}")
                    print(f"  趋势: {overview.get('overall_trend', '')}")
                
                if 'phase_analysis' in analysis:
                    phases = analysis['phase_analysis']
                    print(f"\n📅 阶段分析:")
                    for phase_name, phase_data in phases.items():
                        print(f"  {phase_name}: {phase_data.get('period', '')} - {phase_data.get('characteristics', '')}")
                
                print("\n✅ 大运深度分析结构完整！")
            else:
                print("❌ 缺少dayun_analysis字段")
                
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_master_fortune_analysis()
    test_dayun_deep_analysis()
