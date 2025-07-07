"""
八字排盘算法验证和迭代系统
基于CSV案例数据，验证和改进八字排盘算法的准确性
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import os
import sys

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.app.services.calculators import ShenShaCalculator, FiveElementsCalculator
from backend.app.services.core import Bazi, StemBranch
from backend.app.services.simple_bazi_calculator import SimpleBaziCalculator
from backend.app.services.logger_config import setup_logger

logger = setup_logger("bazi_validation")

class BaziValidationSystem:
    """八字排盘算法验证系统"""
    
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.validation_results = []
        self.test_cases = []
        self.accuracy_stats = {
            "total_cases": 0,
            "pillar_accuracy": {"年柱": 0, "月柱": 0, "日柱": 0, "时柱": 0},
            "element_accuracy": {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0},
            "strength_accuracy": 0,
            "favorable_god_accuracy": 0,
            "dayun_accuracy": 0
        }
    
    def load_test_cases(self):
        """加载测试案例"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.test_cases.append(row)
            
            logger.info(f"成功加载 {len(self.test_cases)} 个测试案例")
            return True
            
        except Exception as e:
            logger.error(f"加载测试案例失败: {e}")
            return False
    
    def validate_single_case(self, test_case: Dict) -> Dict:
        """验证单个测试案例"""
        try:
            # 解析测试案例数据
            case_id = test_case["案例编号"]
            name = test_case["姓名"]
            
            # 构建生日信息
            year = int(test_case["阳历生日_年"])
            month = int(test_case["阳历生日_月"])
            day = int(test_case["阳历生日_日"])
            hour = int(test_case["阳历生日_时"])
            minute = int(test_case["阳历生日_分"])
            
            # 标准答案
            expected_pillars = {
                "年柱": test_case["标准_年柱"],
                "月柱": test_case["标准_月柱"],
                "日柱": test_case["标准_日柱"],
                "时柱": test_case["标准_时柱"]
            }
            
            expected_strength = test_case["标准_日主旺衰"]
            expected_elements = {
                "木": float(test_case["标准_五行得分_木"].replace('%', '')) / 100,
                "火": float(test_case["标准_五行得分_火"].replace('%', '')) / 100,
                "土": float(test_case["标准_五行得分_土"].replace('%', '')) / 100,
                "金": float(test_case["标准_五行得分_金"].replace('%', '')) / 100,
                "水": float(test_case["标准_五行得分_水"].replace('%', '')) / 100
            }
            
            expected_favorable_god = test_case["标准_喜用神"]
            expected_dayun_age = test_case["标准_起运年"] if test_case["标准_起运年"] != "缺" else None
            
            # 使用我们的算法计算
            birth_time = datetime(year, month, day, hour, minute)
            calculator = SimpleBaziCalculator()
            
            # 计算八字
            bazi_result = calculator.calculate_bazi(birth_time, use_true_solar=test_case["是否真太阳时"] == "是")
            
            # 验证结果
            validation_result = {
                "案例编号": case_id,
                "姓名": name,
                "输入": {
                    "生日": f"{year}-{month}-{day} {hour}:{minute}",
                    "真太阳时": test_case["是否真太阳时"] == "是"
                },
                "四柱对比": {},
                "五行对比": {},
                "旺衰对比": {},
                "喜用神对比": {},
                "起运对比": {},
                "准确率": {}
            }
            
            # 比较四柱
            calculated_pillars = {
                "年柱": f"{bazi_result['bazi']['year_pillar']['stem']}{bazi_result['bazi']['year_pillar']['branch']}",
                "月柱": f"{bazi_result['bazi']['month_pillar']['stem']}{bazi_result['bazi']['month_pillar']['branch']}",
                "日柱": f"{bazi_result['bazi']['day_pillar']['stem']}{bazi_result['bazi']['day_pillar']['branch']}",
                "时柱": f"{bazi_result['bazi']['hour_pillar']['stem']}{bazi_result['bazi']['hour_pillar']['branch']}"
            }
            
            pillar_accuracy = 0
            for pillar_name, expected in expected_pillars.items():
                calculated = calculated_pillars[pillar_name]
                expected_clean = expected.split("（")[0]  # 去掉纳音部分
                is_correct = calculated == expected_clean
                
                validation_result["四柱对比"][pillar_name] = {
                    "期望": expected_clean,
                    "计算": calculated,
                    "正确": is_correct
                }
                
                if is_correct:
                    pillar_accuracy += 1
            
            pillar_accuracy = pillar_accuracy / 4
            validation_result["准确率"]["四柱"] = pillar_accuracy
            
            # 比较五行得分
            calculated_elements = bazi_result.get("five_elements", {})
            element_accuracy = 0
            element_count = 0
            
            for element, expected_score in expected_elements.items():
                if element in calculated_elements:
                    calculated_score = calculated_elements[element].get("percentage", 0)
                    score_diff = abs(calculated_score - expected_score)
                    is_accurate = score_diff <= 0.05  # 允许5%的误差
                    
                    validation_result["五行对比"][element] = {
                        "期望": f"{expected_score:.1%}",
                        "计算": f"{calculated_score:.1%}",
                        "误差": f"{score_diff:.1%}",
                        "准确": is_accurate
                    }
                    
                    if is_accurate:
                        element_accuracy += 1
                    element_count += 1
            
            if element_count > 0:
                element_accuracy = element_accuracy / element_count
                validation_result["准确率"]["五行"] = element_accuracy
            
            # 比较旺衰
            calculated_strength = bazi_result.get("strength_analysis", {}).get("conclusion", "")
            strength_match = self._compare_strength(expected_strength, calculated_strength)
            validation_result["旺衰对比"] = {
                "期望": expected_strength,
                "计算": calculated_strength,
                "匹配": strength_match
            }
            validation_result["准确率"]["旺衰"] = 1.0 if strength_match else 0.0
            
            # 比较喜用神
            calculated_favorable = bazi_result.get("favorable_elements", {})
            favorable_match = self._compare_favorable_gods(expected_favorable_god, calculated_favorable)
            validation_result["喜用神对比"] = {
                "期望": expected_favorable_god,
                "计算": calculated_favorable,
                "匹配": favorable_match
            }
            validation_result["准确率"]["喜用神"] = 1.0 if favorable_match else 0.0
            
            # 总体准确率
            overall_accuracy = (
                pillar_accuracy * 0.4 +
                element_accuracy * 0.3 +
                validation_result["准确率"]["旺衰"] * 0.2 +
                validation_result["准确率"]["喜用神"] * 0.1
            )
            validation_result["准确率"]["总体"] = overall_accuracy
            
            return validation_result
            
        except Exception as e:
            logger.error(f"验证案例 {case_id} 失败: {e}")
            return {
                "案例编号": case_id,
                "姓名": name,
                "错误": str(e),
                "准确率": {"总体": 0.0}
            }
    
    def _compare_strength(self, expected: str, calculated: str) -> bool:
        """比较旺衰结果"""
        # 简化的旺衰匹配逻辑
        expected_keywords = ["身强", "身弱", "偏强", "偏弱", "中和", "平和"]
        calculated_keywords = ["身强", "身弱", "偏强", "偏弱", "中和", "平和"]
        
        expected_main = None
        calculated_main = None
        
        for keyword in expected_keywords:
            if keyword in expected:
                expected_main = keyword
                break
        
        for keyword in calculated_keywords:
            if keyword in calculated:
                calculated_main = keyword
                break
        
        if expected_main and calculated_main:
            # 模糊匹配
            if expected_main == calculated_main:
                return True
            elif expected_main in ["身强", "偏强"] and calculated_main in ["身强", "偏强"]:
                return True
            elif expected_main in ["身弱", "偏弱"] and calculated_main in ["身弱", "偏弱"]:
                return True
            elif expected_main in ["中和", "平和"] and calculated_main in ["中和", "平和"]:
                return True
        
        return False
    
    def _compare_favorable_gods(self, expected: str, calculated: Dict) -> bool:
        """比较喜用神结果"""
        # 简化的喜用神匹配逻辑
        expected_elements = []
        element_map = {"木": "木", "火": "火", "土": "土", "金": "金", "水": "水"}
        
        for element in element_map:
            if element in expected:
                expected_elements.append(element)
        
        calculated_elements = []
        if "primary" in calculated:
            calculated_elements.extend(calculated["primary"])
        if "secondary" in calculated:
            calculated_elements.extend(calculated["secondary"])
        
        # 检查是否有匹配
        return len(set(expected_elements) & set(calculated_elements)) > 0
    
    def run_validation(self) -> Dict:
        """运行完整验证"""
        logger.info("开始八字排盘算法验证")
        
        if not self.load_test_cases():
            return {"error": "加载测试案例失败"}
        
        self.validation_results = []
        successful_cases = 0
        
        for i, test_case in enumerate(self.test_cases[:20]):  # 先验证前20个案例
            logger.info(f"验证案例 {i+1}/{len(self.test_cases[:20])}: {test_case['姓名']}")
            
            result = self.validate_single_case(test_case)
            self.validation_results.append(result)
            
            if "错误" not in result:
                successful_cases += 1
        
        # 计算统计信息
        self._calculate_statistics()
        
        # 生成报告
        report = {
            "validation_summary": {
                "total_cases": len(self.validation_results),
                "successful_cases": successful_cases,
                "failed_cases": len(self.validation_results) - successful_cases,
                "overall_accuracy": self.accuracy_stats
            },
            "detailed_results": self.validation_results[:10],  # 显示前10个详细结果
            "recommendations": self._generate_recommendations()
        }
        
        logger.info(f"验证完成，总体准确率: {self.accuracy_stats.get('overall_accuracy', 0):.1%}")
        
        return report
    
    def _calculate_statistics(self):
        """计算统计信息"""
        if not self.validation_results:
            return
        
        total_accuracy = 0
        pillar_accuracies = {"年柱": 0, "月柱": 0, "日柱": 0, "时柱": 0}
        element_accuracies = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        strength_accuracy = 0
        favorable_accuracy = 0
        
        valid_cases = 0
        
        for result in self.validation_results:
            if "错误" in result:
                continue
            
            valid_cases += 1
            accuracy = result.get("准确率", {})
            
            # 总体准确率
            total_accuracy += accuracy.get("总体", 0)
            
            # 四柱准确率
            pillars = result.get("四柱对比", {})
            for pillar_name, pillar_data in pillars.items():
                if pillar_data.get("正确", False):
                    pillar_accuracies[pillar_name] += 1
            
            # 五行准确率
            elements = result.get("五行对比", {})
            for element, element_data in elements.items():
                if element_data.get("准确", False):
                    element_accuracies[element] += 1
            
            # 旺衰准确率
            strength_accuracy += accuracy.get("旺衰", 0)
            
            # 喜用神准确率
            favorable_accuracy += accuracy.get("喜用神", 0)
        
        if valid_cases > 0:
            self.accuracy_stats = {
                "total_cases": valid_cases,
                "overall_accuracy": total_accuracy / valid_cases,
                "pillar_accuracy": {k: v / valid_cases for k, v in pillar_accuracies.items()},
                "element_accuracy": {k: v / valid_cases for k, v in element_accuracies.items()},
                "strength_accuracy": strength_accuracy / valid_cases,
                "favorable_god_accuracy": favorable_accuracy / valid_cases
            }
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 根据准确率统计生成建议
        if self.accuracy_stats.get("overall_accuracy", 0) < 0.8:
            recommendations.append("总体准确率偏低，建议全面检查算法实现")
        
        # 四柱准确率分析
        pillar_acc = self.accuracy_stats.get("pillar_accuracy", {})
        for pillar, acc in pillar_acc.items():
            if acc < 0.9:
                recommendations.append(f"{pillar}准确率为{acc:.1%}，建议检查{pillar}计算逻辑")
        
        # 五行准确率分析
        element_acc = self.accuracy_stats.get("element_accuracy", {})
        low_accuracy_elements = [elem for elem, acc in element_acc.items() if acc < 0.7]
        if low_accuracy_elements:
            recommendations.append(f"五行得分计算需要优化，特别是: {', '.join(low_accuracy_elements)}")
        
        # 旺衰分析
        if self.accuracy_stats.get("strength_accuracy", 0) < 0.7:
            recommendations.append("日主旺衰判断准确率偏低，建议优化旺衰分析算法")
        
        # 喜用神分析
        if self.accuracy_stats.get("favorable_god_accuracy", 0) < 0.6:
            recommendations.append("喜用神分析准确率偏低，建议完善喜用神判断逻辑")
        
        if not recommendations:
            recommendations.append("算法表现良好，可以考虑在更多案例上进行验证")
        
        return recommendations
    
    def save_report(self, filename: str = "bazi_validation_report.json"):
        """保存验证报告"""
        try:
            report = {
                "validation_time": datetime.now().isoformat(),
                "accuracy_stats": self.accuracy_stats,
                "detailed_results": self.validation_results,
                "recommendations": self._generate_recommendations()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            logger.info(f"验证报告已保存到: {filename}")
            
        except Exception as e:
            logger.error(f"保存报告失败: {e}")

def main():
    """主函数"""
    # CSV文件路径
    csv_file = "八字命理案例数据.csv"
    
    # 创建验证系统
    validator = BaziValidationSystem(csv_file)
    
    # 运行验证
    report = validator.run_validation()
    
    # 打印结果
    print("=" * 60)
    print("八字排盘算法验证报告")
    print("=" * 60)
    
    if "error" in report:
        print(f"验证失败: {report['error']}")
        return
    
    summary = report["validation_summary"]
    print(f"总测试案例: {summary['total_cases']}")
    print(f"成功案例: {summary['successful_cases']}")
    print(f"失败案例: {summary['failed_cases']}")
    print(f"总体准确率: {summary['overall_accuracy'].get('overall_accuracy', 0):.1%}")
    print()
    
    print("分项准确率:")
    stats = summary['overall_accuracy']
    print(f"  四柱准确率: {stats.get('pillar_accuracy', {})}")
    print(f"  五行准确率: {stats.get('element_accuracy', {})}")
    print(f"  旺衰准确率: {stats.get('strength_accuracy', 0):.1%}")
    print(f"  喜用神准确率: {stats.get('favorable_god_accuracy', 0):.1%}")
    print()
    
    print("改进建议:")
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"  {i}. {rec}")
    
    # 保存详细报告
    validator.save_report()

if __name__ == "__main__":
    main()
