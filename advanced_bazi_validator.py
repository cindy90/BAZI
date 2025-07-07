#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高级八字算法验证器 - 第二次迭代
基于更精确的算法进行批量验证
"""

import csv
import json
from typing import Dict, List, Tuple
from advanced_bazi_calculator import AdvancedBaziCalculator

class AdvancedBaziValidator:
    def __init__(self):
        self.calculator = AdvancedBaziCalculator()
        
    def parse_date_from_case(self, case_data: Dict) -> Tuple[int, int, int, int]:
        """从案例数据解析出生日期"""
        birth_info = case_data.get('出生时间', '')
        
        # 解析格式如 "1988年12月21日10时"
        try:
            if '年' in birth_info and '月' in birth_info and '日' in birth_info:
                parts = birth_info.replace('年', '-').replace('月', '-').replace('日', '-').replace('时', '')
                date_parts = parts.split('-')
                year = int(date_parts[0])
                month = int(date_parts[1])
                day = int(date_parts[2])
                hour = int(date_parts[3]) if len(date_parts) > 3 and date_parts[3] else 0
                return year, month, day, hour
        except:
            pass
            
        # 默认值
        return 1990, 1, 1, 0
    
    def parse_expected_pillars(self, case_data: Dict) -> Dict[str, str]:
        """解析期望的四柱"""
        bazi = case_data.get('八字', '')
        if len(bazi) >= 8:
            return {
                '年柱': bazi[0:2],
                '月柱': bazi[2:4],
                '日柱': bazi[4:6],
                '时柱': bazi[6:8]
            }
        return {'年柱': '', '月柱': '', '日柱': '', '时柱': ''}
    
    def parse_expected_elements(self, case_data: Dict) -> Dict[str, float]:
        """解析期望的五行分布"""
        elements = {'木': 0.0, '火': 0.0, '土': 0.0, '金': 0.0, '水': 0.0}
        
        for element in elements:
            key = f'五行_{element}'
            if key in case_data and case_data[key]:
                try:
                    value = float(case_data[key].replace('%', '')) / 100
                    elements[element] = value
                except:
                    pass
                    
        return elements
    
    def parse_expected_strength(self, case_data: Dict) -> str:
        """解析期望的旺衰"""
        return case_data.get('旺衰', '').strip()
    
    def compare_pillars(self, expected: Dict[str, str], calculated: Dict[str, str]) -> Dict:
        """比较四柱"""
        details = {}
        matches = 0
        
        for position in ['年柱', '月柱', '日柱', '时柱']:
            expected_pillar = expected.get(position, '')
            calculated_pillar = calculated.get(position, '')
            is_match = expected_pillar == calculated_pillar
            
            details[position] = {
                '期望': expected_pillar,
                '计算': calculated_pillar,
                '匹配': is_match
            }
            
            if is_match:
                matches += 1
                
        return {
            '详情': details,
            '匹配数': matches,
            '准确率': matches / 4
        }
    
    def compare_elements(self, expected: Dict[str, float], calculated: Dict[str, float]) -> Dict:
        """比较五行分布"""
        details = {}
        total_error = 0
        accurate_count = 0
        
        for element in ['木', '火', '土', '金', '水']:
            expected_val = expected.get(element, 0)
            calculated_val = calculated.get(element, 0)
            error = abs(expected_val - calculated_val)
            
            details[element] = {
                '期望': f"{expected_val:.1%}",
                '计算': f"{calculated_val:.1%}",
                '误差': f"{error:.1%}",
                '准确': error <= 0.1  # 10%以内算准确
            }
            
            total_error += error
            if error <= 0.1:
                accurate_count += 1
        
        return {
            '详情': details,
            '平均误差': f"{total_error/5:.1%}",
            '准确率': 1 - (total_error / 5)
        }
    
    def compare_strength(self, expected: str, calculated: str) -> bool:
        """比较旺衰"""
        # 标准化旺衰描述
        strength_mapping = {
            '身旺': ['身旺', '旺', '强'],
            '偏强': ['偏强', '较强'],
            '中和': ['中和', '平衡'],
            '偏弱': ['偏弱', '较弱'],
            '身弱': ['身弱', '弱']
        }
        
        calculated_normalized = calculated.split('（')[0].strip()
        
        for standard, variants in strength_mapping.items():
            if any(variant in expected for variant in variants):
                expected_standard = standard
                break
        else:
            expected_standard = expected
            
        return expected_standard == calculated_normalized
    
    def calculate_overall_accuracy(self, pillar_accuracy: float, element_accuracy: float, strength_match: bool) -> float:
        """计算总体准确率"""
        strength_score = 1.0 if strength_match else 0.0
        return (pillar_accuracy * 0.4 + element_accuracy * 0.4 + strength_score * 0.2)
    
    def validate_cases(self, csv_file: str = '八字命理案例数据.csv') -> Dict:
        """批量验证案例"""
        results = []
        total_pillar_accuracy = 0
        total_element_accuracy = 0
        total_strength_accuracy = 0
        successful_cases = 0
        
        print("开始高级算法验证...")
        
        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                cases = list(reader)
                
            for i, case_data in enumerate(cases[:15], 1):  # 限制测试15个案例
                try:
                    print(f"验证案例 {i}/{len(cases[:15])}: {case_data.get('姓名', f'案例{i}')}")
                    
                    # 解析输入数据
                    year, month, day, hour = self.parse_date_from_case(case_data)
                    expected_pillars = self.parse_expected_pillars(case_data)
                    expected_elements = self.parse_expected_elements(case_data)
                    expected_strength = self.parse_expected_strength(case_data)
                    
                    # 计算八字
                    result = self.calculator.calculate_bazi(year, month, day, hour)
                    
                    calculated_pillars = {
                        '年柱': result.year_pillar,
                        '月柱': result.month_pillar,
                        '日柱': result.day_pillar,
                        '时柱': result.hour_pillar
                    }
                    
                    # 比较结果
                    pillar_comparison = self.compare_pillars(expected_pillars, calculated_pillars)
                    element_comparison = self.compare_elements(expected_elements, result.elements)
                    strength_match = self.compare_strength(expected_strength, result.strength)
                    
                    overall_accuracy = self.calculate_overall_accuracy(
                        pillar_comparison['准确率'],
                        element_comparison['准确率'],
                        strength_match
                    )
                    
                    case_result = {
                        '案例编号': case_data.get('编号', str(i)),
                        '姓名': case_data.get('姓名', f'案例{i}'),
                        '四柱对比': pillar_comparison,
                        '五行对比': element_comparison,
                        '旺衰对比': {
                            '期望': expected_strength,
                            '计算': result.analysis['conclusion'],
                            '匹配': strength_match
                        },
                        '总体准确率': overall_accuracy,
                        '详细分析': result.analysis
                    }
                    
                    results.append(case_result)
                    
                    total_pillar_accuracy += pillar_comparison['准确率']
                    total_element_accuracy += element_comparison['准确率']
                    if strength_match:
                        total_strength_accuracy += 1
                        
                    successful_cases += 1
                    
                except Exception as e:
                    print(f"案例 {i} 验证失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"读取CSV文件失败: {e}")
            return {}
        
        # 计算总体统计
        if successful_cases > 0:
            avg_pillar_accuracy = total_pillar_accuracy / successful_cases
            avg_element_accuracy = total_element_accuracy / successful_cases
            avg_strength_accuracy = total_strength_accuracy / successful_cases
            overall_avg_accuracy = sum(r['总体准确率'] for r in results) / len(results)
            
            summary = {
                'total_cases': len(cases[:15]),
                'successful_cases': successful_cases,
                'failed_cases': len(cases[:15]) - successful_cases,
                'avg_accuracy': overall_avg_accuracy,
                'pillar_accuracy': avg_pillar_accuracy,
                'element_accuracy': avg_element_accuracy,
                'strength_accuracy': avg_strength_accuracy
            }
            
            report = {
                'summary': summary,
                'results': results
            }
            
            # 保存报告
            with open('advanced_validation_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            # 打印统计信息
            print("=" * 60)
            print("高级算法验证报告")
            print("=" * 60)
            print(f"总测试案例: {summary['total_cases']}")
            print(f"成功案例: {summary['successful_cases']}")
            print(f"失败案例: {summary['failed_cases']}")
            print(f"总体准确率: {overall_avg_accuracy:.1%}")
            print(f"四柱准确率: {avg_pillar_accuracy:.1%}")
            print(f"五行准确率: {avg_element_accuracy:.1%}")
            print(f"旺衰准确率: {avg_strength_accuracy:.1%}")
            
            # 显示前几个详细结果
            print("详细结果示例:")
            for i, result in enumerate(results[:3]):
                print(f"案例 {result['案例编号']}: {result['姓名']}")
                print(f"  总体准确率: {result['总体准确率']:.1%}")
                print(f"  四柱匹配: {result['四柱对比']['匹配数']}/4")
                print(f"  五行误差: {result['五行对比']['平均误差']}")
                print(f"  旺衰: {result['旺衰对比']['期望']}（{result['旺衰对比']['计算']}）")
                
            print(f"详细报告已保存到: advanced_validation_report.json")
            return report
        else:
            print("没有成功验证的案例")
            return {}

def main():
    validator = AdvancedBaziValidator()
    validator.validate_cases()

if __name__ == "__main__":
    main()
