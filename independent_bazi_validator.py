"""
独立的八字排盘验证系统
不依赖复杂的backend导入，直接进行四柱计算验证
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# JIAZI 六十甲子表
JIAZI_TABLE = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]

# 天干五行属性
STEM_ELEMENTS = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火", 
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支五行属性
BRANCH_ELEMENTS = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

class IndependentBaziValidator:
    """独立的八字验证器"""
    
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.validation_results = []
        
    def load_test_cases(self):
        """加载测试案例"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"加载测试案例失败: {e}")
            return []
    
    def calculate_pillars(self, birth_time: datetime) -> Dict[str, str]:
        """计算四柱（简化算法）"""
        year = birth_time.year
        month = birth_time.month
        day = birth_time.day
        hour = birth_time.hour
        
        # 计算年柱 (以1984甲子年为基准)
        year_index = (year - 1984) % 60
        if year_index < 0:
            year_index += 60
        year_jiazi = JIAZI_TABLE[year_index]
        
        # 计算月柱 (简化算法，实际需要考虑节气)
        month_index = ((year - 1984) * 12 + month - 1) % 60
        month_jiazi = JIAZI_TABLE[month_index]
        
        # 计算日柱 (以1984年1月1日为基准)
        base_date = datetime(1984, 1, 1)
        days_diff = (birth_time.date() - base_date.date()).days
        day_index = days_diff % 60
        day_jiazi = JIAZI_TABLE[day_index]
        
        # 计算时柱
        hour_index = (days_diff * 12 + hour // 2) % 60
        hour_jiazi = JIAZI_TABLE[hour_index]
        
        return {
            "年柱": year_jiazi,
            "月柱": month_jiazi,
            "日柱": day_jiazi,
            "时柱": hour_jiazi
        }
    
    def calculate_five_elements(self, pillars: Dict[str, str]) -> Dict[str, float]:
        """计算五行得分"""
        elements = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}
        
        # 天干得分
        for pillar_jiazi in pillars.values():
            stem = pillar_jiazi[0]
            branch = pillar_jiazi[1]
            
            # 天干得分
            stem_element = STEM_ELEMENTS.get(stem, "")
            if stem_element:
                elements[stem_element] += 1.0
            
            # 地支得分
            branch_element = BRANCH_ELEMENTS.get(branch, "")
            if branch_element:
                elements[branch_element] += 0.8
        
        # 转换为百分比
        total = sum(elements.values())
        if total > 0:
            for element in elements:
                elements[element] = elements[element] / total
        
        return elements
    
    def analyze_strength(self, pillars: Dict[str, str], five_elements: Dict[str, float]) -> str:
        """分析日主旺衰"""
        day_stem = pillars["日柱"][0]
        day_master_element = STEM_ELEMENTS.get(day_stem, "")
        day_master_score = five_elements.get(day_master_element, 0)
        
        if day_master_score > 0.4:
            return "身强"
        elif day_master_score > 0.3:
            return "偏强"
        elif day_master_score > 0.2:
            return "中和"
        elif day_master_score > 0.1:
            return "偏弱"
        else:
            return "身弱"
    
    def validate_single_case(self, test_case: Dict) -> Dict:
        """验证单个案例"""
        try:
            # 处理CSV列名中的BOM字符
            case_id_key = next((k for k in test_case.keys() if "案例编号" in k), "案例编号")
            case_id = test_case[case_id_key]
            name = test_case["姓名"]
            
            # 解析生日
            year = int(test_case["阳历生日_年"])
            month = int(test_case["阳历生日_月"])
            day = int(test_case["阳历生日_日"])
            hour = int(test_case["阳历生日_时"])
            minute = int(test_case["阳历生日_分"])
            
            birth_time = datetime(year, month, day, hour, minute)
            
            # 标准答案
            expected_pillars = {
                "年柱": test_case["标准_年柱"].split("（")[0],
                "月柱": test_case["标准_月柱"].split("（")[0],
                "日柱": test_case["标准_日柱"].split("（")[0],
                "时柱": test_case["标准_时柱"].split("（")[0]
            }
            
            expected_elements = {
                "木": float(test_case["标准_五行得分_木"].replace('%', '')) / 100,
                "火": float(test_case["标准_五行得分_火"].replace('%', '')) / 100,
                "土": float(test_case["标准_五行得分_土"].replace('%', '')) / 100,
                "金": float(test_case["标准_五行得分_金"].replace('%', '')) / 100,
                "水": float(test_case["标准_五行得分_水"].replace('%', '')) / 100
            }
            
            expected_strength = test_case["标准_日主旺衰"]
            
            # 计算四柱
            calculated_pillars = self.calculate_pillars(birth_time)
            
            # 计算五行
            calculated_elements = self.calculate_five_elements(calculated_pillars)
            
            # 分析旺衰
            calculated_strength = self.analyze_strength(calculated_pillars, calculated_elements)
            
            # 比较结果
            pillar_matches = 0
            for pillar_name in ["年柱", "月柱", "日柱", "时柱"]:
                if calculated_pillars[pillar_name] == expected_pillars[pillar_name]:
                    pillar_matches += 1
            
            pillar_accuracy = pillar_matches / 4
            
            # 五行误差计算
            element_errors = []
            for element in ["木", "火", "土", "金", "水"]:
                error = abs(calculated_elements[element] - expected_elements[element])
                element_errors.append(error)
            
            avg_element_error = sum(element_errors) / len(element_errors)
            element_accuracy = max(0, 1 - avg_element_error * 2)  # 误差越小准确率越高
            
            # 旺衰匹配
            strength_keywords = ["身强", "身弱", "偏强", "偏弱", "中和", "平和"]
            strength_match = False
            for keyword in strength_keywords:
                if keyword in expected_strength and keyword == calculated_strength:
                    strength_match = True
                    break
            
            # 总体准确率
            overall_accuracy = pillar_accuracy * 0.5 + element_accuracy * 0.3 + (1.0 if strength_match else 0.0) * 0.2
            
            return {
                "案例编号": case_id,
                "姓名": name,
                "四柱对比": {
                    "期望": expected_pillars,
                    "计算": calculated_pillars,
                    "匹配数": pillar_matches,
                    "准确率": pillar_accuracy
                },
                "五行对比": {
                    "期望": {k: f"{v:.1%}" for k, v in expected_elements.items()},
                    "计算": {k: f"{v:.1%}" for k, v in calculated_elements.items()},
                    "平均误差": f"{avg_element_error:.1%}",
                    "准确率": element_accuracy
                },
                "旺衰对比": {
                    "期望": expected_strength,
                    "计算": calculated_strength,
                    "匹配": strength_match
                },
                "总体准确率": overall_accuracy
            }
            
        except Exception as e:
            return {
                "案例编号": case_id,
                "姓名": name,
                "错误": str(e),
                "总体准确率": 0.0
            }
    
    def run_validation(self, max_cases: int = 10) -> Dict:
        """运行验证"""
        print("开始八字排盘算法验证...")
        
        test_cases = self.load_test_cases()
        if not test_cases:
            return {"error": "无法加载测试案例"}
        
        # 限制测试案例数量
        test_cases = test_cases[:max_cases]
        
        results = []
        total_accuracy = 0
        pillar_accuracy_sum = 0
        element_accuracy_sum = 0
        strength_matches = 0
        
        for i, test_case in enumerate(test_cases):
            print(f"验证案例 {i+1}/{len(test_cases)}: {test_case['姓名']}")
            
            result = self.validate_single_case(test_case)
            results.append(result)
            
            if "错误" not in result:
                total_accuracy += result["总体准确率"]
                pillar_accuracy_sum += result["四柱对比"]["准确率"]
                element_accuracy_sum += result["五行对比"]["准确率"]
                if result["旺衰对比"]["匹配"]:
                    strength_matches += 1
        
        # 计算统计信息
        successful_cases = len([r for r in results if "错误" not in r])
        if successful_cases > 0:
            avg_accuracy = total_accuracy / successful_cases
            avg_pillar_accuracy = pillar_accuracy_sum / successful_cases
            avg_element_accuracy = element_accuracy_sum / successful_cases
            strength_accuracy = strength_matches / successful_cases
        else:
            avg_accuracy = avg_pillar_accuracy = avg_element_accuracy = strength_accuracy = 0
        
        return {
            "summary": {
                "total_cases": len(results),
                "successful_cases": successful_cases,
                "failed_cases": len(results) - successful_cases,
                "avg_accuracy": avg_accuracy,
                "pillar_accuracy": avg_pillar_accuracy,
                "element_accuracy": avg_element_accuracy,
                "strength_accuracy": strength_accuracy
            },
            "results": results
        }

def main():
    """主函数"""
    csv_file = "八字命理案例数据.csv"
    
    validator = IndependentBaziValidator(csv_file)
    report = validator.run_validation(max_cases=15)  # 验证前15个案例
    
    if "error" in report:
        print(f"验证失败: {report['error']}")
        return
    
    summary = report["summary"]
    
    print("\n" + "="*60)
    print("八字排盘算法验证报告")
    print("="*60)
    print(f"总测试案例: {summary['total_cases']}")
    print(f"成功案例: {summary['successful_cases']}")
    print(f"失败案例: {summary['failed_cases']}")
    print(f"总体准确率: {summary['avg_accuracy']:.1%}")
    print(f"四柱准确率: {summary['pillar_accuracy']:.1%}")
    print(f"五行准确率: {summary['element_accuracy']:.1%}")
    print(f"旺衰准确率: {summary['strength_accuracy']:.1%}")
    print()
    
    print("详细结果:")
    for i, result in enumerate(report["results"][:5]):  # 显示前5个详细结果
        print(f"\n案例 {i+1}: {result['姓名']}")
        if "错误" in result:
            print(f"  错误: {result['错误']}")
        else:
            print(f"  总体准确率: {result['总体准确率']:.1%}")
            print(f"  四柱匹配: {result['四柱对比']['匹配数']}/4")
            print(f"  五行误差: {result['五行对比']['平均误差']}")
            print(f"  旺衰匹配: {result['旺衰对比']['匹配']}")
    
    # 保存详细报告
    with open("validation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细报告已保存到: validation_report.json")

if __name__ == "__main__":
    main()
