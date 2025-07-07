#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修复后的强弱计算
"""

from app.services.calculators import FiveElementsCalculator
from app.services.core import Bazi, StemBranch

def test_strength_calculation():
    """测试强弱计算"""
    print("=== 测试强弱计算修复 ===")
    
    # 高梦泽八字：庚子 癸未 癸酉 己未
    bazi = Bazi(
        year=StemBranch("庚", "子"),
        month=StemBranch("癸", "未"),
        day=StemBranch("癸", "酉"),
        hour=StemBranch("己", "未"),
        gender="女"
    )
    
    print("八字: 庚子 癸未 癸酉 己未")
    print("日主: 癸水")
    print("月令: 未月（夏季土旺）")
    print("金标准: 癸水偏弱")
    print("-" * 40)
    
    # 计算强弱
    strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
    print(f"系统计算结果: {strength}")
    
    # 详细分析
    print("\n=== 详细分析 ===")
    print("日主癸水的力量来源:")
    print("1. 天干: 庚金生水(+), 癸水本身, 己土克水(-)")
    print("2. 地支: 子水帮身(+), 未土克水(-), 酉金生水(+), 未土克水(-)")
    print("3. 月令: 未月土旺，土克水，癸水处囚地(-)")
    print("4. 季节: 夏季火旺土相，对水不利(-)")
    print("5. 整体: 土势强旺(未月+己土+未×2)，金水力量不足以抗衡")
    print("6. 结论: 癸水应为偏弱")
    
    # 判断是否修复成功
    if "偏弱" in strength or "弱" in strength:
        print("\n✓ 强弱计算修复成功！")
        return True
    else:
        print(f"\n❌ 强弱计算仍有问题，结果: {strength}")
        return False

if __name__ == "__main__":
    test_strength_calculation()
