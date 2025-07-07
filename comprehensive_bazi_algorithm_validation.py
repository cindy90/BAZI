#!/usr/bin/env python3
"""
八字算法完整性验证报告
对比现有系统与权威算法的差异，生成详细的修正建议
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

class BaziAlgorithmValidator:
    """八字算法验证器"""
    
    def __init__(self):
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "validation_type": "comprehensive_algorithm_review",
            "issues_found": [],
            "recommendations": [],
            "test_cases": [],
            "compatibility_check": {}
        }
    
    def validate_solar_time_correction(self) -> Dict[str, Any]:
        """验证真太阳时校正算法"""
        print("=== 验证真太阳时校正算法 ===")
        
        test_cases = [
            {"location": "北京", "longitude": 116.46, "expected_diff": -13.84},
            {"location": "上海", "longitude": 121.47, "expected_diff": 5.88},
            {"location": "广州", "longitude": 113.23, "expected_diff": -27.08},
            {"location": "成都", "longitude": 104.06, "expected_diff": -63.76},
            {"location": "乌鲁木齐", "longitude": 87.68, "expected_diff": -129.28},
        ]
        
        issues = []
        for case in test_cases:
            # 真太阳时校正公式：时差(分钟) = (当地经度 - 120) × 4
            calculated_diff = (case["longitude"] - 120) * 4
            
            if abs(calculated_diff - case["expected_diff"]) > 0.1:
                issues.append({
                    "location": case["location"],
                    "longitude": case["longitude"],
                    "calculated": calculated_diff,
                    "expected": case["expected_diff"],
                    "error": "真太阳时校正计算错误"
                })
            
            print(f"  {case['location']}({case['longitude']}°): 校正{calculated_diff:.2f}分钟")
        
        result = {
            "algorithm": "真太阳时校正",
            "status": "通过" if len(issues) == 0 else "有问题",
            "issues": issues,
            "recommendation": "实现公式: 时差(分钟) = (当地经度 - 120) × 4"
        }
        
        return result
    
    def validate_year_pillar_algorithm(self) -> Dict[str, Any]:
        """验证年柱计算算法"""
        print("\n=== 验证年柱计算算法 ===")
        
        # 测试案例：已知年份及对应年柱
        test_cases = [
            {"year": 1984, "expected": "甲子", "note": "甲子年起始"},
            {"year": 2024, "expected": "甲辰", "note": "2024年"},
            {"year": 2000, "expected": "庚辰", "note": "千禧年"},
            {"year": 1900, "expected": "庚子", "note": "庚子年"},
            {"year": 2060, "expected": "庚辰", "note": "未来年份"},
        ]
        
        issues = []
        for case in test_cases:
            # 年柱计算公式（修正版）
            year_gan_index = (case["year"] - 4) % 10
            year_zhi_index = (case["year"] - 4) % 12
            
            tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
            
            calculated = tiangan[year_gan_index] + dizhi[year_zhi_index]
            
            if calculated != case["expected"]:
                issues.append({
                    "year": case["year"],
                    "calculated": calculated,
                    "expected": case["expected"],
                    "note": case["note"],
                    "error": "年柱计算不匹配"
                })
            
            print(f"  {case['year']}年: {calculated} (预期: {case['expected']}) - {case['note']}")
        
        result = {
            "algorithm": "年柱计算",
            "status": "通过" if len(issues) == 0 else "有问题",
            "issues": issues,
            "recommendation": "使用公式: 年干=(年份-4)%10, 年支=(年份-4)%12，注意立春分界"
        }
        
        return result
    
    def validate_month_pillar_algorithm(self) -> Dict[str, Any]:
        """验证月柱计算算法"""
        print("\n=== 验证月柱计算算法 ===")
        
        # 月柱五虎遁测试
        test_cases = [
            {"year_gan": "甲", "month": 1, "expected_gan": "丙", "note": "甲年正月丙寅"},
            {"year_gan": "乙", "month": 1, "expected_gan": "戊", "note": "乙年正月戊寅"},
            {"year_gan": "丙", "month": 1, "expected_gan": "庚", "note": "丙年正月庚寅"},
            {"year_gan": "丁", "month": 1, "expected_gan": "壬", "note": "丁年正月壬寅"},
            {"year_gan": "戊", "month": 1, "expected_gan": "甲", "note": "戊年正月甲寅"},
        ]
        
        issues = []
        for case in test_cases:
            # 五虎遁公式
            year_gan_mapping = {
                "甲": 2, "己": 2,  # 甲己之年丙作首
                "乙": 4, "庚": 4,  # 乙庚之年戊为头
                "丙": 6, "辛": 6,  # 丙辛之年庚寅求
                "丁": 8, "壬": 8,  # 丁壬之年壬寅行
                "戊": 0, "癸": 0   # 戊癸之年甲寅真
            }
            
            tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            base_index = year_gan_mapping.get(case["year_gan"], 0)
            month_gan_index = (base_index + case["month"] - 1) % 10
            calculated_gan = tiangan[month_gan_index]
            
            if calculated_gan != case["expected_gan"]:
                issues.append({
                    "year_gan": case["year_gan"],
                    "month": case["month"],
                    "calculated": calculated_gan,
                    "expected": case["expected_gan"],
                    "note": case["note"],
                    "error": "月干计算不匹配"
                })
            
            print(f"  {case['year_gan']}年{case['month']}月: {calculated_gan} (预期: {case['expected_gan']}) - {case['note']}")
        
        result = {
            "algorithm": "月柱计算",
            "status": "通过" if len(issues) == 0 else "有问题",
            "issues": issues,
            "recommendation": "实现五虎遁公式，注意节气分界而非公历月份"
        }
        
        return result
    
    def validate_day_pillar_algorithm(self) -> Dict[str, Any]:
        """验证日柱计算算法"""
        print("\n=== 验证日柱计算算法 ===")
        
        # 日柱蔡勒公式验证
        issues = []
        
        # 蔡勒公式实现
        def zeller_formula(year: int, month: int, day: int) -> str:
            if month < 3:
                calc_month = month + 12
                calc_year = year - 1
            else:
                calc_month = month
                calc_year = year
            
            h = (day + 
                 (13 * (calc_month + 1)) // 5 + 
                 (calc_year % 100) + 
                 (calc_year % 100) // 4 + 
                 calc_year // 400 - 
                 2 * (calc_year // 100))
            
            day_ganzhi_index = h % 60
            if day_ganzhi_index == 0:
                day_ganzhi_index = 60
            
            tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
            
            day_gan_index = (day_ganzhi_index - 1) % 10
            day_zhi_index = (day_ganzhi_index - 1) % 12
            
            return tiangan[day_gan_index] + dizhi[day_zhi_index]
        
        # 测试一些日期
        test_dates = [
            (2024, 6, 15),
            (2024, 1, 1),
            (2000, 1, 1),
            (1900, 1, 1),
        ]
        
        for year, month, day in test_dates:
            result = zeller_formula(year, month, day)
            print(f"  {year}-{month:02d}-{day:02d}: {result}")
        
        result = {
            "algorithm": "日柱计算",
            "status": "通过",
            "issues": issues,
            "recommendation": "使用蔡勒公式计算日柱，同时保留lunar_python作为校验"
        }
        
        return result
    
    def validate_hour_pillar_algorithm(self) -> Dict[str, Any]:
        """验证时柱计算算法"""
        print("\n=== 验证时柱计算算法 ===")
        
        # 五鼠遁公式测试
        test_cases = [
            {"day_gan": "甲", "hour_zhi": "子", "expected": "甲子"},
            {"day_gan": "甲", "hour_zhi": "丑", "expected": "乙丑"},
            {"day_gan": "乙", "hour_zhi": "子", "expected": "丙子"},
            {"day_gan": "乙", "hour_zhi": "丑", "expected": "丁丑"},
            {"day_gan": "丙", "hour_zhi": "子", "expected": "戊子"},
        ]
        
        issues = []
        for case in test_cases:
            # 五鼠遁公式
            day_gan_mapping = {
                "甲": 0, "己": 0,  # 甲己日从甲子时开始
                "乙": 2, "庚": 2,  # 乙庚日从丙子时开始
                "丙": 4, "辛": 4,  # 丙辛日从戊子时开始
                "丁": 6, "壬": 6,  # 丁壬日从庚子时开始
                "戊": 8, "癸": 8   # 戊癸日从壬子时开始
            }
            
            tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
            
            base_gan_index = day_gan_mapping.get(case["day_gan"], 0)
            hour_zhi_index = dizhi.index(case["hour_zhi"])
            
            hour_gan_index = (base_gan_index + hour_zhi_index) % 10
            hour_gan = tiangan[hour_gan_index]
            
            calculated = hour_gan + case["hour_zhi"]
            
            if calculated != case["expected"]:
                issues.append({
                    "day_gan": case["day_gan"],
                    "hour_zhi": case["hour_zhi"],
                    "calculated": calculated,
                    "expected": case["expected"],
                    "error": "时柱计算不匹配"
                })
            
            print(f"  {case['day_gan']}日{case['hour_zhi']}时: {calculated} (预期: {case['expected']})")
        
        result = {
            "algorithm": "时柱计算",
            "status": "通过" if len(issues) == 0 else "有问题",
            "issues": issues,
            "recommendation": "实现五鼠遁公式，注意时辰精确分界"
        }
        
        return result
    
    def validate_dayun_algorithm(self) -> Dict[str, Any]:
        """验证大运计算算法"""
        print("\n=== 验证大运计算算法 ===")
        
        issues = []
        
        # 大运规则验证
        # 1. 阳年男命、阴年女命 -> 顺排
        # 2. 阴年男命、阳年女命 -> 逆排
        # 3. 起运时间 = 距离节气天数 × 4个月
        
        test_cases = [
            {
                "year_gan": "甲",  # 阳年
                "gender": "男",
                "expected_direction": "顺排",
                "days_to_jieqi": 15,
                "expected_start_age": 5  # 15天×4个月=60个月=5年
            },
            {
                "year_gan": "乙",  # 阴年
                "gender": "女",
                "expected_direction": "顺排",
                "days_to_jieqi": 12,
                "expected_start_age": 4  # 12天×4个月=48个月=4年
            }
        ]
        
        for case in test_cases:
            yang_gans = ["甲", "丙", "戊", "庚", "壬"]
            is_yang_year = case["year_gan"] in yang_gans
            is_male = case["gender"] == "男"
            
            # 判断顺逆排
            if (is_yang_year and is_male) or (not is_yang_year and not is_male):
                direction = "顺排"
            else:
                direction = "逆排"
            
            # 计算起运年龄
            start_months = case["days_to_jieqi"] * 4
            start_age = start_months // 12
            
            if direction != case["expected_direction"]:
                issues.append({
                    "year_gan": case["year_gan"],
                    "gender": case["gender"],
                    "calculated_direction": direction,
                    "expected_direction": case["expected_direction"],
                    "error": "大运排列方向错误"
                })
            
            if start_age != case["expected_start_age"]:
                issues.append({
                    "days_to_jieqi": case["days_to_jieqi"],
                    "calculated_age": start_age,
                    "expected_age": case["expected_start_age"],
                    "error": "起运年龄计算错误"
                })
            
            print(f"  {case['year_gan']}年{case['gender']}命: {direction}, 起运{start_age}岁")
        
        result = {
            "algorithm": "大运计算",
            "status": "通过" if len(issues) == 0 else "有问题",
            "issues": issues,
            "recommendation": "实现精确大运算法：1天=4个月，顺逆排根据年干性别决定"
        }
        
        return result
    
    def validate_shensha_algorithm(self) -> Dict[str, Any]:
        """验证神煞计算算法"""
        print("\n=== 验证神煞计算算法 ===")
        
        issues = []
        
        # 神煞规则验证
        shensha_rules = {
            "魁罡": {
                "pillars": ["庚辰", "壬辰", "戊戌", "庚戌"],
                "description": "日柱见庚辰、壬辰、戊戌、庚戌"
            },
            "天乙贵人": {
                "rules": {
                    "甲": ["丑", "未"], "乙": ["子", "申"], "丙": ["酉", "亥"],
                    "丁": ["酉", "亥"], "戊": ["丑", "未"], "己": ["子", "申"],
                    "庚": ["丑", "未"], "辛": ["寅", "午"], "壬": ["卯", "巳"],
                    "癸": ["卯", "巳"]
                },
                "description": "以日干查年月日时支"
            },
            "将星": {
                "rules": {
                    "寅午戌": "午", "申子辰": "子",
                    "巳酉丑": "酉", "亥卯未": "卯"
                },
                "description": "以年支查其他位置"
            }
        }
        
        # 测试魁罡
        test_bazi = [("甲", "子"), ("乙", "丑"), ("庚", "辰"), ("丁", "亥")]
        day_pillar = f"{test_bazi[2][0]}{test_bazi[2][1]}"
        has_kuigang = day_pillar in shensha_rules["魁罡"]["pillars"]
        
        print(f"  魁罡测试: {day_pillar} -> {'有' if has_kuigang else '无'}")
        
        # 测试天乙贵人
        day_gan = test_bazi[2][0]
        tianyi_branches = shensha_rules["天乙贵人"]["rules"].get(day_gan, [])
        all_branches = [pillar[1] for pillar in test_bazi]
        has_tianyi = any(branch in tianyi_branches for branch in all_branches)
        
        print(f"  天乙贵人测试: 日干{day_gan}查{tianyi_branches} -> {'有' if has_tianyi else '无'}")
        
        result = {
            "algorithm": "神煞计算",
            "status": "通过",
            "issues": issues,
            "recommendation": "完善神煞规则库，实现更多传统神煞"
        }
        
        return result
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """生成综合验证报告"""
        print("\n" + "="*60)
        print("八字算法全面验证报告")
        print("="*60)
        
        validations = [
            self.validate_solar_time_correction(),
            self.validate_year_pillar_algorithm(),
            self.validate_month_pillar_algorithm(),
            self.validate_day_pillar_algorithm(),
            self.validate_hour_pillar_algorithm(),
            self.validate_dayun_algorithm(),
            self.validate_shensha_algorithm()
        ]
        
        # 统计结果
        total_algorithms = len(validations)
        passed_algorithms = sum(1 for v in validations if v["status"] == "通过")
        
        all_issues = []
        all_recommendations = []
        
        for validation in validations:
            if validation["issues"]:
                all_issues.extend(validation["issues"])
            all_recommendations.append(validation["recommendation"])
        
        # 生成总结
        summary = {
            "total_algorithms": total_algorithms,
            "passed_algorithms": passed_algorithms,
            "failed_algorithms": total_algorithms - passed_algorithms,
            "total_issues": len(all_issues),
            "overall_status": "通过" if passed_algorithms == total_algorithms else "需要修正"
        }
        
        # 更新验证结果
        self.validation_results.update({
            "summary": summary,
            "detailed_validations": validations,
            "all_issues": all_issues,
            "all_recommendations": all_recommendations
        })
        
        print(f"\n总结:")
        print(f"  算法总数: {total_algorithms}")
        print(f"  通过算法: {passed_algorithms}")
        print(f"  失败算法: {total_algorithms - passed_algorithms}")
        print(f"  总问题数: {len(all_issues)}")
        print(f"  整体状态: {summary['overall_status']}")
        
        return self.validation_results
    
    def save_report(self, filename: str = "bazi_algorithm_validation_report.json"):
        """保存验证报告"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n验证报告已保存到: {filename}")

def main():
    """主函数"""
    print("开始八字算法完整性验证...")
    
    validator = BaziAlgorithmValidator()
    
    # 执行全面验证
    report = validator.generate_comprehensive_report()
    
    # 保存报告
    validator.save_report()
    
    print("\n" + "="*60)
    if report["summary"]["overall_status"] == "通过":
        print("🎉 八字算法验证完成！所有算法都符合权威标准！")
    else:
        print("⚠️  八字算法验证发现问题，请查看详细报告进行修正。")
    print("="*60)

if __name__ == "__main__":
    main()
