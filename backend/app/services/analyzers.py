"""
八字分析器模块
包含 EventDeductionEngine, AdvancedDayunAnalyzer, AdvancedEventEngine 等分析引擎
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import math
import random
from .core import Bazi, DaYun, StemBranch
from .calculators import FiveElementsCalculator

# 导入或定义常量
try:
    from .constants import STEM_ELEMENTS, BRANCH_ELEMENTS
except ImportError:
    # 备用常量
    STEM_ELEMENTS = {
        "甲": "木", "乙": "木", "丙": "火", "丁": "火", 
        "戊": "土", "己": "土", "庚": "金", "辛": "金", 
        "壬": "水", "癸": "水"
    }
    BRANCH_ELEMENTS = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木", 
        "辰": "土", "巳": "火", "午": "火", "未": "土", 
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }

class EventDeductionEngine:
    """事件反推引擎"""
    
    # 事件规则库
    EVENT_RULES = {
        "career_break": {
            "pattern": "官杀透干+印星生扶",
            "threshold": 0.85
        },
        "marriage": {
            "pattern": "财官合入夫妻宫+红鸾",
            "threshold": 0.92
        },
        "health_issue": {
            "pattern": "忌神冲克用神+病符星",
            "threshold": 0.78
        }
    }
    
    @staticmethod
    def predict_events(
        birth_chart: Bazi, 
        da_yun: DaYun, 
        step: int
    ) -> List[Dict]:
        """预测大运事件"""
        events = []
        
        # 1. 模拟特征提取 - 简化版本以整合到现有系统
        features = set()
        
        # 基于干支信息提取特征
        if birth_chart.day.stem in ["戊", "己", "庚", "辛", "壬", "癸"]:
            features.add("官杀透干")
        
        if da_yun.stem_branch.stem in ["甲", "乙"]:
            features.add("印星生扶")
            
        if da_yun.stem_branch.branch in ["酉", "戌"]:
            features.add("财官合入夫妻宫")
            
        # 根据大运阶段添加一些特征
        if 18 <= da_yun.start_age <= 35:
            features.add("红鸾")
            
        if da_yun.start_age >= 45:
            features.add("病符星")
            
        # 例外情况
        if "官杀透干" in features and "病符星" in features:
            features.add("忌神冲克用神")
        
        # 2. 规则匹配
        for event_type, rule in EventDeductionEngine.EVENT_RULES.items():
            match_score = EventDeductionEngine.calculate_match(
                features, 
                rule["pattern"]
            )
            
            if match_score > rule["threshold"]:
                event_time = None
                if da_yun.start_time:
                    # 在大运期间选择一个时间点
                    offset_years = random.randint(1, 9)
                    event_time = da_yun.start_time + timedelta(days=365 * offset_years)
                
                events.append({
                    "type": event_type,
                    "time": event_time,
                    "score": match_score,
                    "description": EventDeductionEngine.get_event_description(event_type)
                })
                
        return events
    
    @staticmethod
    def calculate_match(features: set, pattern: str) -> float:
        """计算特征匹配度"""
        # 简化实现 - 实际需复杂匹配逻辑
        pattern_features = set(pattern.split("+"))
        intersection = features & pattern_features
        return len(intersection) / len(pattern_features)
    
    @staticmethod
    def get_event_description(event_type: str) -> str:
        """获取事件描述"""
        descriptions = {
            "career_break": "事业发展变化，有升迁或转折机遇",
            "marriage": "婚姻缘分降临，情感生活有重要变化",
            "health_issue": "健康需要关注，注意调养身体"
        }
        return descriptions.get(event_type, "重要人生事件")


class AdvancedDayunAnalyzer:
    """高级大运分析引擎"""
    
    @staticmethod
    def analyze_dayun_fortune_trend(bazi_obj: Bazi, dayun_list: List[DaYun]) -> Dict[str, Any]:
        """分析大运运势走向"""
        day_master_element = STEM_ELEMENTS.get(bazi_obj.day.stem, "")
        analysis = {
            "overall_trend": "平稳",
            "peak_periods": [],
            "challenging_periods": [],
            "turning_points": []
        }
        
        if not day_master_element or not dayun_list:
            return analysis
        
        # 计算每个大运的运势得分
        fortune_scores = []
        for dayun in dayun_list:
            score = AdvancedDayunAnalyzer._calculate_dayun_score(bazi_obj, dayun, day_master_element)
            fortune_scores.append(score)
        
        # 分析整体趋势
        if len(fortune_scores) >= 3:
            early_avg = sum(fortune_scores[:3]) / 3
            late_avg = sum(fortune_scores[-3:]) / 3
            
            if late_avg - early_avg > 10:
                analysis["overall_trend"] = "逐步上升"
            elif early_avg - late_avg > 10:
                analysis["overall_trend"] = "逐步下降"
            else:
                analysis["overall_trend"] = "总体向好" if sum(fortune_scores) / len(fortune_scores) > 60 else "平稳发展"
        
        # 识别高峰期和挑战期
        for i, (dayun, score) in enumerate(zip(dayun_list, fortune_scores)):
            if score >= 75:
                analysis["peak_periods"].append({
                    "period": f"{dayun.start_age}-{dayun.end_age}岁",
                    "dayun": f"{dayun.stem_branch.stem}{dayun.stem_branch.branch}",
                    "description": "运势高峰期，各方面发展顺利"
                })
            elif score <= 40:
                analysis["challenging_periods"].append({
                    "period": f"{dayun.start_age}-{dayun.end_age}岁",
                    "dayun": f"{dayun.stem_branch.stem}{dayun.stem_branch.branch}",
                    "description": "挑战期，需要谨慎应对"
                })
        
        # 识别转折点
        for i in range(1, len(fortune_scores)):
            score_diff = fortune_scores[i] - fortune_scores[i-1]
            if abs(score_diff) >= 20:
                dayun = dayun_list[i]
                direction = "好转" if score_diff > 0 else "下滑"
                analysis["turning_points"].append({
                    "age": dayun.start_age,
                    "description": f"运势明显{direction}",
                    "magnitude": abs(score_diff)
                })
        
        return analysis
    
    @staticmethod
    def _calculate_dayun_score(bazi_obj: Bazi, dayun: DaYun, day_master_element: str) -> float:
        """计算单个大运的得分"""
        base_score = 50  # 基础分数
        
        # 大运天干与日主的关系
        dayun_stem_element = STEM_ELEMENTS.get(dayun.stem_branch.stem, "")
        dayun_branch_element = BRANCH_ELEMENTS.get(dayun.stem_branch.branch, "")
        
        # 生克关系评分
        stem_score = AdvancedDayunAnalyzer._get_element_relationship_score(day_master_element, dayun_stem_element)
        branch_score = AdvancedDayunAnalyzer._get_element_relationship_score(day_master_element, dayun_branch_element)
        
        # 综合评分
        final_score = base_score + stem_score * 0.6 + branch_score * 0.4
        
        # 年龄阶段调整
        age_modifier = AdvancedDayunAnalyzer._get_age_modifier(dayun.start_age)
        final_score *= age_modifier
        
        return max(0, min(100, final_score))
    
    @staticmethod
    def _get_element_relationship_score(day_master: str, other_element: str) -> float:
        """获取五行关系得分"""
        if not other_element:
            return 0
        
        # 五行生克关系
        generate_relations = {
            "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
        }
        
        restrict_relations = {
            "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
        }
        
        if other_element == day_master:
            return 15  # 同类，中等有利
        elif generate_relations.get(other_element) == day_master:
            return 25  # 生我者，有利
        elif generate_relations.get(day_master) == other_element:
            return 10  # 我生者，略有利
        elif restrict_relations.get(other_element) == day_master:
            return -20  # 克我者，不利
        elif restrict_relations.get(day_master) == other_element:
            return 5  # 我克者，略有利
        else:
            return 0
    
    @staticmethod
    def _get_age_modifier(age: int) -> float:
        """根据年龄阶段获取修正系数"""
        if age < 20:
            return 0.9  # 青少年期，潜力大但不稳定
        elif age < 40:
            return 1.1  # 青壮年期，最佳发展期
        elif age < 60:
            return 1.0  # 中年期，稳定期
        else:
            return 0.95  # 老年期，略有衰退
            
    @staticmethod
    def analyze_single_dayun(bazi_obj: Bazi, dayun_gan_zhi: str, start_age: int, end_age: int) -> Dict[str, Any]:
        """分析单个大运的详细信息"""
        try:
            # 创建临时大运对象
            if len(dayun_gan_zhi) != 2:
                raise ValueError(f"Invalid gan_zhi format: {dayun_gan_zhi}")
            
            stem = dayun_gan_zhi[0]
            branch = dayun_gan_zhi[1]
            temp_dayun = DaYun(start_age, StemBranch(stem, branch), end_age=end_age)
            
            # 获取日主五行
            day_master_element = STEM_ELEMENTS.get(bazi_obj.day.stem, "")
            
            # 计算运势得分
            fortune_score = AdvancedDayunAnalyzer._calculate_dayun_score(bazi_obj, temp_dayun, day_master_element)
            
            # 获取大运天干地支的五行
            dayun_stem_element = STEM_ELEMENTS.get(stem, "")
            dayun_branch_element = BRANCH_ELEMENTS.get(branch, "")
            
            # 分析运势趋势
            if fortune_score >= 80:
                trend = "非常有利"
                trend_description = "此大运期间运势极佳，各方面发展顺利，是人生的黄金期。"
            elif fortune_score >= 65:
                trend = "比较有利"
                trend_description = "此大运期间运势较好，多有机遇，适合积极进取。"
            elif fortune_score >= 45:
                trend = "平稳"
                trend_description = "此大运期间运势平稳，宜稳中求进，避免冒险。"
            elif fortune_score >= 30:
                trend = "略有挑战"
                trend_description = "此大运期间会遇到一些挑战，需要谨慎应对。"
            else:
                trend = "需要谨慎"
                trend_description = "此大运期间运势较为起伏，需要格外小心，稳健发展。"
            
            # 分析五行互动
            interaction_analysis = f"大运{dayun_gan_zhi}的天干{stem}({dayun_stem_element})、地支{branch}({dayun_branch_element})与日主{bazi_obj.day.stem}({day_master_element})形成"
            
            # 天干关系分析
            stem_relation_score = AdvancedDayunAnalyzer._get_element_relationship_score(day_master_element, dayun_stem_element)
            if stem_relation_score > 15:
                interaction_analysis += "有利的相生关系"
            elif stem_relation_score < 0:
                interaction_analysis += "需要化解的相克关系"
            else:
                interaction_analysis += "平和的五行关系"
            
            # 生成建议
            suggestions = []
            if fortune_score >= 65:
                suggestions.append("把握机遇，积极进取")
                suggestions.append("适合开展新项目或事业")
                suggestions.append("人际关系良好，可多交友")
            elif fortune_score >= 45:
                suggestions.append("保持稳定，循序渐进")
                suggestions.append("注重基础建设和积累")
                suggestions.append("避免重大变动和冒险")
            else:
                suggestions.append("谨慎保守，以稳为主")
                suggestions.append("多学习充实自己")
                suggestions.append("注意身体健康和人际关系")
            
            return {
                "gan_zhi": dayun_gan_zhi,
                "age_range": f"{start_age}-{end_age}岁",
                "trend": trend,
                "advice": trend_description,  # 前端期望的字段名
                "deep_analysis": f"{start_age}-{end_age}岁，{dayun_gan_zhi}大运期间：{trend_description}建议{', '.join(suggestions[:2])}。",  # 前端期望的字段名
                "fortune_score": fortune_score,
                "stem_element": dayun_stem_element,
                "branch_element": dayun_branch_element,
                "interaction_analysis": interaction_analysis,
                "suggestions": suggestions,
                # 保持兼容性，也包含原字段名
                "trend_description": trend_description,
                "detailed_analysis": f"{start_age}-{end_age}岁，{dayun_gan_zhi}大运期间：{trend_description}建议{', '.join(suggestions[:2])}。"
            }
            
        except Exception as e:
            return {
                "gan_zhi": dayun_gan_zhi,
                "age_range": f"{start_age}-{end_age}岁",
                "trend": "分析失败",
                "advice": f"大运分析过程中发生错误：{str(e)}",  # 前端期望的字段名
                "deep_analysis": f"错误详情：{str(e)}",  # 前端期望的字段名
                "fortune_score": 50,
                "error": str(e),
                # 保持兼容性
                "trend_description": f"大运分析过程中发生错误：{str(e)}"
            }


class AdvancedEventEngine:
    """高级事件预测引擎"""
    
    # 事件规则库
    EVENT_RULES = {
        "career_promotion": {
            "favorable_elements": ["金", "木"],  # 有利的五行
            "age_ranges": [(25, 50)],  # 有利的年龄段
            "required_conditions": ["官星有力", "印星生扶"],
            "base_probability": 0.4
        },
        "marriage_opportunity": {
            "favorable_elements": ["水", "木"],
            "age_ranges": [(22, 35), (45, 55)],
            "required_conditions": ["财官有情", "桃花临运"],
            "base_probability": 0.5
        },
        "financial_breakthrough": {
            "favorable_elements": ["土", "金"],
            "age_ranges": [(30, 60)],
            "required_conditions": ["财星当运", "比劫不夺财"],
            "base_probability": 0.3
        },
        "health_attention": {
            "unfavorable_elements": ["火", "土"],
            "age_ranges": [(40, 80)],
            "required_conditions": ["忌神当运", "冲克太岁"],
            "base_probability": 0.3
        },
        "study_achievement": {
            "favorable_elements": ["木", "水"],
            "age_ranges": [(18, 35)],
            "required_conditions": ["印星有力", "文昌临运"],
            "base_probability": 0.4
        },
        "travel_relocation": {
            "favorable_elements": ["水", "木"],
            "age_ranges": [(20, 70)],
            "required_conditions": ["驿马临运", "冲动宫位"],
            "base_probability": 0.3
        }
    }
    
    @staticmethod
    def predict_life_events(bazi_obj: Bazi, dayun_list: List[DaYun]) -> Dict[str, List[Dict]]:
        """预测人生重要事件"""
        predictions = {}
        day_master_element = STEM_ELEMENTS.get(bazi_obj.day.stem, "")
        
        for event_type, rule in AdvancedEventEngine.EVENT_RULES.items():
            predictions[event_type] = []
            
            for dayun in dayun_list:
                probability = AdvancedEventEngine._calculate_event_probability(
                    bazi_obj, dayun, rule, day_master_element
                )
                
                if probability > 0.5:  # 概率阈值
                    event_time = None
                    if bazi_obj.birth_time:
                        # 在大运期间随机选择一个时间点
                        offset_years = random.randint(2, 8)
                        event_time = bazi_obj.birth_time + timedelta(days=365 * (dayun.start_age + offset_years))
                    
                    predictions[event_type].append({
                        "age_range": f"{dayun.start_age}-{dayun.end_age}岁",
                        "probability": int(probability * 100),
                        "description": AdvancedEventEngine._get_event_description(event_type, probability),
                        "advice": AdvancedEventEngine._get_event_advice(event_type),
                        "estimated_time": event_time.year if event_time else None
                    })
        
        return predictions
    
    @staticmethod
    def _calculate_event_probability(bazi_obj: Bazi, dayun: DaYun, rule: Dict, day_master_element: str) -> float:
        """计算特定事件在特定大运的发生概率"""
        probability = rule["base_probability"]
        
        # 年龄适配度检查
        age_match = False
        for age_range in rule["age_ranges"]:
            if age_range[0] <= dayun.start_age <= age_range[1]:
                age_match = True
                break
        
        if not age_match:
            probability *= 0.3  # 年龄不匹配，概率大幅降低
        
        # 五行适配度检查
        dayun_stem_element = STEM_ELEMENTS.get(dayun.stem_branch.stem, "")
        dayun_branch_element = BRANCH_ELEMENTS.get(dayun.stem_branch.branch, "")
        
        if "favorable_elements" in rule:
            if dayun_stem_element in rule["favorable_elements"] or dayun_branch_element in rule["favorable_elements"]:
                probability *= 1.5
        
        if "unfavorable_elements" in rule:
            if dayun_stem_element in rule["unfavorable_elements"] or dayun_branch_element in rule["unfavorable_elements"]:
                probability *= 1.3  # 不利因素反而增加某些事件概率（如健康问题）
        
        # 随机因素
        random_factor = 0.8 + random.random() * 0.4  # 0.8-1.2的随机系数
        probability *= random_factor
        
        return min(1.0, probability)
    
    @staticmethod
    def _get_event_description(event_type: str, probability: float) -> str:
        """获取事件描述"""
        intensity = "很可能" if probability > 0.8 else "有可能" if probability > 0.6 else "有机会"
        
        descriptions = {
            "career_promotion": f"事业发展机遇，{intensity}有较好的升迁可能",
            "marriage_opportunity": f"感情婚姻机遇，{intensity}遇到合适对象",
            "financial_breakthrough": f"财运突破机会，{intensity}获得显著收益",
            "health_attention": f"健康需要关注，建议适当注意身体调养",
            "study_achievement": f"学业成就机会，{intensity}取得突破",
            "travel_relocation": f"出行迁移机会，{intensity}有重要变动"
        }
        return descriptions.get(event_type, f"{event_type}事件预测")
    
    @staticmethod
    def _get_event_advice(event_type: str) -> str:
        """获取事件建议"""
        advice_map = {
            "career_promotion": "积极展示能力，把握机遇，注重人际关系建设",
            "marriage_opportunity": "保持开放心态，主动社交，注重内在修养",
            "financial_breakthrough": "合理投资规划，避免盲目冒险，稳中求进",
            "health_attention": "定期体检，注意作息，预防胜于治疗",
            "study_achievement": "专心学习，持之以恒，寻求良师指导",
            "travel_relocation": "充分准备，慎重决策，把握变化机遇"
        }
        return advice_map.get(event_type, "顺应自然，积极应对")


class EnhancedLiunianAnalyzer:
    """增强流年分析引擎 - 解决模板字符串和占位符问题"""
    
    @staticmethod
    def analyze_liunian_special_combinations(
        bazi_obj: Bazi,
        current_year_gan: str,
        current_year_zhi: str,
        current_year_ten_god: str,
        liunian_interactions: Dict[str, Any],
        liunian_shensha: List[Dict[str, Any]],
        comprehensive_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """分析流年特殊组合 - 基于真实干支互动"""
        
        special_combinations_analysis = {
            "favorable_combinations": [],
            "special_warnings": [],
            "personalized_insights": [],
            "timing_analysis": [],
            "risk_assessment": []
        }
        
        primary_favorable = comprehensive_analysis.get("final_prognosis", {}).get("primary_favorable", [])
        primary_unfavorable = comprehensive_analysis.get("final_prognosis", {}).get("primary_unfavorable", [])
        
        # 1. 基于真实干支互动分析特殊组合
        EnhancedLiunianAnalyzer._analyze_ganzhi_interactions(
            special_combinations_analysis, liunian_interactions, current_year_ten_god
        )
        
        # 2. 基于神煞标签驱动分析
        EnhancedLiunianAnalyzer._analyze_shensha_influences(
            special_combinations_analysis, liunian_shensha
        )
        
        # 3. 基于五行喜忌分析
        EnhancedLiunianAnalyzer._analyze_wuxing_preferences(
            special_combinations_analysis, current_year_gan, current_year_zhi,
            primary_favorable, primary_unfavorable
        )
        
        # 4. 基于十神特性分析
        EnhancedLiunianAnalyzer._analyze_shishen_characteristics(
            special_combinations_analysis, current_year_ten_god
        )
        
        return special_combinations_analysis
    
    @staticmethod
    def _analyze_ganzhi_interactions(
        analysis: Dict[str, Any],
        interactions: Dict[str, Any],
        current_year_ten_god: str
    ):
        """分析干支互动"""
        
        # 分析六合
        harmonies = interactions.get("harmonies", [])
        for harmony in harmonies:
            if "合日支" in harmony:
                analysis["favorable_combinations"].append(f"流年{harmony}，夫妻感情和谐，配偶运佳")
                analysis["personalized_insights"].append("日支逢合，婚姻感情有利，适合结婚或改善夫妻关系")
            elif "合月支" in harmony:
                analysis["favorable_combinations"].append(f"流年{harmony}，工作环境和谐，同事关系良好")
                analysis["timing_analysis"].append("月支逢合，工作合作运势佳，适合团队项目")
            elif "合年支" in harmony:
                analysis["favorable_combinations"].append(f"流年{harmony}，长辈关系和谐，家庭运势好")
                analysis["personalized_insights"].append("年支逢合，长辈支持，家族事业有发展")
            elif "合时支" in harmony:
                analysis["favorable_combinations"].append(f"流年{harmony}，子女运佳，下属得力")
        
        # 分析六冲
        conflicts = interactions.get("conflicts", [])
        for conflict in conflicts:
            if "冲日支" in conflict:
                analysis["special_warnings"].append(f"流年{conflict}，夫妻关系需要更多沟通理解")
                analysis["risk_assessment"].append("日支受冲，婚姻感情波动，需要耐心处理")
            elif "冲月支" in conflict:
                analysis["special_warnings"].append(f"流年{conflict}，工作变动较大，环境可能改变")
                analysis["risk_assessment"].append("月支受冲，工作环境变化，需要适应调整")
            elif "冲年支" in conflict:
                analysis["special_warnings"].append(f"流年{conflict}，长辈健康需要关注")
                analysis["risk_assessment"].append("年支受冲，家庭事务繁忙，长辈需要照顾")
            elif "冲时支" in conflict:
                analysis["special_warnings"].append(f"流年{conflict}，子女教育需要更多关注")
        
        # 分析三合、三会
        special_combinations = interactions.get("special_combinations", [])
        for combination in special_combinations:
            if "三合" in combination:
                analysis["favorable_combinations"].append(f"流年逢{combination}，团队合作运势佳")
                analysis["timing_analysis"].append("三合局成化，适合合作投资，团队项目")
            elif "三会" in combination:
                analysis["favorable_combinations"].append(f"流年逢{combination}，五行力量集中，专项发展有利")
            elif "天克地冲" in combination:
                analysis["special_warnings"].append(f"流年逢{combination}，需要格外谨慎，避免重大决策")
                analysis["risk_assessment"].append("天克地冲，身心压力大，需要调节情绪")
            elif "岁运并临" in combination:
                analysis["timing_analysis"].append("岁运并临，各方面影响力加倍，是关键转折年")
                analysis["personalized_insights"].append("岁运并临年份，重要决策需要格外慎重")
        
        # 分析相刑
        punishments = interactions.get("punishments", [])
        for punishment in punishments:
            analysis["special_warnings"].append(f"流年逢{punishment}，人际关系需要谨慎")
            analysis["risk_assessment"].append(f"{punishment}，容易有口舌是非，需要低调处理")
        
        # 分析相害
        harms = interactions.get("harms", [])
        for harm in harms:
            analysis["special_warnings"].append(f"流年逢{harm}，合作关系需要明确")
            analysis["risk_assessment"].append(f"{harm}，容易有暗中阻碍，需要防范小人")
    
    @staticmethod
    def _analyze_shensha_influences(
        analysis: Dict[str, Any],
        liunian_shensha: List[Dict[str, Any]]
    ):
        """基于神煞标签驱动分析"""
        
        if not liunian_shensha:
            return
        
        # 优化：将 liunian_shensha 转换为字典，以便快速查找
        shensha_dict = {s["name"]: s for s in liunian_shensha}
        
        # 分类神煞：正面和负面
        positive_shensha = [s for s in liunian_shensha if s.get("positive_tags")]
        negative_shensha = [s for s in liunian_shensha if s.get("negative_tags")]
        
        # 正面神煞分析
        for shensha in positive_shensha:
            shensha_name = shensha.get("name", "")
            positive_tags = shensha.get("positive_tags", [])
            
            if "贵人" in positive_tags:
                analysis["favorable_combinations"].append(f"流年逢{shensha_name}，工作生活有权威人士相助")
                analysis["personalized_insights"].append(f"{shensha_name}护佑，困难时期更容易获得帮助")
            
            if "文昌" in positive_tags or "学习" in positive_tags:
                analysis["favorable_combinations"].append(f"流年逢{shensha_name}，学习考试运势佳，文思敏捷")
                analysis["timing_analysis"].append(f"{shensha_name}临运，适合学习、考试、文书工作")
            
            if "驿马" in positive_tags or "变动" in positive_tags:
                analysis["favorable_combinations"].append(f"流年逢{shensha_name}，有出行迁移或职业变动机会")
                analysis["personalized_insights"].append(f"{shensha_name}临运，变动中蕴含机遇")
            
            if "财富" in positive_tags:
                analysis["favorable_combinations"].append(f"流年逢{shensha_name}，财运亨通，收入增加")
            
            if "桃花" in positive_tags or "感情" in positive_tags:
                analysis["favorable_combinations"].append(f"流年逢{shensha_name}，感情运势佳，异性缘好")
            
            if "健康" in positive_tags:
                analysis["favorable_combinations"].append(f"流年逢{shensha_name}，身体健康，精神状态佳")
        
        # 负面神煞分析
        for shensha in negative_shensha:
            shensha_name = shensha.get("name", "")
            negative_tags = shensha.get("negative_tags", [])
            
            if "空亡" in negative_tags:
                analysis["special_warnings"].append(f"流年逢{shensha_name}，重要决策需要谨慎")
                analysis["risk_assessment"].append(f"{shensha_name}临运，投资决策需要格外小心")
            
            if "劫煞" in negative_tags or "破财" in negative_tags:
                analysis["special_warnings"].append(f"流年逢{shensha_name}，财物安全需要注意")
                analysis["risk_assessment"].append(f"{shensha_name}临运，避免大额投资和借贷")
            
            if "病符" in negative_tags or "健康" in negative_tags:
                analysis["special_warnings"].append(f"流年逢{shensha_name}，健康需要格外关注")
                analysis["risk_assessment"].append(f"{shensha_name}临运，定期体检，注意预防")
            
            if "口舌" in negative_tags or "是非" in negative_tags:
                analysis["special_warnings"].append(f"流年逢{shensha_name}，言语谨慎，避免争执")
                analysis["risk_assessment"].append(f"{shensha_name}临运，低调处事，防范口舌是非")
    
    @staticmethod
    def _analyze_wuxing_preferences(
        analysis: Dict[str, Any],
        current_year_gan: str,
        current_year_zhi: str,
        primary_favorable: List[str],
        primary_unfavorable: List[str]
    ):
        """基于五行喜忌分析"""
        
        try:
            from .constants import STEM_ELEMENTS, BRANCH_ELEMENTS
            gan_element = STEM_ELEMENTS.get(current_year_gan, "")
            zhi_element = BRANCH_ELEMENTS.get(current_year_zhi, "")
        except ImportError:
            # 备用常量
            STEM_ELEMENTS = {
                "甲": "木", "乙": "木", "丙": "火", "丁": "火", 
                "戊": "土", "己": "土", "庚": "金", "辛": "金", 
                "壬": "水", "癸": "水"
            }
            BRANCH_ELEMENTS = {
                "子": "水", "丑": "土", "寅": "木", "卯": "木", 
                "辰": "土", "巳": "火", "午": "火", "未": "土", 
                "申": "金", "酉": "金", "戌": "土", "亥": "水"
            }
            gan_element = STEM_ELEMENTS.get(current_year_gan, "")
            zhi_element = BRANCH_ELEMENTS.get(current_year_zhi, "")
        
        # 喜用神分析
        if gan_element in primary_favorable:
            analysis["favorable_combinations"].append(f"流年天干{current_year_gan}({gan_element})为喜用神，上半年运势佳")
            analysis["timing_analysis"].append(f"{gan_element}行当令，春夏季节运势更为活跃")
        
        if zhi_element in primary_favorable:
            analysis["favorable_combinations"].append(f"流年地支{current_year_zhi}({zhi_element})为喜用神，下半年运势佳")
            analysis["timing_analysis"].append(f"{zhi_element}行辅助，秋冬季节稳定发展")
        
        # 忌神分析
        if gan_element in primary_unfavorable:
            analysis["special_warnings"].append(f"流年天干{current_year_gan}({gan_element})为忌神，上半年需要谨慎")
            analysis["risk_assessment"].append(f"{gan_element}行不利，避免相关领域的重大决策")
        
        if zhi_element in primary_unfavorable:
            analysis["special_warnings"].append(f"流年地支{current_year_zhi}({zhi_element})为忌神，下半年需要谨慎")
            analysis["risk_assessment"].append(f"{zhi_element}行不利，下半年保持稳健策略")
    
    @staticmethod
    def _analyze_shishen_characteristics(
        analysis: Dict[str, Any],
        current_year_ten_god: str
    ):
        """基于十神特性分析"""
        
        ten_god_characteristics = {
            "正财": {
                "favorable": ["财运稳定，适合长期投资", "工作收入稳定，职业发展顺利"],
                "timing": ["财星当令，理财投资运势佳"],
                "insights": ["正财主稳定，适合保守理财策略"]
            },
            "偏财": {
                "favorable": ["投机财运较好，副业收入增加", "商业机会多，但需控制风险"],
                "timing": ["偏财当令，适合开拓新的收入来源"],
                "insights": ["偏财主变动，把握短期机会但避免过度投机"]
            },
            "正官": {
                "favorable": ["事业发展稳定，有升职机会", "权威地位提升，社会声誉良好"],
                "timing": ["正官当令，适合职场发展和公务活动"],
                "insights": ["正官主责任，承担更多义务的同时获得相应地位"]
            },
            "七杀": {
                "warnings": ["工作压力大，需要承受更多挑战", "竞争激烈，需要展现实力"],
                "timing": ["七杀当令，压力与机遇并存"],
                "insights": ["七杀主突破，在压力中寻找突破机会"]
            },
            "正印": {
                "favorable": ["学习运佳，适合进修提升", "长辈关爱，精神支持充足"],
                "timing": ["正印当令，适合学习、培训、文化活动"],
                "insights": ["正印主智慧，通过学习和传承获得成长"]
            },
            "偏印": {
                "favorable": ["创意思维活跃，适合技术创新", "独特见解得到认可"],
                "warnings": ["容易思虑过度，注意精神状态"],
                "insights": ["偏印主创新，发挥独特优势但避免钻牛角尖"]
            },
            "食神": {
                "favorable": ["表达能力强，适合展示才华", "通过技能获得收入"],
                "timing": ["食神当令，创意表达和技能展示的好时机"],
                "insights": ["食神主才华，通过展示个人能力获得认可"]
            },
            "伤官": {
                "favorable": ["创新能力强，打破常规", "个性化表达得到重视"],
                "warnings": ["需注意人际关系，避免过于直接"],
                "insights": ["伤官主创新，发挥创造力但需要包容合作"]
            },
            "比肩": {
                "favorable": ["朋友助力大，团队合作顺利", "平等合作，互相支持"],
                "timing": ["比肩当令，适合团队合作和朋友聚会"],
                "insights": ["比肩主合作，通过平等合作达成共同目标"]
            },
            "劫财": {
                "warnings": ["财运波动，需防破财", "竞争激烈，需要明确界限"],
                "risk": ["避免过度投资，防范财务风险"],
                "insights": ["劫财主竞争，在竞争中保护既得利益"]
            }
        }
        
        characteristics = ten_god_characteristics.get(current_year_ten_god, {})
        
        # 添加有利特征
        for favorable in characteristics.get("favorable", []):
            analysis["favorable_combinations"].append(f"{current_year_ten_god}年：{favorable}")
        
        # 添加时机分析
        for timing in characteristics.get("timing", []):
            analysis["timing_analysis"].append(timing)
        
        # 添加个人洞察
        for insight in characteristics.get("insights", []):
            analysis["personalized_insights"].append(insight)
        
        # 添加警告
        for warning in characteristics.get("warnings", []):
            analysis["special_warnings"].append(f"{current_year_ten_god}年：{warning}")
        
        # 添加风险评估
        for risk in characteristics.get("risk", []):
            analysis["risk_assessment"].append(risk)
    
    @staticmethod
    def generate_enhanced_predicted_events(
        current_year_ten_god: str,
        liunian_gan: str,
        liunian_zhi: str,
        liunian_gan_element: str,
        liunian_zhi_element: str,
        liunian_interactions: Dict[str, Any],
        liunian_shensha: List[Dict[str, Any]],
        comprehensive_analysis: Dict[str, Any],
        current_age: int
    ) -> Dict[str, List[str]]:
        """生成增强的预测事件 - 结合十神、神煞、互动分析"""
        
        predictions = {
            "career": [],
            "wealth": [],
            "health": [],
            "relationship": [],
            "timing": [],
            "strategy": [],
            "warning": []
        }
        
        primary_favorable = comprehensive_analysis.get("final_prognosis", {}).get("primary_favorable", [])
        life_stage = "青年" if current_age < 30 else "中年" if current_age < 60 else "老年"
        
        # 1. 基于十神和神煞的组合预测
        EnhancedLiunianAnalyzer._generate_shishen_shensha_predictions(
            predictions, current_year_ten_god, liunian_shensha, life_stage
        )
        
        # 2. 基于干支互动的事件预测
        EnhancedLiunianAnalyzer._generate_interaction_predictions(
            predictions, liunian_interactions, current_year_ten_god
        )
        
        # 3. 基于五行喜忌的精细预测
        EnhancedLiunianAnalyzer._generate_wuxing_predictions(
            predictions, liunian_gan_element, liunian_zhi_element, primary_favorable
        )
        
        return predictions
    
    @staticmethod
    def _generate_shishen_shensha_predictions(
        predictions: Dict[str, List[str]],
        current_year_ten_god: str,
        liunian_shensha: List[Dict[str, Any]],
        life_stage: str
    ):
        """基于十神+神煞组合生成预测"""
        
        # 优化：将 liunian_shensha 转换为字典，以便快速查找
        shensha_dict = {s["name"]: s for s in liunian_shensha}
        
        # 提取神煞标签集合，用于快速检查
        shensha_tags = set()
        for shensha in liunian_shensha:
            shensha_tags.update(shensha.get("positive_tags", []))
            shensha_tags.update(shensha.get("negative_tags", []))
        
        # 十神+神煞组合预测
        if current_year_ten_god == "正财":
            if "驿马" in shensha_tags:
                predictions["wealth"].append(f"正财遇驿马，{life_stage}期有外出求财、异地合作的机遇")
                predictions["timing"].append("财星配驿马，下半年出差或异地投资运势较好")
            
            if "贵人" in shensha_tags:
                predictions["wealth"].append(f"正财逢贵人，{life_stage}期通过人脉关系获得稳定收入")
                predictions["career"].append("贵人助财，工作中有长辈或权威人士提供机会")
            
            if "空亡" in shensha_tags:
                predictions["warning"].append("正财逢空亡，投资决策需要格外谨慎，避免空头承诺")
        
        elif current_year_ten_god == "偏财":
            if "驿马" in shensha_tags:
                predictions["wealth"].append(f"偏财遇驿马，{life_stage}期投机性收入机会多，但需控制风险")
                predictions["timing"].append("偏财驿马年，适合短期投资和灵活理财")
            
            if "劫煞" in shensha_tags:
                predictions["warning"].append("偏财遇劫煞，需要防范投资陷阱和财务欺诈")
                predictions["wealth"].append("偏财劫煞，避免高风险投资和过度投机")
        
        elif current_year_ten_god == "正官":
            if "文昌" in shensha_tags:
                predictions["career"].append(f"正官逢文昌，{life_stage}期考试、晋升运势特别好")
                predictions["timing"].append("官星文昌，适合参加考试、竞聘、学术活动")
            
            if "贵人" in shensha_tags:
                predictions["career"].append(f"正官遇贵人，{life_stage}期事业发展有权威人士扶持")
                predictions["relationship"].append("官星贵人，配偶或合作伙伴地位较高")
        
        elif current_year_ten_god == "七杀":
            if "将星" in shensha_tags:
                predictions["career"].append(f"七杀配将星，{life_stage}期领导能力突出，适合管理岗位")
                predictions["strategy"].append("七杀将星，发挥领导才能，但需要团队配合")
            
            if "劫煞" in shensha_tags:
                predictions["warning"].append("七杀遇劫煞，工作竞争激烈，需要防范职场是非")
        
        elif current_year_ten_god == "正印":
            if "文昌" in shensha_tags:
                predictions["career"].append(f"正印逢文昌，{life_stage}期学习成果显著，适合教育培训工作")
                predictions["timing"].append("印星文昌，学习、考试、文书工作的最佳时机")
            
            if "贵人" in shensha_tags:
                predictions["health"].append("正印贵人，长辈关爱，身体健康有保障")
        
        elif current_year_ten_god == "食神":
            if "驿马" in shensha_tags:
                predictions["career"].append(f"食神遇驿马，{life_stage}期通过才艺表演或技能培训获得收入")
                predictions["wealth"].append("食神驿马，外出表演或技能展示有不错收益")
            
            if "桃花" in shensha_tags:
                predictions["relationship"].append("食神桃花，个人魅力增加，异性缘佳")
        
        elif current_year_ten_god == "伤官":
            if "驿马" in shensha_tags:
                predictions["career"].append(f"伤官配驿马，{life_stage}期创新项目或自由职业发展好")
                predictions["strategy"].append("伤官驿马，适合创业或改变工作模式")
            
            if "劫煞" in shensha_tags:
                predictions["warning"].append("伤官逢劫煞，言语需要谨慎，避免与权威冲突")
    
    @staticmethod
    def _generate_interaction_predictions(
        predictions: Dict[str, List[str]],
        interactions: Dict[str, Any],
        current_year_ten_god: str
    ):
        """基于干支互动生成预测"""
        
        # 六合预测
        harmonies = interactions.get("harmonies", [])
        for harmony in harmonies:
            if "合日支" in harmony:
                predictions["relationship"].append(f"流年{harmony}，夫妻感情和谐，有结婚或改善关系的机会")
                predictions["wealth"].append("财星合日支，配偶对财运有正面影响")
            
            elif "合月支" in harmony:
                predictions["career"].append(f"流年{harmony}，工作环境和谐，同事合作顺利")
                predictions["timing"].append("月支逢合，工作项目合作的好时机")
        
        # 六冲预测
        conflicts = interactions.get("conflicts", [])
        for conflict in conflicts:
            if "冲日支" in conflict:
                predictions["warning"].append(f"流年{conflict}，夫妻关系需要更多沟通")
                predictions["health"].append("日支受冲，注意身体健康，避免过度劳累")
            
            elif "冲年支" in conflict:
                predictions["warning"].append(f"流年{conflict}，长辈健康需要关注")
                predictions["timing"].append("年支受冲，家庭事务较多，需要合理安排时间")
        
        # 特殊组合预测
        special_combinations = interactions.get("special_combinations", [])
        for combination in special_combinations:
            if "三合" in combination:
                predictions["timing"].append(f"流年逢{combination}，团队合作运势佳，适合合作投资")
                predictions["strategy"].append("三合局成，发挥团队优势，可考虑合作项目")
            
            elif "天克地冲" in combination:
                predictions["warning"].append(f"流年逢{combination}，重大决策需要格外谨慎")
                predictions["health"].append("天克地冲，身心压力大，需要适当调节")
    
    @staticmethod
    def _generate_wuxing_predictions(
        predictions: Dict[str, List[str]],
        gan_element: str,
        zhi_element: str,
        primary_favorable: List[str]
    ):
        """基于五行喜忌生成预测"""
        
        if gan_element in primary_favorable:
            predictions["timing"].append(f"流年天干{gan_element}为喜用神，上半年各方面运势较佳")
            predictions["strategy"].append(f"充分利用{gan_element}的优势，在相关领域积极发展")
        
        if zhi_element in primary_favorable:
            predictions["timing"].append(f"流年地支{zhi_element}为喜用神，下半年运势稳步提升")
            predictions["strategy"].append(f"重点关注{zhi_element}相关的发展机会")
        
        # 五行季节性分析
        season_predictions = {
            "木": "春季运势最佳，适合新项目启动和学习成长",
            "火": "夏季运势旺盛，适合展示才华和社交活动", 
            "土": "季末时期稳定，适合投资理财和基础建设",
            "金": "秋季收获时节，适合总结成果和重要决策",
            "水": "冬季蓄势待发，适合规划学习和内修养"
        }
        
        if gan_element in season_predictions:
            predictions["timing"].append(season_predictions[gan_element])
        
        if zhi_element in season_predictions and zhi_element != gan_element:
            predictions["timing"].append(f"配合{zhi_element}特性：{season_predictions[zhi_element]}")
    
    @staticmethod
    def _create_shensha_lookup_structures(liunian_shensha: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建神煞查找结构，提高性能"""
        if not liunian_shensha:
            return {
                "by_name": {},
                "by_positive_tags": {},
                "by_negative_tags": {},
                "all_positive_tags": set(),
                "all_negative_tags": set(),
                "positive_shensha": [],
                "negative_shensha": []
            }
        
        # 按名称索引
        by_name = {s["name"]: s for s in liunian_shensha}
        
        # 按正面标签索引
        by_positive_tags = {}
        all_positive_tags = set()
        positive_shensha = []
        
        for shensha in liunian_shensha:
            positive_tags = shensha.get("positive_tags", [])
            if positive_tags:
                positive_shensha.append(shensha)
                all_positive_tags.update(positive_tags)
                for tag in positive_tags:
                    if tag not in by_positive_tags:
                        by_positive_tags[tag] = []
                    by_positive_tags[tag].append(shensha)
        
        # 按负面标签索引
        by_negative_tags = {}
        all_negative_tags = set()
        negative_shensha = []
        
        for shensha in liunian_shensha:
            negative_tags = shensha.get("negative_tags", [])
            if negative_tags:
                negative_shensha.append(shensha)
                all_negative_tags.update(negative_tags)
                for tag in negative_tags:
                    if tag not in by_negative_tags:
                        by_negative_tags[tag] = []
                    by_negative_tags[tag].append(shensha)
        
        return {
            "by_name": by_name,
            "by_positive_tags": by_positive_tags,
            "by_negative_tags": by_negative_tags,
            "all_positive_tags": all_positive_tags,
            "all_negative_tags": all_negative_tags,
            "positive_shensha": positive_shensha,
            "negative_shensha": negative_shensha
        }
