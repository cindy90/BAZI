#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的重构验证脚本
"""

try:
    from app.services.calculators import FiveElementsCalculator
    print("✅ FiveElementsCalculator 导入成功")
    
    # 测试静态方法
    print("可用的静态方法:")
    methods = [m for m in dir(FiveElementsCalculator) if not m.startswith('_') and callable(getattr(FiveElementsCalculator, m))]
    for method in methods:
        print(f"  - {method}")
        
    # 测试十神关系计算
    ten_god = FiveElementsCalculator.calculate_ten_god_relation("甲", "戊")
    print(f"\n测试十神关系: 甲 -> 戊 = {ten_god}")
    
    # 测试地支藏干
    hidden_stems = FiveElementsCalculator.get_zhi_hidden_gan("子")
    print(f"测试地支藏干: 子 = {hidden_stems}")
    
    # 测试长生十二宫
    chang_sheng = FiveElementsCalculator.calculate_chang_sheng_twelve_palaces("戊", "子")
    print(f"测试长生十二宫: 戊在子 = {chang_sheng}")
    
    # 测试长生十二宫强度
    strength = FiveElementsCalculator.get_chang_sheng_strength_level("胎")
    print(f"测试长生十二宫强度: 胎 = {strength}")
    
    # 测试人生阶段分析
    phase = FiveElementsCalculator.analyze_dayun_phase(28)
    print(f"测试人生阶段分析: 28岁 = {phase}")
    
    print("\n✅ 所有重构后的函数测试成功！")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
