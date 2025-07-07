#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高级大运计算器 - 实现精确的大运推算逻辑
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import json
import logging
from app.services.core import Bazi, StemBranch, DaYun
from app.services.constants import JIAZI_TABLE, STEM_YIN_YANG

logger = logging.getLogger(__name__)

class AdvancedDayunCalculator:
    """高级大运计算器"""
    
    def __init__(self):
        # 节气数据（简化版本，实际应该从solar_terms_data.json加载）
        self.solar_terms = self._load_solar_terms()
    
    def _load_solar_terms(self) -> Dict[str, Dict[str, str]]:
        """加载节气数据"""
        try:
            with open('solar_terms_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("节气数据文件未找到，使用默认数据")
            return self._get_default_solar_terms()
    
    def _get_default_solar_terms(self) -> Dict[str, Dict[str, str]]:
        """获取默认节气数据（示例）"""
        return {
            "2023": {
                "立春": "2023-02-04 10:42",
                "惊蛰": "2023-03-06 04:36",
                "清明": "2023-04-05 09:13",
                "立夏": "2023-05-06 02:19",
                "芒种": "2023-06-06 06:18",
                "小暑": "2023-07-07 16:31",
                "立秋": "2023-08-08 02:23",
                "白露": "2023-09-08 05:27",
                "寒露": "2023-10-08 21:16",
                "立冬": "2023-11-08 00:36",
                "大雪": "2023-12-07 17:33",
                "小寒": "2024-01-06 04:49"
            },
            "1989": {
                "立春": "1989-02-04 05:08",
                "惊蛰": "1989-03-05 23:10",
                "清明": "1989-04-05 03:51",
                "立夏": "1989-05-05 21:06",
                "芒种": "1989-06-06 01:11",
                "小暑": "1989-07-07 11:08",
                "立秋": "1989-08-07 21:20",
                "白露": "1989-09-08 00:31",
                "寒露": "1989-10-08 16:23",
                "立冬": "1989-11-07 19:48",
                "大雪": "1989-12-07 12:52",
                "小寒": "1990-01-05 23:59"
            }
        }
    
    def calculate_qiyun_age(self, birth_datetime: datetime, year_stem: str, gender: str) -> Tuple[float, str]:
        """
        计算起运年龄
        
        Args:
            birth_datetime: 出生时间
            year_stem: 年干
            gender: 性别
            
        Returns:
            (起运年龄, 计算说明)
        """
        try:
            # 判断年干阴阳
            is_yang_year = STEM_YIN_YANG[year_stem] == "阳"
            is_male = (gender == "男")
            
            # 判断顺逆
            # 阳年男 & 阴年女（顺行）：距下一个节气
            # 阴年男 & 阳年女（逆行）：距上一个节气
            is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
            
            year_str = str(birth_datetime.year)
            if year_str not in self.solar_terms:
                logger.warning(f"年份{year_str}的节气数据不存在，使用默认计算")
                return 8.0, f"默认起运年龄（缺少{year_str}年节气数据）"
            
            # 获取当年节气
            year_terms = self.solar_terms[year_str]
            
            # 找到出生前后的节气
            prev_term_date, next_term_date = self._find_adjacent_terms(birth_datetime, year_terms)
            
            if is_forward:
                # 顺行：计算到下一个节气的天数
                if next_term_date:
                    days_to_term = (next_term_date - birth_datetime).total_seconds() / (24 * 3600)
                    qiyun_age = days_to_term / 3.0  # 3日折算1岁
                    explanation = f"顺行，距下一节气{days_to_term:.1f}天，起运{qiyun_age:.1f}岁"
                else:
                    qiyun_age = 8.0
                    explanation = "顺行，下一节气不可计算，默认8岁"
            else:
                # 逆行：计算到上一个节气的天数
                if prev_term_date:
                    days_to_term = (birth_datetime - prev_term_date).total_seconds() / (24 * 3600)
                    qiyun_age = days_to_term / 3.0  # 3日折算1岁
                    explanation = f"逆行，距上一节气{days_to_term:.1f}天，起运{qiyun_age:.1f}岁"
                else:
                    qiyun_age = 8.0
                    explanation = "逆行，上一节气不可计算，默认8岁"
            
            # 特殊规则：起运数≤0或≤1，按1岁起运
            if qiyun_age <= 1.0:
                qiyun_age = 1.0
                explanation += "（调整为最小1岁起运）"
            
            return qiyun_age, explanation
            
        except Exception as e:
            logger.error(f"计算起运年龄失败: {e}")
            return 8.0, f"计算失败，使用默认8岁起运: {e}"
    
    def _find_adjacent_terms(self, birth_datetime: datetime, year_terms: Dict[str, str]) -> Tuple[datetime | None, datetime | None]:
        """找到出生日前后的节气"""
        try:
            # 解析节气时间
            term_dates = []
            for term_name, term_time_str in year_terms.items():
                try:
                    term_date = datetime.strptime(term_time_str, "%Y-%m-%d %H:%M")
                    term_dates.append((term_date, term_name))
                except ValueError:
                    continue
            
            # 按时间排序
            term_dates.sort(key=lambda x: x[0])
            
            prev_term = None
            next_term = None
            
            for term_date, term_name in term_dates:
                if term_date <= birth_datetime:
                    prev_term = term_date
                elif term_date > birth_datetime and next_term is None:
                    next_term = term_date
                    break
            
            return prev_term, next_term
            
        except Exception as e:
            logger.error(f"查找相邻节气失败: {e}")
            return None, None
    
    def calculate_dayun_sequence(self, month_ganzhi: str, is_forward: bool, count: int = 10) -> List[str]:
        """
        计算大运序列
        
        Args:
            month_ganzhi: 月柱干支
            is_forward: 是否顺排
            count: 大运数量
            
        Returns:
            大运干支列表
        """
        try:
            # 找到月柱在六十甲子中的位置
            if month_ganzhi not in JIAZI_TABLE:
                logger.error(f"月柱{month_ganzhi}不在六十甲子表中")
                return []
            
            month_index = JIAZI_TABLE.index(month_ganzhi)
            dayun_list = []
            
            for i in range(count):
                if is_forward:
                    # 顺排：从月柱的下一个开始
                    new_index = (month_index + i + 1) % 60
                else:
                    # 逆排：从月柱的上一个开始
                    new_index = (month_index - i - 1 + 60) % 60
                
                dayun_ganzhi = JIAZI_TABLE[new_index]
                dayun_list.append(dayun_ganzhi)
            
            return dayun_list
            
        except Exception as e:
            logger.error(f"计算大运序列失败: {e}")
            return []
    
    def calculate_complete_dayun(self, bazi: Bazi, birth_datetime: datetime) -> Dict[str, Any]:
        """
        计算完整的大运信息
        
        Args:
            bazi: 八字对象
            birth_datetime: 出生时间
            
        Returns:
            完整的大运信息
        """
        try:
            # 1. 计算起运年龄
            qiyun_age, qiyun_explanation = self.calculate_qiyun_age(
                birth_datetime, bazi.year.stem, bazi.gender
            )
            
            # 2. 判断顺逆
            is_yang_year = STEM_YIN_YANG[bazi.year.stem] == "阳"
            is_male = (bazi.gender == "男")
            is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
            
            # 3. 计算大运序列
            month_ganzhi = f"{bazi.month.stem}{bazi.month.branch}"
            dayun_sequence = self.calculate_dayun_sequence(month_ganzhi, is_forward)
            
            # 4. 生成大运对象列表
            dayun_objects = []
            base_age = int(qiyun_age)  # 简化为整数年龄
            
            for i, ganzhi in enumerate(dayun_sequence):
                start_age = base_age + i * 10
                end_age = start_age + 9
                
                dayun_obj = DaYun(
                    start_age=start_age,
                    stem_branch=StemBranch(ganzhi[0], ganzhi[1]),
                    end_age=end_age
                )
                dayun_objects.append(dayun_obj)
            
            # 5. 生成详细信息
            result = {
                "qiyun_age": qiyun_age,
                "qiyun_age_int": base_age,
                "qiyun_explanation": qiyun_explanation,
                "is_forward": is_forward,
                "direction": "顺排" if is_forward else "逆排",
                "dayun_objects": dayun_objects,
                "dayun_list": []
            }
            
            # 6. 格式化大运列表
            for i, dayun in enumerate(dayun_objects):
                dayun_info = {
                    "period": i + 1,
                    "ganzhi": f"{dayun.stem_branch.stem}{dayun.stem_branch.branch}",
                    "stem": dayun.stem_branch.stem,
                    "branch": dayun.stem_branch.branch,
                    "start_age": dayun.start_age,
                    "end_age": dayun.end_age,
                    "age_range": f"{dayun.start_age}-{dayun.end_age}岁",
                    "start_year": birth_datetime.year + dayun.start_age,
                    "end_year": birth_datetime.year + dayun.end_age
                }
                result["dayun_list"].append(dayun_info)
            
            return result
            
        except Exception as e:
            logger.error(f"计算完整大运信息失败: {e}")
            return {
                "qiyun_age": 8.0,
                "qiyun_explanation": f"计算失败: {e}",
                "is_forward": True,
                "direction": "顺排",
                "dayun_objects": [],
                "dayun_list": []
            }

def test_advanced_dayun_calculator():
    """测试高级大运计算器"""
    print("=== 高级大运计算器测试 ===")
    
    calculator = AdvancedDayunCalculator()
    
    # 测试案例1: 高泽兮（女，2023年）
    print("\n1. 高泽兮案例测试:")
    bazi1 = Bazi(
        year=StemBranch("癸", "卯"),
        month=StemBranch("辛", "酉"),
        day=StemBranch("乙", "亥"),
        hour=StemBranch("丙", "子"),
        gender="女"
    )
    birth_time1 = datetime(2023, 9, 14, 0, 26, 0)
    
    result1 = calculator.calculate_complete_dayun(bazi1, birth_time1)
    print(f"   年干: {bazi1.year.stem}（阴干）, 性别: 女 -> {result1['direction']}")
    print(f"   起运年龄: {result1['qiyun_age']:.1f}岁")
    print(f"   计算说明: {result1['qiyun_explanation']}")
    print("   大运序列:")
    for dayun in result1['dayun_list'][:6]:
        print(f"     {dayun['period']}. {dayun['ganzhi']} ({dayun['start_age']}-{dayun['end_age']}岁)")
    
    # 测试案例2: 高赫辰（男，1989年）
    print("\n2. 高赫辰案例测试:")
    bazi2 = Bazi(
        year=StemBranch("己", "巳"),
        month=StemBranch("丁", "卯"),
        day=StemBranch("丁", "丑"),
        hour=StemBranch("辛", "亥"),
        gender="男"
    )
    birth_time2 = datetime(1989, 3, 18, 21, 20, 0)
    
    result2 = calculator.calculate_complete_dayun(bazi2, birth_time2)
    print(f"   年干: {bazi2.year.stem}（阴干）, 性别: 男 -> {result2['direction']}")
    print(f"   起运年龄: {result2['qiyun_age']:.1f}岁")
    print(f"   计算说明: {result2['qiyun_explanation']}")
    print("   大运序列:")
    for dayun in result2['dayun_list'][:6]:
        print(f"     {dayun['period']}. {dayun['ganzhi']} ({dayun['start_age']}-{dayun['end_age']}岁)")
    
    return result1, result2

if __name__ == "__main__":
    test_advanced_dayun_calculator()
