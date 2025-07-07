#!/usr/bin/env python3
"""
直接API测试脚本
"""
import requests
import json
from datetime import datetime

def test_api():
    """测试API"""
    print("=== 测试八字排盘API ===")
    
    # 高梦泽案例数据
    test_data = {
        "name": "高梦泽",
        "gender": "女",
        "birth_datetime": "2020-07-29T13:26:00+08:00",
        "is_solar_time": True,
        "birth_place": "北京市朝阳区",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "timezone_offset": 8.0
    }
    
    try:
        # 测试API调用
        response = requests.post(
            "http://localhost:8001/api/v1/bazi/calculate",
            json=test_data,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ API调用成功")
            
            # 验证关键字段
            if "bazi_characters" in result:
                bazi_chars = result["bazi_characters"]
                bazi_str = f"{bazi_chars.get('year_stem', '')}{bazi_chars.get('year_branch', '')} {bazi_chars.get('month_stem', '')}{bazi_chars.get('month_branch', '')} {bazi_chars.get('day_stem', '')}{bazi_chars.get('day_branch', '')} {bazi_chars.get('hour_stem', '')}{bazi_chars.get('hour_branch', '')}"
                print(f"八字: {bazi_str}")
                
                if bazi_str == "庚子 癸未 癸酉 己未":
                    print("✓ 八字计算正确")
                else:
                    print("✗ 八字计算不匹配")
            
            # 验证大运数据
            if "major_cycles" in result:
                major_cycles = result["major_cycles"]
                print(f"大运数量: {len(major_cycles)}")
                if major_cycles:
                    first_cycle = major_cycles[0]
                    print(f"第一步大运: {first_cycle.get('ganzhi', 'N/A')}")
                    
                    if first_cycle.get('ganzhi') == '壬午':
                        print("✓ 大运计算正确")
                    else:
                        print("✗ 大运计算不匹配")
            
            # 验证神煞数据
            if "shen_sha_details" in result:
                shensha_list = result["shen_sha_details"]
                print(f"神煞数量: {len(shensha_list)}")
                shensha_names = [s.get('name', '') for s in shensha_list]
                print(f"神煞: {shensha_names[:10]}...")  # 显示前10个
                
        else:
            print(f"✗ API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到后端服务，请确保后端已启动")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

if __name__ == "__main__":
    test_api()
