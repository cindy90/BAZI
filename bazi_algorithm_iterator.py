"""
八字排盘算法迭代改进系统
基于验证结果，提供具体的改进建议和实施方案
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class BaziAlgorithmIterator:
    """八字算法迭代改进器"""
    
    def __init__(self, validation_report_file: str = "validation_report.json"):
        self.validation_report_file = validation_report_file
        self.report_data = self.load_validation_report()
        
    def load_validation_report(self) -> Dict:
        """加载验证报告"""
        try:
            with open(self.validation_report_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载验证报告失败: {e}")
            return {}
    
    def analyze_accuracy_issues(self) -> Dict[str, List[str]]:
        """分析准确率问题"""
        issues = {
            "四柱计算": [],
            "五行分析": [],
            "旺衰判断": [],
            "算法框架": []
        }
        
        if not self.report_data:
            issues["算法框架"].append("无法获取验证数据，需要先运行验证系统")
            return issues
        
        summary = self.report_data.get("summary", {})
        results = self.report_data.get("results", [])
        
        # 分析四柱准确率
        pillar_accuracy = summary.get("pillar_accuracy", 0)
        if pillar_accuracy < 0.9:
            issues["四柱计算"].extend([
                f"四柱准确率为{pillar_accuracy:.1%}，低于期望的90%",
                "当前算法使用简化的线性计算，未考虑真正的节气换月",
                "建议实现精确的节气计算系统",
                "建议加入农历转公历的精确算法",
                "需要考虑时辰的精确划分（23-1点为子时等）"
            ])
        
        # 分析五行准确率  
        element_accuracy = summary.get("element_accuracy", 0)
        if element_accuracy < 0.8:
            issues["五行分析"].extend([
                f"五行准确率为{element_accuracy:.1%}，需要改进",
                "当前算法只考虑天干地支本气，未考虑地支藏干",
                "建议实现地支藏干的权重计算",
                "需要考虑季节调候对五行强弱的影响",
                "应该加入刑冲合害对五行力量的修正"
            ])
        
        # 分析旺衰准确率
        strength_accuracy = summary.get("strength_accuracy", 0)
        if strength_accuracy < 0.7:
            issues["旺衰判断"].extend([
                f"旺衰准确率为{strength_accuracy:.1%}，亟需改进",
                "当前旺衰判断过于简化，仅基于日主五行比例",
                "建议实现得令、得地、得生、得助的综合分析",
                "需要考虑月令司权对日主强弱的决定性影响",
                "应该分析日主在年月日时各柱的受生受克情况",
                "建议加入格局分析来辅助旺衰判断"
            ])
        
        # 分析具体案例问题
        high_error_cases = [r for r in results if r.get("总体准确率", 0) < 0.3]
        if len(high_error_cases) > len(results) * 0.3:
            issues["算法框架"].extend([
                f"有{len(high_error_cases)}个案例准确率低于30%，算法存在系统性问题",
                "建议重新设计四柱计算的核心算法",
                "需要参考权威的八字排盘软件进行对比验证"
            ])
        
        return issues
    
    def generate_improvement_plan(self) -> Dict[str, Dict]:
        """生成改进计划"""
        issues = self.analyze_accuracy_issues()
        
        improvement_plan = {
            "priority_1_critical": {
                "title": "紧急改进项（影响核心功能）",
                "tasks": [],
                "estimated_days": 0
            },
            "priority_2_important": {
                "title": "重要改进项（提升准确率）",
                "tasks": [],
                "estimated_days": 0
            },
            "priority_3_enhancement": {
                "title": "功能增强项（完善细节）",
                "tasks": [],
                "estimated_days": 0
            }
        }
        
        # 四柱计算改进（优先级1）
        if issues["四柱计算"]:
            improvement_plan["priority_1_critical"]["tasks"].extend([
                {
                    "task": "实现精确的节气计算系统",
                    "description": "基于天文算法计算准确的24节气时间",
                    "implementation": "集成solar_terms库或实现自己的天文计算",
                    "estimated_hours": 16
                },
                {
                    "task": "完善时柱计算逻辑", 
                    "description": "正确处理子时跨日问题和时辰边界",
                    "implementation": "实现23-1点为子时的正确逻辑",
                    "estimated_hours": 8
                },
                {
                    "task": "加入农历公历转换",
                    "description": "支持农历生日的准确转换",
                    "implementation": "集成中华万年历算法",
                    "estimated_hours": 12
                }
            ])
            improvement_plan["priority_1_critical"]["estimated_days"] = 5
        
        # 五行计算改进（优先级2）
        if issues["五行分析"]:
            improvement_plan["priority_2_important"]["tasks"].extend([
                {
                    "task": "实现地支藏干计算",
                    "description": "准确计算地支中隐藏天干的力量",
                    "implementation": "按照传统命理的藏干表和权重计算",
                    "estimated_hours": 12
                },
                {
                    "task": "加入季节调候",
                    "description": "根据出生季节调整五行力量",
                    "implementation": "实现春夏秋冬对各五行的增减效应",
                    "estimated_hours": 8
                },
                {
                    "task": "实现刑冲合害计算",
                    "description": "计算地支间的相互作用对五行的影响",
                    "implementation": "基于传统合冲理论实现力量修正",
                    "estimated_hours": 16
                }
            ])
            improvement_plan["priority_2_important"]["estimated_days"] = 5
        
        # 旺衰判断改进（优先级1）
        if issues["旺衰判断"]:
            improvement_plan["priority_1_critical"]["tasks"].extend([
                {
                    "task": "实现月令司权分析",
                    "description": "准确判断日主在月令中的旺衰状态",
                    "implementation": "基于十二月令的旺相休囚死理论",
                    "estimated_hours": 10
                },
                {
                    "task": "完善得令得地得生得助分析",
                    "description": "全面分析日主的支持力量",
                    "implementation": "分别计算天干地支对日主的帮扶情况",
                    "estimated_hours": 14
                }
            ])
            improvement_plan["priority_1_critical"]["estimated_days"] += 3
        
        # 算法框架改进（优先级3）
        if issues["算法框架"]:
            improvement_plan["priority_3_enhancement"]["tasks"].extend([
                {
                    "task": "建立算法验证框架",
                    "description": "持续验证和改进算法准确率",
                    "implementation": "扩展当前验证系统，加入更多测试案例",
                    "estimated_hours": 8
                },
                {
                    "task": "优化代码结构",
                    "description": "重构计算器以提高可维护性",
                    "implementation": "模块化设计，分离核心算法和辅助功能",
                    "estimated_hours": 12
                }
            ])
            improvement_plan["priority_3_enhancement"]["estimated_days"] = 3
        
        return improvement_plan
    
    def generate_specific_fixes(self) -> List[Dict]:
        """生成具体的修复方案"""
        fixes = []
        
        # 修复1: 节气计算
        fixes.append({
            "issue": "四柱计算不准确",
            "root_cause": "未使用真正的节气来换月",
            "fix_description": "实现基于天文计算的精确节气",
            "code_location": "simple_bazi_calculator.py -> _calculate_pillars",
            "implementation_steps": [
                "1. 安装或实现solar_terms计算库",
                "2. 根据出生年份计算该年的24节气时间",
                "3. 根据出生日期确定正确的月柱",
                "4. 更新月柱计算逻辑"
            ],
            "test_case": "验证康熙皇帝案例 - 1654年5月4日应该正确计算月柱",
            "expected_improvement": "四柱准确率从31.7%提升到80%+"
        })
        
        # 修复2: 地支藏干
        fixes.append({
            "issue": "五行得分偏差较大",
            "root_cause": "只计算天干地支本气，未考虑地支藏干",
            "fix_description": "加入地支藏干的权重计算",
            "code_location": "simple_bazi_calculator.py -> calculate_five_elements",
            "implementation_steps": [
                "1. 添加地支藏干映射表（已存在于constants.py）",
                "2. 为每个地支的藏干分配正确的权重",
                "3. 在五行计算中加入藏干贡献",
                "4. 根据月令调整藏干的力量"
            ],
            "test_case": "验证李清照案例 - 正确计算地支藏干对五行的贡献",
            "expected_improvement": "五行准确率从73.4%提升到85%+"
        })
        
        # 修复3: 旺衰分析
        fixes.append({
            "issue": "旺衰判断准确率过低",
            "root_cause": "过度简化的旺衰判断逻辑",
            "fix_description": "实现传统命理的旺衰分析方法",
            "code_location": "simple_bazi_calculator.py -> _analyze_strength",
            "implementation_steps": [
                "1. 实现月令司权判断（旺相休囚死）",
                "2. 分析日主得令、得地、得生、得助",
                "3. 计算同党异党力量对比",
                "4. 考虑特殊格局的影响"
            ],
            "test_case": "验证多个历史人物案例的旺衰判断",
            "expected_improvement": "旺衰准确率从13.3%提升到70%+"
        })
        
        return fixes
    
    def create_implementation_guide(self) -> str:
        """创建实施指南"""
        improvement_plan = self.generate_improvement_plan()
        specific_fixes = self.generate_specific_fixes()
        
        guide = []
        guide.append("八字排盘算法迭代改进实施指南")
        guide.append("=" * 50)
        guide.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        guide.append("")
        
        # 当前状态分析
        if self.report_data:
            summary = self.report_data.get("summary", {})
            guide.append("当前算法性能:")
            guide.append(f"  总体准确率: {summary.get('avg_accuracy', 0):.1%}")
            guide.append(f"  四柱准确率: {summary.get('pillar_accuracy', 0):.1%}")
            guide.append(f"  五行准确率: {summary.get('element_accuracy', 0):.1%}")
            guide.append(f"  旺衰准确率: {summary.get('strength_accuracy', 0):.1%}")
            guide.append("")
        
        # 改进计划
        guide.append("改进计划:")
        for priority, plan in improvement_plan.items():
            guide.append(f"\n{plan['title']} (预计{plan['estimated_days']}天):")
            for i, task in enumerate(plan['tasks'], 1):
                guide.append(f"  {i}. {task['task']}")
                guide.append(f"     描述: {task['description']}")
                guide.append(f"     实现: {task['implementation']}")
                guide.append(f"     预计: {task['estimated_hours']}小时")
                guide.append("")
        
        # 具体修复方案
        guide.append("具体修复方案:")
        for i, fix in enumerate(specific_fixes, 1):
            guide.append(f"\n修复 {i}: {fix['issue']}")
            guide.append(f"  根本原因: {fix['root_cause']}")
            guide.append(f"  解决方案: {fix['fix_description']}")
            guide.append(f"  代码位置: {fix['code_location']}")
            guide.append(f"  期望改进: {fix['expected_improvement']}")
            guide.append("  实施步骤:")
            for step in fix['implementation_steps']:
                guide.append(f"    {step}")
            guide.append("")
        
        # 验证策略
        guide.append("验证策略:")
        guide.append("  1. 每次修改后运行完整验证测试")
        guide.append("  2. 对比修改前后的准确率变化")
        guide.append("  3. 重点关注历史人物案例的准确性")
        guide.append("  4. 逐步扩展测试案例数量")
        guide.append("  5. 建立回归测试防止性能下降")
        guide.append("")
        
        # 里程碑目标
        guide.append("里程碑目标:")
        guide.append("  第1周: 四柱准确率达到80%+")
        guide.append("  第2周: 五行准确率达到85%+")
        guide.append("  第3周: 旺衰准确率达到70%+")
        guide.append("  第4周: 总体准确率达到80%+")
        
        return "\n".join(guide)
    
    def save_improvement_report(self, filename: str = "bazi_improvement_plan.md"):
        """保存改进报告"""
        try:
            guide = self.create_implementation_guide()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(guide)
                
            print(f"改进计划已保存到: {filename}")
            
            # 同时保存JSON格式的详细数据
            json_filename = filename.replace('.md', '.json')
            improvement_data = {
                "issues": self.analyze_accuracy_issues(),
                "improvement_plan": self.generate_improvement_plan(),
                "specific_fixes": self.generate_specific_fixes(),
                "generation_time": datetime.now().isoformat()
            }
            
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(improvement_data, f, ensure_ascii=False, indent=2)
                
            print(f"详细数据已保存到: {json_filename}")
            
        except Exception as e:
            print(f"保存改进报告失败: {e}")

def main():
    """主函数"""
    # 创建迭代改进器
    iterator = BaziAlgorithmIterator()
    
    # 分析问题
    issues = iterator.analyze_accuracy_issues()
    
    print("八字排盘算法问题分析:")
    print("=" * 40)
    
    for category, issue_list in issues.items():
        if issue_list:
            print(f"\n{category}:")
            for issue in issue_list:
                print(f"  • {issue}")
    
    print("\n" + "=" * 40)
    
    # 生成并保存改进计划
    iterator.save_improvement_report()
    
    # 打印关键建议
    fixes = iterator.generate_specific_fixes()
    print("\n关键改进建议:")
    for i, fix in enumerate(fixes, 1):
        print(f"{i}. {fix['issue']} -> {fix['expected_improvement']}")

if __name__ == "__main__":
    main()
