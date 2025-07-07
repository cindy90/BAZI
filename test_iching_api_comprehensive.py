#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试易经算卦API功能
Test I Ching Divination API Functionality
"""

import requests
import json
import asyncio
from datetime import datetime

def test_iching_api_basic():
    """测试基础易经算卦API"""
    print("🔮 === 测试易经算卦API ===")
    
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/v1/iching/test-divine"
    
    # 测试数据
    test_data = {
        "question": "事业发展如何？",
        "divination_method": "three_coins",
        "diviner_name": "测试用户",
        "context": {
            "background": "想了解近期事业发展方向",
            "specific_concerns": ["工作机会", "薪资提升", "职业规划"]
        }
    }
    
    try:
        print(f"📡 发送请求到: {url}")
        print(f"📝 请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            
            # 打印卦象基本信息
            hexagram = result.get("hexagram", {})
            print(f"\n🎯 卦象信息:")
            print(f"  卦名: {hexagram.get('name', '未知')}")
            print(f"  卦序: {hexagram.get('number', 0)}")
            print(f"  上卦: {hexagram.get('upper_trigram', '未知')}")
            print(f"  下卦: {hexagram.get('lower_trigram', '未知')}")
            print(f"  象辞: {hexagram.get('image', '无')}")
            print(f"  判断: {hexagram.get('judgment', '无')}")
            
            # 打印六爻信息
            lines = hexagram.get("lines", [])
            print(f"\n📜 六爻详情 (共{len(lines)}爻):")
            for i, line in enumerate(lines):
                line_num = line.get("number", i+1)
                yin_yang = line.get("yin_yang", "未知")
                is_changing = line.get("is_changing", False)
                value = line.get("value", 0)
                desc = line.get("description", "无描述")
                
                changing_mark = " (变爻)" if is_changing else ""
                print(f"  {line_num}爻: {yin_yang} (值:{value}){changing_mark}")
                print(f"    {desc}")
            
            # 打印解读信息
            interpretation = result.get("interpretation")
            if interpretation:
                print(f"\n💡 卦象解读:")
                print(f"  整体分析: {interpretation.get('overall_analysis', '无')}")
                print(f"  具体建议: {interpretation.get('specific_advice', '无')}")
                print(f"  时机判断: {interpretation.get('timing_guidance', '无')}")
                print(f"  注意事项: {interpretation.get('warnings', '无')}")
            
            # 检查变卦
            changed_hexagram = result.get("changed_hexagram")
            if changed_hexagram:
                print(f"\n🔄 变卦信息:")
                print(f"  变卦名: {changed_hexagram.get('name', '无')}")
                print(f"  变卦象辞: {changed_hexagram.get('image', '无')}")
            else:
                print(f"\n📌 无变爻，为静卦")
                
        else:
            print(f"❌ API调用失败")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：请确保后端服务已启动 (uvicorn app.main:app --reload)")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_iching_api_advanced():
    """测试高级易经算卦功能"""
    print("\n🔮 === 测试高级易经算卦API ===")
    
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/v1/iching/divine"
    
    # 高级测试数据
    test_data = {
        "question": "投资理财是否合适？",
        "divination_method": "manual_yao",
        "manual_yao_values": [6, 7, 8, 9, 6, 7],  # 手动指定爻值
        "diviner_name": "投资者",
        "context": {
            "background": "考虑进行股票投资",
            "specific_concerns": ["市场风险", "投资时机", "收益预期"],
            "time_frame": "近三个月"
        },
        "consultation_time": datetime.now().isoformat()
    }
    
    try:
        print(f"📡 发送请求到: {url}")
        print(f"📝 请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=45
        )
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 高级API调用成功!")
            
            # 详细分析结果
            print(f"\n🎯 详细分析结果:")
            
            success = result.get("success", False)
            print(f"  成功状态: {success}")
            
            message = result.get("message", "")
            if message:
                print(f"  消息: {message}")
            
            # 检查是否有AI解读
            interpretation = result.get("interpretation")
            if interpretation and hasattr(interpretation, 'ai_enhanced') and interpretation.get('ai_enhanced'):
                print(f"  🤖 AI增强解读: 已启用")
            else:
                print(f"  📝 标准解读: 使用传统方法")
                
        else:
            print(f"❌ 高级API调用失败")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 高级请求异常: {e}")

def test_iching_multiple_questions():
    """测试多个问题的易经算卦"""
    print("\n🔮 === 测试多问题易经算卦 ===")
    
    questions = [
        "今年事业运势如何？",
        "感情婚姻何时到来？", 
        "健康状况需要注意什么？",
        "财运投资有何建议？",
        "学业考试能否成功？"
    ]
    
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/v1/iching/test-divine"
    
    for i, question in enumerate(questions, 1):
        print(f"\n--- 第{i}个问题 ---")
        print(f"问题: {question}")
        
        test_data = {
            "question": question,
            "divination_method": "three_coins",
            "diviner_name": f"测试用户{i}"
        }
        
        try:
            response = requests.post(url, json=test_data, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                hexagram = result.get("hexagram", {})
                name = hexagram.get("name", "未知")
                judgment = hexagram.get("judgment", "无")
                
                print(f"✅ 得卦: {name}")
                print(f"📝 卦辞: {judgment}")
                
                # 简单统计变爻
                lines = hexagram.get("lines", [])
                changing_lines = [line for line in lines if line.get("is_changing", False)]
                if changing_lines:
                    print(f"🔄 变爻: {len(changing_lines)}个")
                else:
                    print(f"📌 静卦无变")
                    
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 异常: {e}")

def test_iching_error_handling():
    """测试易经API错误处理"""
    print("\n🔮 === 测试易经API错误处理 ===")
    
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/v1/iching/divine"
    
    # 测试无效数据
    invalid_tests = [
        {
            "name": "空问题",
            "data": {"question": "", "divination_method": "three_coins"}
        },
        {
            "name": "无效占卜方法",
            "data": {"question": "测试", "divination_method": "invalid_method"}
        },
        {
            "name": "无效手动爻值",
            "data": {
                "question": "测试", 
                "divination_method": "manual_yao",
                "manual_yao_values": [1, 2, 3]  # 无效值
            }
        },
        {
            "name": "手动爻值数量错误",
            "data": {
                "question": "测试",
                "divination_method": "manual_yao", 
                "manual_yao_values": [6, 7, 8]  # 只有3个值
            }
        }
    ]
    
    for test in invalid_tests:
        print(f"\n--- 测试: {test['name']} ---")
        
        try:
            response = requests.post(url, json=test["data"], timeout=15)
            
            print(f"状态码: {response.status_code}")
            if response.status_code != 200:
                print(f"错误响应: {response.text}")
            else:
                print("🤔 意外成功（可能需要加强验证）")
                
        except Exception as e:
            print(f"异常: {e}")

def main():
    """主测试函数"""
    print("🚀 开始易经算卦API测试")
    print("=" * 50)
    
    # 基础功能测试
    test_iching_api_basic()
    
    # 高级功能测试
    test_iching_api_advanced()
    
    # 多问题测试
    test_iching_multiple_questions()
    
    # 错误处理测试
    test_iching_error_handling()
    
    print("\n" + "=" * 50)
    print("🏁 易经算卦API测试完成")

if __name__ == "__main__":
    main()
