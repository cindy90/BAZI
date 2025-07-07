#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
子平法五行强弱算法测试与对比脚本
测试新实现的子平法五行强弱计分算法，与金标准案例对比分析
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.calculators import FiveElementsCalculator
from app.services.core import Bazi, StemBranch
from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
import asyncio

def test_ziping_wuxing_algorithm():
    """测试子平法五行强弱算法"""
    
    print("=" * 60)
    print("子平法五行强弱算法测试")
    print("=" * 60)
    
    # 高泽兮的金标准案例
    print("测试案例：高泽兮")
    print("金标准八字：癸卯 辛酉 乙亥 丙子")
    print("金标准强弱：平和")
    print()
    
    # 直接创建Bazi对象进行测试
    bazi_gaozexl = Bazi(
        year=StemBranch("癸", "卯"),
        month=StemBranch("辛", "酉"),
        day=StemBranch("乙", "亥"),
        hour=StemBranch("丙", "子"),
        gender="女"
    )
    
    # 使用新的子平法算法计算详细强弱分析
    print("子平法五行强弱详细计算过程：")
    print("-" * 40)
    
    detailed_result = FiveElementsCalculator.calculate_day_master_strength_detailed(bazi_gaozexl)
    
    for step in detailed_result["calculation_steps"]:
        print(step)
    
    print()
    print("=" * 40)
    print(f"计算结果：")
    print(f"日主：{detailed_result['day_stem']}({detailed_result['day_element']})")
    print(f"总分：{detailed_result['total_score']:.2f}分")
    print(f"强弱判定：{detailed_result['strength']}")
    print()
    
    # 与金标准对比
    print("与金标准对比：")
    print("-" * 40)
    gold_strength = "平和"
    print(f"  系统判定：{detailed_result['strength']}")
    print(f"  金标准：  {gold_strength}")
    print(f"  强弱匹配：{'✓' if detailed_result['strength'] == gold_strength else '✗'}")
    print()
    
    # 保存详细结果
    output_file = "ziping_wuxing_test_result.json"
    test_result = {
        "test_case": "高泽兮",
        "gold_standard": {
            "bazi": "癸卯 辛酉 乙亥 丙子",
            "strength": gold_strength
        },
        "system_result": detailed_result,
        "comparison": {
            "strength_match": detailed_result['strength'] == gold_strength
        },
        "test_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)
    
    print(f"详细测试结果已保存到：{output_file}")
    print()
    
    # 总结
    print("=" * 60)
    print("测试总结：")
    if detailed_result['strength'] == gold_strength:
        print("✓ 子平法五行强弱算法测试通过")
    else:
        print("✗ 子平法五行强弱算法测试未通过")
        print(f"  系统判定：{detailed_result['strength']}")
        print(f"  金标准：  {gold_strength}")
    print("=" * 60)

def test_multiple_cases():
    """测试多个案例"""
    print("\n" + "=" * 60)
    print("多案例测试")
    print("=" * 60)
    
    # 其他测试案例
    test_cases = [
        {
            "name": "案例1 - 戊土日主",
            "bazi": Bazi(
                year=StemBranch("乙", "丑"),
                month=StemBranch("戊", "寅"),
                day=StemBranch("戊", "申"),
                hour=StemBranch("甲", "寅"),
                gender="女"
            ),
            "expected_strength": "身强"
        },
        {
            "name": "案例2 - 甲木日主",
            "bazi": Bazi(
                year=StemBranch("庚", "戌"),
                month=StemBranch("己", "卯"),
                day=StemBranch("甲", "子"),
                hour=StemBranch("丙", "寅"),
                gender="男"
            ),
            "expected_strength": "身弱"
        },
        {
            "name": "案例3 - 壬水日主",
            "bazi": Bazi(
                year=StemBranch("辛", "未"),
                month=StemBranch("辛", "卯"),
                day=StemBranch("壬", "午"),
                hour=StemBranch("壬", "寅"),
                gender="男"
            ),
            "expected_strength": "平和"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试案例 {i}: {case['name']}")
        print("-" * 40)
        
        try:
            bazi = case["bazi"]
            
            # 计算强弱
            strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
            detailed_result = FiveElementsCalculator.calculate_day_master_strength_detailed(bazi)
            
            print(f"八字：{bazi.year.stem}{bazi.year.branch} "
                  f"{bazi.month.stem}{bazi.month.branch} "
                  f"{bazi.day.stem}{bazi.day.branch} "
                  f"{bazi.hour.stem}{bazi.hour.branch}")
            print(f"日主：{detailed_result['day_stem']}({detailed_result['day_element']})")
            print(f"总分：{detailed_result['total_score']:.2f}分")
            print(f"强弱：{strength}")
            
            if "expected_strength" in case:
                match = strength == case["expected_strength"]
                print(f"期望：{case['expected_strength']} {'✓' if match else '✗'}")
                
        except Exception as e:
            print(f"案例 {i} 测试失败: {e}")
            import traceback
            traceback.print_exc()

def test_detailed_calculation_display():
    """测试详细计算过程显示"""
    print("\n" + "=" * 60)
    print("详细计算过程展示")
    print("=" * 60)
    
    # 使用戊土日主案例展示详细计算过程
    test_bazi = Bazi(
        year=StemBranch("乙", "丑"),
        month=StemBranch("戊", "寅"),
        day=StemBranch("戊", "申"),
        hour=StemBranch("甲", "寅"),
        gender="女"
    )
    
    print("测试案例：乙丑 戊寅 戊申 甲寅")
    print("日主：戊土")
    print()
    
    # 详细计算过程
    detailed_result = FiveElementsCalculator.calculate_day_master_strength_detailed(test_bazi)
    
    print("详细计算过程：")
    print("-" * 40)
    
    for step in detailed_result["calculation_steps"]:
        print(step)
    
    print()
    print("分项得分明细：")
    print("-" * 40)
    for detail in detailed_result["detail_scores"]:
        print(f"  {detail}")
    
    print(f"\n最终结果：")
    print(f"  总分：{detailed_result['total_score']:.2f}分")
    print(f"  强弱：{detailed_result['strength']}")

if __name__ == "__main__":
    test_ziping_wuxing_algorithm()
    test_multiple_cases()
    test_detailed_calculation_display()
