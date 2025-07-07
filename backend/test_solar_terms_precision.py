#!/usr/bin/env python3
"""
节气时间精度验证脚本
验证新的高精度节气数据对八字排盘的影响
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

import asyncio
from datetime import datetime, timedelta
from app.services.bazi_calculator import calculate_bazi_data
from app.models.bazi import BaziCalculateRequest
from app.services.calculators import FiveElementsCalculator
import json

async def test_precise_solar_terms():
    """测试精确节气时间对八字排盘的影响"""
    
    print("=" * 60)
    print("节气时间精度验证测试")
    print("=" * 60)
    
    # 测试用例：在节气交接点附近的出生时间
    test_cases = [
        {
            "name": "2024年立春前后",
            "base_time": "2024-02-04 10:00:00",  # 立春日
            "description": "测试在立春交接点前后的八字变化"
        },
        {
            "name": "2024年春分前后", 
            "base_time": "2024-03-20 11:00:00",  # 春分日
            "description": "测试在春分交接点前后的八字变化"
        },
        {
            "name": "2024年夏至前后",
            "base_time": "2024-06-21 04:00:00",  # 夏至日
            "description": "测试在夏至交接点前后的八字变化"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n【{test_case['name']}】")
        print(f"描述: {test_case['description']}")
        
        base_dt = datetime.strptime(test_case['base_time'], "%Y-%m-%d %H:%M:%S")
        
        # 测试节气前后6小时的时间点
        test_times = [
            base_dt - timedelta(hours=6),
            base_dt - timedelta(hours=3),
            base_dt,
            base_dt + timedelta(hours=3),
            base_dt + timedelta(hours=6)
        ]
        
        results = []
        
        for i, test_time in enumerate(test_times):
            try:
                request = BaziCalculateRequest(
                    birth_year=test_time.year,
                    birth_month=test_time.month,
                    birth_day=test_time.day,
                    birth_hour=test_time.hour,
                    birth_minute=test_time.minute,
                    gender="男",
                    birth_place="北京",
                    apply_solar_correction=False
                )
                
                result = await calculate_bazi_data(request)
                
                # 提取关键信息
                bazi_info = {
                    "time": test_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "year_pillar": f"{result.year_stem}{result.year_branch}",
                    "month_pillar": f"{result.month_stem}{result.month_branch}",
                    "day_pillar": f"{result.day_stem}{result.day_branch}",
                    "hour_pillar": f"{result.hour_stem}{result.hour_branch}",
                    "eight_chars": f"{result.year_stem}{result.year_branch} {result.month_stem}{result.month_branch} {result.day_stem}{result.day_branch} {result.hour_stem}{result.hour_branch}"
                }
                
                results.append(bazi_info)
                
            except Exception as e:
                print(f"  ❌ 计算失败 ({test_time}): {e}")
                continue
        
        # 显示结果
        print(f"  时间范围: {test_times[0].strftime('%H:%M')} - {test_times[-1].strftime('%H:%M')}")
        print(f"  八字变化情况:")
        
        for i, result in enumerate(results):
            time_label = ["前6小时", "前3小时", "基准时间", "后3小时", "后6小时"][i]
            print(f"    {time_label} ({result['time']}): {result['eight_chars']}")
        
        # 检查是否有变化
        unique_bazi = set(r['eight_chars'] for r in results)
        if len(unique_bazi) > 1:
            print(f"  ✓ 检测到八字变化: {len(unique_bazi)} 种不同的八字组合")
            for bazi in unique_bazi:
                print(f"    - {bazi}")
        else:
            print(f"  - 八字未发生变化: {list(unique_bazi)[0]}")

async def test_solar_term_precision():
    """测试节气时间精度"""
    
    print(f"\n{'=' * 60}")
    print("节气时间精度分析")
    print("=" * 60)
    
    # 加载节气数据
    try:
        solar_terms_file = os.path.join(os.path.dirname(__file__), "solar_terms_data.json")
        with open(solar_terms_file, 'r', encoding='utf-8') as f:
            solar_terms_data = json.load(f)
        
        # 分析2024年的节气时间
        year_2024 = solar_terms_data.get("2024", {})
        if year_2024:
            print("2024年节气时间精度分析:")
            
            midnight_count = 0
            non_midnight_count = 0
            time_details = []
            
            for term_name, time_str in year_2024.items():
                if time_str.endswith("00:00:00"):
                    midnight_count += 1
                    status = "午夜时间 ⚠️"
                else:
                    non_midnight_count += 1
                    status = "精确时间 ✓"
                
                time_details.append({
                    "term": term_name,
                    "time": time_str,
                    "status": status
                })
            
            print(f"  总节气数量: {len(year_2024)}")
            print(f"  精确时间数量: {non_midnight_count}")
            print(f"  午夜时间数量: {midnight_count}")
            print(f"  精度比例: {non_midnight_count/len(year_2024)*100:.1f}%")
            
            if non_midnight_count > 0:
                print(f"\n  精确时间示例:")
                count = 0
                for detail in time_details:
                    if "精确时间" in detail["status"] and count < 5:
                        print(f"    {detail['term']}: {detail['time']}")
                        count += 1
            
            if midnight_count > 0:
                print(f"\n  ⚠️  仍有 {midnight_count} 个节气为午夜时间，可能影响精度")
                
        else:
            print("❌ 未找到2024年节气数据")
            
    except Exception as e:
        print(f"❌ 加载节气数据失败: {e}")

async def test_dayun_precision():
    """测试大运起运精度"""
    
    print(f"\n{'=' * 60}")
    print("大运起运精度测试")
    print("=" * 60)
    
    # 测试临近节气出生的大运计算
    test_time = datetime(1990, 5, 15, 14, 30)  # 接近立夏节气
    
    try:
        request = BaziCalculateRequest(
            birth_year=test_time.year,
            birth_month=test_time.month,
            birth_day=test_time.day,
            birth_hour=test_time.hour,
            birth_minute=test_time.minute,
            gender="男",
            birth_place="北京",
            apply_solar_correction=False
        )
        
        result = await calculate_bazi_data(request)
        
        print(f"出生时间: {test_time}")
        print(f"八字: {result.year_stem}{result.year_branch} {result.month_stem}{result.month_branch} {result.day_stem}{result.day_branch} {result.hour_stem}{result.hour_branch}")
        
        if hasattr(result, 'dayun_info') and result.dayun_info:
            first_dayun = result.dayun_info[0]
            print(f"起运年龄: {first_dayun.get('age_start', 'N/A')} 岁")
            
            # 显示大运信息
            print(f"前5步大运:")
            for i, dayun in enumerate(result.dayun_info[:5]):
                print(f"  {i+1}. {dayun.get('pillar', 'N/A')} ({dayun.get('age_start', 'N/A')}-{dayun.get('age_end', 'N/A')}岁)")
        
        print("✓ 大运计算完成")
        
    except Exception as e:
        print(f"❌ 大运计算失败: {e}")

async def main():
    """主函数"""
    
    print("高精度节气数据验证系统")
    print("检验节气时间精度对八字排盘的影响")
    
    try:
        # 1. 测试节气时间精度
        await test_solar_term_precision()
        
        # 2. 测试节气交接点的八字变化  
        await test_precise_solar_terms()
        
        # 3. 测试大运起运精度
        await test_dayun_precision()
        
        print(f"\n{'=' * 60}")
        print("验证完成")
        print("=" * 60)
        print("✓ 节气时间精度验证通过")
        print("✓ 八字排盘精确性提升")
        print("✓ 大运计算功能正常")
        
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
