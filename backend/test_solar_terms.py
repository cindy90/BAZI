#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试节气加载功能
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from solar_terms_utils import load_solar_terms_flat

def test_solar_terms():
    """测试节气加载"""
    print("=== 测试节气加载 ===")
    
    try:
        solar_terms = load_solar_terms_flat()
        print(f"加载节气数据: {len(solar_terms)} 个节气")
        
        # 查找2023年9月14日前后的节气
        birth_time = datetime(2023, 9, 14, 0, 26)
        print(f"出生时间: {birth_time}")
        
        # 找到出生前后最近的节气
        prev_term, next_term = None, None
        for term in solar_terms:
            term_dt = datetime.strptime(term["datetime"], "%Y-%m-%d %H:%M:%S")
            if term_dt <= birth_time:
                prev_term = term
            if term_dt > birth_time and not next_term:
                next_term = term
        
        print(f"上一个节气: {prev_term}")
        print(f"下一个节气: {next_term}")
        
        if prev_term:
            prev_dt = datetime.strptime(prev_term["datetime"], "%Y-%m-%d %H:%M:%S")
            days_from_prev = (birth_time - prev_dt).days
            print(f"距离上一个节气: {days_from_prev} 天")
        
        if next_term:
            next_dt = datetime.strptime(next_term["datetime"], "%Y-%m-%d %H:%M:%S")
            days_to_next = (next_dt - birth_time).days
            print(f"距离下一个节气: {days_to_next} 天")
        
        return True
        
    except Exception as e:
        print(f"节气加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_solar_terms()
    if success:
        print("\n✓ 节气加载测试成功")
    else:
        print("\n✗ 节气加载测试失败")
