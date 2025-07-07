#!/usr/bin/env python3
"""
测试流年神煞分析重构功能
验证 analyze_liunian_shensha 方法以本命盘为基准，在流年干支上查找神煞
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.services.core import Bazi, StemBranch
    from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
    from datetime import datetime
    import json
    
    print("成功导入所需模块")
except ImportError as e:
    print(f"导入失败: {e}")
    sys.exit(1)

def test_liunian_shensha_analysis():
    """测试流年神煞分析功能"""
    print("=" * 60)
    print("测试流年神煞分析重构功能")
    print("=" * 60)
    
    # 测试用例1: 甲子年生人，流年乙丑
    print("\n【测试用例1】甲子年生人，流年乙丑")
    print("-" * 40)
    
    # 创建八字对象
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    print(f"本命盘：{bazi.year.stem}{bazi.year.branch}年 {bazi.month.stem}{bazi.month.branch}月 {bazi.day.stem}{bazi.day.branch}日 {bazi.hour.stem}{bazi.hour.branch}时")
    print(f"日主：{bazi.day.stem}　年干：{bazi.year.stem}")
    
    # 创建神煞计算器
    shen_sha_calculator = ShenShaCalculator()
    
    # 分析流年神煞
    liunian_gan = "乙"
    liunian_zhi = "丑"
    print(f"流年：{liunian_gan}{liunian_zhi}")
    
    liunian_shensha = FiveElementsCalculator.analyze_liunian_shensha(
        bazi, liunian_gan, liunian_zhi, shen_sha_calculator
    )
    
    print(f"\n流年神煞分析结果：")
    if liunian_shensha:
        for i, shensha in enumerate(liunian_shensha, 1):
            print(f"{i}. {shensha['name']}")
            print(f"   位置：{shensha['position']}")
            print(f"   强度：{shensha['strength']}")
            print(f"   描述：{shensha['description']}")
            print(f"   正面标签：{shensha['positive_tags']}")
            print(f"   负面标签：{shensha['negative_tags']}")
            print()
    else:
        print("   无特殊神煞")
    
    # 测试用例2: 验证天乙贵人
    print("\n【测试用例2】验证天乙贵人")
    print("-" * 40)
    
    # 戊土日主，流年遇到丑或未，应该有天乙贵人
    bazi2 = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),  # 戊土日主
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    print(f"本命盘：{bazi2.year.stem}{bazi2.year.branch}年 {bazi2.month.stem}{bazi2.month.branch}月 {bazi2.day.stem}{bazi2.day.branch}日 {bazi2.hour.stem}{bazi2.hour.branch}时")
    print(f"日主：{bazi2.day.stem}（戊土日主，贵人在丑未）")
    
    # 流年辛未，应该有天乙贵人
    liunian_gan2 = "辛"
    liunian_zhi2 = "未"
    print(f"流年：{liunian_gan2}{liunian_zhi2}")
    
    liunian_shensha2 = FiveElementsCalculator.analyze_liunian_shensha(
        bazi2, liunian_gan2, liunian_zhi2, shen_sha_calculator
    )
    
    print(f"\n流年神煞分析结果：")
    if liunian_shensha2:
        for i, shensha in enumerate(liunian_shensha2, 1):
            print(f"{i}. {shensha['name']}")
            print(f"   位置：{shensha['position']}")
            print(f"   强度：{shensha['strength']}")
            print(f"   描述：{shensha['description']}")
            print(f"   正面标签：{shensha['positive_tags']}")
            print(f"   负面标签：{shensha['negative_tags']}")
            if 'base_stem' in shensha:
                print(f"   基准天干：{shensha['base_stem']}")
            if 'trigger_zhi' in shensha:
                print(f"   触发地支：{shensha['trigger_zhi']}")
            print()
    else:
        print("   无特殊神煞")
    
    # 测试用例3: 验证桃花星
    print("\n【测试用例3】验证桃花星")
    print("-" * 40)
    
    # 子年生人，流年遇到酉，应该有桃花星
    bazi3 = Bazi(
        year=StemBranch("甲", "子"),  # 子年生人
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    print(f"本命盘：{bazi3.year.stem}{bazi3.year.branch}年 {bazi3.month.stem}{bazi3.month.branch}月 {bazi3.day.stem}{bazi3.day.branch}日 {bazi3.hour.stem}{bazi3.hour.branch}时")
    print(f"年支：{bazi3.year.branch}（子年生人，桃花在酉）")
    
    # 流年癸酉，应该有桃花星
    liunian_gan3 = "癸"
    liunian_zhi3 = "酉"
    print(f"流年：{liunian_gan3}{liunian_zhi3}")
    
    liunian_shensha3 = FiveElementsCalculator.analyze_liunian_shensha(
        bazi3, liunian_gan3, liunian_zhi3, shen_sha_calculator
    )
    
    print(f"\n流年神煞分析结果：")
    if liunian_shensha3:
        for i, shensha in enumerate(liunian_shensha3, 1):
            print(f"{i}. {shensha['name']}")
            print(f"   位置：{shensha['position']}")
            print(f"   强度：{shensha['strength']}")
            print(f"   描述：{shensha['description']}")
            print(f"   正面标签：{shensha['positive_tags']}")
            print(f"   负面标签：{shensha['negative_tags']}")
            if 'base_zhi' in shensha:
                print(f"   基准地支：{shensha['base_zhi']}")
            if 'trigger_zhi' in shensha:
                print(f"   触发地支：{shensha['trigger_zhi']}")
            print()
    else:
        print("   无特殊神煞")
    
    # 测试用例4: 集成测试 - 完整流年分析
    print("\n【测试用例4】集成测试 - 验证与传统方法的差异")
    print("-" * 40)
    
    try:
        # 比较新旧方法的差异
        from app.services.core import Bazi, StemBranch
        
        # 创建一个临时的流年八字对象（旧方法）
        temp_bazi = Bazi(
            year=StemBranch(liunian_gan2, liunian_zhi2),
            month=bazi2.month,
            day=bazi2.day,
            hour=bazi2.hour,
            gender=bazi2.gender,
            birth_time=bazi2.birth_time
        )
        
        # 旧方法：计算包含流年的神煞
        old_method_shensha = shen_sha_calculator.calculate_shensha(temp_bazi)
        old_method_liunian = []
        for key, shensha in old_method_shensha.items():
            if shensha.active and "年" in shensha.position:
                old_method_liunian.append({
                    "name": shensha.name,
                    "description": shensha.description
                })
        
        # 新方法：已经计算过的结果
        new_method_liunian = liunian_shensha2
        
        print(f"旧方法结果（{len(old_method_liunian)}个）:")
        for shensha in old_method_liunian:
            print(f"  - {shensha['name']}: {shensha['description']}")
        
        print(f"\n新方法结果（{len(new_method_liunian)}个）:")
        for shensha in new_method_liunian:
            print(f"  - {shensha['name']}: {shensha['description']}")
        
        # 比较差异
        old_names = set(s['name'] for s in old_method_liunian)
        new_names = set(s['name'] for s in new_method_liunian)
        
        print(f"\n差异分析:")
        print(f"  旧方法独有：{old_names - new_names}")
        print(f"  新方法独有：{new_names - old_names}")
        print(f"  共同神煞：{old_names & new_names}")
        
    except Exception as e:
        print(f"集成测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_liunian_shensha_analysis()
