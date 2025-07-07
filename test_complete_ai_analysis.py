#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整的DeepSeek AI命理分析功能
"""

import requests
import json

def test_complete_master_analysis():
    """测试完整的命理大师级分析"""
    
    url = "http://localhost:8000/api/v1/bazi/master-fortune-analysis"
    
    data = {
        "name": "王小明",
        "gender": "男",
        "birth_datetime": "1985-06-15T14:30:00+08:00",
        "is_solar_time": True,
        "birth_place": "上海市"
    }
    
    try:
        print("=== Testing Complete Master Fortune Analysis ===")
        
        response = requests.post(url, json=data, params={"target_year": 2025})
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis Type: {result.get('analysis_type')}")
            
            if 'fortune_analysis' in result:
                fortune = result['fortune_analysis']
                
                print("\n🔮 Complete Analysis Structure:")
                for section, content in fortune.items():
                    print(f"\n📋 {section.upper()}:")
                    if isinstance(content, dict):
                        for key, value in content.items():
                            if isinstance(value, list):
                                print(f"  • {key}: {', '.join(value)}")
                            else:
                                print(f"  • {key}: {value}")
                    else:
                        print(f"  {content}")
                
                # 检查关键分析模块
                required_sections = [
                    'overall_fortune', 'career_analysis', 'wealth_analysis',
                    'relationship_analysis', 'health_analysis', 'conclusion'
                ]
                
                missing_sections = [s for s in required_sections if s not in fortune]
                if missing_sections:
                    print(f"\n⚠️ Missing sections: {missing_sections}")
                else:
                    print(f"\n✅ All required sections present!")
                
                # 输出AI分析质量评估
                if 'overall_fortune' in fortune:
                    summary_length = len(fortune['overall_fortune'].get('summary', ''))
                    print(f"\n📊 Analysis Quality Metrics:")
                    print(f"  • Summary length: {summary_length} characters")
                    print(f"  • Score provided: {fortune['overall_fortune'].get('score', 'N/A')}")
                    
                    if summary_length > 50:
                        print("  ✅ AI generated substantial content")
                    else:
                        print("  ⚠️ AI content seems brief")
            
            else:
                print("❌ No fortune_analysis in response")
                print(f"Response keys: {list(result.keys())}")
                
        else:
            print(f"❌ API failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_dayun_deep_analysis():
    """测试大运深度分析"""
    
    url = "http://localhost:8000/api/v1/bazi/dayun-deep-analysis"
    
    request_data = {
        "name": "李小华",
        "gender": "女",
        "birth_datetime": "1992-03-10T09:15:00+08:00",
        "is_solar_time": True
    }
    
    params = {
        "dayun_gan_zhi": "戊戌",
        "start_age": 25,
        "end_age": 35
    }
    
    try:
        print("\n=== Testing Dayun Deep Analysis ===")
        
        response = requests.post(url, json=request_data, params=params)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis Success: {result.get('success')}")
            
            if 'dayun_analysis' in result:
                analysis = result['dayun_analysis']
                print(f"\n🔄 Dayun Analysis Sections: {list(analysis.keys())}")
                
                if 'cycle_overview' in analysis:
                    overview = analysis['cycle_overview']
                    print(f"\n📈 Cycle Overview:")
                    print(f"  • Nature: {overview.get('nature', 'N/A')}")
                    print(f"  • Theme: {overview.get('theme', 'N/A')}")
                    print(f"  • Trend: {overview.get('overall_trend', 'N/A')}")
                
                print("✅ Dayun deep analysis working!")
            else:
                print(f"❌ Missing dayun_analysis: {list(result.keys())}")
                if 'error' in result:
                    print(f"Error: {result['error']}")
                
        else:
            print(f"❌ API failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_complete_master_analysis()
    test_dayun_deep_analysis()
