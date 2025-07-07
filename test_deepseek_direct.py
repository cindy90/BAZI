#!/usr/bin/env python3
"""
完整测试DeepSeek服务和新的Prompt系统
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_deepseek_service():
    """测试DeepSeek服务本身"""
    try:
        from backend.app.services.deepseek_service import deepseek_service
        from backend.app.services.core import Bazi, StemBranch
        from datetime import datetime
        
        print("Successfully imported DeepSeek service")
        print(f"Force mock mode: {deepseek_service.force_mock}")
        
        # 创建测试八字对象
        bazi_obj = Bazi(
            year=StemBranch("己", "巳"),
            month=StemBranch("丙", "子"),
            day=StemBranch("丙", "寅"),
            hour=StemBranch("壬", "辰"),
            gender="女",
            birth_time=datetime(1990, 4, 29, 10, 30)
        )
        
        # 测试数据
        analysis_data = {
            "day_master_strength": "中和",
            "day_master_element": "火",
            "five_elements_score": {"木": "20%", "火": "25%", "土": "20%", "金": "15%", "水": "20%"},
            "major_cycles": [],
            "zodiac_sign": "马",
            "palace_info": {}
        }
        
        print("\nTesting master fortune analysis...")
        import asyncio
        
        # 测试大师级分析
        result = asyncio.run(deepseek_service.generate_master_fortune_analysis(
            bazi_obj, analysis_data, 2025
        ))
        
        print(f"Master analysis result keys: {list(result.keys())}")
        
        if 'overall_fortune' in result:
            print("Overall fortune structure found!")
            print(f"Summary: {result['overall_fortune'].get('summary', '')}")
            
        if 'career_analysis' in result:
            print("Career analysis structure found!")
            
        print("\nDeepSeek service test completed successfully!")
        
    except Exception as e:
        print(f"DeepSeek service test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_deepseek_service()
