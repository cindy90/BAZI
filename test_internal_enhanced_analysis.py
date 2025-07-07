#!/usr/bin/env python3
"""
测试增强分析功能的内部逻辑
"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest

async def test_internal_enhanced_analysis():
    """测试内部增强分析逻辑"""
    print("🔍 开始测试内部增强分析功能...")
    
    # 创建测试请求
    test_request = BaziCalculateRequest(
        name="测试用户",
        gender="男",
        birth_datetime=datetime(1990, 5, 15, 14, 30, 0),
        is_solar_time=True,
        birth_place="北京",
        longitude=116.4074,
        latitude=39.9042,
        timezone_offset=8.0
    )
    
    try:
        # 调用计算函数
        result = await calculate_bazi_data(test_request)
        print("✅ 计算成功！")
        
        # 检查 current_year_fortune 字段
        if hasattr(result, 'current_year_fortune') and result.current_year_fortune:
            current_year_fortune = result.current_year_fortune
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
                    
            print("\n✅ 增强分析功能测试完成！")
            
        else:
            print("❌ 未找到current_year_fortune字段")
            print("当前结果字段包含：", [attr for attr in dir(result) if not attr.startswith('_')])
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_internal_enhanced_analysis())
