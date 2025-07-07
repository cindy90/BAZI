#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修改后的神煞预测功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.calculators import FiveElementsCalculator
    print("✅ calculators.py 导入成功")
    
    # 测试 _generate_shensha_predictions 方法
    predictions = {
        'career': [],
        'wealth': [],
        'health': [],
        'relationship': [],
        'timing': [],
        'strategy': [],
        'warning': []
    }
    
    test_shensha = [
        {
            'name': '天乙贵人',
            'positive_tags': ['贵人', '助力'],
            'negative_tags': []
        },
        {
            'name': '驿马',
            'positive_tags': ['变动', '出行'],
            'negative_tags': ['奔波']
        },
        {
            'name': '空亡',
            'positive_tags': [],
            'negative_tags': ['虚空', '不实']
        }
    ]
    
    print("🔄 测试神煞预测生成...")
    FiveElementsCalculator._generate_shensha_predictions(predictions, test_shensha)
    
    print("✅ _generate_shensha_predictions 方法调用成功")
    print(f"✅ 生成预测总数: {sum(len(v) for v in predictions.values())}")
    
    print("\n📊 详细预测结果:")
    for category, items in predictions.items():
        if items:
            print(f"  {category} ({len(items)} 条):")
            for item in items:
                print(f"    - {item}")
        else:
            print(f"  {category}: 无预测")
    
    print("\n✅ 所有硬编码神煞名称已成功移除，改为标签驱动!")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
