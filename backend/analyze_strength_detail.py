#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
详细分析强弱计算过程
"""

from app.services.constants import *

def analyze_gaomengze_strength_detail():
    """详细分析高梦泽案例的强弱计算"""
    print("=== 高梦泽强弱计算详细分析 ===")
    
    # 八字：庚子 癸未 癸酉 己未
    # 日主：癸水
    
    day_element = "水"
    total_score = 0.0
    
    print(f"日主：癸水 ({day_element})")
    print("计算过程:")
    
    # 1. 月令得气
    month_branch = "未"
    month_element = BRANCH_ELEMENTS.get(month_branch, "")
    print(f"\n1. 月令分析:")
    print(f"   月支：{month_branch}")
    print(f"   月令五行：{month_element}")
    print(f"   日主五行：{day_element}")
    
    if month_element == day_element:
        score = 0.3
        print(f"   月令同五行，得月令：+{score}")
    elif month_element in FIVE_ELEMENTS_GENERATION.get(day_element, []):
        score = 0.2
        print(f"   月令生日主：+{score}")
    elif day_element in FIVE_ELEMENTS_GENERATION.get(month_element, []):
        score = -0.2
        print(f"   月令克日主：{score}")
    else:
        score = -0.1
        print(f"   其他情况：{score}")
    
    total_score += score
    print(f"   当前总分：{total_score}")
    
    # 2. 天干分析
    stems = ["庚", "癸", "己"]  # 不包含日主癸
    print(f"\n2. 天干分析:")
    for i, stem in enumerate(stems):
        stem_element = STEM_ELEMENTS.get(stem, "")
        print(f"   {['年', '月', '时'][i]}干{stem}({stem_element}):")
        
        if stem_element == day_element:
            score = 0.1
            print(f"     同类天干：+{score}")
        elif stem_element in FIVE_ELEMENTS_GENERATION.get(day_element, []):
            score = 0.05
            print(f"     天干生日主：+{score}")
        elif day_element in FIVE_ELEMENTS_GENERATION.get(stem_element, []):
            score = -0.05
            print(f"     天干克日主：{score}")
        else:
            score = 0
            print(f"     无直接关系：{score}")
        
        total_score += score
        print(f"     当前总分：{total_score}")
    
    # 3. 地支分析
    branches = ["子", "未", "酉", "未"]
    print(f"\n3. 地支分析:")
    for i, branch in enumerate(branches):
        branch_element = BRANCH_ELEMENTS.get(branch, "")
        print(f"   {['年', '月', '日', '时'][i]}支{branch}({branch_element}):")
        
        if branch_element == day_element:
            score = 0.15
            print(f"     地支同五行：+{score}")
        elif branch_element in FIVE_ELEMENTS_GENERATION.get(day_element, []):
            score = 0.1
            print(f"     地支生日主：+{score}")
        elif day_element in FIVE_ELEMENTS_GENERATION.get(branch_element, []):
            score = -0.1
            print(f"     地支克日主：{score}")
        else:
            score = 0
            print(f"     无直接关系：{score}")
        
        total_score += score
        
        # 藏干分析
        hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
        print(f"     藏干：{hidden_stems}")
        for hidden_stem, strength in hidden_stems.items():
            hidden_element = STEM_ELEMENTS.get(hidden_stem, "")
            if hidden_element == day_element:
                hidden_score = strength * 0.05
                print(f"       {hidden_stem}({hidden_element})同五行：+{hidden_score}")
                total_score += hidden_score
            elif hidden_element in FIVE_ELEMENTS_GENERATION.get(day_element, []):
                hidden_score = strength * 0.03
                print(f"       {hidden_stem}({hidden_element})生日主：+{hidden_score}")
                total_score += hidden_score
        
        print(f"     当前总分：{total_score}")
    
    # 4. 季节调节
    print(f"\n4. 季节调节:")
    print(f"   月支：{month_branch}")
    if month_branch in ["巳", "午", "未"]:  # 夏季
        print(f"   夏季，火旺土相")
        if day_element == "水":
            score = -0.1
            print(f"   水在夏季不利：{score}")
            total_score += score
    
    print(f"   最终总分：{total_score}")
    
    # 5. 判断结果
    print(f"\n5. 判断结果:")
    if total_score >= 0.3:
        result = "日主过强，需要泄耗，忌生助"
    elif total_score >= 0.1:
        result = "日主偏强，宜泄耗，忌生助"
    elif total_score >= -0.1:
        result = "日主中和，宜生助"
    elif total_score >= -0.3:
        result = "日主偏弱，宜生助，忌克泄"
    else:
        result = "日主极弱，急需生助"
    
    print(f"   根据总分{total_score}，判断为：{result}")
    print(f"   金标准：癸水偏弱")
    
    # 6. 问题分析
    print(f"\n6. 问题分析:")
    print(f"   系统计算总分：{total_score}")
    print(f"   系统判断：{result}")
    print(f"   期望结果：癸水偏弱")
    
    if total_score >= -0.1:
        print(f"   问题：计算得分过高，未能正确反映土势强旺对水的压制")
        print(f"   建议：加大月令不利、土克水的权重")

if __name__ == "__main__":
    analyze_gaomengze_strength_detail()
