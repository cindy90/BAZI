#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
深入分析高梦泽案例的五行旺衰判断
"""

from app.services.calculators import FiveElementsCalculator
from app.services.core import Bazi, StemBranch
from app.services.constants import JIAZI_TABLE
import json

def analyze_wuxing_strength():
    """分析五行旺衰"""
    print("=== 五行旺衰深入分析 ===")
    
    # 高梦泽八字：庚子 癸未 癸酉 己未
    bazi = Bazi(
        year=StemBranch("庚", "子"),
        month=StemBranch("癸", "未"),
        day=StemBranch("癸", "酉"),
        hour=StemBranch("己", "未"),
        gender="女"
    )
    
    calculator = FiveElementsCalculator()
    
    # 1. 基础五行分析
    print("1. 基础五行统计:")
    basic_analysis = calculator.analyze_basic_five_elements(bazi)
    print(f"   五行得分: {basic_analysis['five_elements_score']}")
    print(f"   日主强弱: {basic_analysis['day_master_strength']}")
    print(f"   日主五行: {basic_analysis['day_master_element']}")
    
    # 2. 月令分析
    print("\n2. 月令分析:")
    print(f"   月令: {bazi.month.branch} (未)")
    print(f"   季节: 夏季土旺")
    print(f"   对癸水的影响: 土克水，水处囚地")
    
    # 3. 地支藏干分析
    print("\n3. 地支藏干分析:")
    from app.services.constants import BRANCH_HIDDEN_STEMS
    
    for pillar_name, pillar in [("年", bazi.year), ("月", bazi.month), ("日", bazi.day), ("时", bazi.hour)]:
        hidden_stems = BRANCH_HIDDEN_STEMS.get(pillar.branch, [])
        print(f"   {pillar_name}柱{pillar.branch}: {hidden_stems}")
    
    # 4. 同党异党分析
    print("\n4. 同党异党分析:")
    print("   日主: 癸水 (阴水)")
    print("   同党 (生扶日主): 金生水、水帮水")
    print("   异党 (克泄耗日主): 土克水、木泄水、火耗水")
    
    print("\n   具体分析:")
    print("   天干: 庚(金) 癸(水) 癸(水) 己(土)")
    print("   - 庚金生癸水 (+)")
    print("   - 癸水帮癸水 (+)")
    print("   - 己土克癸水 (-)")
    
    print("\n   地支: 子(水) 未(土) 酉(金) 未(土)")
    print("   - 子水帮癸水 (+)")
    print("   - 未土克癸水 (-)")
    print("   - 酉金生癸水 (+)")
    print("   - 未土克癸水 (-)")
    
    # 5. 力量对比
    print("\n5. 力量对比:")
    print("   同党力量: 庚金 + 癸水 + 子水 + 酉金")
    print("   异党力量: 己土 + 未土×2 (未月土旺，力量倍增)")
    print("   月令未土当令，土势强旺")
    print("   结论: 异党力量 > 同党力量，癸水应为偏弱")
    
    # 6. 综合分析
    print("\n6. 综合分析结果:")
    comprehensive_analysis = calculator.analyze_comprehensive_gods(bazi)
    print(f"   综合分析: {json.dumps(comprehensive_analysis, ensure_ascii=False, indent=2)}")
    
    return bazi, basic_analysis, comprehensive_analysis

def check_strength_calculation_logic():
    """检查强弱计算逻辑"""
    print("\n=== 强弱计算逻辑检查 ===")
    
    # 检查五行计算器的逻辑
    from app.services.calculators import FiveElementsCalculator
    import inspect
    
    # 获取计算方法
    methods = [method for method in dir(FiveElementsCalculator) if not method.startswith('_')]
    print(f"FiveElementsCalculator 可用方法: {methods}")
    
    # 检查关键方法
    calc = FiveElementsCalculator()
    
    # 检查是否有专门的强弱计算方法
    if hasattr(calc, 'calculate_day_master_strength'):
        print("✓ 发现专门的强弱计算方法")
        sig = inspect.signature(calc.calculate_day_master_strength)
        print(f"   方法签名: {sig}")
    else:
        print("❌ 未找到专门的强弱计算方法")
    
    # 检查是否考虑了月令
    if hasattr(calc, 'get_month_element_strength'):
        print("✓ 发现月令元素强度计算方法")
    else:
        print("❌ 未找到月令强度计算方法")

if __name__ == "__main__":
    bazi, basic_analysis, comprehensive_analysis = analyze_wuxing_strength()
    check_strength_calculation_logic()
