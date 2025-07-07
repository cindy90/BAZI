#!/usr/bin/env python3
"""
简化版测试增强流年分析功能
直接使用计算器模块测试
"""
import sys
import os
import json
from datetime import datetime

# 添加backend目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.calculators import FiveElementsCalculator, ShenShaCalculator
from app.services.core import Bazi, StemBranch
from app.services.constants import STEM_ELEMENTS, BRANCH_ELEMENTS

def create_test_bazi():
    """创建测试用的八字对象"""
    # 1990年6月15日10点30分 男命
    # 庚午年 壬午月 丁酉日 乙巳时
    bazi = Bazi(
        year=StemBranch("庚", "午"),
        month=StemBranch("壬", "午"),
        day=StemBranch("丁", "酉"),
        hour=StemBranch("乙", "巳"),
        gender="男",
        birth_time=datetime(1990, 6, 15, 10, 30)
    )
    return bazi

def test_liunian_interactions():
    """测试流年互动分析"""
    print("=== 测试流年互动分析 ===")
    
    bazi = create_test_bazi()
    print(f"测试八字: {bazi.year.stem}{bazi.year.branch} {bazi.month.stem}{bazi.month.branch} {bazi.day.stem}{bazi.day.branch} {bazi.hour.stem}{bazi.hour.branch}")
    
    # 测试2025年乙巳流年
    liunian_gan = "乙"
    liunian_zhi = "巳"
    dayun_gan = "戊"  # 假设大运
    dayun_zhi = "子"
    
    print(f"流年: {liunian_gan}{liunian_zhi}")
    print(f"大运: {dayun_gan}{dayun_zhi}")
    
    # 分析流年互动
    interactions = FiveElementsCalculator.analyze_liunian_interactions(
        bazi, liunian_gan, liunian_zhi, dayun_gan, dayun_zhi
    )
    
    print(f"\n--- 互动分析结果 ---")
    print(f"整体评估: {interactions.get('overall_assessment', '未知')}")
    
    if interactions.get('conflicts'):
        print(f"冲突 ({len(interactions['conflicts'])}):")
        for conflict in interactions['conflicts']:
            print(f"  • {conflict}")
    
    if interactions.get('harmonies'):
        print(f"和谐 ({len(interactions['harmonies'])}):")
        for harmony in interactions['harmonies']:
            print(f"  • {harmony}")
    
    if interactions.get('punishments'):
        print(f"刑罚 ({len(interactions['punishments'])}):")
        for punishment in interactions['punishments']:
            print(f"  • {punishment}")
    
    if interactions.get('harms'):
        print(f"相害 ({len(interactions['harms'])}):")
        for harm in interactions['harms']:
            print(f"  • {harm}")
    
    if interactions.get('special_combinations'):
        print(f"特殊组合 ({len(interactions['special_combinations'])}):")
        for combo in interactions['special_combinations']:
            print(f"  • {combo}")
    
    return interactions

def test_liunian_shensha():
    """测试流年神煞分析"""
    print("\n=== 测试流年神煞分析 ===")
    
    bazi = create_test_bazi()
    liunian_gan = "乙"
    liunian_zhi = "巳"
    
    # 创建神煞计算器
    shen_sha_calculator = ShenShaCalculator()
    
    # 分析流年神煞
    liunian_shensha = FiveElementsCalculator.analyze_liunian_shensha(
        bazi, liunian_gan, liunian_zhi, shen_sha_calculator
    )
    
    print(f"流年神煞 ({len(liunian_shensha)}):")
    for shensha in liunian_shensha:
        print(f"  • {shensha['name']}: {shensha['description']}")
        if shensha.get('positive_tags'):
            print(f"    正面标签: {', '.join(shensha['positive_tags'])}")
        if shensha.get('negative_tags'):
            print(f"    负面标签: {', '.join(shensha['negative_tags'])}")
    
    return liunian_shensha

def test_enhanced_predictions():
    """测试增强版预测生成"""
    print("\n=== 测试增强版预测生成 ===")
    
    bazi = create_test_bazi()
    
    # 准备参数
    current_year_ten_god = "伤官"
    liunian_gan = "乙"
    liunian_zhi = "巳"
    liunian_gan_element = STEM_ELEMENTS.get(liunian_gan, "")
    liunian_zhi_element = BRANCH_ELEMENTS.get(liunian_zhi, "")
    current_age = 35
    current_dayun = "戊子"
    current_dayun_ten_god = "偏财"
    
    print(f"流年十神: {current_year_ten_god}")
    print(f"流年干支: {liunian_gan}({liunian_gan_element}) {liunian_zhi}({liunian_zhi_element})")
    print(f"当前年龄: {current_age}")
    print(f"当前大运: {current_dayun} ({current_dayun_ten_god})")
    
    # 先获取互动分析和神煞分析
    interactions = FiveElementsCalculator.analyze_liunian_interactions(
        bazi, liunian_gan, liunian_zhi, "戊", "子"
    )
    
    shen_sha_calculator = ShenShaCalculator()
    liunian_shensha = FiveElementsCalculator.analyze_liunian_shensha(
        bazi, liunian_gan, liunian_zhi, shen_sha_calculator
    )
    
    # 获取综合分析
    comprehensive_analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
    
    # 生成增强版预测
    predictions = FiveElementsCalculator.generate_enhanced_predictions(
        current_year_ten_god, liunian_gan, liunian_zhi,
        liunian_gan_element, liunian_zhi_element,
        interactions, liunian_shensha, comprehensive_analysis,
        bazi, current_age, current_dayun, current_dayun_ten_god
    )
    
    print(f"\n--- 增强版预测结果 ---")
    categories = ["career", "wealth", "health", "relationship", "timing", "strategy", "warning"]
    for category in categories:
        if category in predictions:
            events = predictions[category]
            print(f"\n{category.upper()} ({len(events)}):")
            for event in events:
                print(f"  • {event}")
    
    return predictions

def test_comprehensive_analysis():
    """测试综合分析功能"""
    print("\n=== 测试综合分析功能 ===")
    
    bazi = create_test_bazi()
    
    # 获取综合分析
    comprehensive_analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
    
    print(f"--- 综合分析结果 ---")
    
    # 基础分析
    basic_analysis = comprehensive_analysis.get("basic_analysis", {})
    print(f"日主强度: {basic_analysis.get('day_master_strength', 0):.2f}")
    print(f"强弱判断: {basic_analysis.get('strength_level', '未知')}")
    print(f"喜用神: {', '.join(basic_analysis.get('favorable_elements', []))}")
    print(f"忌神: {', '.join(basic_analysis.get('unfavorable_elements', []))}")
    
    # 格局分析
    pattern_analysis = comprehensive_analysis.get("pattern_analysis", {})
    print(f"主格局: {pattern_analysis.get('primary_pattern', '未知')}")
    print(f"格局用神: {', '.join(pattern_analysis.get('pattern_gods', []))}")
    
    # 最终建议
    final_prognosis = comprehensive_analysis.get("final_prognosis", {})
    print(f"综合评分: {final_prognosis.get('overall_rating', 0):.1f}")
    print(f"主要喜用神: {', '.join(final_prognosis.get('primary_favorable', []))}")
    print(f"次要喜用神: {', '.join(final_prognosis.get('secondary_favorable', []))}")
    
    return comprehensive_analysis

def save_test_results():
    """保存测试结果"""
    print("\n=== 保存测试结果 ===")
    
    bazi = create_test_bazi()
    
    # 运行所有测试
    interactions = test_liunian_interactions()
    liunian_shensha = test_liunian_shensha()
    predictions = test_enhanced_predictions()
    comprehensive_analysis = test_comprehensive_analysis()
    
    # 整合结果
    test_results = {
        "test_info": {
            "bazi": f"{bazi.year.stem}{bazi.year.branch} {bazi.month.stem}{bazi.month.branch} {bazi.day.stem}{bazi.day.branch} {bazi.hour.stem}{bazi.hour.branch}",
            "liunian": "乙巳",
            "test_time": datetime.now().isoformat()
        },
        "liunian_interactions": interactions,
        "liunian_shensha": liunian_shensha,
        "enhanced_predictions": predictions,
        "comprehensive_analysis": comprehensive_analysis
    }
    
    # 保存文件
    filename = f"enhanced_liunian_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 测试结果已保存到: {filename}")
    return filename

def main():
    """主函数"""
    print("=== 增强版流年分析功能测试 ===")
    print("测试八字: 庚午 壬午 丁酉 乙巳 (1990年6月15日10点30分 男命)")
    print("测试流年: 2025年乙巳")
    print("="*50)
    
    try:
        # 运行测试
        test_liunian_interactions()
        test_liunian_shensha()
        test_enhanced_predictions()
        test_comprehensive_analysis()
        
        # 保存结果
        filename = save_test_results()
        
        print(f"\n✅ 所有测试完成，结果保存在: {filename}")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
