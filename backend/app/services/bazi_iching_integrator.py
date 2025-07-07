# -*- coding: utf-8 -*-
"""
高级易经八字联合分析模块
Advanced I Ching and Bazi Integrated Analysis Module

将易经卦象与八字命理结合，提供更深入的命运分析
Combining I Ching hexagrams with Bazi numerology for deeper destiny analysis
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import random
import math
from app.schemas.bazi import BaziCalculateResponse
from app.schemas.iching import IChingDivinationResponse, HexagramData, HexagramLine

class BaziIchingIntegrator:
    """八字易经联合分析器"""
    
    # 八字与易经的对应关系
    BAZI_HEXAGRAM_MAPPING = {
        # 年柱对应的卦象（简化映射）
        "甲子": "屯", "乙丑": "蒙", "丙寅": "需", "丁卯": "讼", "戊辰": "师", "己巳": "比",
        "庚午": "小畜", "辛未": "履", "壬申": "泰", "癸酉": "否", "甲戌": "同人", "乙亥": "大有",
        "丙子": "谦", "丁丑": "豫", "戊寅": "随", "己卯": "蛊", "庚辰": "临", "辛巳": "观",
        "壬午": "噬嗑", "癸未": "贲", "甲申": "剥", "乙酉": "复", "丙戌": "无妄", "丁亥": "大畜",
        "戊子": "颐", "己丑": "大过", "庚寅": "坎", "辛卯": "离", "壬辰": "咸", "癸巳": "恒",
        "甲午": "遁", "乙未": "大壮", "丙申": "晋", "丁酉": "明夷", "戊戌": "家人", "己亥": "睽",
        "庚子": "蹇", "辛丑": "解", "壬寅": "损", "癸卯": "益", "甲辰": "夬", "乙巳": "姤",
        "丙午": "萃", "丁未": "升", "戊申": "困", "己酉": "井", "庚戌": "革", "辛亥": "鼎",
        "壬子": "震", "癸丑": "艮", "甲寅": "渐", "乙卯": "归妹", "丙辰": "丰", "丁巳": "旅",
        "戊午": "巽", "己未": "兑", "庚申": "涣", "辛酉": "节", "壬戌": "中孚", "癸亥": "小过"
    }
    
    # 五行与八卦的对应关系
    ELEMENT_TRIGRAM_MAPPING = {
        "金": ["乾", "兑"],
        "木": ["震", "巽"], 
        "水": ["坎"],
        "火": ["离"],
        "土": ["艮", "坤"]
    }
    
    # 八卦象征意义
    TRIGRAM_MEANINGS = {
        "乾": {"nature": "天", "attribute": "刚健", "direction": "西北", "season": "秋冬之间"},
        "坤": {"nature": "地", "attribute": "柔顺", "direction": "西南", "season": "夏秋之间"},
        "震": {"nature": "雷", "attribute": "动", "direction": "正东", "season": "春"},
        "巽": {"nature": "风", "attribute": "顺", "direction": "东南", "season": "春夏之间"},
        "坎": {"nature": "水", "attribute": "险", "direction": "正北", "season": "冬"},
        "离": {"nature": "火", "attribute": "明", "direction": "正南", "season": "夏"},
        "艮": {"nature": "山", "attribute": "止", "direction": "东北", "season": "冬春之间"},
        "兑": {"nature": "泽", "attribute": "悦", "direction": "正西", "season": "秋"}
    }
    
    @classmethod
    def generate_bazi_based_hexagram(cls, bazi_result: BaziCalculateResponse, question: str = "") -> HexagramData:
        """
        基于八字信息生成对应的卦象
        
        Args:
            bazi_result: 八字计算结果
            question: 问卦内容
            
        Returns:
            HexagramData: 生成的卦象数据
        """
        try:
            # 提取八字基本信息
            bazi_chars = bazi_result.bazi_characters
            year_pillar = f"{bazi_chars.get('year_stem', '')}{bazi_chars.get('year_branch', '')}"
            day_pillar = f"{bazi_chars.get('day_stem', '')}{bazi_chars.get('day_branch', '')}"
            
            # 获取五行分布
            five_elements = bazi_result.five_elements_score
            day_master = bazi_result.day_master_element
            
            print(f"DEBUG: 基于八字生成卦象 - 年柱:{year_pillar}, 日柱:{day_pillar}, 日主:{day_master}")
            
            # 根据八字信息确定上下卦
            upper_trigram = cls._determine_trigram_from_bazi(year_pillar, day_master, "upper")
            lower_trigram = cls._determine_trigram_from_bazi(day_pillar, day_master, "lower")
            
            # 生成六爻
            yao_values = cls._generate_yao_from_bazi(bazi_result, question)
            
            # 计算卦象序号和名称
            hexagram_number = cls._calculate_hexagram_number(upper_trigram, lower_trigram)
            hexagram_name = cls._get_hexagram_name(hexagram_number, upper_trigram, lower_trigram)
            
            # 构建爻辞
            lines = []
            for i, yao_value in enumerate(yao_values):
                line = HexagramLine(
                    number=i + 1,
                    value=yao_value,
                    yin_yang="阳" if yao_value in [7, 9] else "阴",
                    is_changing=yao_value in [6, 9],
                    description=cls._get_yao_description(i + 1, yao_value, hexagram_name)
                )
                lines.append(line)
            
            # 生成卦辞和象辞
            judgment = cls._generate_judgment(hexagram_name, bazi_result, question)
            image = cls._generate_image(upper_trigram, lower_trigram, bazi_result)
            
            return HexagramData(
                name=hexagram_name,
                number=hexagram_number,
                upper_trigram=upper_trigram,
                lower_trigram=lower_trigram,
                image=image,
                judgment=judgment,
                lines=lines
            )
            
        except Exception as e:
            print(f"ERROR: 基于八字生成卦象失败: {e}")
            # 返回默认卦象
            return cls._get_default_hexagram()
    
    @classmethod
    def analyze_bazi_hexagram_compatibility(
        cls, 
        bazi_result: BaziCalculateResponse, 
        hexagram_data: HexagramData
    ) -> Dict[str, Any]:
        """
        分析八字与卦象的相合度
        
        Args:
            bazi_result: 八字结果
            hexagram_data: 卦象数据
            
        Returns:
            Dict[str, Any]: 相合度分析结果
        """
        analysis = {
            "compatibility_score": 0.0,
            "element_harmony": {},
            "seasonal_match": "",
            "directional_guidance": "",
            "timing_advice": "",
            "integrated_interpretation": ""
        }
        
        try:
            # 1. 五行相合度分析
            bazi_elements = bazi_result.five_elements_score
            hexagram_elements = cls._extract_hexagram_elements(hexagram_data)
            
            element_harmony = cls._analyze_element_harmony(bazi_elements, hexagram_elements)
            analysis["element_harmony"] = element_harmony
            
            # 2. 计算整体相合度
            compatibility_score = cls._calculate_compatibility_score(bazi_result, hexagram_data)
            analysis["compatibility_score"] = compatibility_score
            
            # 3. 季节匹配分析
            birth_time = getattr(bazi_result, 'birth_time', None)
            if birth_time:
                seasonal_match = cls._analyze_seasonal_match(birth_time, hexagram_data)
                analysis["seasonal_match"] = seasonal_match
            
            # 4. 方位指导
            directional_guidance = cls._generate_directional_guidance(hexagram_data)
            analysis["directional_guidance"] = directional_guidance
            
            # 5. 时机建议
            timing_advice = cls._generate_timing_advice(bazi_result, hexagram_data)
            analysis["timing_advice"] = timing_advice
            
            # 6. 综合解读
            integrated_interpretation = cls._generate_integrated_interpretation(
                bazi_result, hexagram_data, analysis
            )
            analysis["integrated_interpretation"] = integrated_interpretation
            
        except Exception as e:
            print(f"ERROR: 八字卦象相合度分析失败: {e}")
            analysis["integrated_interpretation"] = "分析过程中出现错误，建议重新占卜"
        
        return analysis
    
    @classmethod
    def predict_life_trends_with_iching(
        cls, 
        bazi_result: BaziCalculateResponse,
        target_years: Optional[List[int]] = None
    ) -> Dict[int, Dict[str, Any]]:
        """
        结合易经预测人生趋势
        
        Args:
            bazi_result: 八字结果
            target_years: 目标年份列表
            
        Returns:
            Dict[int, Dict[str, Any]]: 年份到预测结果的映射
        """
        predictions = {}
        
        if target_years is None:
            current_year = datetime.now().year
            target_years = list(range(current_year, current_year + 5))
        
        for year in target_years:
            try:
                # 为每年生成特定卦象
                year_question = f"{year}年运势如何？"
                year_hexagram = cls.generate_bazi_based_hexagram(bazi_result, year_question)
                
                # 分析该年的运势
                yearly_analysis = {
                    "hexagram": {
                        "name": year_hexagram.name,
                        "upper_trigram": year_hexagram.upper_trigram,
                        "lower_trigram": year_hexagram.lower_trigram,
                        "judgment": year_hexagram.judgment
                    },
                    "fortune_trend": cls._analyze_yearly_fortune(year_hexagram, bazi_result),
                    "key_events": cls._predict_yearly_events(year_hexagram, bazi_result, year),
                    "advice": cls._generate_yearly_advice(year_hexagram, bazi_result),
                    "favorable_months": cls._identify_favorable_months(year_hexagram, year),
                    "caution_periods": cls._identify_caution_periods(year_hexagram, year)
                }
                
                predictions[year] = yearly_analysis
                
            except Exception as e:
                print(f"ERROR: 预测{year}年运势失败: {e}")
                predictions[year] = {
                    "error": f"预测失败: {str(e)}",
                    "advice": "建议重新分析"
                }
        
        return predictions
    
    @classmethod
    def _determine_trigram_from_bazi(cls, pillar: str, day_master: str, position: str) -> str:
        """根据八字柱确定卦象"""
        if len(pillar) < 2:
            return "乾"  # 默认值
            
        gan = pillar[0]
        zhi = pillar[1]
        
        # 天干对应的卦象
        gan_trigram_map = {
            "甲": "震", "乙": "巽",
            "丙": "离", "丁": "离", 
            "戊": "艮", "己": "坤",
            "庚": "乾", "辛": "兑",
            "壬": "坎", "癸": "坎"
        }
        
        # 地支对应的卦象
        zhi_trigram_map = {
            "子": "坎", "丑": "艮", "寅": "震", "卯": "震",
            "辰": "巽", "巳": "离", "午": "离", "未": "坤",
            "申": "乾", "酉": "兑", "戌": "乾", "亥": "坎"
        }
        
        # 根据位置选择卦象
        if position == "upper":
            base_trigram = gan_trigram_map.get(gan, "乾")
        else:
            base_trigram = zhi_trigram_map.get(zhi, "坤")
        
        return base_trigram
    
    @classmethod
    def _generate_yao_from_bazi(cls, bazi_result: BaziCalculateResponse, question: str) -> List[int]:
        """根据八字信息生成六爻"""
        yao_values = []
        
        # 使用八字信息作为随机种子
        bazi_chars = bazi_result.bazi_characters
        seed_str = "".join([
            bazi_chars.get('year_stem', ''),
            bazi_chars.get('year_branch', ''),
            bazi_chars.get('day_stem', ''),
            bazi_chars.get('day_branch', ''),
            question
        ])
        
        # 转换为数字种子
        seed = sum(ord(c) for c in seed_str) % 10000
        random.seed(seed)
        
        # 生成六爻（6-9的值）
        for i in range(6):
            # 根据五行得分调整爻值概率
            five_elements = bazi_result.five_elements_score
            
            # 提取百分比数值
            element_scores = {}
            for element, score_str in five_elements.items():
                try:
                    if isinstance(score_str, str) and score_str.endswith('%'):
                        element_scores[element] = float(score_str.rstrip('%'))
                    else:
                        element_scores[element] = float(score_str)
                except (ValueError, TypeError):
                    element_scores[element] = 20.0  # 默认值
            
            # 根据五行强弱调整爻值
            dominant_element = max(element_scores.keys(), key=lambda k: element_scores[k])
            dominant_score = element_scores[dominant_element]
            
            # 强势五行更容易产生阳爻和变爻
            if dominant_score > 25:
                yao_prob = [0.15, 0.35, 0.35, 0.15]  # [6, 7, 8, 9] 偏向阳爻
            elif dominant_score < 15:
                yao_prob = [0.25, 0.25, 0.40, 0.10]  # 偏向阴爻
            else:
                yao_prob = [0.20, 0.30, 0.30, 0.20]  # 平衡
            
            # 根据概率选择爻值
            rand_val = random.random()
            cumulative = 0
            for idx, prob in enumerate(yao_prob):
                cumulative += prob
                if rand_val <= cumulative:
                    yao_values.append(6 + idx)
                    break
        
        return yao_values
    
    @classmethod
    def _calculate_hexagram_number(cls, upper_trigram: str, lower_trigram: str) -> int:
        """计算卦象序号"""
        # 简化的64卦序号计算
        trigram_numbers = {
            "乾": 1, "兑": 2, "离": 3, "震": 4,
            "巽": 5, "坎": 6, "艮": 7, "坤": 8
        }
        
        upper_num = trigram_numbers.get(upper_trigram, 1)
        lower_num = trigram_numbers.get(lower_trigram, 1)
        
        # 使用简化公式计算卦序
        hexagram_num = (upper_num - 1) * 8 + lower_num
        return min(64, max(1, hexagram_num))
    
    @classmethod
    def _get_hexagram_name(cls, number: int, upper: str, lower: str) -> str:
        """获取卦名"""
        # 简化的卦名映射
        special_names = {
            1: "乾为天", 2: "坤为地", 29: "坎为水", 30: "离为火",
            51: "震为雷", 57: "巽为风", 52: "艮为山", 58: "兑为泽"
        }
        
        if number in special_names:
            return special_names[number]
        
        # 组合卦名
        trigram_nature = {
            "乾": "天", "坤": "地", "震": "雷", "巽": "风",
            "坎": "水", "离": "火", "艮": "山", "兑": "泽"
        }
        
        upper_nature = trigram_nature.get(upper, upper)
        lower_nature = trigram_nature.get(lower, lower)
        
        return f"{upper_nature}{lower_nature}卦"
    
    @classmethod
    def _get_yao_description(cls, line_number: int, yao_value: int, hexagram_name: str) -> str:
        """获取爻辞描述"""
        position_meanings = {
            1: "初爻代表事物的开始，基础阶段",
            2: "二爻代表发展阶段，需要稳固",  
            3: "三爻代表转折点，变化关键",
            4: "四爻代表接近成功，需要谨慎",
            5: "五爻代表巅峰状态，功成名就",
            6: "上爻代表结束阶段，物极必反"
        }
        
        base_desc = position_meanings.get(line_number, f"第{line_number}爻")
        
        # 根据爻值添加具体描述
        if yao_value == 6:  # 老阴
            return f"{base_desc}，阴爻变阳，柔中有刚"
        elif yao_value == 7:  # 少阳
            return f"{base_desc}，阳爻稳定，积极向上"
        elif yao_value == 8:  # 少阴
            return f"{base_desc}，阴爻平和，需要等待"
        elif yao_value == 9:  # 老阳
            return f"{base_desc}，阳爻变阴，刚极必变"
        else:
            return base_desc
    
    @classmethod
    def _generate_judgment(cls, hexagram_name: str, bazi_result: BaziCalculateResponse, question: str) -> str:
        """生成卦辞"""
        day_master = bazi_result.day_master_element
        day_strength = bazi_result.day_master_strength
        
        # 根据日主和卦象生成卦辞
        if "强" in day_strength:
            judgment_style = "刚健有力，主动出击"
        elif "弱" in day_strength:
            judgment_style = "柔顺应变，以退为进"
        else:
            judgment_style = "中正平和，顺势而为"
        
        return f"{hexagram_name}：{judgment_style}。{question}的答案在于把握时机，顺应自然规律。"
    
    @classmethod
    def _generate_image(cls, upper_trigram: str, lower_trigram: str, bazi_result: BaziCalculateResponse) -> str:
        """生成象辞"""
        upper_meaning = cls.TRIGRAM_MEANINGS.get(upper_trigram, {})
        lower_meaning = cls.TRIGRAM_MEANINGS.get(lower_trigram, {})
        
        upper_nature = upper_meaning.get("nature", upper_trigram)
        lower_nature = lower_meaning.get("nature", lower_trigram)
        
        return f"{upper_nature}在上，{lower_nature}在下，象征天地人和谐统一。君子观此象，应当效法自然，顺应天道。"
    
    @classmethod
    def _get_default_hexagram(cls) -> HexagramData:
        """获取默认卦象"""
        lines = []
        for i in range(6):
            lines.append(HexagramLine(
                number=i + 1,
                value=7,
                yin_yang="阳",
                is_changing=False,
                description=f"第{i+1}爻：阳爻稳定"
            ))
        
        return HexagramData(
            name="乾为天",
            number=1,
            upper_trigram="乾",
            lower_trigram="乾",
            image="天行健，君子以自强不息",
            judgment="乾：元，亨，利，贞",
            lines=lines
        )
    
    @classmethod
    def _extract_hexagram_elements(cls, hexagram_data: HexagramData) -> Dict[str, float]:
        """提取卦象的五行分布"""
        upper_elements = cls.ELEMENT_TRIGRAM_MAPPING
        element_scores = {"金": 0.0, "木": 0.0, "水": 0.0, "火": 0.0, "土": 0.0}
        
        # 上卦贡献
        for element, trigrams in upper_elements.items():
            if hexagram_data.upper_trigram in trigrams:
                element_scores[element] += 50.0
        
        # 下卦贡献
        for element, trigrams in upper_elements.items():
            if hexagram_data.lower_trigram in trigrams:
                element_scores[element] += 50.0
        
        return element_scores
    
    @classmethod
    def _analyze_element_harmony(cls, bazi_elements: Dict, hexagram_elements: Dict) -> Dict[str, Any]:
        """分析五行和谐度"""
        harmony_analysis = {"total_score": 0.0, "details": {}}
        
        total_harmony = 0.0
        
        for element in ["金", "木", "水", "火", "土"]:
            # 提取八字五行百分比
            bazi_percent = 0.0
            if element in bazi_elements:
                bazi_score_str = bazi_elements[element]
                if isinstance(bazi_score_str, str) and bazi_score_str.endswith('%'):
                    bazi_percent = float(bazi_score_str.rstrip('%'))
            
            # 提取卦象五行分布
            hexagram_percent = hexagram_elements.get(element, 0.0)
            
            # 计算和谐度（差值越小越和谐）
            diff = abs(bazi_percent - hexagram_percent)
            harmony_score = max(0, 100 - diff * 2)  # 简化的和谐度计算
            
            harmony_analysis["details"][element] = {
                "bazi_percent": bazi_percent,
                "hexagram_percent": hexagram_percent,
                "harmony_score": harmony_score
            }
            
            total_harmony += harmony_score
        
        harmony_analysis["total_score"] = total_harmony / 5.0
        return harmony_analysis
    
    @classmethod 
    def _calculate_compatibility_score(cls, bazi_result: BaziCalculateResponse, hexagram_data: HexagramData) -> float:
        """计算整体相合度得分"""
        base_score = 60.0  # 基础分
        
        # 1. 五行匹配加分
        bazi_elements = bazi_result.five_elements_score
        hexagram_elements = cls._extract_hexagram_elements(hexagram_data)
        element_harmony = cls._analyze_element_harmony(bazi_elements, hexagram_elements)
        base_score += (element_harmony["total_score"] - 60) * 0.3
        
        # 2. 日主强弱与卦象匹配
        day_strength = bazi_result.day_master_strength
        if "强" in day_strength and hexagram_data.upper_trigram in ["乾", "震", "离"]:
            base_score += 10  # 强势日主配强势卦象
        elif "弱" in day_strength and hexagram_data.lower_trigram in ["坤", "巽", "坎"]:
            base_score += 10  # 弱势日主配柔顺卦象
        
        # 3. 随机因子
        import random
        base_score += random.uniform(-5, 5)
        
        return max(0, min(100, base_score))
    
    @classmethod
    def _analyze_seasonal_match(cls, birth_time: datetime, hexagram_data: HexagramData) -> str:
        """分析季节匹配度"""
        month = birth_time.month
        
        # 确定出生季节
        if month in [3, 4, 5]:
            birth_season = "春"
        elif month in [6, 7, 8]:
            birth_season = "夏" 
        elif month in [9, 10, 11]:
            birth_season = "秋"
        else:
            birth_season = "冬"
        
        # 获取卦象对应季节
        upper_season = cls.TRIGRAM_MEANINGS.get(hexagram_data.upper_trigram, {}).get("season", "")
        lower_season = cls.TRIGRAM_MEANINGS.get(hexagram_data.lower_trigram, {}).get("season", "")
        
        if birth_season in upper_season or birth_season in lower_season:
            return f"卦象与出生季节{birth_season}高度匹配，有利于发挥天赋优势"
        else:
            return f"卦象与出生季节{birth_season}形成互补，有助于平衡发展"
    
    @classmethod
    def _generate_directional_guidance(cls, hexagram_data: HexagramData) -> str:
        """生成方位指导"""
        upper_direction = cls.TRIGRAM_MEANINGS.get(hexagram_data.upper_trigram, {}).get("direction", "")
        lower_direction = cls.TRIGRAM_MEANINGS.get(hexagram_data.lower_trigram, {}).get("direction", "")
        
        directions = []
        if upper_direction:
            directions.append(upper_direction)
        if lower_direction and lower_direction != upper_direction:
            directions.append(lower_direction)
        
        if directions:
            return f"有利方位：{' 和 '.join(directions)}，建议在这些方向发展事业或居住"
        else:
            return "方位无特殊要求，重在内心修养和行为准则"
    
    @classmethod
    def _generate_timing_advice(cls, bazi_result: BaziCalculateResponse, hexagram_data: HexagramData) -> str:
        """生成时机建议"""
        # 简化的时机分析
        changing_lines = [line for line in hexagram_data.lines if line.is_changing]
        
        if len(changing_lines) == 0:
            return "当前时机稳定，适合持续推进既定计划"
        elif len(changing_lines) <= 2:
            return "时机正在变化，需要灵活调整策略，把握机遇"
        else:
            return "变化激烈的时期，建议谨慎观望，以不变应万变"
    
    @classmethod
    def _generate_integrated_interpretation(
        cls, 
        bazi_result: BaziCalculateResponse, 
        hexagram_data: HexagramData, 
        analysis: Dict[str, Any]
    ) -> str:
        """生成综合解读"""
        compatibility_score = analysis.get("compatibility_score", 60)
        
        if compatibility_score >= 80:
            compatibility_level = "高度契合"
        elif compatibility_score >= 65:
            compatibility_level = "较为契合"
        elif compatibility_score >= 50:
            compatibility_level = "基本契合"
        else:
            compatibility_level = "需要调和"
        
        interpretation = f"""
根据您的八字命理与{hexagram_data.name}卦象的综合分析：

【相合度评估】：{compatibility_level}（{compatibility_score:.1f}分）

【五行匹配】：{analysis.get('element_harmony', {}).get('total_score', 0):.1f}分
您的八字五行分布与卦象五行呈现{compatibility_level}的状态，这说明当前的运势走向与您的先天命格基本协调。

【季节时令】：{analysis.get('seasonal_match', '季节匹配分析')}

【方位指导】：{analysis.get('directional_guidance', '方位指导信息')}

【时机把握】：{analysis.get('timing_advice', '时机建议')}

【卦象启示】：{hexagram_data.judgment}
{hexagram_data.image}

【综合建议】：
基于八字与卦象的双重指引，建议您在当前阶段注重内外兼修，既要发挥自身的先天优势，也要顺应外在环境的变化节拍。保持中正平和的心态，以不变应万变，同时把握住关键的转折时机。
"""
        
        return interpretation.strip()
    
    @classmethod
    def _analyze_yearly_fortune(cls, hexagram: HexagramData, bazi_result: BaziCalculateResponse) -> str:
        """分析年运势走向"""
        # 基于卦象分析年运势
        if hexagram.upper_trigram in ["乾", "震", "离"]:
            if hexagram.lower_trigram in ["乾", "震", "离"]:
                return "运势强劲上升，适合积极进取"
            else:
                return "运势稳中有升，需要把握机会"
        elif hexagram.upper_trigram in ["坤", "巽", "坎"]:
            if hexagram.lower_trigram in ["坤", "巽", "坎"]:
                return "运势相对平缓，适合稳扎稳打"
            else:
                return "运势有起伏变化，需要灵活应对"
        else:
            return "运势总体稳定，保持平常心"
    
    @classmethod
    def _predict_yearly_events(cls, hexagram: HexagramData, bazi_result: BaziCalculateResponse, year: int) -> List[str]:
        """预测年度重要事件"""
        events = []
        
        # 根据变爻预测事件
        changing_lines = [line for line in hexagram.lines if line.is_changing]
        
        if len(changing_lines) >= 2:
            events.append("可能有重要的人生转折或决策机会")
        
        if hexagram.upper_trigram == "离":
            events.append("事业或学业方面可能有突破性进展")
        
        if hexagram.lower_trigram == "兑":
            events.append("人际关系和合作方面有良好发展")
        
        if hexagram.name and "水" in hexagram.name:
            events.append("财运方面需要特别关注")
        
        if not events:
            events.append("整体运势平稳，重在积累和沉淀")
        
        return events
    
    @classmethod
    def _generate_yearly_advice(cls, hexagram: HexagramData, bazi_result: BaziCalculateResponse) -> str:
        """生成年度建议"""
        advice_parts = []
        
        # 基于上卦的建议
        if hexagram.upper_trigram == "乾":
            advice_parts.append("保持积极主动的态度")
        elif hexagram.upper_trigram == "坤":
            advice_parts.append("以柔克刚，注重包容与合作")
        elif hexagram.upper_trigram == "震":
            advice_parts.append("抓住机遇，勇于创新")
        elif hexagram.upper_trigram == "巽":
            advice_parts.append("顺势而为，循序渐进")
        
        # 基于下卦的建议
        if hexagram.lower_trigram == "坎":
            advice_parts.append("面对困难要有智慧和耐心")
        elif hexagram.lower_trigram == "离":
            advice_parts.append("发挥才华，展现光明面")
        elif hexagram.lower_trigram == "艮":
            advice_parts.append("适时停止，反思总结")
        elif hexagram.lower_trigram == "兑":
            advice_parts.append("保持愉悦心情，广结善缘")
        
        return "；".join(advice_parts) + "。"
    
    @classmethod
    def _identify_favorable_months(cls, hexagram: HexagramData, year: int) -> List[str]:
        """识别有利月份"""
        favorable_months = []
        
        # 根据卦象特征识别有利月份
        if hexagram.upper_trigram in ["乾", "震"]:
            favorable_months.extend(["春分前后", "立夏前后"])
        
        if hexagram.lower_trigram in ["离", "兑"]:
            favorable_months.extend(["夏至前后", "秋分前后"])
        
        if "水" in hexagram.name:
            favorable_months.extend(["冬至前后"])
        
        if not favorable_months:
            favorable_months = ["春夏交接", "秋冬过渡"]
        
        return favorable_months
    
    @classmethod
    def _identify_caution_periods(cls, hexagram: HexagramData, year: int) -> List[str]:
        """识别需要谨慎的时期"""
        caution_periods = []
        
        # 根据变爻数量判断
        changing_lines = [line for line in hexagram.lines if line.is_changing]
        
        if len(changing_lines) >= 3:
            caution_periods.append("年中变化剧烈期")
        
        if hexagram.upper_trigram == "坎":
            caution_periods.append("冬季需要特别小心")
        
        if hexagram.lower_trigram == "艮":
            caution_periods.append("年末需要谨慎收尾")
        
        if not caution_periods:
            caution_periods = ["季节交替时期"]
        
        return caution_periods

# 便捷函数
def integrate_bazi_iching_analysis(
    bazi_result: BaziCalculateResponse, 
    question: str = "综合运势如何？"
) -> Dict[str, Any]:
    """
    便捷的八字易经综合分析函数
    
    Args:
        bazi_result: 八字计算结果
        question: 问卦问题
        
    Returns:
        Dict[str, Any]: 综合分析结果
    """
    integrator = BaziIchingIntegrator()
    
    # 生成对应卦象
    hexagram = integrator.generate_bazi_based_hexagram(bazi_result, question)
    
    # 分析相合度
    compatibility = integrator.analyze_bazi_hexagram_compatibility(bazi_result, hexagram)
    
    # 预测未来趋势
    current_year = datetime.now().year
    future_trends = integrator.predict_life_trends_with_iching(
        bazi_result, 
        [current_year, current_year + 1, current_year + 2]
    )
    
    return {
        "hexagram": {
            "name": hexagram.name,
            "number": hexagram.number,
            "upper_trigram": hexagram.upper_trigram,
            "lower_trigram": hexagram.lower_trigram,
            "image": hexagram.image,
            "judgment": hexagram.judgment,
            "lines": [
                {
                    "number": line.number,
                    "yin_yang": line.yin_yang,
                    "is_changing": line.is_changing,
                    "description": line.description
                } for line in hexagram.lines
            ]
        },
        "compatibility_analysis": compatibility,
        "future_trends": future_trends,
        "summary": {
            "question": question,
            "compatibility_score": compatibility.get("compatibility_score", 0),
            "main_advice": compatibility.get("integrated_interpretation", ""),
            "next_year_outlook": future_trends.get(current_year + 1, {}).get("fortune_trend", "")
        }
    }
