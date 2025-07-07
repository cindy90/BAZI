"""
八字计算核心数据结构模块
包含 StemBranch, Bazi, DaYun, ShenSha 等基础类
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from collections import deque
import functools


class StemBranch:
    """干支结构"""
    def __init__(self, stem: str, branch: str):
        self.stem = stem    # 天干
        self.branch = branch # 地支
        
    def __repr__(self):
        return f"{self.stem}{self.branch}"
    
    def __eq__(self, other):
        if isinstance(other, StemBranch):
            return self.stem == other.stem and self.branch == other.branch
        return False


class Bazi:
    """八字命盘"""
    def __init__(
        self, 
        year: StemBranch, 
        month: StemBranch, 
        day: StemBranch, 
        hour: StemBranch,
        gender: str,  # '男' 或 '女'
        birth_time: Optional[datetime] = None
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.gender = gender
        self.birth_time = birth_time
        self.day_master = self.day.stem  # 日干作为日主
        self.zodiac = self._get_zodiac()  # 计算生肖
        
    def _get_zodiac(self) -> str:
        """根据年支计算生肖"""
        zodiac_map = {
            "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔", 
            "辰": "龙", "巳": "蛇", "午": "马", "未": "羊", 
            "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪"
        }
        return zodiac_map.get(self.year.branch, "")
    
    def get_bazi_characters(self) -> Dict[str, str]:
        """获取八字字符信息"""
        return {
            "year_stem": self.year.stem,
            "year_branch": self.year.branch,
            "month_stem": self.month.stem,
            "month_branch": self.month.branch,
            "day_stem": self.day.stem,
            "day_branch": self.day.branch,
            "hour_stem": self.hour.stem,
            "hour_branch": self.hour.branch
        }
    
    def get_day_master(self) -> str:
        """获取日主"""
        return self.day_master
    
    def get_zodiac(self) -> str:
        """获取生肖"""
        return self.zodiac
    
    def get_year_stem(self) -> str:
        return self.year.stem
        
    def is_male(self) -> bool:
        return self.gender == '男'
    
    def get_position_element(self, position: str) -> str:
        """获取指定位置的五行（默认返回地支五行）
        
        Args:
            position: 位置，支持中文("年","月","日","时")和英文("year","month","day","hour")
            
        Returns:
            对应的五行属性，如果位置无效则返回空字符串
        """
        try:
            # 导入常量，避免循环导入
            from .constants import BRANCH_ELEMENTS, STEM_ELEMENTS
            
            pos_mapping = {
                # 中文位置 - 返回地支五行
                "年": self.year.branch,
                "月": self.month.branch,
                "日": self.day.branch,
                "时": self.hour.branch,
                # 英文位置 - 返回地支五行
                "year": self.year.branch,
                "month": self.month.branch,
                "day": self.day.branch,
                "hour": self.hour.branch,
                # 英文复数形式
                "years": self.year.branch,
                "months": self.month.branch,
                "days": self.day.branch,
                "hours": self.hour.branch
            }
            
            branch = pos_mapping.get(position, "")
            if branch:
                return BRANCH_ELEMENTS.get(branch, "")
            return ""
            
        except ImportError:
            # 如果导入失败，使用备用常量
            BRANCH_ELEMENTS = {
                "子": "水", "丑": "土", "寅": "木", "卯": "木", 
                "辰": "土", "巳": "火", "午": "火", "未": "土", 
                "申": "金", "酉": "金", "戌": "土", "亥": "水"
            }
            
            pos_mapping = {
                "年": self.year.branch, "月": self.month.branch,
                "日": self.day.branch, "时": self.hour.branch,
                "year": self.year.branch, "month": self.month.branch,
                "day": self.day.branch, "hour": self.hour.branch,
                "years": self.year.branch, "months": self.month.branch,
                "days": self.day.branch, "hours": self.hour.branch
            }
            
            branch = pos_mapping.get(position, "")
            if branch:
                return BRANCH_ELEMENTS.get(branch, "")
            return ""
        except Exception:
            return ""
    
    def get_position_branch(self, position: str) -> str:
        """获取指定位置的地支"""
        pos_mapping = {
            "年": self.year.branch,
            "月": self.month.branch,
            "日": self.day.branch,
            "时": self.hour.branch
        }
        
        return pos_mapping.get(position, "")
    
    def get_position_stem(self, position: str) -> str:
        """获取指定位置的天干"""
        pos_mapping = {
            "年": self.year.stem,
            "月": self.month.stem,
            "日": self.day.stem,
            "时": self.hour.stem
        }
        
        return pos_mapping.get(position, "")
    
    def get_position_stem_branch(self, position: str) -> Optional[StemBranch]:
        """获取指定位置的完整干支"""
        pos_mapping = {
            "年": self.year,
            "月": self.month,
            "日": self.day,
            "时": self.hour
        }
        
        return pos_mapping.get(position, None)
    
    def get_all_stems(self) -> List[str]:
        """获取四柱天干列表"""
        return [
            self.year.stem,
            self.month.stem,
            self.day.stem,
            self.hour.stem
        ]
    
    def get_all_branches(self) -> List[str]:
        """获取四柱地支列表"""
        return [
            self.year.branch,
            self.month.branch,
            self.day.branch,
            self.hour.branch
        ]
    
    def get_pillar_branch(self, pillar_name: str) -> str:
        """根据柱名获取对应的地支
        
        Args:
            pillar_name: 柱名，支持中文("年","月","日","时")和英文("year","month","day","hour")
            
        Returns:
            对应的地支，如果柱名无效则返回空字符串
        """
        name_mapping = {
            # 中文柱名
            "年": self.year.branch,
            "月": self.month.branch,
            "日": self.day.branch,
            "时": self.hour.branch,
            # 英文柱名
            "year": self.year.branch,
            "month": self.month.branch,
            "day": self.day.branch,
            "hour": self.hour.branch,
            # 英文复数形式
            "years": self.year.branch,
            "months": self.month.branch,
            "days": self.day.branch,
            "hours": self.hour.branch
        }
        return name_mapping.get(pillar_name, "")
    
    def get_pillar_element(self, pillar_name: str) -> str:
        """根据柱名获取对应的五行（默认返回地支五行）
        
        Args:
            pillar_name: 柱名，支持中文("年","月","日","时")和英文("year","month","day","hour")
            
        Returns:
            对应的五行属性，如果柱名无效则返回空字符串
        """
        try:
            # 导入常量，避免循环导入
            from .constants import BRANCH_ELEMENTS, STEM_ELEMENTS
            
            name_mapping = {
                # 中文柱名 - 返回地支五行
                "年": self.year.branch,
                "月": self.month.branch,
                "日": self.day.branch,
                "时": self.hour.branch,
                # 英文柱名 - 返回地支五行
                "year": self.year.branch,
                "month": self.month.branch,
                "day": self.day.branch,
                "hour": self.hour.branch
            }
            
            branch = name_mapping.get(pillar_name, "")
            return BRANCH_ELEMENTS.get(branch, "")
        except ImportError:
            # 备用常量定义
            branch_elements = {
                "子": "水", "丑": "土", "寅": "木", "卯": "木",
                "辰": "土", "巳": "火", "午": "火", "未": "土",
                "申": "金", "酉": "金", "戌": "土", "亥": "水"
            }
            name_mapping = {
                "年": self.year.branch, "月": self.month.branch,
                "日": self.day.branch, "时": self.hour.branch,
                "year": self.year.branch, "month": self.month.branch,
                "day": self.day.branch, "hour": self.hour.branch
            }
            branch = name_mapping.get(pillar_name, "")
            return branch_elements.get(branch, "")
    
    def get_pillar_stem_element(self, pillar_name: str) -> str:
        """根据柱名获取对应的天干五行
        
        Args:
            pillar_name: 柱名，支持中文("年","月","日","时")和英文("year","month","day","hour")
            
        Returns:
            对应的天干五行属性，如果柱名无效则返回空字符串
        """
        try:
            from .constants import STEM_ELEMENTS
            
            name_mapping = {
                # 中文柱名 - 返回天干五行
                "年": self.year.stem,
                "月": self.month.stem,
                "日": self.day.stem,
                "时": self.hour.stem,
                # 英文柱名 - 返回天干五行
                "year": self.year.stem,
                "month": self.month.stem,
                "day": self.day.stem,
                "hour": self.hour.stem
            }
            
            stem = name_mapping.get(pillar_name, "")
            return STEM_ELEMENTS.get(stem, "")
        except ImportError:
            # 备用常量定义
            stem_elements = {
                "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
                "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
            }
            name_mapping = {
                "年": self.year.stem, "月": self.month.stem,
                "日": self.day.stem, "时": self.hour.stem,
                "year": self.year.stem, "month": self.month.stem,
                "day": self.day.stem, "hour": self.hour.stem
            }
            stem = name_mapping.get(pillar_name, "")
            return stem_elements.get(stem, "")
    
    def get_stem_branch_string(self, pillar_name: str) -> str:
        """根据柱名获取完整的干支字符串
        
        Args:
            pillar_name: 柱名，支持中文("年","月","日","时")和英文("year","month","day","hour")
            
        Returns:
            完整的干支字符串，如"甲子"，如果柱名无效则返回空字符串
        """
        name_mapping = {
            # 中文柱名
            "年": self.year,
            "月": self.month,
            "日": self.day,
            "时": self.hour,
            # 英文柱名
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour
        }
        
        stem_branch = name_mapping.get(pillar_name)
        if stem_branch:
            return f"{stem_branch.stem}{stem_branch.branch}"
        return ""
    
    def has_stem_in_pillars(self, stem: str) -> bool:
        """检查指定天干是否出现在四柱中
        
        Args:
            stem: 天干
            
        Returns:
            如果天干存在于四柱中则返回True，否则返回False
        """
        return stem in self.get_all_stems()
    
    def has_branch_in_pillars(self, branch: str) -> bool:
        """检查指定地支是否出现在四柱中
        
        Args:
            branch: 地支
            
        Returns:
            如果地支存在于四柱中则返回True，否则返回False
        """
        return branch in self.get_all_branches()
    
    def count_element_in_pillars(self, element: str) -> int:
        """统计指定五行在四柱中出现的次数（包括天干和地支）
        
        Args:
            element: 五行名称（"金","木","水","火","土"）
            
        Returns:
            五行出现的总次数
        """
        try:
            from .constants import STEM_ELEMENTS, BRANCH_ELEMENTS
            
            count = 0
            
            # 统计天干五行
            for stem in self.get_all_stems():
                if STEM_ELEMENTS.get(stem, "") == element:
                    count += 1
            
            # 统计地支五行
            for branch in self.get_all_branches():
                if BRANCH_ELEMENTS.get(branch, "") == element:
                    count += 1
            
            return count
        except ImportError:
            return 0
    
    def get_dominant_element(self) -> str:
        """获取主导五行"""
        distribution = self.get_elements_distribution()
        if not distribution:
            return ""
        return max(distribution.keys(), key=lambda x: distribution[x])
    
    def count_branch_occurrences(self, branch: str) -> int:
        """统计某个地支在四柱中出现的次数"""
        return self.get_all_branches().count(branch)
    
    def count_stem_occurrences(self, stem: str) -> int:
        """统计某个天干在四柱中出现的次数"""
        return self.get_all_stems().count(stem)
    
    def find_branch_positions(self, branch: str) -> List[str]:
        """查找某个地支在四柱中的位置"""
        positions = []
        branch_positions = [
            ("年", self.year.branch),
            ("月", self.month.branch),
            ("日", self.day.branch),
            ("时", self.hour.branch)
        ]
        
        for position, pillar_branch in branch_positions:
            if pillar_branch == branch:
                positions.append(position)
        
        return positions
    
    def find_stem_positions(self, stem: str) -> List[str]:
        """查找某个天干在四柱中的位置"""
        positions = []
        stem_positions = [
            ("年", self.year.stem),
            ("月", self.month.stem),
            ("日", self.day.stem),
            ("时", self.hour.stem)
        ]
        
        for position, pillar_stem in stem_positions:
            if pillar_stem == stem:
                positions.append(position)
        
        return positions
    
    def has_stem_branch_combination(self, stem: str, branch: str) -> bool:
        """检查是否存在特定的干支组合"""
        target_combination = stem + branch
        pillars = self.get_all_stem_branches()
        return target_combination in pillars
    
    def get_branch_elements(self) -> List[str]:
        """获取所有地支对应的五行"""
        from .constants import BRANCH_ELEMENTS
        return [BRANCH_ELEMENTS.get(branch, "") for branch in self.get_all_branches()]
    
    def get_stem_elements(self) -> List[str]:
        """获取所有天干对应的五行"""
        from .constants import STEM_ELEMENTS
        return [STEM_ELEMENTS.get(stem, "") for stem in self.get_all_stems()]
    
    def get_hidden_stems_in_branches(self) -> Dict[str, List[str]]:
        """获取所有地支中的藏干"""
        from .constants import BRANCH_HIDDEN_STEMS
        
        hidden_stems = {}
        for i, branch in enumerate(self.get_all_branches()):
            position = ["年", "月", "日", "时"][i]
            hidden_stems_dict = BRANCH_HIDDEN_STEMS.get(branch, {})
            hidden_stems[position] = list(hidden_stems_dict.keys())
        
        return hidden_stems
    
    def analyze_branch_relationships(self, target_branch: str) -> Dict[str, List[str]]:
        """分析某个地支与命局的关系"""
        import constants
        
        relationships = {
            "conflicts": [],
            "combinations": [],
            "punishments": [],
            "harms": []
        }
        
        # 检查六冲
        conflict_pairs = [tuple(pair) for pair in constants.BRANCH_SIX_CONFLICTS]
        for pair in conflict_pairs:
            if target_branch in pair:
                conflict_branch = pair[1] if pair[0] == target_branch else pair[0]
                positions = self.find_branch_positions(conflict_branch)
                for pos in positions:
                    relationships["conflicts"].append(f"{target_branch}冲{pos}支{conflict_branch}")
        
        # 检查六合
        for (branch1, branch2), _ in constants.BRANCH_SIX_COMBINATIONS.items():
            if target_branch == branch1:
                positions = self.find_branch_positions(branch2)
                for pos in positions:
                    relationships["combinations"].append(f"{target_branch}合{pos}支{branch2}")
            elif target_branch == branch2:
                positions = self.find_branch_positions(branch1)
                for pos in positions:
                    relationships["combinations"].append(f"{target_branch}合{pos}支{branch1}")
        
        return relationships
    
    def get_month_season(self) -> str:
        """获取月令对应的季节"""
        season_map = {
            "寅": "春", "卯": "春", "辰": "春",
            "巳": "夏", "午": "夏", "未": "夏", 
            "申": "秋", "酉": "秋", "戌": "秋",
            "亥": "冬", "子": "冬", "丑": "冬"
        }
        return season_map.get(self.month.branch, "")
    
    def is_day_master_strong(self) -> Optional[bool]:
        """简单判断日主强弱（基于月令）"""
        import constants
        
        day_element = constants.STEM_ELEMENTS.get(self.day.stem, "")
        month_element = constants.BRANCH_ELEMENTS.get(self.month.branch, "")
        
        if not day_element or not month_element:
            return None
        
        # 简化规则：月令生扶为强，月令克耗为弱
        if month_element == day_element:
            return True  # 月令同气
        elif day_element == "木" and month_element == "水":
            return True  # 水生木
        elif day_element == "火" and month_element == "木":
            return True  # 木生火
        elif day_element == "土" and month_element == "火":
            return True  # 火生土
        elif day_element == "金" and month_element == "土":
            return True  # 土生金
        elif day_element == "水" and month_element == "金":
            return True  # 金生水
        else:
            return False  # 其他情况视为偏弱
    
    def __str__(self):
        """字符串表示"""
        return f"{self.year}{self.month}{self.day}{self.hour}"
    
    def __repr__(self):
        """详细表示"""
        return f"Bazi(年:{self.year}, 月:{self.month}, 日:{self.day}, 时:{self.hour}, 性别:{self.gender})"

    def get_elements_distribution(self) -> Dict[str, int]:
        """获取八字中五行分布统计
        
        Returns:
            五行分布字典，键为五行名称，值为出现次数
        """
        from .constants import STEM_ELEMENTS, BRANCH_ELEMENTS
        
        distribution = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        
        # 统计天干五行
        for stem in self.get_all_stems():
            element = STEM_ELEMENTS.get(stem, "")
            if element in distribution:
                distribution[element] += 1
        
        # 统计地支五行
        for branch in self.get_all_branches():
            element = BRANCH_ELEMENTS.get(branch, "")
            if element in distribution:
                distribution[element] += 1
        
        return distribution
    
    def get_all_stem_branches(self) -> List[str]:
        """获取四柱天干地支组合列表
        
        Returns:
            四柱天干地支组合列表，如 ["甲子", "乙丑", "丙寅", "丁卯"]
        """
        return [
            self.year.stem + self.year.branch,
            self.month.stem + self.month.branch,
            self.day.stem + self.day.branch,
            self.hour.stem + self.hour.branch
        ]
    
    def get_stem_by_type(self, stem_type: str) -> str:
        """根据类型获取天干
        
        Args:
            stem_type: 天干类型 ("year_stem", "month_stem", "day_stem", "hour_stem")
            
        Returns:
            对应的天干，如果类型无效则返回空字符串
        """
        mapping = {
            "year_stem": self.year.stem,
            "month_stem": self.month.stem,
            "day_stem": self.day.stem,
            "hour_stem": self.hour.stem
        }
        return mapping.get(stem_type, "")
    
    def get_branch_by_type(self, branch_type: str) -> str:
        """根据类型获取地支
        
        Args:
            branch_type: 地支类型 ("year_branch", "month_branch", "day_branch", "hour_branch")
            
        Returns:
            对应的地支，如果类型无效则返回空字符串
        """
        mapping = {
            "year_branch": self.year.branch,
            "month_branch": self.month.branch,
            "day_branch": self.day.branch,
            "hour_branch": self.hour.branch
        }
        return mapping.get(branch_type, "")
    
    @staticmethod
    def safe_get_name(obj) -> str:
        """
        安全获取对象的名称或字符串表示
        
        Args:
            obj: 需要获取名称的对象
            
        Returns:
            对象的名称或字符串表示
        """
        if obj is None:
            return "未知"
        if hasattr(obj, 'name'):
            return str(obj.name)
        if hasattr(obj, '__name__'):
            return str(obj.__name__)
        return str(obj)
    

class DaYun:
    """大运"""
    def __init__(
        self, 
        start_age: int, 
        stem_branch: StemBranch, 
        start_time: Optional[datetime] = None,
        events: Optional[List] = None,
        end_age: Optional[int] = None
    ):
        self.start_age = start_age  # 起运年龄
        self.stem_branch = stem_branch  # 大运干支
        self.start_time = start_time  # 起运时间
        self.events = events or []  # 大运期间的事件
        self.end_age = end_age or (start_age + 9)  # 结束年龄


class ShenSha:
    """神煞"""
    def __init__(
        self, 
        name: str, 
        position: str, 
        strength: float = 1.0,
        active: bool = True,
        tags: Optional[List[str]] = None,
        description: str = "",
        auspicious_level: int = 5
    ):
        self.name = name  # 神煞名称
        self.position = position  # 作用位置
        self.strength = strength  # 作用强度
        self.active = active  # 是否激活
        self.tags = tags or []  # 附加标签
        self.description = description  # 神煞描述
        self.auspicious_level = auspicious_level  # 吉凶等级 (1-10, 1最凶, 10最吉)
        self.positive_tags = []  # 正面标签
        self.negative_tags = []  # 负面标签
        
    def add_tag(self, tag: str):
        self.tags.append(tag)


class FortuneModel:
    """大运模型引擎"""
    
    # 六十甲子表
    JIAZI = [
        StemBranch("甲", "子"), StemBranch("乙", "丑"), StemBranch("丙", "寅"), StemBranch("丁", "卯"), StemBranch("戊", "辰"),
        StemBranch("己", "巳"), StemBranch("庚", "午"), StemBranch("辛", "未"), StemBranch("壬", "申"), StemBranch("癸", "酉"),
        StemBranch("甲", "戌"), StemBranch("乙", "亥"), StemBranch("丙", "子"), StemBranch("丁", "丑"), StemBranch("戊", "寅"),
        StemBranch("己", "卯"), StemBranch("庚", "辰"), StemBranch("辛", "巳"), StemBranch("壬", "午"), StemBranch("癸", "未"),
        StemBranch("甲", "申"), StemBranch("乙", "酉"), StemBranch("丙", "戌"), StemBranch("丁", "亥"), StemBranch("戊", "子"),
        StemBranch("己", "丑"), StemBranch("庚", "寅"), StemBranch("辛", "卯"), StemBranch("壬", "辰"), StemBranch("癸", "巳"),
        StemBranch("甲", "午"), StemBranch("乙", "未"), StemBranch("丙", "申"), StemBranch("丁", "酉"), StemBranch("戊", "戌"),
        StemBranch("己", "亥"), StemBranch("庚", "子"), StemBranch("辛", "丑"), StemBranch("壬", "寅"), StemBranch("癸", "卯"),
        StemBranch("甲", "辰"), StemBranch("乙", "巳"), StemBranch("丙", "午"), StemBranch("丁", "未"), StemBranch("戊", "申"),
        StemBranch("己", "酉"), StemBranch("庚", "戌"), StemBranch("辛", "亥"), StemBranch("壬", "子"), StemBranch("癸", "丑"),
        StemBranch("甲", "寅"), StemBranch("乙", "卯"), StemBranch("丙", "辰"), StemBranch("丁", "巳"), StemBranch("戊", "午"),
        StemBranch("己", "未"), StemBranch("庚", "申"), StemBranch("辛", "酉"), StemBranch("壬", "戌"), StemBranch("癸", "亥")
    ]
    
    @classmethod
    @functools.lru_cache(maxsize=128)
    def calculate_da_yun(cls, birth_chart: Bazi) -> List[DaYun]:
        """计算大运"""
        da_yun_list = []
        
        # 1. 确定顺逆排
        yang_stems = {"甲", "丙", "戊", "庚", "壬"}
        is_forward = (
            (birth_chart.get_year_stem() in yang_stems and birth_chart.is_male()) or
            (birth_chart.get_year_stem() not in yang_stems and not birth_chart.is_male())
        )
        
        # 2. 计算起运时间（简化版，实际需精确计算节气）
        if birth_chart.birth_time:
            start_time = birth_chart.birth_time + timedelta(days=365*8)  # 默认8岁起运
        else:
            start_time = None
        
        # 3. 大运干支序列生成
        fortune_sequence = cls.generate_sequence(
            base=birth_chart.month,
            forward=is_forward,
            steps=10
        )
        
        # 4. 构建大运对象
        for i, stem_branch in enumerate(fortune_sequence):
            start_age = i * 10
            da_yun = DaYun(
                start_age=start_age,
                end_age=start_age + 9,
                stem_branch=stem_branch,
                start_time=start_time + timedelta(days=365*10*i) if start_time else None
            )
            
            # 集成事件反推（简化版）
            da_yun.events = []
            
            da_yun_list.append(da_yun)
            
        return da_yun_list
    
    @classmethod
    def generate_sequence(
        cls, 
        base: StemBranch, 
        forward: bool, 
        steps: int
    ) -> List[StemBranch]:
        """生成干支序列"""
        # 构建六十甲子环状队列
        jiazi_ring = deque(cls.JIAZI)
        
        # 找到基础干支位置
        base_idx = None
        for i, item in enumerate(cls.JIAZI):
            if item.stem == base.stem and item.branch == base.branch:
                base_idx = i
                break
        
        if base_idx is None:
            base_idx = 0  # 默认值，以防找不到匹配
            
        jiazi_ring.rotate(-base_idx)  # 将基础干支旋转到队列开头
        
        sequence = []
        step = 1 if forward else -1
        
        for i in range(1, steps + 1):
            # 计算新位置
            idx = step * i % len(jiazi_ring)
            if idx < 0:
                idx += len(jiazi_ring)
            sequence.append(jiazi_ring[idx])
            
        return sequence
