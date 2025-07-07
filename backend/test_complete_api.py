#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接API测试 - 测试完整的API流程
"""

import requests
import json
from datetime import datetime

def test_complete_api_flow():
    """测试完整的API流程"""
    print("=== 完整API流程测试 ===")
    
    # API端点
    base_url = "http://localhost:8000"
    api_url = f"{base_url}/api/v1/bazi/calculate"
    
    # 测试数据
    test_data = {
        "name": "测试用户",
        "gender": "男",
        "birth_datetime": "1990-03-15T14:30:00",
        "is_solar_time": True,
        "birth_place": "北京",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "timezone_offset": 8.0
    }
    
    try:
        print(f"发送请求到: {api_url}")
        print(f"请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(api_url, json=test_data, timeout=30)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ API调用成功")
            
            # 检查主要字段
            print(f"返回字段: {list(result.keys())}")
            
            # 检查八字信息
            if 'bazi_characters' in result:
                print(f"✓ 八字: {result['bazi_characters']}")
            
            # 检查日主信息
            if 'day_master_element' in result:
                print(f"✓ 日主: {result['day_master_element']}")
            
            if 'day_master_strength' in result:
                print(f"✓ 强弱: {result['day_master_strength']}")
            
            # 检查神煞详情
            if 'shen_sha_details' in result:
                shensha_list = result['shen_sha_details']
                print(f"✓ 神煞数量: {len(shensha_list)}")
                
                # 检查每个神煞的auspicious_level
                for i, shensha in enumerate(shensha_list[:3]):
                    print(f"  神煞 {i+1}: {shensha.get('name', 'N/A')}")
                    print(f"    吉凶等级: {shensha.get('auspicious_level', 'N/A')}")
                    print(f"    强度: {shensha.get('strength', 'N/A')}")
                    print(f"    描述: {shensha.get('description', 'N/A')}")
            
            # 检查流年分析
            if 'current_year_fortune' in result:
                current_year = result['current_year_fortune']
                print(f"✓ 流年分析: {current_year.get('year', 'N/A')} - {current_year.get('gan_zhi', 'N/A')}")
                
                if 'shensha_analysis' in current_year:
                    liunian_shensha = current_year['shensha_analysis']
                    print(f"  流年神煞类型: {type(liunian_shensha)}")
                    if isinstance(liunian_shensha, dict):
                        print(f"  有利神煞: {liunian_shensha.get('favorable_count', 'N/A')}")
                        print(f"  不利神煞: {liunian_shensha.get('unfavorable_count', 'N/A')}")
            
            # 检查五行分析
            if 'five_elements_score' in result:
                print(f"✓ 五行得分: {result['five_elements_score']}")
            
            # 检查喜用神
            if 'favorable_elements' in result:
                print(f"✓ 喜用神: {result['favorable_elements']}")
            
            print(f"\n=== API测试完成 ===")
            return True
            
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_complete_api_flow()
