#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的健康检查测试
"""

import requests
import json

def test_health_check():
    """测试健康检查接口"""
    print("=== 健康检查测试 ===")
    
    # 测试根路径
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        
        if response.status_code == 200:
            print(f"✓ 后端服务正常运行")
            print(f"响应: {response.json()}")
        else:
            print(f"❌ 后端服务异常: {response.status_code}")
            print(f"响应: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到后端服务: {e}")
    
    # 测试文档页面
    try:
        response = requests.get("http://localhost:8000/docs", timeout=10)
        
        if response.status_code == 200:
            print(f"✓ API文档可访问")
        else:
            print(f"❌ API文档不可访问: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API文档连接失败: {e}")

if __name__ == "__main__":
    test_health_check()
