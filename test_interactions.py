"""
测试干支互动分析功能
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.core import Bazi, StemBranch

def test_interactions():
    """测试干支互动分析"""
    
    # 创建一个测试八字：甲子年 乙丑月 丙寅日 丁卯时
    bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("乙", "丑"), 
        day=StemBranch("丙", "寅"),
        hour=StemBranch("丁", "卯"),
        gender="男"
    )
    
    # 简单的干支互动分析功能
    def analyze_simple_interactions(bazi_obj):
        stems = [bazi_obj.year.stem, bazi_obj.month.stem, bazi_obj.day.stem, bazi_obj.hour.stem]
        branches = [bazi_obj.year.branch, bazi_obj.month.branch, bazi_obj.day.branch, bazi_obj.hour.branch]
        
        results = {
            "stem_combinations": [],
            "branch_six_combinations": [],
            "branch_conflicts": [],
            "summary": f"天干: {stems}, 地支: {branches}"
        }
        
        # 天干五合检查
        combinations = {
            ("甲", "己"): "土", ("乙", "庚"): "金", ("丙", "辛"): "水", 
            ("丁", "壬"): "木", ("戊", "癸"): "火"
        }
        
        for i in range(len(stems)):
            for j in range(i + 1, len(stems)):
                pair = (stems[i], stems[j])
                if pair in combinations or (stems[j], stems[i]) in combinations:
                    element = combinations.get(pair, combinations.get((stems[j], stems[i])))
                    results["stem_combinations"].append({
                        "type": "天干五合",
                        "combination": f"{stems[i]}{stems[j]}",
                        "element": element,
                        "positions": [f"第{i+1}柱干", f"第{j+1}柱干"]
                    })
        
        # 地支六冲检查
        conflicts = {
            ("子", "午"), ("丑", "未"), ("寅", "申"), 
            ("卯", "酉"), ("辰", "戌"), ("巳", "亥")
        }
        
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):
                pair = (branches[i], branches[j])
                if pair in conflicts or (branches[j], branches[i]) in conflicts:
                    results["branch_conflicts"].append({
                        "type": "地支六冲",
                        "combination": f"{branches[i]}{branches[j]}",
                        "positions": [f"第{i+1}柱支", f"第{j+1}柱支"]
                    })
        
        return results
    
    # 执行分析
    interactions = analyze_simple_interactions(bazi)
    
    print("=== 干支互动分析测试结果 ===")
    print(f"八字: {bazi.year}{bazi.month}{bazi.day}{bazi.hour}")
    print(f"天干五合: {interactions['stem_combinations']}")
    print(f"地支六冲: {interactions['branch_conflicts']}")
    print(f"摘要: {interactions['summary']}")
    
    return interactions

if __name__ == "__main__":
    test_interactions()
