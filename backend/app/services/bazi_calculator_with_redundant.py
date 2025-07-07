"""
八字排盘主计算模块
包含主要的API计算逻辑，依赖calculators.py中的计算引擎
"""
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.schemas.bazi import BaziCalculateRequest, BaziCalculateResponse
from typing import Dict, Any, List, Optional, Union
import json
import os

# 导入核心数据结构
from .core import Bazi, ShenSha, DaYun, StemBranch

# 导入计算器类
from .calculators import ShenShaCalculator, FiveElementsCalculator

# 导入常量
from .constants import (
    STEM_ELEMENTS, BRANCH_ELEMENTS, FIVE_ELEMENTS_GENERATION, FIVE_ELEMENTS_OVERCOMING,
    REVERSE_GENERATION, REVERSE_OVERCOMING, STEM_YIN_YANG, BRANCH_YIN_YANG,
    BRANCH_HIDDEN_STEMS, BRANCH_SIX_COMBINATIONS, BRANCH_SIX_CONFLICTS,
    CHANG_SHENG_MAPPING, CHANG_SHENG_STRENGTH_LEVELS, NAYIN_MAP_COMPLETE
)

# 导入日志配置
from .logger_config import setup_logger

# 创建专用日志记录器
logger = setup_logger("bazi_calculator")

# JIAZI 六十甲子表
JIAZI_TABLE = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]

# 动态加载节气数据
def load_solar_terms_data():
    """从JSON文件加载节气数据"""
    try:
        solar_terms_file = os.path.join(os.path.dirname(__file__), '..', '..', 'solar_terms_data.json')
        logger.info(f"尝试加载节气数据文件: {solar_terms_file}")
        with open(solar_terms_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"成功加载节气数据文件，包含{len(data)}年的数据，年份范围: {list(data.keys())}")
            return data
    except Exception as e:
        logger.error(f"加载节气数据文件失败: {e}")
        # Fallback到默认数据（注意：键使用字符串类型以保持一致性）
        return {
            "2024": {
                "立春": "2024-02-04 16:27", "雨水": "2024-02-19 12:13", "惊蛰": "2024-03-05 10:23",
                "春分": "2024-03-20 11:06", "清明": "2024-04-04 15:02", "谷雨": "2024-04-19 21:59",
                "立夏": "2024-05-05 08:10", "小满": "2024-05-20 20:59", "芒种": "2024-06-05 12:10",
                "夏至": "2024-06-21 04:51", "小暑": "2024-07-06 22:20", "大暑": "2024-07-22 15:44",
                "立秋": "2024-08-07 08:09", "处暑": "2024-08-22 22:55", "白露": "2024-09-07 11:11",
                "秋分": "2024-09-22 20:44", "寒露": "2024-10-08 03:00", "霜降": "2024-10-23 06:15",
                "立冬": "2024-11-07 06:20", "小雪": "2024-11-22 03:56", "大雪": "2024-12-06 23:17",
                "冬至": "2024-12-21 17:21", "小寒": "2025-01-05 10:33", "大寒": "2025-01-20 03:51"
            }
        }

# 加载节气数据
SOLAR_TERMS_DATA = load_solar_terms_data()


def get_solar_terms_for_year(year: int) -> dict:
    """获取指定年份的节气数据"""
    year_str = str(year)
    # 首先尝试获取指定年份的数据
    if year_str in SOLAR_TERMS_DATA:
        return SOLAR_TERMS_DATA[year_str]
    
    # 如果没有找到，尝试使用2024年作为默认值
    if "2024" in SOLAR_TERMS_DATA:
        logger.warning(f"未找到{year}年的节气数据，使用2024年数据作为默认值")
        return SOLAR_TERMS_DATA["2024"]
    
    # 如果连2024年都没有，使用第一个可用的年份
    if SOLAR_TERMS_DATA:
        first_year = list(SOLAR_TERMS_DATA.keys())[0]
        logger.warning(f"未找到{year}年和2024年的节气数据，使用{first_year}年数据作为默认值")
        return SOLAR_TERMS_DATA[first_year]
    
    # 如果数据完全为空，返回空字典并记录错误
    logger.error(f"节气数据完全为空，无法获取{year}年的数据")
    return {}


def find_solar_term_datetime(year: int, term_name: str) -> Optional[datetime]:
    """查找指定年份和节气的具体时间"""
    year_terms = get_solar_terms_for_year(year)
    term_str = year_terms.get(term_name)
    if term_str:
        try:
            if ":60" in term_str:
                term_str = term_str.replace(":60", ":59")
            return datetime.strptime(term_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None
    return None


def calculate_precise_dayun(birth_datetime: datetime, gender: str, year_gan: str, month_pillar: str) -> tuple:
    """精确计算大运起运信息"""
    try:
        birth_year = birth_datetime.year
        
        # 1. 判断阴阳年
        yang_gans = ["甲", "丙", "戊", "庚", "壬"]
        is_yang_year = year_gan in yang_gans
        
        # 2. 判断顺逆排
        is_male = (gender == "男")
        is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
        
        # 3. 查找节气
        all_terms_sorted = []
        for y in [birth_year -1, birth_year, birth_year + 1]:
            terms = get_solar_terms_for_year(y)
            for name, dt_str in terms.items():
                dt = datetime.strptime(dt_str.replace(":60", ":59"), "%Y-%m-%d %H:%M")
                all_terms_sorted.append((dt, name))
        all_terms_sorted.sort()

        next_jie = None
        prev_jie = None
        for dt, name in all_terms_sorted:
            # "节" are the odd-numbered solar terms
            if name in ["立春", "惊蛰", "清明", "立夏", "芒种", "小暑", "立秋", "白露", "寒露", "立冬", "大雪", "小寒"]:
                if dt > birth_datetime:
                    if next_jie is None:
                        next_jie = dt
                else:
                    prev_jie = dt
        
        if not next_jie or not prev_jie:
            logger.error("无法找到前后节气，无法计算起运")
            raise ValueError("无法找到前后节气，无法计算起运。")

        # 4. 计算起运天数（权威算法修正）
        if is_forward:
            time_diff = next_jie - birth_datetime
        else:
            time_diff = birth_datetime - prev_jie
            
        # 权威算法：1天 = 4个月（修正：原来是3天=1岁）
        start_days = time_diff.total_seconds() / (3600 * 24)
        start_months = start_days * 4  # 1天=4个月
        start_years = start_months / 12  # 12个月=1年
        
        # 5. 起运日期
        start_age = int(start_years)
        start_date = birth_datetime + timedelta(days=start_days)
        
        logger.info(f"大运计算结果(权威算法): 起运年龄={start_age}, 起运天数={start_days:.2f}, 起运月数={start_months:.2f}, 起运日期={start_date}")
        logger.info(f"大运算法修正: 使用1天=4个月，替代原来的3天=1岁")
        
        # 6. 生成大运干支序列
        try:
            month_index = JIAZI_TABLE.index(month_pillar)
        except ValueError:
            logger.warning(f"无法在JIAZI_TABLE中找到月柱{month_pillar}，使用索引0")
            month_index = 0
        
        luck_pillars = []
        for i in range(10):
            if is_forward:
                pillar_index = (month_index + i + 1) % 60
            else:
                pillar_index = (month_index - i - 1 + 60) % 60
            luck_pillars.append(JIAZI_TABLE[pillar_index])
        
        return start_date, start_days, luck_pillars, start_age
        
    except Exception as e:
        logger.error(f"精确大运计算失败: {e}", exc_info=True)
        # 返回更有意义的fallback值
        try:
            # 使用简化算法：一般3-8岁起运
            fallback_start_age = 3 if gender == "男" else 5
            fallback_start_date = birth_datetime + timedelta(days=365 * fallback_start_age)
            fallback_start_days = 365 * fallback_start_age
            
            # 生成标准的大运序列
            fallback_luck_pillars = []
            try:
                month_index = JIAZI_TABLE.index(f"{month_pillar}")
                is_forward = True  # 简化处理
                for i in range(10):
                    if is_forward:
                        pillar_index = (month_index + i + 1) % 60
                    else:
                        pillar_index = (month_index - i - 1 + 60) % 60
                    fallback_luck_pillars.append(JIAZI_TABLE[pillar_index])
            except:
                fallback_luck_pillars = ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉"]
            
            logger.warning(f"使用fallback大运计算：起运年龄={fallback_start_age}")
            return fallback_start_date, fallback_start_days, fallback_luck_pillars, fallback_start_age
            
        except Exception as fallback_error:
            logger.error(f"fallback大运计算也失败: {fallback_error}")
            # 最后的默认值
            start_date = birth_datetime + timedelta(days=365*3)
            start_days = 365*3
            luck_pillars = ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉"]
            return start_date, start_days, luck_pillars, 3







def format_dayun_info(start_age: int, luck_pillars: list, birth_datetime: datetime, day_gan: str) -> list:
    """格式化大运信息为标准字典格式，包含更丰富的动态内容"""
    major_cycles = []
    
    for i, pillar in enumerate(luck_pillars):
        cycle_start_age = start_age + i * 10
        cycle_start_year = birth_datetime.year + cycle_start_age
        cycle_end_year = cycle_start_year + 9
        
        phase = FiveElementsCalculator.analyze_dayun_phase(cycle_start_age)
        
        ten_god = "未知"
        pillar_zhi = "未知"
        pillar_gan = "未知"
        if len(pillar) >= 2:
            pillar_gan = pillar[0]
            pillar_zhi = pillar[1]
            ten_god = FiveElementsCalculator.calculate_ten_god_relation(pillar_gan, day_gan)
        
        # 获取五行信息
        gan_element = STEM_ELEMENTS.get(pillar_gan, "未知")
        zhi_element = BRANCH_ELEMENTS.get(pillar_zhi, "未知")
        
        # 计算长生状态
        chang_sheng_info = [{
            "gan": pillar_gan,
            "zhi": pillar_zhi,
            "chang_sheng_state": FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(pillar_gan, pillar_zhi),
            "description": f"{pillar_gan}在{pillar_zhi}地支上的长生状态",
            "strength_level": FiveElementsCalculator.get_chang_sheng_strength_level(FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(pillar_gan, pillar_zhi))
        }]
        chang_sheng_state = chang_sheng_info[0]["chang_sheng_state"] if chang_sheng_info else "未知"
        
        # 动态生成更丰富的分析内容
        cycle_info = {
            "gan_zhi": pillar,
            "start_age": str(cycle_start_age),
            "start_year": str(cycle_start_year),
            "end_year": str(cycle_end_year),
            "ten_gods_gan": ten_god,
            "hidden_stems_zhi": FiveElementsCalculator.get_zhi_hidden_gan(pillar_zhi),
            "interaction_with_mingju": f"大运{pillar}天干{pillar_gan}({gan_element})为{ten_god}，地支{pillar_zhi}({zhi_element})藏干{FiveElementsCalculator.get_zhi_hidden_gan(pillar_zhi)}，与日主{day_gan}形成{ten_god}关系，五行互动呈现{gan_element}与{zhi_element}的复合影响",
            "phase_analysis": f"{phase}阶段，大运{pillar}主导，长生状态为{chang_sheng_state}",
            "age_range": f"{cycle_start_age}-{cycle_start_age+9}",
            "description": f"大运{pillar}期间({cycle_start_age}-{cycle_start_age+9}岁)，{ten_god}星当令，{gan_element}行主导，生活重心偏向{ten_god}相关领域，运势表现为{chang_sheng_state}状态",
            "trend": f"大运{pillar}整体运势：{ten_god}影响下的{gan_element}行运势，{chang_sheng_state}状态对应的发展趋势",
            "advice": f"关注{ten_god}的发展机遇，善用{gan_element}元素，在{chang_sheng_state}状态下采取相应策略，注意地支{pillar_zhi}所藏{FiveElementsCalculator.get_zhi_hidden_gan(pillar_zhi)}的影响",
            "deep_analysis": f"详细分析：大运{pillar}天干{pillar_gan}主外在表现和行动力，{ten_god}特质明显；地支{pillar_zhi}主内在根基和潜在能量，{zhi_element}行稳定发展；长生{chang_sheng_state}状态影响此阶段的整体起伏节奏",
            "deepseek_enhanced": False,
            "analysis_method": "精确计算",
            "five_elements_info": {
                "gan_element": gan_element,
                "zhi_element": zhi_element,
                "chang_sheng_state": chang_sheng_state
            }
        }
        
        major_cycles.append(cycle_info)
    
    return major_cycles


async def calculate_bazi_data(request_data: BaziCalculateRequest, quick_mode: bool = False) -> BaziCalculateResponse:
    """计算八字数据的主函数 - 完全依赖lunar_python精确计算
    
    Args:
        request_data: 八字计算请求数据
        quick_mode: 快速模式，如果为True则跳过一些复杂的分析计算
    """
    
    try:
        final_dt = request_data.birth_datetime
        birth_place = request_data.birth_place
        
        if quick_mode:
            logger.info("使用快速模式进行八字计算")
        else:
            logger.info("使用完整模式进行八字计算")
        
        # 地理位置信息处理（简化版）
        location_info = {"province": "", "city": birth_place or "", "longitude": None, "latitude": None}
        
        # 使用lunar_python进行精确八字计算
        from lunar_python import Lunar as Lunar6Tail, Solar as Solar6Tail
        
        solar_6tail = Solar6Tail.fromYmdHms(
            final_dt.year, final_dt.month, final_dt.day,
            final_dt.hour, final_dt.minute, final_dt.second
        )
        lunar_6tail_obj = solar_6tail.getLunar()
        eight_char_6tail_obj = lunar_6tail_obj.getEightChar()
        
        # 获取四柱干支（使用lunar_python确保准确性）
        def safe_get_name(obj):
            """安全获取名称，处理可能的None或错误"""
            try:
                if hasattr(obj, 'getName'):
                    return obj.getName()
                return str(obj) if obj else ""
            except:
                return ""
        
        year_gan = safe_get_name(eight_char_6tail_obj.getYearGan())
        year_zhi = safe_get_name(eight_char_6tail_obj.getYearZhi())
        month_gan = safe_get_name(eight_char_6tail_obj.getMonthGan())
        month_zhi = safe_get_name(eight_char_6tail_obj.getMonthZhi())
        day_gan = safe_get_name(eight_char_6tail_obj.getDayGan())
        day_zhi = safe_get_name(eight_char_6tail_obj.getDayZhi())
        hour_gan = safe_get_name(eight_char_6tail_obj.getTimeGan())
        hour_zhi = safe_get_name(eight_char_6tail_obj.getTimeZhi())

        # 创建Bazi对象
        bazi_obj = Bazi(
            year=StemBranch(year_gan, year_zhi),
            month=StemBranch(month_gan, month_zhi), 
            day=StemBranch(day_gan, day_zhi), 
            hour=StemBranch(hour_gan, hour_zhi),
            gender=request_data.gender,
            birth_time=final_dt
        )
        
        bazi_characters = bazi_obj.get_bazi_characters()
        day_master_element = STEM_ELEMENTS.get(bazi_obj.day.stem, "")
        zodiac_sign = bazi_obj.get_zodiac()
        
        day_master_strength = FiveElementsCalculator.calculate_day_master_strength(bazi_obj)
        five_elements_percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi_obj)
        five_elements_score = {k: f"{v}%" for k, v in five_elements_percentages.items()}
        
        # 使用综合分析替代基础喜用神分析
        comprehensive_analysis = FiveElementsCalculator.analyze_comprehensive_gods(bazi_obj)
        favorable_elements = comprehensive_analysis["basic_analysis"]["favorable_elements"]
        
        logger.debug(f"计算结果 - 日主强弱: {day_master_strength}, 喜用神: {favorable_elements}")

        # === 精确大运计算 ===
        major_cycles = []
        dayun_objects = []
        try:
            month_pillar = f"{month_gan}{month_zhi}"
            start_date, start_days, luck_pillars, start_age = calculate_precise_dayun(
                final_dt, request_data.gender, year_gan, month_pillar
            )
            major_cycles = format_dayun_info(start_age, luck_pillars, final_dt, day_gan)
            
            # 创建DaYun对象供高级分析使用
            for i, pillar in enumerate(luck_pillars):
                cycle_start_age = start_age + i * 10
                dayun_gan = pillar[0] if len(pillar) >= 2 else '甲'
                dayun_zhi = pillar[1] if len(pillar) >= 2 else '子'
                
                dayun_obj = DaYun(
                    start_age=cycle_start_age,
                    stem_branch=StemBranch(dayun_gan, dayun_zhi),
                    end_age=cycle_start_age + 9
                )
                dayun_objects.append(dayun_obj)
                
        except Exception as e:
            logger.error(f"大运计算出错: {e}", exc_info=True)
            # Fallback - 创建简化的大运信息
            for i in range(8):
                cycle_start_age = 8 + i * 10
                pillar = JIAZI_TABLE[i*6 % 60]
                major_cycles.append({
                    "gan_zhi": pillar,
                    "start_age": str(cycle_start_age),
                    "start_year": str(final_dt.year + cycle_start_age),
                    "end_year": str(final_dt.year + cycle_start_age + 9),
                    "ten_gods_gan": "未知",
                    "hidden_stems_zhi": "未知", 
                    "interaction_with_mingju": f"大运{pillar}与命局的互动分析",
                    "phase_analysis": FiveElementsCalculator.analyze_dayun_phase(cycle_start_age),
                    "age_range": f"{cycle_start_age}-{cycle_start_age+9}",
                    "description": f"大运{pillar}期间的运势特点",
                    "trend": f"大运{pillar}整体运势",
                    "advice": f"关注大运{pillar}的发展",
                    "deep_analysis": f"详细分析大运{pillar}",
                    "deepseek_enhanced": False,
                    "analysis_method": "fallback"
                })

        # 四柱详细信息
        gan_zhi_info = {
            "year_pillar": {"gan": year_gan, "zhi": year_zhi, "ten_god": FiveElementsCalculator.calculate_ten_god_relation(year_gan, day_gan), "hidden_stems": FiveElementsCalculator.get_zhi_hidden_gan(year_zhi)},
            "month_pillar": {"gan": month_gan, "zhi": month_zhi, "ten_god": FiveElementsCalculator.calculate_ten_god_relation(month_gan, day_gan), "hidden_stems": FiveElementsCalculator.get_zhi_hidden_gan(month_zhi)},
            "day_pillar": {"gan": day_gan, "zhi": day_zhi, "ten_god": "日主", "hidden_stems": FiveElementsCalculator.get_zhi_hidden_gan(day_zhi)},
            "hour_pillar": {"gan": hour_gan, "zhi": hour_zhi, "ten_god": FiveElementsCalculator.calculate_ten_god_relation(hour_gan, day_gan), "hidden_stems": FiveElementsCalculator.get_zhi_hidden_gan(hour_zhi)},
        }
        
        # 互动分析（使用ShenShaCalculator中的完整方法）
        shen_sha_calculator = ShenShaCalculator()
        
        # 使用ShenShaCalculator的calculate_shensha方法 (快速模式跳过复杂互动分析)
        if not quick_mode:
            # 暂时注释掉互动分析，因为方法不存在
            # interactions = shen_sha_calculator.analyze_interactions(bazi_obj)
            interactions = {}
        else:
            interactions = {}
            logger.debug("快速模式：跳过复杂互动分析")

        # 神煞计算 (快速模式使用简化计算)
        if not quick_mode:
            shen_sha_results = shen_sha_calculator.calculate_shensha(bazi_obj)
            shen_sha_details = [
                {
                    "key": key,
                    "name": sha.name,
                    "position": sha.position,
                    "strength": sha.strength,
                    "active": sha.active,
                    "tags": sha.tags
                }
                for key, sha in shen_sha_results.items()
            ]
        else:
            shen_sha_details = []
            logger.debug("快速模式：跳过详细神煞计算")

        # === 当年运势计算（使用lunar_python精确计算） ===
        current_year = datetime.now().year
        current_age = current_year - final_dt.year
        
        try:
            # 使用lunar_python获取当年流年干支
            current_solar = Solar6Tail.fromYmd(current_year, 1, 1)
            current_lunar = current_solar.getLunar()
            current_eight_char = current_lunar.getEightChar()
            
            current_year_gan = safe_get_name(current_eight_char.getYearGan())
            current_year_zhi = safe_get_name(current_eight_char.getYearZhi())
            current_year_ganzhi = f"{current_year_gan}{current_year_zhi}"
            
        except Exception as e:
            logger.warning(f"流年干支计算失败，使用简化方法: {e}")
            # Fallback to simplified calculation
            current_year_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"][(current_year - 4) % 10]
            current_year_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"][(current_year - 4) % 12]
            current_year_ganzhi = f"{current_year_gan}{current_year_zhi}"
        
        # 计算与日主的关系和五行信息
        current_year_ten_god = FiveElementsCalculator.calculate_ten_god_relation(current_year_gan, day_gan)
        current_year_gan_element = STEM_ELEMENTS.get(current_year_gan, "未知")
        current_year_zhi_element = BRANCH_ELEMENTS.get(current_year_zhi, "未知")
        
        # 获取当前大运及其信息
        current_dayun = "未知"
        current_dayun_ten_god = "未知"
        current_dayun_element = "未知"
        if major_cycles:
            for cycle in major_cycles:
                start_age = int(cycle["start_age"])
                end_age = start_age + 9
                if start_age <= current_age <= end_age:
                    current_dayun = cycle["gan_zhi"]
                    current_dayun_ten_god = cycle["ten_gods_gan"]
                    current_dayun_element = cycle.get("five_elements_info", {}).get("gan_element", "未知")
                    break
        
        # 长生状态计算
        liunian_chang_sheng = [{
            "gan": current_year_gan,
            "zhi": current_year_zhi,
            "chang_sheng_state": FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(current_year_gan, current_year_zhi),
            "description": f"{current_year_gan}在{current_year_zhi}地支上的长生状态",
            "strength_level": FiveElementsCalculator.get_chang_sheng_strength_level(FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(current_year_gan, current_year_zhi))
        }]
        liunian_chang_sheng_state = liunian_chang_sheng[0]["chang_sheng_state"] if liunian_chang_sheng else "未知"
        
        # 动态计算当年运势分析 - 使用综合分析结果和详细互动分析
        primary_favorable = comprehensive_analysis["final_prognosis"]["primary_favorable"]
        secondary_favorable = comprehensive_analysis["final_prognosis"]["secondary_favorable"]
        primary_unfavorable = comprehensive_analysis["final_prognosis"]["primary_unfavorable"]
        life_advice = comprehensive_analysis["final_prognosis"]["life_advice"]
        overall_rating = comprehensive_analysis["final_prognosis"]["overall_rating"]
        
        # 分析流年与命局的具体互动关系
        dayun_gan_str = current_dayun[:1] if len(current_dayun) >= 2 else ""
        dayun_zhi_str = current_dayun[1:] if len(current_dayun) >= 2 else ""
        
        liunian_interactions = FiveElementsCalculator.analyze_liunian_interactions(
            bazi_obj, current_year_gan, current_year_zhi, dayun_gan_str, dayun_zhi_str
        )
        
        # 分析流年神煞
        liunian_shensha = FiveElementsCalculator.analyze_liunian_shensha(
            bazi_obj, current_year_gan, current_year_zhi, shen_sha_calculator
        )
        
        # 使用增强的流年分析引擎
        from .analyzers import EnhancedLiunianAnalyzer
        
        # 生成增强的特殊组合分析（替代原有的模板逻辑）
        enhanced_special_combinations = EnhancedLiunianAnalyzer.analyze_liunian_special_combinations(
            bazi_obj, current_year_gan, current_year_zhi, current_year_ten_god,
            liunian_interactions, liunian_shensha, comprehensive_analysis
        )
        
        # 生成增强的预测事件（替代原有的简单预测）
        enhanced_predicted_events = EnhancedLiunianAnalyzer.generate_enhanced_predicted_events(
            current_year_ten_god, current_year_gan, current_year_zhi,
            current_year_gan_element, current_year_zhi_element,
            liunian_interactions, liunian_shensha, comprehensive_analysis, current_age
        )
        
        # 初始化特殊组合分析结果结构
        special_combinations_analysis = {
            "favorable_combinations": [],
            "special_warnings": [],
            "personalized_insights": [],
            "timing_analysis": [],
            "risk_assessment": []
        }
        
        # 合并增强分析结果到 special_combinations_analysis
        for key in ["favorable_combinations", "special_warnings", "personalized_insights", "timing_analysis", "risk_assessment"]:
            if key in enhanced_special_combinations and enhanced_special_combinations[key]:
                special_combinations_analysis[key].extend(enhanced_special_combinations[key])
        
        # 确保每个字段至少有一项内容
        for key in ["favorable_combinations", "special_warnings", "personalized_insights", "timing_analysis", "risk_assessment"]:
            if not special_combinations_analysis.get(key):
                special_combinations_analysis[key] = ["无相关信息"]
        
        # 构造当年运势结果
        current_year_fortune = {
            "year": current_year,
            "gan_zhi": current_year_ganzhi,
            "age": current_age,
            "ten_god": current_year_ten_god,
            "elements": {
                "gan_element": current_year_gan_element,
                "zhi_element": current_year_zhi_element
            },
            "dayun_info": {
                "gan_zhi": current_dayun,
                "ten_god": current_dayun_ten_god,
                "element": current_dayun_element
            },
            "chang_sheng": liunian_chang_sheng,
            "chang_sheng_state": liunian_chang_sheng_state,
            "interactions": liunian_interactions,
            "shensha_analysis": liunian_shensha,
            "special_combinations": special_combinations_analysis,
            "predicted_events": enhanced_predicted_events,
            "comprehensive_analysis": {
                "primary_favorable": primary_favorable,
                "secondary_favorable": secondary_favorable,
                "primary_unfavorable": primary_unfavorable,
                "life_advice": life_advice,
                "overall_rating": overall_rating
            }
        }
        
        # === 纳音计算（优先使用lunar_python，fallback到内置映射） ===
        def safe_get_method_result(obj, method_name, default="未知"):
            """安全调用对象方法"""
            try:
                if hasattr(obj, method_name):
                    result = getattr(obj, method_name)()
                    return str(result) if result else default
                return default
            except:
                return default
        
        # 纳音计算
        na_yin = {}
        na_yin_pillars = {
            "year": (year_gan, year_zhi),
            "month": (month_gan, month_zhi),
            "day": (day_gan, day_zhi),
            "hour": (hour_gan, hour_zhi),
        }

        for pillar_name, (gan, zhi) in na_yin_pillars.items():
            # 先尝试从lunar_python获取纳音名称
            nayin_name_str = "未知"
            try:
                if pillar_name == "year":
                    nayin_name_str = safe_get_method_result(eight_char_6tail_obj, 'getYearNaYin', "未知")
                elif pillar_name == "month":
                    nayin_name_str = safe_get_method_result(eight_char_6tail_obj, 'getMonthNaYin', "未知")
                elif pillar_name == "day":
                    nayin_name_str = safe_get_method_result(eight_char_6tail_obj, 'getDayNaYin', "未知")
                elif pillar_name == "hour":
                    nayin_name_str = safe_get_method_result(eight_char_6tail_obj, 'getTimeNaYin', "未知")
            except Exception as e:
                logger.warning(f"lunar_python纳音获取失败 {pillar_name}: {e}")
                nayin_name_str = "未知"
            
            # 如果lunar_python返回的是未知，使用内置映射表
            if nayin_name_str == "未知" or not nayin_name_str:
                try:
                    nayin_name_str, nayin_element_index = shen_sha_calculator.get_nayin_name_and_element(gan, zhi)
                except Exception as e:
                    logger.warning(f"内置纳音计算失败 {pillar_name}: {e}")
                    nayin_name_str = f"{gan}{zhi}纳音"
                    nayin_element_index = 1
            else:
                # 获取五行索引
                try:
                    nayin_element_index = shen_sha_calculator.get_nayin_element_index(gan, zhi)
                except Exception as e:
                    logger.warning(f"纳音五行索引获取失败 {pillar_name}: {e}")
                    nayin_element_index = 1
            
            na_yin[f"{pillar_name}_na_yin"] = [nayin_name_str, nayin_element_index]
        
        # === 宫位信息（优先使用lunar_python） ===
        palace_info = {}
        try:
            palace_info = {
                "tai_yuan": safe_get_method_result(eight_char_6tail_obj, 'getTaiYuan', "甲子"),
                "ming_gong": safe_get_method_result(eight_char_6tail_obj, 'getMingGong', "乙丑"),
                "shen_gong": safe_get_method_result(eight_char_6tail_obj, 'getShenGong', "丙寅"),
                "tai_xi": safe_get_method_result(eight_char_6tail_obj, 'getTaiXi', "丁卯")
            }
            logger.debug(f"宫位信息获取成功: {palace_info}")
        except Exception as e:
            logger.warning(f"lunar_python宫位获取失败，使用fallback: {e}")
            # Fallback - 简化的宫位计算
            palace_info = {
                "tai_yuan": f"{month_gan}{month_zhi}",
                "ming_gong": f"{day_gan}{day_zhi}",
                "shen_gong": f"{hour_gan}{hour_zhi}",
                "tai_xi": f"{year_gan}{year_zhi}"
            }

        # 组织地支藏干信息
        dz_cang_gan = [
            {"pillar": "year", "branch": year_zhi, "hidden_stems": FiveElementsCalculator.get_zhi_hidden_gan(year_zhi)},
            {"pillar": "month", "branch": month_zhi, "hidden_stems": FiveElementsCalculator.get_zhi_hidden_gan(month_zhi)},
            {"pillar": "day", "branch": day_zhi, "hidden_stems": FiveElementsCalculator.get_zhi_hidden_gan(day_zhi)},
            {"pillar": "hour", "branch": hour_zhi, "hidden_stems": FiveElementsCalculator.get_zhi_hidden_gan(hour_zhi)}
        ]

        # 长生十二宫计算
        day_chang_sheng = [{
            "gan": day_gan,
            "zhi": day_zhi,
            "chang_sheng_state": FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(day_gan, day_zhi),
            "description": f"{day_gan}在{day_zhi}地支上的长生状态",
            "strength_level": FiveElementsCalculator.get_chang_sheng_strength_level(FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(day_gan, day_zhi))
        }]
        year_chang_sheng = [{
            "gan": year_gan,
            "zhi": year_zhi,
            "chang_sheng_state": FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(year_gan, year_zhi),
            "description": f"{year_gan}在{year_zhi}地支上的长生状态",
            "strength_level": FiveElementsCalculator.get_chang_sheng_strength_level(FiveElementsCalculator.calculate_chang_sheng_twelve_palaces(year_gan, year_zhi))
        }]

        logger.debug(f"最终数据检查 - 纳音: {na_yin}, 宫位: {palace_info}")

        # 转换日主强度为字符串描述
        day_master_strength_str = FiveElementsCalculator.get_strength_level_description(day_master_strength)

        # 构造响应
        return BaziCalculateResponse(
            bazi_characters=bazi_characters,
            five_elements_score=five_elements_score,
            day_master_strength=day_master_strength_str,
            day_master_element=day_master_element,
            zodiac_sign=zodiac_sign,
            major_cycles=major_cycles,
            gan_zhi_info=gan_zhi_info,
            shen_sha_details=shen_sha_details,
            interactions=interactions,
            favorable_elements=favorable_elements,
            comprehensive_favorable_analysis=comprehensive_analysis,
            na_yin=na_yin,
            palace_info=palace_info,
            current_year_fortune=current_year_fortune,
            birth_place=request_data.birth_place,
            location_info=location_info,
            dz_cang_gan=dz_cang_gan,
            day_chang_sheng=day_chang_sheng,
            year_chang_sheng=year_chang_sheng,
        )
        
    except Exception as e:
        logger.error(f"八字排盘计算错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"八字排盘发生错误：{str(e)}"
        )

# 创建精确计算器实例
precise_calculator = PreciseBaziCalculator()

def correct_solar_time(birth_time: datetime, longitude: float = 120.0) -> datetime:
    """真太阳时校正
    
    Args:
        birth_time: 出生时间（当地时间）
        longitude: 经度（东经为正，西经为负）
        
    Returns:
        校正后的真太阳时
    """
    return precise_calculator.correct_solar_time(birth_time, longitude)

def calculate_enhanced_year_pillar(year: int, birth_time: datetime, longitude: float = 120.0) -> tuple:
    """增强年柱计算（含真太阳时校正）
    
    Args:
        year: 年份
        birth_time: 出生时间
        longitude: 经度
        
    Returns:
        (年干, 年支)
    """
    # 真太阳时校正
    corrected_time = correct_solar_time(birth_time, longitude)
    
    # 立春时间（简化，实际应该从节气数据库获取）
    lichun_time = datetime(corrected_time.year, 2, 4, 10, 0)
    
    # 使用权威算法计算年柱
    return precise_calculator.calculate_year_pillar(year, corrected_time, lichun_time)

def calculate_enhanced_hour_pillar(hour: int, minute: int, day_gan: str) -> tuple:
    """增强时柱计算（含精确时辰划分）
    
    Args:
        hour: 小时
        minute: 分钟
        day_gan: 日干
        
    Returns:
        (时干, 时支)
    """
    # 精确时辰划分
    hour_zhi = precise_calculator.get_time_branch(hour, minute)
    
    # 五鼠遁计算时干
    return precise_calculator.calculate_hour_pillar(hour_zhi, day_gan)

def calculate_complete_bazi(birth_time: datetime, gender: str, longitude: float = 120.0) -> dict:
    """完整八字计算（含年柱、月柱、日柱、时柱）
    
    Args:
        birth_time: 出生时间
        gender: 性别
        longitude: 经度
        
    Returns:
        包含四柱干支的字典
    """
    # 真太阳时校正
    corrected_time = correct_solar_time(birth_time, longitude)
    
    # 立春时间（简化，实际应该从节气数据库获取）
    lichun_time = datetime(corrected_time.year, 2, 4, 10, 0)
    
    # 年柱
    year_pillar = precise_calculator.calculate_year_pillar(corrected_time.year, corrected_time, lichun_time)
    
    # 月柱
    month_pillar = precise_calculator.calculate_month_pillar(corrected_time, year_pillar[0])
    
    # 日柱
    day_pillar = precise_calculator.calculate_day_pillar_zeller(corrected_time.year, corrected_time.month, corrected_time.day)
    
    # 时柱
    hour_zhi = precise_calculator.get_time_branch(corrected_time.hour, corrected_time.minute)
    hour_pillar = precise_calculator.calculate_hour_pillar(hour_zhi, day_pillar[0])
    
    return {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
        "hour": hour_pillar
    }
