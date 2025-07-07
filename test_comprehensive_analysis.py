#!/usr/bin/env python3
"""
测试综合分析功能
验证新的 analyze_comprehensive_gods 方法和 comprehensive_favorable_analysis 字段
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from backend.app.services.calculators import FiveElementsCalculator
from backend.app.services.core import Bazi, StemBranch
from backend.app.schemas.bazi import BaziCalculateRequest
from backend.app.services.bazi_calculator import calculate_bazi_data
import json
import asyncio

def test_comprehensive_analysis():
    """测试综合分析功能"""
    print("=== 测试综合分析功能 ===")
    
    # 创建测试八字
    bazi_obj = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("庚", "午"),
        hour=StemBranch("戊", "申"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    try:
        # 测试综合分析方法
        comprehensive_analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi_obj)
        
        print(f"✓ 综合分析成功完成")
        print(f"✓ 基础分析: {comprehensive_analysis['basic_analysis']['strength_level']}")
        print(f"✓ 主要喜用神: {comprehensive_analysis['final_prognosis']['primary_favorable']}")
        print(f"✓ 次要喜用神: {comprehensive_analysis['final_prognosis']['secondary_favorable']}")
        print(f"✓ 命局格局: {comprehensive_analysis['pattern_analysis']['primary_pattern']}")
        print(f"✓ 综合评分: {comprehensive_analysis['final_prognosis']['overall_rating']}")
        print(f"✓ 季节分析: {comprehensive_analysis['season_analysis']['season']} - {comprehensive_analysis['season_analysis']['adjustment_needed']}")
        
        # 验证数据结构完整性
        required_keys = ['basic_analysis', 'season_analysis', 'circulation_analysis', 
                        'pathology_analysis', 'pattern_analysis', 'final_prognosis']
        
        for key in required_keys:
            if key in comprehensive_analysis:
                print(f"✓ {key} 数据完整")
            else:
                print(f"✗ {key} 数据缺失")
        
        return True
        
    except Exception as e:
        print(f"✗ 综合分析失败: {e}")
        return False

async def test_full_api_integration():
    """测试完整API集成"""
    print("\n=== 测试完整API集成 ===")
    
    # 创建测试请求
    test_request = BaziCalculateRequest(
        name="测试用户",
        birth_datetime=datetime(1984, 2, 15, 14, 30),
        gender="男",
        birth_place="北京",
        is_solar_time=True,
        longitude=116.4,
        latitude=39.9,
        timezone_offset=8
    )
    
    try:
        # 调用完整计算
        result = await calculate_bazi_data(test_request, quick_mode=False)
        
        print(f"✓ API调用成功")
        print(f"✓ 八字: {result.bazi_characters}")
        print(f"✓ 日主强弱: {result.day_master_strength}")
        print(f"✓ 喜用神: {result.favorable_elements}")
        
        # 验证综合分析字段
        if result.comprehensive_favorable_analysis:
            print(f"✓ 综合分析字段存在")
            comp_analysis = result.comprehensive_favorable_analysis
            
            print(f"✓ 基础分析: {comp_analysis['basic_analysis']['analysis']}")
            print(f"✓ 格局分析: {comp_analysis['pattern_analysis']['pattern_description']}")
            print(f"✓ 生活建议: {comp_analysis['final_prognosis']['life_advice']}")
            
            # 验证当年运势是否使用了综合分析
            if result.current_year_fortune:
                if 'comprehensive_rating' in result.current_year_fortune:
                    print(f"✓ 当年运势已集成综合分析")
                    print(f"✓ 综合评分: {result.current_year_fortune['comprehensive_rating']}")
                else:
                    print(f"✗ 当年运势未集成综合分析")
            
        else:
            print(f"✗ 综合分析字段缺失")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ API集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    # 测试极端八字
    extreme_cases = [
        # 五行偏枯
        Bazi(
            year=StemBranch("甲", "寅"),
            month=StemBranch("乙", "卯"),
            day=StemBranch("丙", "辰"),
            hour=StemBranch("丁", "巳"),
            gender="女",
            birth_time=datetime(1990, 3, 15, 8, 30)
        ),
        # 五行平衡
        Bazi(
            year=StemBranch("甲", "子"),
            month=StemBranch("丙", "寅"),
            day=StemBranch("戊", "辰"),
            hour=StemBranch("庚", "申"),
            gender="男",
            birth_time=datetime(1985, 5, 20, 10, 15)
        )
    ]
    
    for i, bazi in enumerate(extreme_cases):
        try:
            analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
            print(f"✓ 边界情况 {i+1} 分析成功")
            print(f"  - 强弱: {analysis['basic_analysis']['strength_level']}")
            print(f"  - 格局: {analysis['pattern_analysis']['primary_pattern']}")
            print(f"  - 评分: {analysis['final_prognosis']['overall_rating']}")
        except Exception as e:
            print(f"✗ 边界情况 {i+1} 分析失败: {e}")
            return False
    
    return True

def save_test_results():
    """保存测试结果到文件"""
    print("\n=== 保存测试结果 ===")
    
    try:
        # 生成测试样本
        bazi_obj = Bazi(
            year=StemBranch("甲", "子"),
            month=StemBranch("丙", "寅"),
            day=StemBranch("庚", "午"),
            hour=StemBranch("戊", "申"),
            gender="男",
            birth_time=datetime(1984, 2, 15, 14, 30)
        )
        
        analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi_obj)
        
        # 保存结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_analysis_test_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✓ 测试结果已保存到: {filename}")
        return True
        
    except Exception as e:
        print(f"✗ 保存测试结果失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试综合分析功能...")
    
    test_results = []
    
    # 运行各项测试
    test_results.append(("综合分析功能", test_comprehensive_analysis()))
    test_results.append(("完整API集成", asyncio.run(test_full_api_integration())))
    test_results.append(("边界情况", test_edge_cases()))
    test_results.append(("保存测试结果", save_test_results()))
    
    # 汇总测试结果
    print("\n" + "="*50)
    print("测试结果汇总:")
    print("="*50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试均通过！综合分析功能实现成功！")
        return True
    else:
        print("❌ 部分测试失败，请检查错误信息")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
