"""
简化的八字计算器，用于验证系统
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import json
import os

# 导入核心数据结构
from .core import Bazi, ShenSha, DaYun, StemBranch

# 导入计算器类
from .calculators import ShenShaCalculator, FiveElementsCalculator

# 导入常量
from .constants import STEM_ELEMENTS, BRANCH_ELEMENTS, NAYIN_MAP_COMPLETE

# 导入日志配置
from .logger_config import setup_logger

# 创建专用日志记录器
logger = setup_logger("simple_bazi_calculator")

# JIAZI 六十甲子表
JIAZI_TABLE = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]

class SimpleBaziCalculator:
    """简化的八字计算器"""
    
    def __init__(self):
        self.shensha_calculator = ShenShaCalculator()
        self.elements_calculator = FiveElementsCalculator()
    
    def calculate_bazi(self, birth_time: datetime, use_true_solar: bool = False) -> Dict[str, Any]:
        """计算八字"""
        try:
            # 计算四柱
            pillars = self._calculate_pillars(birth_time)
            
            # 创建Bazi对象
            bazi_obj = Bazi(
                year=StemBranch(pillars["年柱"]["stem"], pillars["年柱"]["branch"]),
                month=StemBranch(pillars["月柱"]["stem"], pillars["月柱"]["branch"]),
                day=StemBranch(pillars["日柱"]["stem"], pillars["日柱"]["branch"]),
                hour=StemBranch(pillars["时柱"]["stem"], pillars["时柱"]["branch"]),
                birth_time=birth_time,
                gender="未知"  # 添加默认性别参数
            )
            
            # 计算五行得分
            five_elements = self.elements_calculator.calculate_comprehensive_scores(bazi_obj)
            
            # 计算旺衰
            strength_analysis = self._analyze_strength(bazi_obj, five_elements)
            
            # 计算喜用神
            favorable_elements = self._calculate_favorable_elements(bazi_obj, five_elements, strength_analysis)
            
            # 计算神煞
            shensha_results = self.shensha_calculator.calculate_shensha(bazi_obj)
            
            # 构建结果
            result = {
                "bazi": {
                    "year_pillar": pillars["年柱"],
                    "month_pillar": pillars["月柱"],
                    "day_pillar": pillars["日柱"],
                    "hour_pillar": pillars["时柱"]
                },
                "five_elements": self._format_five_elements(five_elements),
                "strength_analysis": strength_analysis,
                "favorable_elements": favorable_elements,
                "shensha": shensha_results,
                "birth_info": {
                    "birth_time": birth_time.isoformat(),
                    "use_true_solar": use_true_solar
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"八字计算失败: {e}")
            raise
    
    def _calculate_pillars(self, birth_time: datetime) -> Dict[str, Dict]:
        """计算四柱"""
        # 简化的四柱计算，使用公历直接计算
        year = birth_time.year
        month = birth_time.month
        day = birth_time.day
        hour = birth_time.hour
        
        # 计算年柱 (从1984年甲子年开始)
        year_index = (year - 1984) % 60
        if year_index < 0:
            year_index += 60
        year_jiazi = JIAZI_TABLE[year_index]
        
        # 计算月柱 (简化计算)
        month_index = ((year - 1984) * 12 + month - 1) % 60
        month_jiazi = JIAZI_TABLE[month_index]
        
        # 计算日柱 (从1984年1月1日开始)
        base_date = datetime(1984, 1, 1)
        days_diff = (birth_time.date() - base_date.date()).days
        day_index = days_diff % 60
        day_jiazi = JIAZI_TABLE[day_index]
        
        # 计算时柱
        hour_index = (days_diff * 12 + hour // 2) % 60
        hour_jiazi = JIAZI_TABLE[hour_index]
        
        return {
            "年柱": {"stem": year_jiazi[0], "branch": year_jiazi[1], "nayin": NAYIN_MAP_COMPLETE.get(year_jiazi, "")},
            "月柱": {"stem": month_jiazi[0], "branch": month_jiazi[1], "nayin": NAYIN_MAP_COMPLETE.get(month_jiazi, "")},
            "日柱": {"stem": day_jiazi[0], "branch": day_jiazi[1], "nayin": NAYIN_MAP_COMPLETE.get(day_jiazi, "")},
            "时柱": {"stem": hour_jiazi[0], "branch": hour_jiazi[1], "nayin": NAYIN_MAP_COMPLETE.get(hour_jiazi, "")}
        }
    
    def _format_five_elements(self, five_elements: Dict[str, float]) -> Dict[str, Dict]:
        """格式化五行得分"""
        total = sum(five_elements.values())
        formatted = {}
        
        for element, score in five_elements.items():
            percentage = score / total if total > 0 else 0
            formatted[element] = {
                "score": score,
                "percentage": percentage
            }
        
        return formatted
    
    def _analyze_strength(self, bazi_obj: Bazi, five_elements: Dict[str, float]) -> Dict[str, Any]:
        """分析日主旺衰"""
        day_master_element = STEM_ELEMENTS.get(bazi_obj.day.stem, "")
        day_master_score = five_elements.get(day_master_element, 0)
        
        total_score = sum(five_elements.values())
        day_master_percentage = day_master_score / total_score if total_score > 0 else 0
        
        # 简化的旺衰判断
        if day_master_percentage > 0.4:
            strength = "身强"
        elif day_master_percentage > 0.3:
            strength = "偏强"
        elif day_master_percentage > 0.2:
            strength = "中和"
        elif day_master_percentage > 0.1:
            strength = "偏弱"
        else:
            strength = "身弱"
        
        return {
            "day_master_element": day_master_element,
            "day_master_score": day_master_score,
            "day_master_percentage": day_master_percentage,
            "strength": strength,
            "conclusion": f"{strength}（{day_master_element}：{day_master_percentage:.1%}）"
        }
    
    def _calculate_favorable_elements(self, bazi_obj: Bazi, five_elements: Dict[str, float], 
                                    strength_analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """计算喜用神"""
        day_master_element = strength_analysis["day_master_element"]
        strength = strength_analysis["strength"]
        
        # 简化的喜用神判断
        if strength in ["身强", "偏强"]:
            # 身强喜克泄耗
            if day_master_element == "木":
                primary = ["火", "金", "土"]
                secondary = ["水"]
            elif day_master_element == "火":
                primary = ["土", "水", "金"]
                secondary = ["木"]
            elif day_master_element == "土":
                primary = ["金", "木", "水"]
                secondary = ["火"]
            elif day_master_element == "金":
                primary = ["水", "火", "木"]
                secondary = ["土"]
            else:  # 水
                primary = ["木", "土", "火"]
                secondary = ["金"]
        else:
            # 身弱喜生扶
            if day_master_element == "木":
                primary = ["水", "木"]
                secondary = ["火"]
            elif day_master_element == "火":
                primary = ["木", "火"]
                secondary = ["土"]
            elif day_master_element == "土":
                primary = ["火", "土"]
                secondary = ["金"]
            elif day_master_element == "金":
                primary = ["土", "金"]
                secondary = ["水"]
            else:  # 水
                primary = ["金", "水"]
                secondary = ["木"]
        
        return {
            "primary": primary[:2],  # 取前两个作为主要喜用神
            "secondary": secondary[:1]  # 取第一个作为次要喜用神
        }
