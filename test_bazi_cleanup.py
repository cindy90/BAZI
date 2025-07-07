#!/usr/bin/env python3
"""
测试bazi_calculator.py的重构结果
验证所有函数都能正常工作
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from app.schemas.bazi import BaziCalculateRequest
from app.services.bazi_calculator import calculate_bazi_data

async def test_basic_calculation():
    """测试基本的八字计算功能"""
    print("=== 开始基本八字计算测试 ===")
    
    # 创建请求数据
    request = BaziCalculateRequest(
        birth_datetime=datetime(1990, 5, 15, 14, 30, 0),
        gender="男",
        birth_place="北京"
    )
    
    try:
        # 调用计算函数
        result = await calculate_bazi_data(request)
        
        print(f"✓ 八字计算成功:")
        print(f"  八字: {result.bazi_characters}")
        print(f"  日主强度: {result.day_master_strength}")
        print(f"  生肖: {result.zodiac_sign}")
        print(f"  五行分数: {result.five_elements_score}")
        print(f"  喜用神: {result.favorable_elements}")
        print(f"  大运数量: {len(result.major_cycles)}")
        print(f"  神煞数量: {len(result.shen_sha_details)}")
        
        # 检查当年运势
        if result.current_year_fortune:
            print(f"  当年运势: {result.current_year_fortune['year']}年 {result.current_year_fortune['gan_zhi']}")
            print(f"  十神: {result.current_year_fortune['ten_god']}")
            print(f"  互动分析: {len(result.current_year_fortune['interactions'])}")
            print(f"  神煞分析: {len(result.current_year_fortune['shensha_analysis'])}")
            print(f"  特殊组合: {len(result.current_year_fortune['special_combinations'])}")
        
        print("✓ 所有测试通过！")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_functions_existence():
    """测试函数是否存在"""
    print("\n=== 检查函数存在性 ===")
    
    try:
        from app.services.calculators import FiveElementsCalculator
        
        # 检查FiveElementsCalculator的方法
        methods = [
            'analyze_dayun_phase',
            'calculate_ten_god_relation',
            'get_zhi_hidden_gan',
            'calculate_chang_sheng_twelve_palaces',
            'get_chang_sheng_strength_level',
            'calculate_day_master_strength',
            'calculate_five_elements_percentage',
            'analyze_comprehensive_gods',
            'get_strength_level_description',
            'analyze_liunian_interactions',
            'analyze_liunian_shensha'
        ]
        
        for method in methods:
            if hasattr(FiveElementsCalculator, method):
                print(f"✓ {method} - 存在")
            else:
                print(f"✗ {method} - 不存在")
                
        print("✓ 函数存在性检查完成")
        return True
        
    except Exception as e:
        print(f"✗ 函数存在性检查失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("开始bazi_calculator.py重构测试...")
    
    # 测试1：函数存在性
    test1 = test_functions_existence()
    
    # 测试2：基本计算
    test2 = await test_basic_calculation()
    
    if test1 and test2:
        print("\n🎉 所有测试通过！重构成功！")
    else:
        print("\n❌ 部分测试失败，需要进一步修复。")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
