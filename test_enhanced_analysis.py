#!/usr/bin/env python3
"""
测试增强分析功能
"""
import asyncio
import aiohttp
import json
from datetime import datetime

async def test_enhanced_analysis():
    """测试增强的流年分析功能"""
    
    # 测试数据
    test_data = {
        "name": "测试用户",
        "gender": "男",
        "birth_datetime": "1990-05-15T14:30:00+08:00",
        "is_solar_time": True,
        "birth_place": "北京",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "timezone_offset": 8.0
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            print("🔍 开始测试增强分析功能...")
            
            # 发送请求
            async with session.post(
                "http://localhost:8000/api/v1/bazi/calculate",
                json=test_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ 请求成功！")
                    
                    # 检查流年运势结果
                    if "current_year_fortune" in result:
                        current_year_fortune = result["current_year_fortune"]
                        print(f"\n📅 {current_year_fortune.get('year', 'N/A')}年运势分析:")
                        print(f"   流年干支: {current_year_fortune.get('gan_zhi', 'N/A')}")
                        print(f"   当前年龄: {current_year_fortune.get('age', 'N/A')}")
                        print(f"   流年十神: {current_year_fortune.get('ten_god', 'N/A')}")
                        
                        # 检查特殊组合分析
                        special_combinations = current_year_fortune.get("special_combinations", {})
                        if special_combinations:
                            print("\n🔮 特殊组合分析:")
                            for key, values in special_combinations.items():
                                if values and isinstance(values, list):
                                    print(f"   {key}:")
                                    for value in values[:3]:  # 显示前3个
                                        print(f"     - {value}")
                        
                        # 检查预测事件
                        predicted_events = current_year_fortune.get("predicted_events", {})
                        if predicted_events:
                            print("\n📊 预测事件:")
                            for category, events in predicted_events.items():
                                if events and isinstance(events, list):
                                    print(f"   {category}:")
                                    for event in events[:2]:  # 显示前2个
                                        print(f"     - {event}")
                        
                        # 检查神煞分析
                        shensha_analysis = current_year_fortune.get("shensha_analysis", [])
                        if shensha_analysis:
                            print(f"\n🌟 神煞分析: 共{len(shensha_analysis)}个")
                            for shensha in shensha_analysis[:3]:  # 显示前3个
                                print(f"   - {shensha.get('name', 'N/A')}: {shensha.get('description', 'N/A')}")
                        
                        # 检查互动分析
                        interactions = current_year_fortune.get("interactions", {})
                        if interactions:
                            print(f"\n🔄 互动分析:")
                            for key, value in interactions.items():
                                if value:
                                    print(f"   {key}: {value}")
                                    
                        print("\n✅ 增强分析功能测试完成！")
                        
                    else:
                        print("❌ 未找到current_year_fortune字段")
                        
                else:
                    error_text = await response.text()
                    print(f"❌ 请求失败: {response.status}")
                    print(f"错误信息: {error_text}")
                    
        except Exception as e:
            print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_analysis())
