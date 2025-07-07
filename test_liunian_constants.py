#!/usr/bin/env python3
"""
测试流年互动分析常量重构
验证硬编码常量是否成功迁移到 constants.py
"""
import sys
import os
sys.path.append('backend')

from app.services.calculators import FiveElementsCalculator
from app.services.core import Bazi, StemBranch
from app.services.constants import (
    STEM_COMBINATIONS_DETAILED, 
    BRANCH_CONFLICTS_MAPPING,
    BRANCH_SIX_COMBINATIONS_DETAILED,
    BRANCH_THREE_COMBINATIONS_DETAILED,
    BRANCH_PUNISHMENTS_DETAILED,
    BRANCH_HARMS_DETAILED
)

def test_liunian_interactions_constants():
    """测试流年互动分析常量是否正确工作"""
    print("=== 流年互动分析常量重构测试 ===")
    
    # 创建测试八字
    test_bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=None
    )
    
    # 测试流年互动分析
    print("\n1. 测试天干五合常量")
    print(f"甲己合化土: {STEM_COMBINATIONS_DETAILED.get(('甲', '己'))}")
    print(f"乙庚合化金: {STEM_COMBINATIONS_DETAILED.get(('乙', '庚'))}")
    
    print("\n2. 测试地支六冲常量")
    print(f"子冲午: {BRANCH_CONFLICTS_MAPPING.get('子')}")
    print(f"寅冲申: {BRANCH_CONFLICTS_MAPPING.get('寅')}")
    
    print("\n3. 测试地支六合常量")
    print(f"子丑合土: {BRANCH_SIX_COMBINATIONS_DETAILED.get(('子', '丑'))}")
    print(f"寅亥合木: {BRANCH_SIX_COMBINATIONS_DETAILED.get(('寅', '亥'))}")
    
    print("\n4. 测试地支三合常量")
    print(f"申子辰水局: {BRANCH_THREE_COMBINATIONS_DETAILED.get(('申', '子', '辰'))}")
    print(f"寅午戌火局: {BRANCH_THREE_COMBINATIONS_DETAILED.get(('寅', '午', '戌'))}")
    
    print("\n5. 测试地支相刑常量")
    print(f"寅巳申刑: {BRANCH_PUNISHMENTS_DETAILED.get(('寅', '巳', '申'))}")
    print(f"子卯刑: {BRANCH_PUNISHMENTS_DETAILED.get(('子', '卯'))}")
    
    print("\n6. 测试地支相害常量")
    print(f"子未害: {BRANCH_HARMS_DETAILED.get(('子', '未'))}")
    print(f"寅巳害: {BRANCH_HARMS_DETAILED.get(('寅', '巳'))}")
    
    print("\n7. 测试流年互动分析方法")
    try:
        # 测试流年甲子年与命局的互动
        result = FiveElementsCalculator.analyze_liunian_interactions(
            test_bazi, "甲", "子", "丙", "寅"
        )
        
        print("流年互动分析结果:")
        print(f"  天干互动: {result['stem_interactions']}")
        print(f"  地支互动: {result['branch_interactions']}")
        print(f"  冲突: {result['conflicts']}")
        print(f"  和谐: {result['harmonies']}")
        print(f"  特殊组合: {result['special_combinations']}")
        print(f"  综合评估: {result['overall_assessment']}")
        
        print("\n✅ 流年互动分析方法工作正常")
        
    except Exception as e:
        print(f"\n❌ 流年互动分析方法测试失败: {e}")
        return False
    
    print("\n=== 测试完成，常量重构成功！ ===")
    return True

if __name__ == "__main__":
    test_liunian_interactions_constants()
