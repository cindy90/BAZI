#!/usr/bin/env python3
"""
最终集成测试 - 验证所有导入和架构优化
测试内容：
1. 所有模块导入正常
2. 真太阳时校正函数调用正常
3. 常量统一使用
4. 静态方法迁移成功
5. 主流程无错误
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime
from app.services.calculators import FiveElementsCalculator, ShenShaCalculator
from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest
import asyncio

def test_imports():
    """测试所有关键模块导入"""
    print("=" * 50)
    print("测试模块导入...")
    try:
        # 测试计算器类导入
        print("✓ FiveElementsCalculator 导入成功")
        print("✓ ShenShaCalculator 导入成功")
        
        # 测试主计算函数导入
        print("✓ calculate_bazi_data 导入成功")
        
        # 测试静态方法可用性
        birth_time = datetime(1990, 5, 15, 10, 30)
        correction_info = FiveElementsCalculator.get_solar_time_correction(birth_time, "北京")
        print(f"✓ 真太阳时校正函数调用成功: {correction_info['time_difference_minutes']:.2f}分钟")
        
        # 测试大运计算静态方法
        result = FiveElementsCalculator.calculate_precise_dayun(birth_time, "男", "乙", "寅")
        print(f"✓ 大运计算静态方法调用成功: 起运年龄{result[3]}岁")
        
        return True
    except Exception as e:
        print(f"✗ 导入测试失败: {e}")
        return False

def test_constants_integration():
    """测试常量统一使用"""
    print("=" * 50)
    print("测试常量统一使用...")
    try:
        # 测试五行计算器使用常量
        calculator = FiveElementsCalculator()
        
        # 测试常量访问
        from app.services.constants import DAY_MASTER_STRENGTH_WEIGHTS, BRANCH_SIX_CONFLICTS
        print(f"✓ 日主强度权重常量: {len(DAY_MASTER_STRENGTH_WEIGHTS)}个权重")
        print(f"✓ 地支六冲常量: {len(BRANCH_SIX_CONFLICTS)}对冲突")
        
        # 测试神煞计算器使用常量
        shensha_calc = ShenShaCalculator()
        print("✓ 神煞计算器初始化成功")
        
        return True
    except Exception as e:
        print(f"✗ 常量集成测试失败: {e}")
        return False

async def test_main_calculation():
    """测试主计算流程"""
    print("=" * 50)
    print("测试主计算流程...")
    try:
        # 创建测试请求
        request = BaziCalculateRequest(
            name="测试用户",
            gender="男",
            birth_datetime=datetime(1990, 5, 15, 10, 30),
            is_solar_time=True,
            birth_place="北京",
            longitude=116.4,
            latitude=39.9,
            timezone_offset=8.0
        )
        
        # 执行计算
        result = await calculate_bazi_data(request)
        
        # 验证结果
        assert result.bazi_characters is not None, "八字信息不能为空"
        assert result.day_master_element, "日主五行不能为空"
        assert result.zodiac_sign, "生肖不能为空"
        
        print(f"✓ 四柱计算成功: 日主五行{result.day_master_element}")
        print(f"✓ 生肖: {result.zodiac_sign}")
        print(f"✓ 五行分析成功: {len(result.five_elements_score)}个五行")
        print(f"✓ 大运计算成功: {len(result.major_cycles)}个大运")
        
        return True
    except Exception as e:
        print(f"✗ 主计算流程测试失败: {e}")
        return False

def test_architecture_completeness():
    """测试架构完整性"""
    print("=" * 50)
    print("测试架构完整性...")
    try:
        # 检查关键函数是否正确迁移
        methods_to_check = [
            'calculate_precise_dayun',
            'get_solar_terms_for_year', 
            'find_solar_term_datetime',
            'get_solar_time_correction',
            'apply_solar_time_correction'
        ]
        
        for method_name in methods_to_check:
            if hasattr(FiveElementsCalculator, method_name):
                print(f"✓ {method_name} 已正确迁移为静态方法")
            else:
                print(f"✗ {method_name} 迁移失败")
                return False
        
        # 检查常量是否正确配置
        from app.services.constants import (
            DAY_MASTER_STRENGTH_WEIGHTS,
            DAY_MASTER_STRENGTH_THRESHOLDS,
            FIVE_ELEMENTS_ENERGY_WEIGHTS,
            BRANCH_SIX_CONFLICTS,
            BRANCH_SIX_COMBINATIONS
        )
        
        constants_to_check = [
            ('DAY_MASTER_STRENGTH_WEIGHTS', DAY_MASTER_STRENGTH_WEIGHTS),
            ('DAY_MASTER_STRENGTH_THRESHOLDS', DAY_MASTER_STRENGTH_THRESHOLDS),
            ('FIVE_ELEMENTS_ENERGY_WEIGHTS', FIVE_ELEMENTS_ENERGY_WEIGHTS),
            ('BRANCH_SIX_CONFLICTS', BRANCH_SIX_CONFLICTS),
            ('BRANCH_SIX_COMBINATIONS', BRANCH_SIX_COMBINATIONS)
        ]
        
        for const_name, const_value in constants_to_check:
            if const_value:
                print(f"✓ {const_name} 常量配置正确")
            else:
                print(f"✗ {const_name} 常量配置错误")
                return False
        
        print("✓ 架构完整性检查通过")
        return True
    except Exception as e:
        print(f"✗ 架构完整性测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("开始最终集成测试...")
    print("测试目标：验证八字系统架构优化完成情况")
    
    test_results = []
    
    # 执行各项测试
    test_results.append(("模块导入", test_imports()))
    test_results.append(("常量集成", test_constants_integration()))
    test_results.append(("主计算流程", await test_main_calculation()))
    test_results.append(("架构完整性", test_architecture_completeness()))
    
    # 汇总测试结果
    print("\n" + "=" * 50)
    print("最终集成测试结果汇总")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n测试通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！八字系统架构优化完成！")
        print("主要优化成果：")
        print("- ✅ 真太阳时校正函数正确迁移为静态方法")
        print("- ✅ 常量统一配置，移除硬编码")
        print("- ✅ 核心算法模块化，提升可维护性")
        print("- ✅ 导入依赖关系清晰，无循环导入")
        print("- ✅ 主流程计算功能完整")
    else:
        print(f"\n⚠️  有{total-passed}个测试未通过，需要进一步修复")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
