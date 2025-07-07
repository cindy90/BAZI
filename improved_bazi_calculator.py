"""
精确的八字排盘计算器 - 改进版
实现基于节气的准确四柱计算
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import math

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

# 地支藏干及权重
BRANCH_HIDDEN_STEMS = {
    "子": {"癸": 1.0},
    "丑": {"己": 0.6, "癸": 0.3, "辛": 0.1},
    "寅": {"甲": 0.6, "丙": 0.3, "戊": 0.1},
    "卯": {"乙": 1.0},
    "辰": {"戊": 0.6, "乙": 0.3, "癸": 0.1},
    "巳": {"丙": 0.6, "戊": 0.3, "庚": 0.1},
    "午": {"丁": 0.7, "己": 0.3},
    "未": {"己": 0.6, "丁": 0.3, "乙": 0.1},
    "申": {"庚": 0.6, "壬": 0.3, "戊": 0.1},
    "酉": {"辛": 1.0},
    "戌": {"戊": 0.6, "辛": 0.3, "丁": 0.1},
    "亥": {"壬": 0.7, "甲": 0.3}
}

# 月令对应的地支（按节气）
MONTH_BRANCHES = {
    1: "寅",  # 立春后
    2: "卯",  # 惊蛰后
    3: "辰",  # 清明后
    4: "巳",  # 立夏后
    5: "午",  # 芒种后
    6: "未",  # 小暑后
    7: "申",  # 立秋后
    8: "酉",  # 白露后
    9: "戌",  # 寒露后
    10: "亥", # 立冬后
    11: "子", # 大雪后
    12: "丑"  # 小寒后
}

class ImprovedBaziCalculator:
    """改进的八字计算器"""
    
    def __init__(self):
        # 基准时间：1984年甲子年
        self.base_year = 1984
        self.base_date = datetime(1984, 1, 1)
        
    def calculate_solar_term_month(self, birth_time: datetime) -> int:
        """根据节气计算正确的八字月份"""
        year = birth_time.year
        month = birth_time.month
        day = birth_time.day
        
        # 简化的节气计算（实际应该使用天文算法）
        # 这里使用近似的节气日期
        solar_terms = {
            2: (4, 19),   # 立春, 雨水
            3: (6, 21),   # 惊蛰, 春分
            4: (5, 20),   # 清明, 谷雨
            5: (6, 21),   # 立夏, 小满
            6: (6, 21),   # 芒种, 夏至
            7: (7, 23),   # 小暑, 大暑
            8: (8, 23),   # 立秋, 处暑
            9: (8, 23),   # 白露, 秋分
            10: (8, 24),  # 寒露, 霜降
            11: (8, 22),  # 立冬, 小雪
            12: (7, 22),  # 大雪, 冬至
            1: (6, 20)    # 小寒, 大寒
        }
        
        # 获取当月的节气日期
        if month in solar_terms:
            term1_day, term2_day = solar_terms[month]
            
            if day < term1_day:
                # 在第一个节气之前，使用上个月的地支
                bazi_month = month - 1 if month > 1 else 12
            else:
                # 在第一个节气之后，使用当前月的地支
                bazi_month = month
        else:
            bazi_month = month
            
        return bazi_month
    
    def calculate_pillars(self, birth_time: datetime) -> Dict[str, Dict]:
        """计算四柱（改进版）"""
        year = birth_time.year
        month = birth_time.month
        day = birth_time.day
        hour = birth_time.hour
        
        # 计算年柱
        year_index = (year - self.base_year) % 60
        if year_index < 0:
            year_index += 60
        year_jiazi = JIAZI_TABLE[year_index]
        
        # 计算月柱（基于节气）
        bazi_month = self.calculate_solar_term_month(birth_time)
        month_branch = MONTH_BRANCHES[bazi_month]
        
        # 月干的计算：年干遁月法
        year_stem = year_jiazi[0]
        month_stem_index = self._get_month_stem_index(year_stem, bazi_month)
        month_stem = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"][month_stem_index % 10]
        month_jiazi = month_stem + month_branch
        
        # 计算日柱（更精确的算法）
        days_diff = self._calculate_days_since_base(birth_time)
        day_index = days_diff % 60
        day_jiazi = JIAZI_TABLE[day_index]
        
        # 计算时柱（日干遁时法）
        hour_branch_index = self._get_hour_branch_index(hour)
        hour_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        hour_branch = hour_branches[hour_branch_index]
        
        day_stem = day_jiazi[0]
        hour_stem_index = self._get_hour_stem_index(day_stem, hour_branch_index)
        hour_stem = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"][hour_stem_index % 10]
        hour_jiazi = hour_stem + hour_branch
        
        return {
            "年柱": {"stem": year_jiazi[0], "branch": year_jiazi[1], "jiazi": year_jiazi},
            "月柱": {"stem": month_stem, "branch": month_branch, "jiazi": month_jiazi},
            "日柱": {"stem": day_jiazi[0], "branch": day_jiazi[1], "jiazi": day_jiazi},
            "时柱": {"stem": hour_stem, "branch": hour_branch, "jiazi": hour_jiazi}
        }
    
    def _get_month_stem_index(self, year_stem: str, month: int) -> int:
        """根据年干推月干"""
        year_stem_index = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"].index(year_stem)
        
        # 年干遁月法：甲己之年丙作首
        month_start_index = {
            0: 2, 5: 2,  # 甲己年从丙开始
            1: 4, 6: 4,  # 乙庚年从戊开始
            2: 6, 7: 6,  # 丙辛年从庚开始  
            3: 8, 8: 8,  # 丁壬年从壬开始
            4: 0, 9: 0   # 戊癸年从甲开始
        }
        
        base_index = month_start_index[year_stem_index]
        return (base_index + month - 1) % 10
    
    def _calculate_days_since_base(self, birth_time: datetime) -> int:
        """计算从基准日期开始的天数"""
        # 使用更精确的日期计算
        delta = birth_time.date() - self.base_date.date()
        return delta.days
    
    def _get_hour_branch_index(self, hour: int) -> int:
        """根据时间获取时支索引"""
        # 处理子时跨日问题：23-1点为子时
        if hour == 23:
            return 0  # 子时
        else:
            return (hour + 1) // 2
    
    def _get_hour_stem_index(self, day_stem: str, hour_branch_index: int) -> int:
        """根据日干推时干"""
        day_stem_index = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"].index(day_stem)
        
        # 日干遁时法：甲己还是甲
        hour_start_index = {
            0: 0, 5: 0,  # 甲己日从甲子开始
            1: 2, 6: 2,  # 乙庚日从丙子开始
            2: 4, 7: 4,  # 丙辛日从戊子开始
            3: 6, 8: 6,  # 丁壬日从庚子开始
            4: 8, 9: 8   # 戊癸日从壬子开始
        }
        
        base_index = hour_start_index[day_stem_index]
        return (base_index + hour_branch_index) % 10
    
    def calculate_five_elements_with_hidden_stems(self, pillars: Dict[str, Dict]) -> Dict[str, float]:
        """计算五行得分（包含地支藏干）"""
        elements = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}
        
        # 天干得分
        for pillar_name, pillar_data in pillars.items():
            stem = pillar_data["stem"]
            branch = pillar_data["branch"]
            
            # 天干得分（权重1.0）
            stem_element = STEM_ELEMENTS.get(stem, "")
            if stem_element:
                elements[stem_element] += 1.0
            
            # 地支本气得分（权重0.8）
            branch_element = BRANCH_ELEMENTS.get(branch, "")
            if branch_element:
                elements[branch_element] += 0.8
            
            # 地支藏干得分
            hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
            for hidden_stem, weight in hidden_stems.items():
                hidden_element = STEM_ELEMENTS.get(hidden_stem, "")
                if hidden_element:
                    # 藏干权重 * 0.4
                    elements[hidden_element] += weight * 0.4
        
        # 转换为百分比
        total = sum(elements.values())
        if total > 0:
            for element in elements:
                elements[element] = elements[element] / total
        
        return elements
    
    def analyze_strength_improved(self, pillars: Dict[str, Dict], five_elements: Dict[str, float], 
                                birth_time: datetime) -> Dict[str, Any]:
        """改进的旺衰分析"""
        day_stem = pillars["日柱"]["stem"]
        day_branch = pillars["日柱"]["branch"]
        month_branch = pillars["月柱"]["branch"]
        
        day_master_element = STEM_ELEMENTS.get(day_stem, "")
        
        # 1. 分析得令（月令司权）
        season_strength = self._analyze_seasonal_strength(day_master_element, birth_time.month)
        
        # 2. 分析得地（地支根基）
        root_strength = self._analyze_root_strength(day_stem, pillars)
        
        # 3. 分析得生（印星力量）
        support_strength = self._analyze_support_strength(day_master_element, five_elements)
        
        # 4. 分析得助（比劫力量）
        helper_strength = five_elements.get(day_master_element, 0)
        
        # 综合评分
        total_strength = (
            season_strength * 0.4 +    # 月令最重要
            root_strength * 0.3 +      # 地支根基
            support_strength * 0.2 +   # 印星生扶
            helper_strength * 0.1       # 比劫助身
        )
        
        # 判断旺衰
        if total_strength > 0.6:
            strength = "身强"
        elif total_strength > 0.45:
            strength = "偏强"
        elif total_strength > 0.35:
            strength = "中和"
        elif total_strength > 0.25:
            strength = "偏弱"
        else:
            strength = "身弱"
        
        return {
            "day_master_element": day_master_element,
            "season_strength": season_strength,
            "root_strength": root_strength,
            "support_strength": support_strength,
            "helper_strength": helper_strength,
            "total_strength": total_strength,
            "strength": strength,
            "conclusion": f"{strength}（综合评分：{total_strength:.1%}）"
        }
    
    def _analyze_seasonal_strength(self, element: str, month: int) -> float:
        """分析月令司权"""
        # 旺相休囚死的简化版本
        seasonal_strength = {
            "春": {"木": 1.0, "火": 0.8, "土": 0.3, "金": 0.2, "水": 0.4},
            "夏": {"木": 0.4, "火": 1.0, "土": 0.8, "金": 0.2, "水": 0.1},
            "秋": {"木": 0.2, "火": 0.3, "土": 0.6, "金": 1.0, "水": 0.4},
            "冬": {"木": 0.3, "火": 0.1, "土": 0.4, "金": 0.6, "水": 1.0}
        }
        
        if month in [3, 4, 5]:
            season = "春"
        elif month in [6, 7, 8]:
            season = "夏"
        elif month in [9, 10, 11]:
            season = "秋"
        else:
            season = "冬"
        
        return seasonal_strength[season].get(element, 0.5)
    
    def _analyze_root_strength(self, day_stem: str, pillars: Dict[str, Dict]) -> float:
        """分析地支根基"""
        root_score = 0.0
        day_element = STEM_ELEMENTS.get(day_stem, "")
        
        for pillar_name, pillar_data in pillars.items():
            branch = pillar_data["branch"]
            
            # 检查地支藏干中是否有日主
            hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
            for hidden_stem, weight in hidden_stems.items():
                if hidden_stem == day_stem:
                    # 找到日主的根
                    root_score += weight
                elif STEM_ELEMENTS.get(hidden_stem, "") == day_element:
                    # 找到同类五行的根
                    root_score += weight * 0.5
        
        return min(root_score, 1.0)  # 限制在1.0以内
    
    def _analyze_support_strength(self, day_element: str, five_elements: Dict[str, float]) -> float:
        """分析印星力量（生我者为印）"""
        # 五行相生关系
        support_elements = {
            "木": "水",
            "火": "木", 
            "土": "火",
            "金": "土",
            "水": "金"
        }
        
        support_element = support_elements.get(day_element, "")
        return five_elements.get(support_element, 0)

# 测试新的计算器
def test_improved_calculator():
    """测试改进的计算器"""
    calculator = ImprovedBaziCalculator()
    
    # 测试一个案例
    birth_time = datetime(1654, 5, 4, 6, 0)  # 康熙皇帝
    
    pillars = calculator.calculate_pillars(birth_time)
    five_elements = calculator.calculate_five_elements_with_hidden_stems(pillars)
    strength = calculator.analyze_strength_improved(pillars, five_elements, birth_time)
    
    print("改进后的八字计算结果:")
    print(f"四柱: {pillars}")
    print(f"五行: {five_elements}")
    print(f"旺衰: {strength}")

if __name__ == "__main__":
    test_improved_calculator()
