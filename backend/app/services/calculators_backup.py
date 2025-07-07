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
        """应用神煞强度修正 - 完整实现版本"""
        strength_modifier = rule.get("strength_modifier", {})
        
        # 检查各种修正条件
        if "favorable_element" in strength_modifier:
            # 检查是否为喜用神
            if self._is_favorable_element(shensha, birth_chart, positions):
                shensha.strength *= strength_modifier["favorable_element"]
                shensha.add_tag("喜用神增强")
        
        if "conflict" in strength_modifier:
            # 检查是否有冲
            if self._has_conflict(shensha, birth_chart, positions):
                shensha.strength *= strength_modifier["conflict"]
                shensha.add_tag("受冲")
        
        if "harmony" in strength_modifier:
            # 检查是否有合
            if self._has_harmony(shensha, birth_chart, positions):
                shensha.strength *= strength_modifier["harmony"]
                shensha.add_tag("受合")
        
        if "multiple_appearance" in strength_modifier:
            # 检查是否多现
            if len(positions) > 1:
                shensha.strength *= strength_modifier["multiple_appearance"]
                shensha.add_tag("多现")
        
        # 检查日主强弱相关修正
        if "day_master_weak" in strength_modifier or "day_master_strong" in strength_modifier:
            day_master_strength = FiveElementsCalculator.calculate_day_master_strength(birth_chart)
            if day_master_strength in ["偏弱", "极弱"] and "day_master_weak" in strength_modifier:
                shensha.strength *= strength_modifier["day_master_weak"]
                shensha.add_tag("日主弱影响")
            elif day_master_strength in ["偏强", "中强"] and "day_master_strong" in strength_modifier:
                shensha.strength *= strength_modifier["day_master_strong"]
                shensha.add_tag("日主强影响")
        
        # 应用位置影响
        positions_influence = rule.get("positions_influence", {})
        if positions_influence:
            for pos in positions:
                if pos in positions_influence:
                    shensha.add_tag(f"{pos}位: {positions_influence[pos]}")
    
    def _is_favorable_element(self, shensha: ShenSha, birth_chart: Bazi, positions: List[str]) -> bool:
        """判断神煞是否为喜用神 - 真实实现版本"""
        try:
            # 获取命盘的喜用神
            favorable_elements = FiveElementsCalculator.get_favorable_elements(birth_chart)
            
            # 检查神煞所在位置的五行
            for pos in positions:
                pos_element = self._get_position_element(pos, birth_chart)
                if pos_element in favorable_elements:
                    return True
            
            return False
        except Exception as e:
            logger.warning(f"判断喜用神失败: {e}")
            return False
    
    def _has_conflict(self, shensha: ShenSha, birth_chart: Bazi, positions: List[str]) -> bool:
        """判断神煞是否有冲 - 真实实现版本"""
        try:
            # 构建地支六冲字典
            conflict_map = {}
            for (b1, b2) in BRANCH_SIX_CONFLICTS:
                conflict_map[b1] = b2
                conflict_map[b2] = b1
            
            # 获取所有地支
            all_branches = birth_chart.get_all_branches()
            
            # 检查神煞位置是否被冲
            for pos in positions:
                pos_branch = self._get_position_branch(pos, birth_chart)
                if pos_branch:
                    conflict_branch = conflict_map.get(pos_branch)
                    if conflict_branch and conflict_branch in all_branches:
                        return True
            
            return False
        except Exception as e:
            logger.warning(f"判断冲克失败: {e}")
            return False
    
    def _has_harmony(self, shensha: ShenSha, birth_chart: Bazi, positions: List[str]) -> bool:
        """判断神煞是否有合 - 真实实现版本"""
        try:
            # 构建地支六合字典
            harmony_map = {}
            for (b1, b2) in BRANCH_SIX_COMBINATIONS:
                harmony_map[b1] = b2
                harmony_map[b2] = b1
            
            # 获取所有地支
            all_branches = birth_chart.get_all_branches()
            
            # 检查神煞位置是否有合
            for pos in positions:
                pos_branch = self._get_position_branch(pos, birth_chart)
                if pos_branch:
                    harmony_branch = harmony_map.get(pos_branch)
                    if harmony_branch and harmony_branch in all_branches:
                        return True
            
            return False
        except Exception as e:
            logger.warning(f"判断合化失败: {e}")
            return False
    
    def _get_position_element(self, position: str, birth_chart: Bazi) -> str:
        """获取指定位置的五行"""
        pos_mapping = {
            "年": birth_chart.year.branch,
            "月": birth_chart.month.branch,
            "日": birth_chart.day.branch,
            "时": birth_chart.hour.branch
        }
        
        branch = pos_mapping.get(position, "")
        return BRANCH_ELEMENTS.get(branch, "")
    
    def _get_position_branch(self, position: str, birth_chart: Bazi) -> str:
        """获取指定位置的地支"""
        pos_mapping = {
            "年": birth_chart.year.branch,
            "月": birth_chart.month.branch,
            "日": birth_chart.day.branch,
            "时": birth_chart.hour.branch
        }
        
        return pos_mapping.get(position, "")
    
    def _process_interactions(self, shen_sha_map: Dict[str, ShenSha], birth_chart: Bazi):
        """处理神煞互动关系 - 通用版本，基于规则驱动"""
        try:
            # 为每个激活的神煞重新应用修正器，考虑其他神煞的影响
            for key, shensha in shen_sha_map.items():
                if not shensha.active:
                    continue
                
                rule = self.rules_dict.get(key)
                if not rule:
                    continue
                
                # 检查是否有与其他神煞的特殊互动
                self._check_shensha_interactions(shensha, shen_sha_map, birth_chart, rule)
                
        except Exception as e:
            logger.error(f"神煞互动处理失败: {e}")
    
    def _check_shensha_interactions(self, shensha: ShenSha, all_shensha: Dict[str, ShenSha], 
                                   birth_chart: Bazi, rule: dict):
        """检查特定神煞与其他神煞的互动 - 完全数据驱动版本"""
        try:
            # 获取互动规则
            interactions = self.shensha_data.get("shensha_interactions", {})
            
            # 检查所有互动规则
            for interaction_key, interaction_rule in interactions.items():
                if self._check_interaction_condition(shensha, all_shensha, birth_chart, interaction_rule):
                    self._apply_interaction_effects(shensha, all_shensha, birth_chart, interaction_rule)
                    logger.debug(f"应用互动规则: {interaction_key} -> {shensha.name}")
                    
        except Exception as e:
            logger.error(f"检查神煞互动失败: {e}")
    
    def _check_interaction_condition(self, shensha: ShenSha, all_shensha: Dict[str, ShenSha], 
                                   birth_chart: Bazi, interaction_rule: dict) -> bool:
        """检查互动条件是否满足"""
        try:
            # 检查神煞键是否匹配
            target_keys = interaction_rule.get("shensha_keys", [])
            if not self._match_shensha_keys(shensha, target_keys):
                return False
            
            # 检查条件类型
            condition = interaction_rule.get("condition", "")
            
            if condition == "same_position":
                return self._check_same_position(shensha, all_shensha, target_keys)
            elif condition == "branch_conflict":
                return self._check_branch_conflict(shensha, birth_chart)
            elif condition == "branch_harmony":
                return self._check_branch_harmony(shensha, birth_chart)
            elif condition == "multiple_appearance":
                return self._check_multiple_appearance(shensha, all_shensha)
            elif condition == "favorable_element":
                return self._check_favorable_element(shensha, birth_chart)
            elif condition == "unfavorable_element":
                return self._check_unfavorable_element(shensha, birth_chart)
            elif condition == "with_official_or_seal":
                return self._check_with_official_or_seal(birth_chart)
            elif condition == "no_official_or_seal":
                return not self._check_with_official_or_seal(birth_chart)
            elif condition == "with_seal":
                return self._check_with_seal(birth_chart)
            
            return False
            
        except Exception as e:
            logger.error(f"检查互动条件失败: {e}")
            return False
    
    def _match_shensha_keys(self, shensha: ShenSha, target_keys: List[str]) -> bool:
        """检查神煞键是否匹配"""
        if "*" in target_keys:
            return True
        
        # 根据神煞名称反查键
        shensha_key = None
        for key, rule in self.rules_dict.items():
            if rule.get("name") == shensha.name:
                shensha_key = key
                break
        
        return shensha_key in target_keys
    
    def _check_same_position(self, shensha: ShenSha, all_shensha: Dict[str, ShenSha], 
                           target_keys: List[str]) -> bool:
        """检查是否在同一位置"""
        positions = shensha.position.split(", ") if shensha.position else []
        
        for key in target_keys:
            if key in all_shensha and all_shensha[key].active:
                other_positions = all_shensha[key].position.split(", ") if all_shensha[key].position else []
                if any(pos in other_positions for pos in positions):
                    return True
        return False
    
    def _check_branch_conflict(self, shensha: ShenSha, birth_chart: Bazi) -> bool:
        """检查是否存在地支冲突"""
        positions = shensha.position.split(", ") if shensha.position else []
        
        for pos in positions:
            target_branch = birth_chart.get_position_branch(pos)
            if target_branch and self._count_conflicts(birth_chart, target_branch) > 0:
                return True
        return False
    
    def _check_branch_harmony(self, shensha: ShenSha, birth_chart: Bazi) -> bool:
        """检查是否存在地支合化"""
        positions = shensha.position.split(", ") if shensha.position else []
        
        for pos in positions:
            target_branch = birth_chart.get_position_branch(pos)
            if target_branch and self._count_harmonies(birth_chart, target_branch) > 0:
                return True
        return False
    
    def _check_multiple_appearance(self, shensha: ShenSha, all_shensha: Dict[str, ShenSha]) -> bool:
        """检查是否多次出现"""
        count = 0
        for other_shensha in all_shensha.values():
            if other_shensha.name == shensha.name and other_shensha.active:
                count += 1
        return count > 1
    
    def _check_favorable_element(self, shensha: ShenSha, birth_chart: Bazi) -> bool:
        """检查是否为喜用神 - 简化版本"""
        try:
            # 获取神煞对应的五行
            positions = shensha.position.split(", ") if shensha.position else []
            
            # 简化判断：春生木旺，夏生火旺，秋生金旺，冬生水旺
            # 如果神煞五行与日主需要的五行匹配，则为喜用神
            day_stem = birth_chart.day.stem
            day_element = STEM_ELEMENTS.get(day_stem, "")
            
            # 根据月令判断季节
            month_branch = birth_chart.month.branch
            season = self._get_season_from_branch(month_branch)
            
            # 简化的喜用神判断
            favorable_elements = self._get_favorable_elements_by_season(day_element, season)
            
            for pos in positions:
                pos_element = birth_chart.get_position_element(pos)
                if pos_element in favorable_elements:
                    return True
            
            return False
        except Exception as e:
            logger.warning(f"检查喜用神失败: {e}")
            return False
    
    def _check_unfavorable_element(self, shensha: ShenSha, birth_chart: Bazi) -> bool:
        """检查是否为忌神 - 简化版本"""
        try:
            # 与 _check_favorable_element 相反
            return not self._check_favorable_element(shensha, birth_chart)
        except Exception as e:
            logger.warning(f"检查忌神失败: {e}")
            return False
    
    def _check_with_official_or_seal(self, birth_chart: Bazi) -> bool:
        """检查是否有官杀或印绶 - 简化版本"""
        try:
            day_stem = birth_chart.day.stem
            day_element = STEM_ELEMENTS.get(day_stem, "")
            
            # 获取所有干支
            all_stems = [birth_chart.year.stem, birth_chart.month.stem, birth_chart.hour.stem]
            all_branches = birth_chart.get_all_branches()
            
            # 检查是否有官杀（克日主的五行）
            official_element = FIVE_ELEMENTS_OVERCOMING.get(day_element, "")
            
            # 检查是否有印绶（生日主的五行）
            seal_element = REVERSE_GENERATION.get(day_element, "")
            
            for stem in all_stems:
                stem_element = STEM_ELEMENTS.get(stem, "")
                if stem_element in [official_element, seal_element]:
                    return True
            
            # 检查地支藏干
            for branch in all_branches:
                hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
                for hidden_stem in hidden_stems.keys():
                    hidden_element = STEM_ELEMENTS.get(hidden_stem, "")
                    if hidden_element in [official_element, seal_element]:
                        return True
            
            return False
        except Exception as e:
            logger.warning(f"检查官杀印绶失败: {e}")
            return False
    
    def _check_with_seal(self, birth_chart: Bazi) -> bool:
        """检查是否有印绶 - 简化版本"""
        try:
            day_stem = birth_chart.day.stem
            day_element = STEM_ELEMENTS.get(day_stem, "")
            
            # 获取所有干支
            all_stems = [birth_chart.year.stem, birth_chart.month.stem, birth_chart.hour.stem]
            all_branches = birth_chart.get_all_branches()
            
            # 检查是否有印绶（生日主的五行）
            seal_element = REVERSE_GENERATION.get(day_element, "")
            
            for stem in all_stems:
                stem_element = STEM_ELEMENTS.get(stem, "")
                if stem_element == seal_element:
                    return True
            
            # 检查地支藏干
            for branch in all_branches:
                hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, {})
                for hidden_stem in hidden_stems.keys():
                    hidden_element = STEM_ELEMENTS.get(hidden_stem, "")
                    if hidden_element == seal_element:
                        return True
            
            return False
        except Exception as e:
            logger.warning(f"检查印绶失败: {e}")
            return False
    
    def _get_season_from_branch(self, branch: str) -> str:
        """根据月支获取季节"""
        branch_to_season = {
            "寅": "春", "卯": "春", "辰": "春",
            "巳": "夏", "午": "夏", "未": "夏",
            "申": "秋", "酉": "秋", "戌": "秋",
            "亥": "冬", "子": "冬", "丑": "冬"
        }
        return branch_to_season.get(branch, "春")
    
    def _get_favorable_elements_by_season(self, day_element: str, season: str) -> List[str]:
        """根据日主五行和季节获取喜用神五行"""
        # 简化的喜用神判断规则
        favorable_map = {
            "春": {
                "木": ["火", "土"],  # 春生木旺，喜火泄秀，土制木
                "火": ["木", "土"],  # 春生火相，喜木生，土泄
                "土": ["火", "金"],  # 春生土死，喜火生，金泄
                "金": ["水", "土"],  # 春生金囚，喜水泄，土生
                "水": ["金", "木"]   # 春生水休，喜金生，木泄
            },
            "夏": {
                "木": ["水", "金"],  # 夏生木死，喜水生，金制火
                "火": ["土", "金"],  # 夏生火旺，喜土泄，金制
                "土": ["水", "木"],  # 夏生土相，喜水润，木疏
                "金": ["水", "土"],  # 夏生金囚，喜水生，土生
                "水": ["金", "水"]   # 夏生水死，喜金生，比肩
            },
            "秋": {
                "木": ["水", "火"],  # 秋生木囚，喜水生，火制金
                "火": ["木", "水"],  # 秋生火死，喜木生，水调候
                "土": ["火", "金"],  # 秋生土相，喜火生，金泄
                "金": ["土", "水"],  # 秋生金旺，喜土生，水泄
                "水": ["金", "木"]   # 秋生水相，喜金生，木泄
            },
            "冬": {
                "木": ["火", "水"],  # 冬生木休，喜火暖，水生
                "火": ["木", "土"],  # 冬生火囚，喜木生，土止水
                "土": ["火", "金"],  # 冬生土死，喜火暖，金泄
                "金": ["火", "土"],  # 冬生金相，喜火暖，土生
                "水": ["土", "木"]   # 冬生水旺，喜土止，木泄
            }
        }
        
        return favorable_map.get(season, {}).get(day_element, [])

