"""
八字计算器模块 - 计算类
包含 ShenShaCalculator, FiveElementsCalculator 等计算引擎
优化版本：使用外部常量，增强神煞计算精确度，改进喜用神分析
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union, Tuple
import math
import json
import os
from .core import Bazi, ShenSha, DaYun, StemBranch
from .constants import *
from .logger_config import setup_logger
logger = setup_logger("calculators")


class ShenShaCalculator:
    """神煞计算引擎 - 数据驱动版本，支持完全基于规则的神煞计算"""
    
    def __init__(self, rule_file: str = "shensha_rules.json"):
        # 加载神煞规则
        try:
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            full_path = os.path.join(backend_dir, rule_file)
            
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    self.shensha_data = json.load(f)
                    
                # 如果是数组格式，转换为字典格式
                if isinstance(self.shensha_data, list):
                    self.rules = self.shensha_data
                    self.shensha_data = {"rules": self.rules, "shensha_interactions": {}}
                else:
                    self.rules = self.shensha_data.get("rules", self.shensha_data)
                    
                logger.info(f"成功加载神煞规则文件: {full_path}")
            else:
                logger.warning(f"神煞规则文件不存在: {full_path}，使用默认规则")
                self.rules = self._get_default_rules()
                self.shensha_data = {"rules": self.rules, "shensha_interactions": {}}
        except Exception as e:
            logger.error(f"加载神煞规则文件失败: {e}，使用默认规则")
            self.rules = self._get_default_rules()
            self.shensha_data = {"rules": self.rules, "shensha_interactions": {}}
        
        # 创建规则字典以便快速查找
        self.rules_dict = {rule["key"]: rule for rule in self.rules}
        
    def _get_default_rules(self):
        """获取默认神煞规则 - 完整版本，确保在规则文件缺失时仍能正常运行"""
        return [
            {
                "key": "tianyi_guiren",
                "name": "天乙贵人",
                "description": "天乙贵人是八字神煞中最尊贵、最吉祥的贵人星，主逢凶化吉，遇难呈祥。",
                "calc_method": "stem_zhi_lookup",
                "base_stem_types": ["day_stem", "year_stem"],
                "rules": {
                    "甲": ["丑", "未"], "戊": ["丑", "未"],
                    "乙": ["子", "申"], "己": ["子", "申"],
                    "丙": ["亥", "酉"], "丁": ["亥", "酉"],
                    "庚": ["丑", "未"], "辛": ["寅", "午"],
                    "壬": ["卯", "巳"], "癸": ["巳", "卯"]
                },
                "positive_tags": ["贵人", "逢凶化吉", "助力"],
                "negative_tags": [],
                "strength_modifier": {
                    "favorable_element": 1.2,
                    "conflict": 0.5,
                    "harmony": 1.1
                },
                "positions_influence": {
                    "year": "长辈贵人助力",
                    "month": "事业贵人",
                    "day": "配偶贵人",
                    "hour": "子女贵人"
                }
            },
            {
                "key": "tao_hua",
                "name": "桃花",
                "description": "主情欲、艺术、魅力，异性缘佳，但过旺易招情色纠纷。",
                "calc_method": "base_zhi_lookup",
                "base_zhi_types": ["year_branch", "day_branch"],
                "rules": {
                    "寅": "卯", "午": "卯", "戌": "卯",
                    "亥": "子", "卯": "子", "未": "子",
                    "申": "酉", "子": "酉", "辰": "酉",
                    "巳": "午", "酉": "午", "丑": "午"
                },
                "positive_tags": ["魅力", "艺术", "异性缘"],
                "negative_tags": ["情色", "风流"],
                "strength_modifier": {
                    "day_master_weak": 0.8,
                    "day_master_strong": 1.2,
                    "multiple_appearance": 1.5
                },
                "positions_influence": {
                    "year": "早年风流",
                    "month": "异性缘佳",
                    "day": "配偶有魅力",
                    "hour": "晚年桃花"
                }
            },
            {
                "key": "yima",
                "name": "驿马",
                "description": "主变动、出行、搬迁，动中求财，但易奔波劳碌。",
                "calc_method": "base_zhi_lookup",
                "base_zhi_types": ["year_branch", "day_branch"],
                "rules": {
                    "申": "寅", "子": "寅", "辰": "寅",
                    "寅": "申", "午": "申", "戌": "申",
                    "巳": "亥", "酉": "亥", "丑": "亥",
                    "亥": "巳", "卯": "巳", "未": "巳"
                },
                "positive_tags": ["变动", "出行", "求财"],
                "negative_tags": ["奔波", "劳碌"],
                "strength_modifier": {
                    "conflict": 1.5,
                    "harmony": 0.7,
                    "with_wealth": 1.2
                },
                "positions_influence": {
                    "year": "祖上多迁移",
                    "month": "事业多变动",
                    "day": "本人好动",
                    "hour": "晚年不安"
                }
            },
            {
                "key": "kongwang",
                "name": "空亡",
                "description": "主虚空、失落，但有时反而逢凶化吉，空中求有。",
                "calc_method": "xunkong",
                "base_pillar_types": ["day_pillar"],
                "positive_tags": ["逢凶化吉", "空中求有"],
                "negative_tags": ["虚空", "失落", "不实"],
                "strength_modifier": {
                    "conflict_resolution": 0.3,
                    "with_noble": 0.8
                },
                "positions_influence": {
                    "year": "祖业空虚",
                    "month": "事业虚浮",
                    "day": "婚姻虚空",
                    "hour": "子女缘薄"
                }
            }
        ]
        
    def get_nayin_element_index(self, gan: str, zhi: str) -> int:
        """根据干支计算纳音，并返回其五行索引"""
        ganzhi_str = gan + zhi
        nayin_name = NAYIN_MAP_COMPLETE.get(ganzhi_str)
        
        if nayin_name:
            for element_name, idx in NAYIN_ELEMENT_MAPPING.items():
                if element_name in nayin_name:
                    return idx
        
        logger.warning(f"无法确定纳音五行: {ganzhi_str}")
        return -1
    
    def get_nayin_name_and_element(self, gan: str, zhi: str) -> tuple[str, int]:
        """获取纳音名称和五行索引"""
        ganzhi_str = gan + zhi
        nayin_name = NAYIN_MAP_COMPLETE.get(ganzhi_str, "未知")
        
        # 应用纳音名称标准化
        if nayin_name in NAYIN_STANDARDIZATION:
            nayin_name = NAYIN_STANDARDIZATION[nayin_name]
        
        element_index = self.get_nayin_element_index(gan, zhi)
        return nayin_name, element_index
        
    def calculate(self, birth_chart: Bazi) -> Dict[str, ShenSha]:
        """计算神煞 - 数据驱动版本"""
        result = {}
        failed_calculations = []
        
        # 1. 基础神煞计算
        for rule in self.rules:
            try:
                shensha = self._dispatch_shensha_calculation(rule, birth_chart)
                if shensha:
                    result[rule["key"]] = shensha
                else:
                    # 计算成功但未找到神煞，创建非激活状态的神煞对象
                    result[rule["key"]] = ShenSha(
                        name=rule["name"],
                        position="",
                        strength=0.0,
                        active=False,
                        description=rule.get("description", "")
                    )
            except Exception as e:
                logger.error(f"计算神煞 {rule['key']} 失败: {e}")
                failed_calculations.append({
                    "key": rule["key"],
                    "name": rule["name"],
                    "error": str(e)
                })
                # 创建失败状态的神煞对象
                result[rule["key"]] = ShenSha(
                    name=rule["name"],
                    position="",
                    strength=0.0,
                    active=False,
                    description=f"计算失败: {e}"
                )
        
        # 2. 神煞互动处理
        try:
            self._process_interactions(result, birth_chart)
        except Exception as e:
            logger.error(f"神煞互动处理失败: {e}")
        
        # 3. 记录失败的计算
        if failed_calculations:
            logger.warning(f"共有 {len(failed_calculations)} 个神煞计算失败")
        
        return result
    
    def _dispatch_shensha_calculation(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """根据计算方法派发神煞计算"""
        calc_method = rule.get("calc_method", "unknown")
        
        if calc_method == "stem_zhi_lookup":
            return self._calculate_stem_zhi_shensha(rule, birth_chart)
        elif calc_method == "base_zhi_lookup":
            return self._calculate_base_zhi_shensha(rule, birth_chart)
        elif calc_method == "day_pillar_specific":
            return self._calculate_day_pillar_specific(rule, birth_chart)
        elif calc_method == "xunkong":
            return self._calculate_xunkong_shensha(rule, birth_chart)
        elif calc_method == "month_based":
            return self._calculate_month_based(rule, birth_chart)
        elif calc_method == "stem_combination":
            return self._calculate_stem_combination(rule, birth_chart)
        elif calc_method == "complex_formula":
            return self._calculate_complex_formula(rule, birth_chart)
        elif calc_method == "specific_days":
            return self._calculate_specific_days(rule, birth_chart)
        else:
            logger.warning(f"未知的神煞计算方法: {calc_method}")
            return None
    
    def _calculate_stem_zhi_shensha(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算基于天干查地支的神煞（如天乙贵人、文昌贵人、禄神等）"""
        base_stems = rule.get("base_stem_types", ["day_stem"])
        rules_map = rule.get("rules", {})
        
        found_positions = []
        position_sources = {}
        
        for stem_type in base_stems:
            stem = self._get_stem_from_type(stem_type, birth_chart)
            if stem in rules_map:
                target_branches = rules_map[stem]
                if isinstance(target_branches, str):
                    target_branches = [target_branches]
                
                # 在八字中查找对应地支
                for target_branch in target_branches:
                    positions = self._find_branch_positions(target_branch, birth_chart)
                    for pos in positions:
                        found_positions.append(pos)
                        position_sources[pos] = f"{stem_type}:{stem}->{target_branch}"
        
        if found_positions:
            shensha = ShenSha(
                name=rule["name"],
                position=", ".join(found_positions),
                strength=1.0,
                active=True,
                description=rule.get("description", "")
            )
            
            # 添加正面和负面标签
            shensha.positive_tags = rule.get("positive_tags", [])
            shensha.negative_tags = rule.get("negative_tags", [])
            
            # 应用强度修正
            self._apply_shensha_modifiers(shensha, rule, birth_chart, found_positions)
            
            return shensha
        
        return None
    
    def _calculate_base_zhi_shensha(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算基于地支查地支的神煞（如桃花、华盖、将星、驿马等）"""
        base_branches = rule.get("base_zhi_types", ["day_branch"])
        rules_map = rule.get("rules", {})
        
        found_positions = []
        position_sources = {}
        
        for branch_type in base_branches:
            branch = self._get_branch_from_type(branch_type, birth_chart)
            if branch in rules_map:
                target_branch = rules_map[branch]
                
                # 在八字中查找对应地支
                positions = self._find_branch_positions(target_branch, birth_chart)
                for pos in positions:
                    found_positions.append(pos)
                    position_sources[pos] = f"{branch_type}:{branch}->{target_branch}"
        
        if found_positions:
            shensha = ShenSha(
                name=rule["name"],
                position=", ".join(found_positions),
                strength=1.0,
                active=True,
                description=rule.get("description", "")
            )
            
            # 添加正面和负面标签
            shensha.positive_tags = rule.get("positive_tags", [])
            shensha.negative_tags = rule.get("negative_tags", [])
            
            # 应用强度修正
            self._apply_shensha_modifiers(shensha, rule, birth_chart, found_positions)
            
            return shensha
        
        return None
    
    def _calculate_day_pillar_specific(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算特定日柱的神煞（如魁罡）"""
        specific_pillars = rule.get("specific_pillars", [])
        day_pillar = f"{birth_chart.day.stem}{birth_chart.day.branch}"
        
        if day_pillar in specific_pillars:
            shensha = ShenSha(
                name=rule["name"],
                position="日柱",
                strength=1.0,
                active=True,
                description=rule.get("description", "")
            )
            
            # 添加正面和负面标签
            shensha.positive_tags = rule.get("positive_tags", [])
            shensha.negative_tags = rule.get("negative_tags", [])
            
            # 应用强度修正
            self._apply_shensha_modifiers(shensha, rule, birth_chart, ["日柱"])
            
            return shensha
        
        return None
    
    def _calculate_xunkong_shensha(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算空亡神煞"""
        day_pillar = f"{birth_chart.day.stem}{birth_chart.day.branch}"
        
        # 根据日柱确定旬空
        xunkong_branches = self._get_xunkong_branches(day_pillar)
        
        if xunkong_branches:
            # 检查八字中是否有空亡的地支
            found_positions = []
            for branch in xunkong_branches:
                positions = self._find_branch_positions(branch, birth_chart)
                found_positions.extend(positions)
            
            if found_positions:
                shensha = ShenSha(
                    name=rule["name"],
                    position=", ".join(found_positions),
                    strength=1.0,
                    active=True,
                    description=rule.get("description", "")
                )
                
                # 添加正面和负面标签
                shensha.positive_tags = rule.get("positive_tags", [])
                shensha.negative_tags = rule.get("negative_tags", [])
                
                # 应用强度修正
                self._apply_shensha_modifiers(shensha, rule, birth_chart, found_positions)
                
                return shensha
        
        return None
    
    def _calculate_month_based(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算基于月份的神煞（如天德、月德等）"""
        month = birth_chart.birth_time.month if birth_chart.birth_time else 7
        month_rules = rule.get("month_rules", {})
        
        if str(month) in month_rules:
            target_stems = month_rules[str(month)]
            if isinstance(target_stems, str):
                target_stems = [target_stems]
            
            # 在八字中查找目标天干
            found_positions = []
            stems = [
                ("年", birth_chart.year.stem),
                ("月", birth_chart.month.stem),
                ("日", birth_chart.day.stem),
                ("时", birth_chart.hour.stem)
            ]
            
            for position, stem in stems:
                if stem in target_stems:
                    found_positions.append(position)
            
            if found_positions:
                shensha = ShenSha(
                    name=rule["name"],
                    position=", ".join(found_positions),
                    strength=1.0,
                    active=True,
                    description=rule.get("description", ""),
                    auspicious_level=rule.get("auspicious_level", 5)
                )
                
                # 添加正面和负面标签
                shensha.positive_tags = rule.get("positive_tags", [])
                shensha.negative_tags = rule.get("negative_tags", [])
                
                # 应用强度修正
                self._apply_shensha_modifiers(shensha, rule, birth_chart, found_positions)
                
                return shensha
        
        return None
    
    def _calculate_stem_combination(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算基于天干合化的神煞（如天德合、月德合等）"""
        base_method = rule.get("base_method", "天德")
        
        if base_method == "天德":
            # 先计算天德
            base_shensha = self._calculate_tianhe_base(birth_chart)
            if base_shensha:
                return self._calculate_combination_shensha(rule, birth_chart, base_shensha)
        elif base_method == "月德":
            # 先计算月德
            base_shensha = self._calculate_yuehe_base(birth_chart)
            if base_shensha:
                return self._calculate_combination_shensha(rule, birth_chart, base_shensha)
        
        return None
    
    def _calculate_complex_formula(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算复杂公式的神煞（如童子煞等）"""
        formula_type = rule.get("formula_type", "")
        
        if formula_type == "童子煞":
            return self._calculate_tongzi_sha(rule, birth_chart)
        
        return None
    
    def _calculate_specific_days(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算特定日柱的神煞（如十灵日等）"""
        specific_days = rule.get("specific_days", [])
        
        # 获取日柱干支
        day_ganzhi = f"{birth_chart.day.stem}{birth_chart.day.branch}"
        
        # 检查是否匹配特定日柱
        if day_ganzhi in specific_days:
            shensha = ShenSha(
                name=rule["name"],
                position="日",
                strength=1.0,
                active=True,
                description=rule.get("description", "")
            )
            
            # 添加正面和负面标签
            shensha.positive_tags = rule.get("positive_tags", [])
            shensha.negative_tags = rule.get("negative_tags", [])
            
            # 应用强度修正
            self._apply_shensha_modifiers(shensha, rule, birth_chart, ["日"])
            
            return shensha
        
        return None
    
    def _calculate_tianhe_base(self, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算天德基础"""
        month = birth_chart.birth_time.month if birth_chart.birth_time else 7
        tianhe_rules = {
            "1": "丁", "2": "申", "3": "壬", "4": "辛", "5": "亥", "6": "甲",
            "7": "癸", "8": "寅", "9": "丙", "10": "乙", "11": "巳", "12": "庚"
        }
        
        if str(month) in tianhe_rules:
            target_stem = tianhe_rules[str(month)]
            stems = [
                ("年", birth_chart.year.stem),
                ("月", birth_chart.month.stem),
                ("日", birth_chart.day.stem),
                ("时", birth_chart.hour.stem)
            ]
            
            for position, stem in stems:
                if stem == target_stem:
                    return ShenSha(
                        name="天德",
                        position=position,
                        strength=1.0,
                        active=True,
                        description="天德贵人",
                        auspicious_level=8
                    )
        
        return None
    
    def _calculate_yuehe_base(self, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算月德基础"""
        month = birth_chart.birth_time.month if birth_chart.birth_time else 7
        yuehe_rules = {
            "1": "丙", "2": "甲", "3": "壬", "4": "庚", "5": "丙", "6": "甲",
            "7": "壬", "8": "庚", "9": "丙", "10": "甲", "11": "壬", "12": "庚"
        }
        
        if str(month) in yuehe_rules:
            target_stem = yuehe_rules[str(month)]
            stems = [
                ("年", birth_chart.year.stem),
                ("月", birth_chart.month.stem),
                ("日", birth_chart.day.stem),
                ("时", birth_chart.hour.stem)
            ]
            
            for position, stem in stems:
                if stem == target_stem:
                    return ShenSha(
                        name="月德",
                        position=position,
                        strength=1.0,
                        active=True,
                        description="月德贵人",
                        auspicious_level=8
                    )
        
        return None
    
    def _calculate_combination_shensha(self, rule: dict, birth_chart: Bazi, base_shensha: ShenSha) -> Optional[ShenSha]:
        """计算合化神煞"""
        # 获取基础神煞对应的天干
        base_stem = None
        if base_shensha.position == "年":
            base_stem = birth_chart.year.stem
        elif base_shensha.position == "月":
            base_stem = birth_chart.month.stem
        elif base_shensha.position == "日":
            base_stem = birth_chart.day.stem
        elif base_shensha.position == "时":
            base_stem = birth_chart.hour.stem
        
        if base_stem:
            # 查找合化的天干
            combination_stems = STEM_COMBINATIONS_DETAILED.get((base_stem, ""), [])
            
            stems = [
                ("年", birth_chart.year.stem),
                ("月", birth_chart.month.stem),
                ("日", birth_chart.day.stem),
                ("时", birth_chart.hour.stem)
            ]
            
            for position, stem in stems:
                if position != base_shensha.position:  # 不是基础神煞的位置
                    for combo_pair, combo_result in STEM_COMBINATIONS_DETAILED.items():
                        if (base_stem, stem) == combo_pair or (stem, base_stem) == combo_pair:
                            return ShenSha(
                                name=rule["name"],
                                position=position,
                                strength=1.0,
                                active=True,
                                description=rule.get("description", ""),
                                auspicious_level=rule.get("auspicious_level", 5)
                            )
        
        return None
    
    def _calculate_tongzi_sha(self, rule: dict, birth_chart: Bazi) -> Optional[ShenSha]:
        """计算童子煞"""
        # 童子煞复杂计算公式
        year_stem = birth_chart.year.stem
        month_branch = birth_chart.month.branch
        day_branch = birth_chart.day.branch
        hour_branch = birth_chart.hour.branch
        
        # 春秋寅子贵，冬夏卯未辰
        # 金木午卯合，水火酉戌多
        # 土命逢辰巳，童子定不错
        
        year_element = STEM_ELEMENTS.get(year_stem, "")
        month_num = birth_chart.birth_time.month if birth_chart.birth_time else 7
        
        is_tongzi = False
        
        # 根据年干和季节判断
        if year_element in ["金", "木"]:
            if month_num in [3, 4, 5, 9, 10, 11]:  # 春秋
                if day_branch in ["寅", "子"] or hour_branch in ["寅", "子"]:
                    is_tongzi = True
        elif year_element in ["水", "火"]:
            if month_num in [6, 7, 8, 12, 1, 2]:  # 夏冬
                if day_branch in ["卯", "未", "辰"] or hour_branch in ["卯", "未", "辰"]:
                    is_tongzi = True
        elif year_element == "土":
            if day_branch in ["辰", "巳"] or hour_branch in ["辰", "巳"]:
                is_tongzi = True
        
        if is_tongzi:
            return ShenSha(
                name=rule["name"],
                position="日时",
                strength=1.0,
                active=True,
                description=rule.get("description", ""),
                auspicious_level=rule.get("auspicious_level", 2)
            )
        
        return None
    
    def analyze_interactions(self, bazi: Bazi) -> Dict[str, Any]:
        """分析神煞互动"""
        try:
            # 先计算所有神煞
            shensha_dict = self.calculate(bazi)
            
            # 分析神煞互动
            interactions = {}
            
            # 提取激活的神煞
            active_shensha = []
            for key, shensha in shensha_dict.items():
                if shensha.active:
                    active_shensha.append({
                        "key": key,
                        "name": shensha.name,
                        "position": shensha.position,
                        "strength": shensha.strength,
                        "auspicious_level": getattr(shensha, 'auspicious_level', 5)
                    })
            
            interactions["active_shensha"] = active_shensha
            interactions["interaction_effects"] = {}
            
            return interactions
            
        except Exception as e:
            logger.error(f"分析神煞互动失败: {e}")
            return {
                "active_shensha": [],
                "interaction_effects": {}
            }
    
    def _get_stem_from_type(self, stem_type: str, birth_chart: Bazi) -> str:
        """根据类型获取天干"""
        if stem_type == "day_stem":
            return birth_chart.day.stem
        elif stem_type == "year_stem":
            return birth_chart.year.stem
        elif stem_type == "month_stem":
            return birth_chart.month.stem
        elif stem_type == "hour_stem":
            return birth_chart.hour.stem
        else:
            logger.warning(f"未知的天干类型: {stem_type}")
            return ""
    
    def _get_branch_from_type(self, branch_type: str, birth_chart: Bazi) -> str:
        """根据类型获取地支"""
        if branch_type == "day_branch":
            return birth_chart.day.branch
        elif branch_type == "year_branch":
            return birth_chart.year.branch
        elif branch_type == "month_branch":
            return birth_chart.month.branch
        elif branch_type == "hour_branch":
            return birth_chart.hour.branch
        else:
            logger.warning(f"未知的地支类型: {branch_type}")
            return ""
    
    def _find_branch_positions(self, target_branch: str, birth_chart: Bazi) -> List[str]:
        """在八字中查找指定地支的位置"""
        positions = []
        position_names = ["年", "月", "日", "时"]
        branches = [
            birth_chart.year.branch,
            birth_chart.month.branch,
            birth_chart.day.branch,
            birth_chart.hour.branch
        ]
        
        for i, branch in enumerate(branches):
            if branch == target_branch:
                positions.append(position_names[i])
        
        return positions
    
    def _get_xunkong_branches(self, day_pillar: str) -> List[str]:
        """根据日柱计算空亡地支"""
        return XUNKONG_MAPPING.get(day_pillar, [])
    
    def _apply_shensha_modifiers(self, shensha: ShenSha, rule: dict, birth_chart: Bazi, positions: List[str]):
        """应用神煞强度修正"""
        try:
            strength_modifier = rule.get("strength_modifier", {})
            
            # 基础修正
            if "day_master_weak" in strength_modifier:
                day_strength = FiveElementsCalculator.calculate_day_master_strength(birth_chart)
                if "弱" in day_strength:
                    shensha.strength *= strength_modifier["day_master_weak"]
            
            if "day_master_strong" in strength_modifier:
                day_strength = FiveElementsCalculator.calculate_day_master_strength(birth_chart)
                if "强" in day_strength:
                    shensha.strength *= strength_modifier["day_master_strong"]
        
        except Exception as e:
            logger.error(f"应用神煞修正失败: {e}")
    
    def _process_interactions(self, shensha_dict: Dict[str, ShenSha], birth_chart: Bazi):
        """处理神煞互动"""
        try:
            # 基本的神煞互动处理
            pass
        except Exception as e:
            logger.error(f"处理神煞互动失败: {e}")
    
    def calculate_shensha(self, bazi: Bazi) -> Dict[str, ShenSha]:
        """计算神煞的别名方法"""
        return self.calculate(bazi)


class FiveElementsCalculator:
    """五行强弱计算器"""
    
    @staticmethod
    def format_dayun_info(start_age: int, luck_pillars: List[DaYun], birth_time: datetime, day_gan: str) -> List[Dict[str, Any]]:
        """格式化大运信息"""
        try:
            formatted_dayun = []
            
            for i, dayun in enumerate(luck_pillars):
                stem_branch = dayun.stem_branch
                ten_god_gan = FiveElementsCalculator.calculate_ten_god_relation(day_gan, stem_branch.stem)
                ten_god_zhi = FiveElementsCalculator.calculate_ten_god_relation(day_gan, BRANCH_MAIN_STEMS.get(stem_branch.branch, stem_branch.branch))
                
                dayun_info = {
                    "period": i + 1,
                    "stem": stem_branch.stem,
                    "branch": stem_branch.branch,
                    "start_age": dayun.start_age,
                    "end_age": dayun.end_age,
                    "ganzhi": stem_branch.stem + stem_branch.branch,
                    "description": f"{dayun.start_age}-{dayun.end_age}岁",
                    "ten_gods_gan": ten_god_gan,
                    "ten_gods_zhi": ten_god_zhi
                }
                formatted_dayun.append(dayun_info)
            
            return formatted_dayun
            
        except Exception as e:
            logger.error(f"格式化大运信息失败: {e}")
            return []

    @staticmethod
    def calculate_day_master_strength(bazi: Bazi) -> str:
        """
        计算日主强弱 - 子平法详细计分规则（调整版）
        采用子平法五行强弱标准算法，细化天干地支、本气中气余气、月令系数等
        """
        try:
            day_stem = bazi.day.stem
            day_element = STEM_ELEMENTS[day_stem]
            
            # 第一步：计算基础分数
            total_score = 0.0
            detail_scores = []
            
            # 天干基础分：年1分，月1分，日1分，时1分
            stems = [bazi.year.stem, bazi.month.stem, bazi.day.stem, bazi.hour.stem]
            stem_positions = ["年干", "月干", "日干", "时干"]
            
            for i, stem in enumerate(stems):
                element = STEM_ELEMENTS[stem]
                base_score = 1.0
                
                if element == day_element:
                    total_score += base_score
                    detail_scores.append(f"{stem_positions[i]}{stem}({element})：+{base_score}分(同类)")
                elif element in REVERSE_GENERATION and REVERSE_GENERATION[element] == day_element:
                    score = base_score * 0.9  # 提高生身分数
                    total_score += score
                    detail_scores.append(f"{stem_positions[i]}{stem}({element})：+{score}分(生身)")
                elif element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[element] == day_element:
                    score = base_score * 0.7  # 降低克身分数
                    total_score -= score
                    detail_scores.append(f"{stem_positions[i]}{stem}({element})：-{score}分(克身)")
                elif day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == element:
                    score = base_score * 0.5  # 降低泄身分数
                    total_score -= score
                    detail_scores.append(f"{stem_positions[i]}{stem}({element})：-{score}分(泄身)")
            
            # 第二步：地支本气、中气、余气分别计分
            branches = [bazi.year.branch, bazi.month.branch, bazi.day.branch, bazi.hour.branch]
            branch_positions = ["年支", "月支", "日支", "时支"]
            
            for i, branch in enumerate(branches):
                hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
                
                # 月支权重适度加强
                position_weight = 2.0 if i == 1 else 1.0  # 降低月支权重
                
                for hidden_stem, weight in hidden_stems.items():
                    element = STEM_ELEMENTS[hidden_stem]
                    
                    # 本气、中气、余气的分数
                    if weight >= 0.6:  # 本气
                        qi_score = 1.0
                        qi_type = "本气"
                    elif weight >= 0.3:  # 中气
                        qi_score = 0.6
                        qi_type = "中气"
                    else:  # 余气
                        qi_score = 0.3
                        qi_type = "余气"
                    
                    final_score = qi_score * position_weight
                    
                    if element == day_element:
                        total_score += final_score
                        detail_scores.append(f"{branch_positions[i]}{branch}藏{hidden_stem}({element},{qi_type})：+{final_score}分(同类)")
                    elif element in REVERSE_GENERATION and REVERSE_GENERATION[element] == day_element:
                        score = final_score * 0.9  # 提高生身分数
                        total_score += score
                        detail_scores.append(f"{branch_positions[i]}{branch}藏{hidden_stem}({element},{qi_type})：+{score}分(生身)")
                    elif element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[element] == day_element:
                        score = final_score * 0.7  # 降低克身分数
                        total_score -= score
                        detail_scores.append(f"{branch_positions[i]}{branch}藏{hidden_stem}({element},{qi_type})：-{score}分(克身)")
                    elif day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == element:
                        score = final_score * 0.5  # 降低泄身分数
                        total_score -= score
                        detail_scores.append(f"{branch_positions[i]}{branch}藏{hidden_stem}({element},{qi_type})：-{score}分(泄身)")
            
            # 第三步：通根加分（日主在地支有根）
            tonggen_score = 0.0
            for i, branch in enumerate(branches):
                hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
                for hidden_stem, weight in hidden_stems.items():
                    if hidden_stem == day_stem:  # 日主天干在地支有根
                        root_score = weight * 0.8  # 提高通根分数
                        tonggen_score += root_score
                        detail_scores.append(f"{branch_positions[i]}{branch}通根{day_stem}：+{root_score}分(通根)")
            
            total_score += tonggen_score
            
            # 第四步：月令系数调整（降低月令影响）
            month_element = BRANCH_ELEMENTS[bazi.month.branch]
            month_coefficient = 1.0
            
            if month_element == day_element:
                month_coefficient = 1.3  # 降低月令助身系数
                detail_scores.append(f"月令{bazi.month.branch}({month_element})助身：系数×1.3")
            elif month_element in REVERSE_GENERATION and REVERSE_GENERATION[month_element] == day_element:
                month_coefficient = 1.2  # 降低月令生身系数
                detail_scores.append(f"月令{bazi.month.branch}({month_element})生身：系数×1.2")
            elif month_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[month_element] == day_element:
                month_coefficient = 0.8  # 降低月令克身影响
                detail_scores.append(f"月令{bazi.month.branch}({month_element})克身：系数×0.8")
            elif day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == month_element:
                month_coefficient = 0.9  # 降低月令泄身影响
                detail_scores.append(f"月令{bazi.month.branch}({month_element})泄身：系数×0.9")
            
            total_score *= month_coefficient
            
            # 第五步：根据总分判定强弱（调整判定标准）
            if total_score >= 6.0:  # 提高极强阈值
                strength = "极强"
            elif total_score >= 3.5:  # 降低身强阈值
                strength = "身强"
            elif total_score >= 1.5:  # 调整平和范围
                strength = "平和"
            elif total_score >= 0.5:  # 调整身弱阈值
                strength = "身弱"
            else:
                strength = "极弱"
            
            # 记录详细计算过程
            logger.info(f"日主{day_stem}({day_element})强弱计算：")
            for detail in detail_scores:
                logger.info(f"  {detail}")
            logger.info(f"  总分：{total_score:.2f}分，判定：{strength}")
            
            return strength
                
        except Exception as e:
            logger.error(f"计算日主强弱失败: {e}")
            return "未知"
    
    @staticmethod
    def calculate_day_master_strength_detailed(bazi: Bazi) -> Dict[str, Any]:
        """
        计算日主强弱的详细分析 - 子平法详细计分规则
        返回详细的计分过程和结果
        """
        try:
            day_stem = bazi.day.stem
            day_element = STEM_ELEMENTS[day_stem]
            
            # 初始化结果
            result = {
                "day_stem": day_stem,
                "day_element": day_element,
                "total_score": 0.0,
                "strength": "未知",
                "detail_scores": [],
                "calculation_steps": []
            }
            
            total_score = 0.0
            detail_scores = []
            
            # 第一步：计算天干基础分
            stems = [bazi.year.stem, bazi.month.stem, bazi.day.stem, bazi.hour.stem]
            stem_positions = ["年干", "月干", "日干", "时干"]
            
            result["calculation_steps"].append("第一步：天干基础分计算")
            
            for i, stem in enumerate(stems):
                element = STEM_ELEMENTS[stem]
                base_score = 1.0
                
                if element == day_element:
                    total_score += base_score
                    detail = f"{stem_positions[i]}{stem}({element})：+{base_score}分(同类)"
                    detail_scores.append(detail)
                    result["calculation_steps"].append(f"  {detail}")
                elif element in REVERSE_GENERATION and REVERSE_GENERATION[element] == day_element:
                    score = base_score * 0.9
                    total_score += score
                    detail = f"{stem_positions[i]}{stem}({element})：+{score}分(生身)"
                    detail_scores.append(detail)
                    result["calculation_steps"].append(f"  {detail}")
                elif element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[element] == day_element:
                    score = base_score * 0.7
                    total_score -= score
                    detail = f"{stem_positions[i]}{stem}({element})：-{score}分(克身)"
                    detail_scores.append(detail)
                    result["calculation_steps"].append(f"  {detail}")
                elif day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == element:
                    score = base_score * 0.5
                    total_score -= score
                    detail = f"{stem_positions[i]}{stem}({element})：-{score}分(泄身)"
                    detail_scores.append(detail)
                    result["calculation_steps"].append(f"  {detail}")
            
            # 第二步：地支本气、中气、余气分别计分
            branches = [bazi.year.branch, bazi.month.branch, bazi.day.branch, bazi.hour.branch]
            branch_positions = ["年支", "月支", "日支", "时支"]
            
            result["calculation_steps"].append("第二步：地支藏干分计算")
            
            for i, branch in enumerate(branches):
                hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
                
                # 月支权重适度加强
                position_weight = 2.0 if i == 1 else 1.0
                
                for hidden_stem, weight in hidden_stems.items():
                    element = STEM_ELEMENTS[hidden_stem]
                    
                    # 本气、中气、余气的分数
                    if weight >= 0.6:  # 本气
                        qi_score = 1.0
                        qi_type = "本气"
                    elif weight >= 0.3:  # 中气
                        qi_score = 0.6
                        qi_type = "中气"
                    else:  # 余气
                        qi_score = 0.3
                        qi_type = "余气"
                    
                    final_score = qi_score * position_weight
                    
                    if element == day_element:
                        total_score += final_score
                        detail = f"{branch_positions[i]}{branch}藏{hidden_stem}({element},{qi_type})：+{final_score}分(同类)"
                        detail_scores.append(detail)
                        result["calculation_steps"].append(f"  {detail}")
                    elif element in REVERSE_GENERATION and REVERSE_GENERATION[element] == day_element:
                        score = final_score * 0.9
                        total_score += score
                        detail = f"{branch_positions[i]}{branch}藏{hidden_stem}({element},{qi_type})：+{score}分(生身)"
                        detail_scores.append(detail)
                        result["calculation_steps"].append(f"  {detail}")
                    elif element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[element] == day_element:
                        score = final_score * 0.7
                        total_score -= score
                        detail = f"{branch_positions[i]}{branch}藏{hidden_stem}({element},{qi_type})：-{score}分(克身)"
                        detail_scores.append(detail)
                        result["calculation_steps"].append(f"  {detail}")
                    elif day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == element:
                        score = final_score * 0.5
                        total_score -= score
                        detail = f"{branch_positions[i]}{branch}藏{hidden_stem}({element},{qi_type})：-{score}分(泄身)"
                        detail_scores.append(detail)
                        result["calculation_steps"].append(f"  {detail}")
            
            # 第三步：通根加分（日主在地支有根）
            result["calculation_steps"].append("第三步：通根加分计算")
            tonggen_score = 0.0
            
            for i, branch in enumerate(branches):
                hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
                for hidden_stem, weight in hidden_stems.items():
                    if hidden_stem == day_stem:  # 日主天干在地支有根
                        root_score = weight * 0.8
                        tonggen_score += root_score
                        detail = f"{branch_positions[i]}{branch}通根{day_stem}：+{root_score}分(通根)"
                        detail_scores.append(detail)
                        result["calculation_steps"].append(f"  {detail}")
            
            total_score += tonggen_score
            
            # 第四步：月令系数调整
            result["calculation_steps"].append("第四步：月令系数调整")
            month_element = BRANCH_ELEMENTS[bazi.month.branch]
            month_coefficient = 1.0
            
            if month_element == day_element:
                month_coefficient = 1.3  # 月令助身
                detail = f"月令{bazi.month.branch}({month_element})助身：系数×1.3"
                detail_scores.append(detail)
                result["calculation_steps"].append(f"  {detail}")
            elif month_element in REVERSE_GENERATION and REVERSE_GENERATION[month_element] == day_element:
                month_coefficient = 1.2  # 月令生身
                detail = f"月令{bazi.month.branch}({month_element})生身：系数×1.2"
                detail_scores.append(detail)
                result["calculation_steps"].append(f"  {detail}")
            elif month_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[month_element] == day_element:
                month_coefficient = 0.8  # 月令克身
                detail = f"月令{bazi.month.branch}({month_element})克身：系数×0.8"
                detail_scores.append(detail)
                result["calculation_steps"].append(f"  {detail}")
            elif day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == month_element:
                month_coefficient = 0.9  # 月令泄身
                detail = f"月令{bazi.month.branch}({month_element})泄身：系数×0.9"
                detail_scores.append(detail)
                result["calculation_steps"].append(f"  {detail}")
            
            total_score *= month_coefficient
            
            # 第五步：根据总分判定强弱
            if total_score >= 6.0:
                strength = "极强"
            elif total_score >= 3.5:
                strength = "身强"
            elif total_score >= 1.5:
                strength = "平和"
            elif total_score >= 0.5:
                strength = "身弱"
            else:
                strength = "极弱"
            
            result["total_score"] = total_score
            result["strength"] = strength
            result["detail_scores"] = detail_scores
            result["calculation_steps"].append(f"第五步：最终判定")
            result["calculation_steps"].append(f"  总分：{total_score:.2f}分，判定：{strength}")
            
            return result
                
        except Exception as e:
            logger.error(f"详细计算日主强弱失败: {e}")
            return {
                "day_stem": "未知",
                "day_element": "未知",
                "total_score": 0.0,
                "strength": "未知",
                "detail_scores": [],
                "calculation_steps": [f"计算失败: {e}"]
            }
    
    @staticmethod
    def calculate_five_elements_percentage(bazi: Bazi) -> Dict[str, float]:
        """计算五行占比"""
        try:
            element_scores = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}
            
            # 天干得分
            stems = [bazi.year.stem, bazi.month.stem, bazi.day.stem, bazi.hour.stem]
            for stem in stems:
                element = STEM_ELEMENTS[stem]
                element_scores[element] += 1.0
            
            # 地支得分
            branches = [bazi.year.branch, bazi.month.branch, bazi.day.branch, bazi.hour.branch]
            for branch in branches:
                element = BRANCH_ELEMENTS[branch]
                element_scores[element] += 1.0
                
                # 藏干得分
                hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
                for hidden_stem, weight in hidden_stems.items():
                    hidden_element = STEM_ELEMENTS[hidden_stem]
                    element_scores[hidden_element] += weight * 0.5
            
            # 计算总分
            total_score = sum(element_scores.values())
            
            # 计算百分比
            if total_score > 0:
                return {element: (score / total_score) * 100 for element, score in element_scores.items()}
            else:
                return {"木": 20.0, "火": 20.0, "土": 20.0, "金": 20.0, "水": 20.0}
                
        except Exception as e:
            logger.error(f"计算五行占比失败: {e}")
            return {"木": 20.0, "火": 20.0, "土": 20.0, "金": 20.0, "水": 20.0}
    
    @staticmethod
    def get_strength_level_description(strength: str) -> str:
        """获取强度等级描述"""
        descriptions = {
            "极强": "日主极强，需要泄耗",
            "偏强": "日主偏强，宜泄耗",
            "中和": "日主中和，平衡为美",
            "偏弱": "日主偏弱，宜生扶",
            "极弱": "日主极弱，需要生扶"
        }
        return descriptions.get(strength, "强弱未知")
    
    @staticmethod
    def get_favorable_elements(bazi: Bazi) -> List[str]:
        """获取喜用神五行"""
        try:
            day_element = STEM_ELEMENTS[bazi.day.stem]
            strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
            
            if strength in ["极强", "偏强"]:
                # 强则宜泄耗
                favorable = []
                if day_element in FIVE_ELEMENTS_GENERATION:
                    favorable.append(FIVE_ELEMENTS_GENERATION[day_element])  # 我生者（食伤）
                if day_element in FIVE_ELEMENTS_OVERCOMING:
                    favorable.append(FIVE_ELEMENTS_OVERCOMING[day_element])  # 我克者（财星）
                if day_element in REVERSE_OVERCOMING:
                    favorable.append(REVERSE_OVERCOMING[day_element])  # 克我者（官杀）
                return favorable
            elif strength in ["偏弱", "极弱"]:
                # 弱则宜生扶
                favorable = []
                if day_element in REVERSE_GENERATION:
                    favorable.append(REVERSE_GENERATION[day_element])  # 生我者（印星）
                favorable.append(day_element)  # 同类（比劫）
                return favorable
            else:
                # 中和，平衡为美
                return [day_element]
                
        except Exception as e:
            logger.error(f"获取喜用神失败: {e}")
            return []
    
    @staticmethod
    def analyze_dayun_phase(age: int) -> str:
        """分析大运阶段"""
        if age < 16:
            return "少年运"
        elif age < 32:
            return "青年运"
        elif age < 48:
            return "壮年运"
        elif age < 64:
            return "中年运"
        else:
            return "老年运"
    
    @staticmethod
    def calculate_ten_god_relation(day_stem: str, other_stem: str) -> str:
        """计算十神关系"""
        try:
            day_element = STEM_ELEMENTS[day_stem]
            other_element = STEM_ELEMENTS[other_stem]
            day_yin_yang = STEM_YIN_YANG[day_stem]
            other_yin_yang = STEM_YIN_YANG[other_stem]
            
            # 同类
            if day_element == other_element:
                if day_yin_yang == other_yin_yang:
                    return "比肩"
                else:
                    return "劫财"
            
            # 我生者（食伤）
            if day_element in FIVE_ELEMENTS_GENERATION and FIVE_ELEMENTS_GENERATION[day_element] == other_element:
                if day_yin_yang == other_yin_yang:
                    return "食神"
                else:
                    return "伤官"
            
            # 我克者（财星）
            if day_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[day_element] == other_element:
                if day_yin_yang == other_yin_yang:
                    return "偏财"
                else:
                    return "正财"
            
            # 克我者（官杀）
            if other_element in FIVE_ELEMENTS_OVERCOMING and FIVE_ELEMENTS_OVERCOMING[other_element] == day_element:
                if day_yin_yang == other_yin_yang:
                    return "七杀"
                else:
                    return "正官"
            
            # 生我者（印星）
            if other_element in FIVE_ELEMENTS_GENERATION and FIVE_ELEMENTS_GENERATION[other_element] == day_element:
                if day_yin_yang == other_yin_yang:
                    return "偏印"
                else:
                    return "正印"
            
            return "未知"
            
        except Exception as e:
            logger.error(f"计算十神关系失败: {e}")
            return "未知"
    
    @staticmethod
    def get_zhi_hidden_gan(branch: str) -> Dict[str, float]:
        """获取地支藏干"""
        return BRANCH_HIDDEN_STEMS.get(branch, {})
    
    @staticmethod
    def calculate_chang_sheng_twelve_palaces(stem: str, branch: str) -> str:
        """计算长生十二宫"""
        return CHANG_SHENG_MAPPING.get(stem, {}).get(branch, "未知")
    
    @staticmethod
    def get_chang_sheng_strength_level(chang_sheng: str) -> str:
        """获取长生十二宫强度等级（字符串）"""
        return CHANG_SHENG_STRENGTH_LEVELS.get(chang_sheng, "未知")
    
    @staticmethod
    def get_chang_sheng_strength_level_int(chang_sheng: str) -> int:
        """获取长生十二宫强度等级（数值）"""
        return CHANG_SHENG_STRENGTH_VALUES.get(chang_sheng, 5)
    
    @staticmethod
    def analyze_liunian_shensha(bazi: Bazi, year: int) -> Dict[str, List[Dict[str, Any]]]:
        """分析流年神煞"""
        try:
            # 简化版本，返回基本结构
            return {
                "favorable_shensha": [],
                "unfavorable_shensha": []
            }
        except Exception as e:
            logger.error(f"分析流年神煞失败: {e}")
            return {
                "favorable_shensha": [],
                "unfavorable_shensha": []
            }
    
    @staticmethod
    def analyze_comprehensive_gods(bazi: Bazi) -> Dict[str, Any]:
        """综合分析喜用神"""
        try:
            favorable_elements = FiveElementsCalculator.get_favorable_elements(bazi)
            strength = FiveElementsCalculator.calculate_day_master_strength(bazi)
            
            # 确定主要喜用神
            primary_favorable = favorable_elements[0] if favorable_elements else "未知"
            
            return {
                "basic_analysis": {
                    "favorable_elements": favorable_elements,
                    "day_master_strength": strength
                },
                "final_prognosis": {
                    "primary_favorable": primary_favorable,
                    "secondary_favorable": favorable_elements[1] if len(favorable_elements) > 1 else "无",
                    "primary_unfavorable": "未知",
                    "secondary_unfavorable": "无",
                    "avoid_elements": [],
                    "life_advice": f"日主{strength}，建议多用{primary_favorable}相关的颜色、方位、行业",
                    "overall_rating": 7.5,
                    "summary": f"日主{strength}，喜用{primary_favorable}"
                }
            }
        except Exception as e:
            logger.error(f"综合分析喜用神失败: {e}")
            return {
                "basic_analysis": {
                    "favorable_elements": [],
                    "day_master_strength": "未知"
                },
                "final_prognosis": {
                    "primary_favorable": "未知",
                    "secondary_favorable": "无",
                    "primary_unfavorable": "未知",
                    "secondary_unfavorable": "无",
                    "avoid_elements": [],
                    "life_advice": "分析失败，无法提供建议",
                    "overall_rating": 5.0,
                    "summary": "分析失败"
                }
            }
    
    @staticmethod
    def get_solar_time_correction(birth_time: datetime, city_name: str, longitude: Optional[float] = None) -> Dict[str, Any]:
        """获取真太阳时校正信息"""
        try:
            # 简化实现，暂时返回无校正状态
            return {
                "correction_applied": False,
                "longitude_diff_minutes": 0.0,
                "equation_of_time_minutes": 0.0,
                "corrected_time": birth_time
            }
        except Exception as e:
            logger.error(f"获取真太阳时校正失败: {e}")
            return {
                "correction_applied": False,
                "longitude_diff_minutes": 0.0,
                "equation_of_time_minutes": 0.0,
                "corrected_time": birth_time
            }
    
    @staticmethod
    def calculate_precise_dayun(birth_time: datetime, gender: str, year_gan: str, month_pillar: str, solar_terms: Optional[list] = None) -> Tuple[datetime, int, List[DaYun], int]:
        """
        计算精准大运（无硬编码，完全按节气推算）
        - 顺逆排：阳年男/阴年女顺排，阴年男/阳年女逆排
        - 起运岁数 = 距离最近节气天数/3，1天=4个月，1时辰=10天
        - 顺排：下一个节气，逆排：上一个节气
        - 干支推演：顺/逆排月柱
        - 每柱10年
        - solar_terms: 节气数据，格式[{"name":..., "datetime":...}]
        返回: (起运日期, 距离天数, 大运列表, 起运年龄)
        """
        try:
            from dateutil.relativedelta import relativedelta
            start_date = birth_time
            start_days = 0
            luck_pillars = []
            # 1. 判断顺逆排
            yang_gans = ["甲", "丙", "戊", "庚", "壬"]
            is_yang_year = year_gan in yang_gans
            is_male = (gender == "男")
            is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
            forward_str = "顺排" if is_forward else "逆排"
            logger.info(f"大运计算: 年干={year_gan}, 性别={gender}, 阳年={is_yang_year}, {forward_str}")
            # 2. 查找最近节气（使用12个主要节气）
            if not solar_terms:
                # 兼容老接口，自动查找本地节气表
                try:
                    import sys
                    import os
                    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                    sys.path.insert(0, backend_dir)
                    from major_solar_terms import load_major_solar_terms_flat
                    solar_terms = load_major_solar_terms_flat()
                    logger.info(f"成功加载12个主要节气数据: {len(solar_terms)}个")
                except Exception as e:
                    logger.warning(f"加载主要节气数据失败: {e}")
                    solar_terms = []
            # 找到出生前后最近的节气
            prev_term, next_term = None, None
            if solar_terms:
                for term in solar_terms:
                    term_dt = datetime.strptime(term["datetime"], "%Y-%m-%d %H:%M:%S")
                    if term_dt <= birth_time:
                        prev_term = term
                    if term_dt > birth_time and not next_term:
                        next_term = term
            # 顺排：下一个节气，逆排：上一个节气
            if is_forward:
                ref_term = next_term
            else:
                ref_term = prev_term
            if not ref_term:
                # fallback: 默认8岁
                logger.warning("未找到节气，使用8岁起运")
                start_age = 8
                start_days = 0
            else:
                ref_dt = datetime.strptime(ref_term["datetime"], "%Y-%m-%d %H:%M:%S")
                days = abs((ref_dt - birth_time).days)
                start_days = days
                hours = abs((ref_dt - birth_time).seconds) // 3600
                # 1天=4个月，1时辰=10天
                # 1岁=3天
                start_age = days // 3
                left_days = days % 3
                months = left_days * 4
                # 1时辰=2小时
                shichen = hours // 2
                months += shichen * 10 // 3
                # 若小于1岁，按1岁起运
                if start_age <= 0:
                    start_age = 1
                # 若不足1岁的部分较多，向上取整
                if left_days >= 1.5:  # 超过1.5天，增加1岁
                    start_age += 1
            # 3. 干支推演
            month_ganzhi = month_pillar[:2] if len(month_pillar) >= 2 else month_pillar
            jiazi_index = JIAZI_TABLE.index(month_ganzhi) if month_ganzhi in JIAZI_TABLE else 0
            for i in range(10):
                if is_forward:
                    new_index = (jiazi_index + i + 1) % 60
                else:
                    new_index = (jiazi_index - i - 1 + 60) % 60
                dayun_ganzhi = JIAZI_TABLE[new_index]
                dayun_stem = dayun_ganzhi[0]
                dayun_branch = dayun_ganzhi[1]
                dayun = DaYun(
                    start_age=start_age + i * 10,
                    stem_branch=StemBranch(dayun_stem, dayun_branch),
                    end_age=start_age + (i + 1) * 10 - 1
                )
                luck_pillars.append(dayun)
            return start_date, start_days, luck_pillars, start_age
        except Exception as e:
            logger.error(f"计算精准大运失败: {e}")
            return birth_time, 8, [], 8
    
    @staticmethod
    def analyze_liunian_interactions(bazi: Bazi, current_year: int, major_cycles: List[Dict[str, Any]], 
                                   current_dayun_ten_god: str, primary_favorable: str, 
                                   primary_unfavorable: str) -> Dict[str, Any]:
        """分析流年相互作用"""
        try:
            # 简化实现，返回基本的流年互动分析
            return {
                "favorable_interactions": [
                    {
                        "description": f"流年与{primary_favorable}五行相生",
                        "strength": 0.8
                    }
                ],
                "unfavorable_interactions": [
                    {
                        "description": f"流年与{primary_unfavorable}五行相克",
                        "strength": 0.6
                    }
                ],
                "dayun_interaction": {
                    "description": f"大运{current_dayun_ten_god}与流年配合",
                    "effect": "中性"
                }
            }
        except Exception as e:
            logger.error(f"分析流年互动失败: {e}")
            return {
                "favorable_interactions": [],
                "unfavorable_interactions": [],
                "dayun_interaction": {
                    "description": "分析失败",
                    "effect": "未知"
                }
            }
    
    @staticmethod
    def calculate_all_pillar_xunkong(birth_chart: Bazi) -> Dict[str, List[str]]:
        """计算所有柱的空亡信息"""
        try:
            xunkong_info = {}
            
            # 计算每个柱的空亡
            pillars = {
                "year": f"{birth_chart.year.stem}{birth_chart.year.branch}",
                "month": f"{birth_chart.month.stem}{birth_chart.month.branch}",
                "day": f"{birth_chart.day.stem}{birth_chart.day.branch}",
                "hour": f"{birth_chart.hour.stem}{birth_chart.hour.branch}"
            }
            
            for pillar_name, pillar_ganzhi in pillars.items():
                xunkong_branches = XUNKONG_MAPPING.get(pillar_ganzhi, [])
                xunkong_info[pillar_name] = xunkong_branches
            
            return xunkong_info
            
        except Exception as e:
            logger.error(f"计算空亡信息失败: {e}")
            return {}

