#!/usr/bin/env python3
"""
完整测试新的数据驱动八字计算引擎
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.calculators import ShenShaCalculator, FiveElementsCalculator
from app.services.core import StemBranch, Bazi
from datetime import datetime

def test_complete_bazi_analysis():
    """完整的八字分析测试"""
    print("=" * 80)
    print("完整八字计算引擎测试 - 神煞 + 高级喜用神分析")
    print("=" * 80)
    
    # 创建一个典型的测试用例
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丁", "卯"),
        day=StemBranch("戊", "戌"),  # 戊戌日（魁罡）
        hour=StemBranch("癸", "亥"),
        gender="男",
        birth_time=datetime(1984, 3, 15, 22, 30)  # 春季，子时
    )
    
    print(f"测试八字: {bazi.year} {bazi.month} {bazi.day} {bazi.hour}")
    print(f"性别: {bazi.gender}")
    print(f"出生时间: {bazi.birth_time.strftime('%Y年%m月%d日 %H:%M')}")
    print(f"日主: {bazi.day_master} ({bazi.zodiac}年)")
    print()
    
    # === 1. 神煞分析 ===
    print("🔮 神煞分析")
    print("-" * 40)
    shensha_calculator = ShenShaCalculator()
    shensha_result = shensha_calculator.calculate(bazi)
    
    active_shensha = [(key, shensha) for key, shensha in shensha_result.items() if shensha.active]
    
    if active_shensha:
        for key, shensha in active_shensha:
            print(f"✨ {shensha.name}: {shensha.position}")
            print(f"   强度: {shensha.strength:.2f}")
            print(f"   描述: {shensha.description[:50]}...")
            if shensha.positive_tags:
                print(f"   吉: {', '.join(shensha.positive_tags)}")
            if shensha.negative_tags:
                print(f"   凶: {', '.join(shensha.negative_tags)}")
            if shensha.tags:
                print(f"   备注: {', '.join(shensha.tags)}")
            print()
    else:
        print("未发现明显的神煞")
    
    # === 2. 五行分析 ===
    print("⚖️ 五行强弱分析")
    print("-" * 40)
    
    # 五行得分
    scores = FiveElementsCalculator.calculate_comprehensive_scores(bazi)
    percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi)
    day_master_strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
    
    print("五行得分与百分比:")
    for element in ["金", "木", "水", "火", "土"]:
        score = scores.get(element, 0)
        percentage = percentages.get(element, 0)
        print(f"  {element}: {score:.2f} ({percentage:.1f}%)")
    
    print(f"\n日主强弱: {day_master_strength}")
    
    # 五行平衡分析
    balance = FiveElementsCalculator.analyze_five_elements_balance(bazi)
    print(f"五行平衡度: {balance['balance']}")
    if balance['missing']:
        print(f"缺失五行: {', '.join(balance['missing'])}")
    if balance['excess']:
        print(f"过旺五行: {', '.join(balance['excess'])}")
    print()
    
    # === 3. 喜用神分析 ===
    print("🎯 喜用神分析")
    print("-" * 40)
    
    # 基础喜用神
    basic_favorable = FiveElementsCalculator.get_favorable_elements(bazi)
    print(f"基础喜用神: {', '.join(basic_favorable)}")
    
    # 高级喜用神分析
    advanced_analysis = FiveElementsCalculator.get_advanced_favorable_elements(bazi)
    print(f"高级喜用神: {', '.join(advanced_analysis['primary_favorable'])}")
    print(f"调候用神: {', '.join(advanced_analysis['seasonal_priority'])} (季节: {advanced_analysis['season']})")
    if advanced_analysis['mediation_gods']:
        print(f"通关用神: {', '.join(advanced_analysis['mediation_gods'])}")
    if advanced_analysis['conflicts_detected']:
        print(f"五行冲突: {', '.join(advanced_analysis['conflicts_detected'])}")
    print()
    
    # 病药用神分析
    disease_medicine = FiveElementsCalculator.analyze_disease_medicine_gods(bazi)
    print("病药用神分析:")
    print(f"  病症: {', '.join(disease_medicine['diseases'])}")
    print(f"  用神: {', '.join(disease_medicine['medicines'])}")
    print(f"  日主占比: {disease_medicine['day_master_ratio']:.1%}")
    print()
    
    # 格局分析
    pattern_analysis = FiveElementsCalculator.analyze_pattern_and_gods(bazi)
    print("格局分析:")
    print(f"  格局: {pattern_analysis['pattern']}")
    print(f"  格局喜神: {', '.join(pattern_analysis['favorable_gods'])}")
    print(f"  格局忌神: {', '.join(pattern_analysis['avoid_gods'])}")
    print()
    
    # 综合用神分析
    comprehensive = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
    print("🎲 综合用神分析")
    print("-" * 40)
    print(f"最终主要用神: {', '.join(comprehensive['primary_gods'])}")
    print(f"最终次要用神: {', '.join(comprehensive['secondary_gods'])}")
    print()
    print("权重排序:")
    for god, weight in list(comprehensive['all_weights'].items())[:6]:
        print(f"  {god}: {weight:.3f}")
    print()
    print("综合分析摘要:")
    print(f"  {comprehensive['comprehensive_summary']}")
    print()
    
    # === 4. 干支互动分析 ===
    print("🔄 干支互动分析")
    print("-" * 40)
    interactions = shensha_calculator.analyze_interactions(bazi)
    
    all_interactions = []
    for category, items in interactions.items():
        if items:
            all_interactions.extend(items)
    
    if all_interactions:
        for interaction in all_interactions:
            print(f"  {interaction['type']}: {interaction['combination']}")
            if 'element' in interaction:
                print(f"    化神: {interaction['element']}")
            if 'penalty_type' in interaction:
                print(f"    刑类: {interaction['penalty_type']}")
            print(f"    位置: {', '.join(interaction['positions'])}")
    else:
        print("  未发现明显的干支互动关系")
    print()
    
    # === 5. 实用建议 ===
    print("💡 实用建议")
    print("-" * 40)
    primary_god = comprehensive['primary_gods'][0] if comprehensive['primary_gods'] else "木"
    
    color_suggestions = {
        "金": "白色、银色、金色",
        "木": "绿色、青色",
        "水": "黑色、蓝色",
        "火": "红色、紫色",
        "土": "黄色、棕色"
    }
    
    direction_suggestions = {
        "金": "西方",
        "木": "东方",
        "水": "北方",
        "火": "南方",
        "土": "中央、西南、东北"
    }
    
    career_suggestions = {
        "金": "金融、机械、汽车、科技",
        "木": "林业、文教、设计、服装",
        "水": "贸易、物流、旅游、饮食",
        "火": "能源、媒体、娱乐、电子",
        "土": "房地产、建筑、农业、土产"
    }
    
    print(f"主要用神为{primary_god}行，建议:")
    print(f"  颜色: {color_suggestions.get(primary_god, '根据个人喜好')}")
    print(f"  方位: {direction_suggestions.get(primary_god, '无特殊要求')}")
    print(f"  职业: {career_suggestions.get(primary_god, '根据个人兴趣')}")
    
    # 神煞相关建议
    if active_shensha:
        print(f"\n神煞提醒:")
        for key, shensha in active_shensha:
            if shensha.name == "魁罡":
                print(f"  ⚠️ 命带{shensha.name}，性格刚强果断，需注意婚姻感情")
            elif shensha.name == "天乙贵人":
                print(f"  ✨ 命带{shensha.name}，常有贵人相助，遇难呈祥")
            elif shensha.name == "桃花":
                print(f"  🌸 命带{shensha.name}，异性缘佳，需注意感情纠纷")
    
    print("\n" + "=" * 80)
    print("分析完成！以上为基于传统命理学的分析结果，仅供参考。")
    print("=" * 80)

def test_performance():
    """性能测试"""
    print("\n🚀 性能测试")
    print("-" * 30)
    import time
    
    # 创建100个随机八字进行性能测试
    test_count = 10
    total_time = 0
    
    stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    import random
    
    for i in range(test_count):
        # 随机生成八字
        year = StemBranch(random.choice(stems), random.choice(branches))
        month = StemBranch(random.choice(stems), random.choice(branches))
        day = StemBranch(random.choice(stems), random.choice(branches))
        hour = StemBranch(random.choice(stems), random.choice(branches))
        
        bazi = Bazi(year, month, day, hour, "男", datetime(1990, 6, 15, 12, 0))
        
        start_time = time.time()
        
        # 完整计算
        shensha_calculator = ShenShaCalculator()
        shensha_result = shensha_calculator.calculate(bazi)
        comprehensive = FiveElementsCalculator.analyze_comprehensive_gods(bazi)
        
        end_time = time.time()
        elapsed = end_time - start_time
        total_time += elapsed
        
        if i < 3:  # 只显示前3个的详细信息
            print(f"  测试 {i+1}: {elapsed:.3f}s")
    
    average_time = total_time / test_count
    print(f"\n平均计算时间: {average_time:.3f}s")
    print(f"总计算时间: {total_time:.3f}s")
    print(f"测试样本数: {test_count}")

if __name__ == "__main__":
    test_complete_bazi_analysis()
    test_performance()
