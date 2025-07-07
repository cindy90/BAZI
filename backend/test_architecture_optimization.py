#!/usr/bin/env python3
"""
测试优化后的代码架构
验证函数迁移和常量统一化是否成功
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_calculator_methods():
    """测试迁移到calculators.py的方法"""
    print("=== 测试计算器方法迁移 ===")
    
    try:
        from app.services.calculators import FiveElementsCalculator
        
        # 测试节气数据获取
        print("1. 测试节气数据获取...")
        solar_terms = FiveElementsCalculator.get_solar_terms_for_year(2024)
        print(f"   2024年节气数据: {list(solar_terms.keys())[:5]}...")
        
        # 测试节气时间查找
        print("2. 测试节气时间查找...")
        lichun = FiveElementsCalculator.find_solar_term_datetime(2024, "立春")
        print(f"   2024年立春时间: {lichun}")
        
        # 测试大运计算
        print("3. 测试大运计算...")
        birth_datetime = datetime(1985, 6, 15, 14, 30)
        start_date, start_days, luck_pillars, start_age = FiveElementsCalculator.calculate_precise_dayun(
            birth_datetime, "男", "乙", "壬午"
        )
        print(f"   起运年龄: {start_age}, 起运天数: {start_days:.2f}")
        print(f"   大运序列: {luck_pillars[:3]}...")
        
        print("✓ 计算器方法迁移测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 计算器方法迁移测试失败: {e}")
        return False

def test_constants_import():
    """测试常量导入的统一性"""
    print("\n=== 测试常量导入统一性 ===")
    
    try:
        # 测试从bazi_calculator导入常量
        from app.services.bazi_calculator import JIAZI_TABLE
        print(f"1. bazi_calculator中JIAZI_TABLE长度: {len(JIAZI_TABLE)}")
        
        # 测试从constants导入常量
        from app.services.constants import JIAZI_TABLE as CONST_JIAZI_TABLE
        print(f"2. constants中JIAZI_TABLE长度: {len(CONST_JIAZI_TABLE)}")
        
        # 验证两者一致性
        if JIAZI_TABLE == CONST_JIAZI_TABLE:
            print("✓ 常量导入统一性测试通过")
            return True
        else:
            print("✗ 常量导入不一致")
            return False
            
    except Exception as e:
        print(f"✗ 常量导入统一性测试失败: {e}")
        return False

def test_main_calculator():
    """测试主计算器功能"""
    print("\n=== 测试主计算器功能 ===")
    
    try:
        from app.services.calculators import FiveElementsCalculator, ShenShaCalculator
        from app.services.core import Bazi, StemBranch
        
        # 创建测试八字
        bazi_obj = Bazi(
            year=StemBranch("乙", "丑"),
            month=StemBranch("戊", "午"),
            day=StemBranch("甲", "寅"),
            hour=StemBranch("丁", "未"),
            gender="男"
        )
        
        # 测试喜用神分析
        print("1. 测试喜用神分析...")
        gods_analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi_obj)
        print(f"   日主: {gods_analysis['basic_analysis']['day_element']}")
        print(f"   喜用神: {gods_analysis['basic_analysis']['favorable_elements']}")
        
        # 测试五行能量计算
        print("2. 测试五行能量计算...")
        energy_scores = FiveElementsCalculator.calculate_comprehensive_five_elements_energy(bazi_obj)
        percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi_obj)
        print(f"   五行能量分数: {energy_scores}")
        print(f"   五行能量百分比: {percentages}")
        
        # 测试流年互动
        print("3. 测试流年互动分析...")
        interactions = FiveElementsCalculator.analyze_liunian_interactions(
            bazi_obj, "甲", "子", "戊", "戌"
        )
        print(f"   天干互动: {len(interactions['stem_interactions'])}个")
        print(f"   地支互动: {len(interactions['branch_interactions'])}个")
        
        print("✓ 主计算器功能测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 主计算器功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始代码架构优化测试...")
    print("=" * 50)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(test_calculator_methods())
    test_results.append(test_constants_import())
    test_results.append(test_main_calculator())
    
    print("\n" + "=" * 50)
    
    if all(test_results):
        print("🎉 所有测试通过！代码架构优化成功！")
        print("✓ 函数迁移完成")
        print("✓ 常量导入统一")
        print("✓ 主功能正常")
    else:
        print("⚠️  部分测试失败，需要进一步调试")
        
    return all(test_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
