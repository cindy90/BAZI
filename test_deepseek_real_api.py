#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试DeepSeek API连接和真实分析功能
"""

import asyncio
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_deepseek_api():
    """测试DeepSeek API连接"""
    try:
        from backend.app.services.deepseek_service import deepseek_service
        
        print("Testing DeepSeek API connection...")
        print(f"API Key configured: {bool(deepseek_service.api_key)}")
        print(f"Force mock: {deepseek_service.force_mock}")
        print(f"Base URL: {deepseek_service.base_url}")
        print(f"Model: {deepseek_service.model}")
        
        if not deepseek_service.api_key:
            print("ERROR: DeepSeek API key not found!")
            print("Please set DEEPSEEK_API_KEY environment variable")
            return
        
        # 测试简单的AI调用
        print("\n--- Testing simple AI call ---")
        
        test_bazi_data = {
            "bazi_characters": {
                "year_stem": "己", "year_branch": "巳",
                "month_stem": "丙", "month_branch": "子", 
                "day_stem": "丙", "day_branch": "寅",
                "hour_stem": "壬", "hour_branch": "辰"
            },
            "day_master_element": "火",
            "day_master_strength": "中和",
            "zodiac_sign": "蛇",
            "five_elements_score": {
                "木": "20%", "火": "25%", "土": "20%", "金": "15%", "水": "20%"
            }
        }
        
        result = await deepseek_service.generate_detailed_fortune_analysis(test_bazi_data, "2025")
        
        print(f"API call result type: {type(result)}")
        print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict) and 'career' in result:
            print(f"Career analysis: {result['career'][:100]}..." if result['career'] else "Empty")
        
        print("\nDeepSeek API test completed successfully!")
        
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_master_analysis():
    """测试命理大师级分析"""
    try:
        from backend.app.services.deepseek_service import deepseek_service
        from backend.app.services.core import Bazi, StemBranch
        from datetime import datetime
        
        print("\n--- Testing Master Fortune Analysis ---")
        
        # 创建测试八字对象
        bazi_obj = Bazi(
            year=StemBranch("己", "巳"),
            month=StemBranch("丙", "子"),
            day=StemBranch("丙", "寅"),
            hour=StemBranch("壬", "辰"),
            gender="女",
            birth_time=datetime(1990, 4, 29, 10, 30)
        )
        
        analysis_data = {
            "day_master_strength": "中和",
            "day_master_element": "火",
            "five_elements_score": {"木": "20%", "火": "25%", "土": "20%", "金": "15%", "水": "20%"},
            "zodiac_sign": "蛇",
            "major_cycles": [],
            "palace_info": {}
        }
        
        result = await deepseek_service.generate_master_fortune_analysis(bazi_obj, analysis_data, 2025)
        
        print(f"Master analysis result type: {type(result)}")
        if isinstance(result, dict):
            print(f"Analysis sections: {list(result.keys())}")
            
            if 'overall_fortune' in result:
                overall = result['overall_fortune']
                print(f"\nOverall fortune summary: {overall.get('summary', 'N/A')}")
                print(f"Score: {overall.get('score', 'N/A')}")
        
        print("Master analysis test completed!")
        
    except Exception as e:
        print(f"Master analysis test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_deepseek_api())
    asyncio.run(test_master_analysis())
