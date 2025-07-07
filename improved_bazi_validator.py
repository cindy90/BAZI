"""
使用改进算法的八字验证系统
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Optional
from improved_bazi_calculator import ImprovedBaziCalculator

class ImprovedBaziValidator:
    """使用改进算法的验证器"""
    
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.calculator = ImprovedBaziCalculator()
        
    def load_test_cases(self):
        """加载测试案例"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"加载测试案例失败: {e}")
            return []
    
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
            
            # 使用改进的算法计算
            calculated_pillars = self.calculator.calculate_pillars(birth_time)
            calculated_elements = self.calculator.calculate_five_elements_with_hidden_stems(calculated_pillars)
            calculated_strength_analysis = self.calculator.analyze_strength_improved(
                calculated_pillars, calculated_elements, birth_time
            )
            
            # 格式化四柱结果
            calculated_pillars_formatted = {
                "年柱": calculated_pillars["年柱"]["jiazi"],
                "月柱": calculated_pillars["月柱"]["jiazi"],
                "日柱": calculated_pillars["日柱"]["jiazi"],
                "时柱": calculated_pillars["时柱"]["jiazi"]
            }
            
            # 比较结果
            pillar_matches = 0
            pillar_details = {}
            for pillar_name in ["年柱", "月柱", "日柱", "时柱"]:
                expected = expected_pillars[pillar_name]
                calculated = calculated_pillars_formatted[pillar_name]
                is_match = calculated == expected
                
                pillar_details[pillar_name] = {
                    "期望": expected,
                    "计算": calculated,
                    "匹配": is_match
                }
                
                if is_match:
                    pillar_matches += 1
            
            pillar_accuracy = pillar_matches / 4
            
            # 五行误差计算
            element_errors = []
            element_details = {}
            for element in ["木", "火", "土", "金", "水"]:
                expected_score = expected_elements[element]
                calculated_score = calculated_elements[element]
                error = abs(calculated_score - expected_score)
                element_errors.append(error)
                
                element_details[element] = {
                    "期望": f"{expected_score:.1%}",
                    "计算": f"{calculated_score:.1%}",
                    "误差": f"{error:.1%}",
                    "准确": error <= 0.05
                }
            
            avg_element_error = sum(element_errors) / len(element_errors)
            element_accuracy = max(0, 1 - avg_element_error * 2)
            
            # 旺衰匹配
            calculated_strength = calculated_strength_analysis["strength"]
            strength_match = self._compare_strength(expected_strength, calculated_strength)
            
            # 总体准确率
            overall_accuracy = pillar_accuracy * 0.5 + element_accuracy * 0.3 + (1.0 if strength_match else 0.0) * 0.2
            
            return {
                "案例编号": case_id,
                "姓名": name,
                "四柱对比": {
                    "详情": pillar_details,
                    "匹配数": pillar_matches,
                    "准确率": pillar_accuracy
                },
                "五行对比": {
                    "详情": element_details,
                    "平均误差": f"{avg_element_error:.1%}",
                    "准确率": element_accuracy
                },
                "旺衰对比": {
                    "期望": expected_strength,
                    "计算": f"{calculated_strength}（{calculated_strength_analysis['conclusion']}）",
                    "匹配": strength_match
                },
                "总体准确率": overall_accuracy,
                "详细分析": calculated_strength_analysis
            }
            
        except Exception as e:
            return {
                "案例编号": case_id,
                "姓名": name,
                "错误": str(e),
                "总体准确率": 0.0
            }
    
    def _compare_strength(self, expected: str, calculated: str) -> bool:
        """比较旺衰结果"""
        strength_keywords = ["身强", "身弱", "偏强", "偏弱", "中和", "平和"]
        
        expected_main = None
        calculated_main = calculated
        
        for keyword in strength_keywords:
            if keyword in expected:
                expected_main = keyword
                break
        
        if expected_main and calculated_main:
            if expected_main == calculated_main:
                return True
            elif expected_main in ["身强", "偏强"] and calculated_main in ["身强", "偏强"]:
                return True
            elif expected_main in ["身弱", "偏弱"] and calculated_main in ["身弱", "偏弱"]:
                return True
            elif expected_main in ["中和", "平和"] and calculated_main in ["中和", "平和"]:
                return True
        
        return False
    
    def run_validation(self, max_cases: int = 15) -> Dict:
        """运行验证"""
        print("开始改进算法验证...")
        
        test_cases = self.load_test_cases()
        if not test_cases:
            return {"error": "无法加载测试案例"}
        
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
    
    validator = ImprovedBaziValidator(csv_file)
    report = validator.run_validation(max_cases=15)
    
    if "error" in report:
        print(f"验证失败: {report['error']}")
        return
    
    summary = report["summary"]
    
    print("\n" + "="*60)
    print("改进算法验证报告")
    print("="*60)
    print(f"总测试案例: {summary['total_cases']}")
    print(f"成功案例: {summary['successful_cases']}")
    print(f"失败案例: {summary['failed_cases']}")
    print(f"总体准确率: {summary['avg_accuracy']:.1%}")
    print(f"四柱准确率: {summary['pillar_accuracy']:.1%}")
    print(f"五行准确率: {summary['element_accuracy']:.1%}")
    print(f"旺衰准确率: {summary['strength_accuracy']:.1%}")
    print()
    
    print("改进效果对比:")
    print("  之前四柱准确率: 31.7% -> 现在: {:.1%}".format(summary['pillar_accuracy']))
    print("  之前五行准确率: 73.4% -> 现在: {:.1%}".format(summary['element_accuracy']))
    print("  之前旺衰准确率: 13.3% -> 现在: {:.1%}".format(summary['strength_accuracy']))
    print("  之前总体准确率: 40.5% -> 现在: {:.1%}".format(summary['avg_accuracy']))
    print()
    
    print("详细结果示例:")
    for i, result in enumerate(report["results"][:3]):
        print(f"\n案例 {i+1}: {result['姓名']}")
        if "错误" in result:
            print(f"  错误: {result['错误']}")
        else:
            print(f"  总体准确率: {result['总体准确率']:.1%}")
            print(f"  四柱匹配: {result['四柱对比']['匹配数']}/4")
            print(f"  五行误差: {result['五行对比']['平均误差']}")
            print(f"  旺衰: {result['旺衰对比']['计算']}")
    
    # 保存详细报告
    with open("improved_validation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细报告已保存到: improved_validation_report.json")

if __name__ == "__main__":
    main()
