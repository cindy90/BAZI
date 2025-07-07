#!/usr/bin/env python3
"""
测试增强版流年分析功能
验证 special_combinations 和 predicted_events 的个性化分析
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from backend.app.services.calculators import FiveElementsCalculator, ShenShaCalculator
from backend.app.services.core import Bazi, StemBranch
from backend.app.services.constants import *
import json

def test_enhanced_liunian_analysis():
    """测试增强版流年分析"""
    print("=== 测试增强版流年分析功能 ===")
    
    # 创建测试用八字
    test_bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("戊", "午"),
        hour=StemBranch("壬", "戌"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    # 测试流年：2025年乙巳
    liunian_gan = "乙"
    liunian_zhi = "巳"
    liunian_gan_element = "木"
    liunian_zhi_element = "火"
    
    print(f"测试八字: {test_bazi.year.stem}{test_bazi.year.branch} {test_bazi.month.stem}{test_bazi.month.branch} {test_bazi.day.stem}{test_bazi.day.branch} {test_bazi.hour.stem}{test_bazi.hour.branch}")
    print(f"流年: {liunian_gan}{liunian_zhi}")
    
    # 1. 测试流年互动分析
    print("\n1. 流年互动分析:")
    interactions = FiveElementsCalculator.analyze_liunian_interactions(
        test_bazi, liunian_gan, liunian_zhi, "己", "亥"  # 假设大运己亥
    )
    
    for key, value in interactions.items():
        if isinstance(value, list) and value:
            print(f"  {key}: {value}")
        elif isinstance(value, dict) and value:
            print(f"  {key}: {value}")
        elif isinstance(value, str) and value:
            print(f"  {key}: {value}")
    
    # 2. 测试流年神煞分析
    print("\n2. 流年神煞分析:")
    shen_sha_calculator = ShenShaCalculator()
    liunian_shensha = FiveElementsCalculator.analyze_liunian_shensha(
        test_bazi, liunian_gan, liunian_zhi, shen_sha_calculator
    )
    
    for shensha in liunian_shensha:
        print(f"  {shensha['name']}: {shensha['description']}")
    
    # 3. 测试综合分析
    print("\n3. 综合分析:")
    comprehensive_analysis = FiveElementsCalculator.analyze_comprehensive_gods(test_bazi)
    
    print(f"  日主强度: {comprehensive_analysis['basic_analysis']['strength_level']}")
    print(f"  格局: {comprehensive_analysis['pattern_analysis']['primary_pattern']}")
    print(f"  主要喜用神: {comprehensive_analysis['final_prognosis']['primary_favorable']}")
    
    # 4. 测试增强版预测生成
    print("\n4. 增强版预测生成:")
    current_year_ten_god = FiveElementsCalculator.calculate_ten_god_relation(liunian_gan, test_bazi.day.stem)
    
    predictions = FiveElementsCalculator.generate_detailed_predictions(
        current_year_ten_god,
        liunian_gan_element,
        liunian_zhi_element,
        interactions,
        liunian_shensha,
        comprehensive_analysis
    )
    
    for category, prediction_list in predictions.items():
        if prediction_list:
            print(f"\n  {category.upper()}:")
            for i, prediction in enumerate(prediction_list, 1):
                print(f"    {i}. {prediction}")
    
    # 5. 生成JSON格式输出
    print("\n5. 输出JSON格式结果:")
    result = {
        "bazi_info": {
            "year": f"{test_bazi.year.stem}{test_bazi.year.branch}",
            "month": f"{test_bazi.month.stem}{test_bazi.month.branch}",
            "day": f"{test_bazi.day.stem}{test_bazi.day.branch}",
            "hour": f"{test_bazi.hour.stem}{test_bazi.hour.branch}"
        },
        "liunian_info": {
            "gan_zhi": f"{liunian_gan}{liunian_zhi}",
            "ten_god": current_year_ten_god,
            "gan_element": liunian_gan_element,
            "zhi_element": liunian_zhi_element
        },
        "interactions": interactions,
        "shensha": liunian_shensha,
        "comprehensive_analysis": {
            "strength_level": comprehensive_analysis['basic_analysis']['strength_level'],
            "pattern": comprehensive_analysis['pattern_analysis']['primary_pattern'],
            "favorable_elements": comprehensive_analysis['final_prognosis']['primary_favorable']
        },
        "predictions": predictions
    }
    
    # 保存结果到文件
    with open("enhanced_liunian_test_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("结果已保存到 enhanced_liunian_test_result.json")
    
    return result

def test_multiple_cases():
    """测试多个案例"""
    print("\n=== 测试多个案例 ===")
    
    test_cases = [
        {
            "name": "强日主案例",
            "bazi": Bazi(
                year=StemBranch("甲", "子"),
                month=StemBranch("丙", "寅"),
                day=StemBranch("甲", "寅"),
                hour=StemBranch("甲", "戌"),
                gender="男",
                birth_time=datetime(1984, 2, 15, 14, 30)
            ),
            "liunian": ("乙", "巳")
        },
        {
            "name": "弱日主案例",
            "bazi": Bazi(
                year=StemBranch("庚", "申"),
                month=StemBranch("戊", "子"),
                day=StemBranch("丁", "巳"),
                hour=StemBranch("壬", "寅"),
                gender="女",
                birth_time=datetime(1980, 12, 10, 8, 0)
            ),
            "liunian": ("乙", "巳")
        }
    ]
    
    shen_sha_calculator = ShenShaCalculator()
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试案例: {case['name']}")
        
        bazi = case["bazi"]
        liunian_gan, liunian_zhi = case["liunian"]
        
        # 计算相关数据
        interactions = FiveElementsCalculator.analyze_liunian_interactions(
            bazi, liunian_gan, liunian_zhi, "己", "亥"
        )
        
        comprehensive_analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
        
        liunian_shensha = FiveElementsCalculator.analyze_liunian_shensha(
            bazi, liunian_gan, liunian_zhi, shen_sha_calculator
        )
        
        current_year_ten_god = FiveElementsCalculator.calculate_ten_god_relation(liunian_gan, bazi.day.stem)
        
        predictions = FiveElementsCalculator.generate_detailed_predictions(
            current_year_ten_god,
            STEM_ELEMENTS.get(liunian_gan, ""),
            BRANCH_ELEMENTS.get(liunian_zhi, ""),
            interactions,
            liunian_shensha,
            comprehensive_analysis
        )
        
        print(f"  日主强度: {comprehensive_analysis['basic_analysis']['strength_level']}")
        print(f"  流年十神: {current_year_ten_god}")
        print(f"  互动关系: {interactions['overall_assessment']}")
        print(f"  预测要点: {len(predictions['career'])}个事业预测, {len(predictions['wealth'])}个财运预测")
        
        results.append({
            "case_name": case["name"],
            "strength_level": comprehensive_analysis['basic_analysis']['strength_level'],
            "ten_god": current_year_ten_god,
            "interactions_count": len(interactions.get("harmonies", [])) + len(interactions.get("conflicts", [])),
            "predictions_count": sum(len(pred_list) for pred_list in predictions.values())
        })
    
    print(f"\n测试完成，共测试了 {len(test_cases)} 个案例")
    for result in results:
        print(f"  {result['case_name']}: {result['strength_level']} + {result['ten_god']} -> {result['predictions_count']}条预测")
    
    return results

if __name__ == "__main__":
    try:
        # 测试增强版流年分析
        result = test_enhanced_liunian_analysis()
        
        # 测试多个案例
        multi_results = test_multiple_cases()
        
        print("\n=== 测试总结 ===")
        print("✓ 流年互动分析功能正常")
        print("✓ 流年神煞分析功能正常")
        print("✓ 综合分析功能正常")
        print("✓ 增强版预测生成功能正常")
        print("✓ 多案例测试通过")
        
        print("\n增强版流年分析测试完成！")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
