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

# 导入地理位置服务
from .location_service import LocationService

# 导入常量
from .constants import (
    STEM_ELEMENTS, BRANCH_ELEMENTS, FIVE_ELEMENTS_GENERATION, FIVE_ELEMENTS_OVERCOMING,
    REVERSE_GENERATION, REVERSE_OVERCOMING, STEM_YIN_YANG, BRANCH_YIN_YANG,
    BRANCH_HIDDEN_STEMS, BRANCH_SIX_COMBINATIONS, BRANCH_SIX_CONFLICTS,
    CHANG_SHENG_MAPPING, CHANG_SHENG_STRENGTH_LEVELS, NAYIN_MAP_COMPLETE,
    JIAZI_TABLE
)

# 导入日志配置
from .logger_config import setup_logger

# 创建专用日志记录器
logger = setup_logger("bazi_calculator")

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


# 主计算函数
async def calculate_bazi_data(request_data: BaziCalculateRequest, quick_mode: bool = False) -> BaziCalculateResponse:
    """计算八字数据的主函数 - 完全依赖lunar_python精确计算，可选真太阳时校正
    
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
        
        # 初始化地理位置服务
        location_service = LocationService()
        
        # 地理位置信息处理（使用LocationService）
        location_info = {
            "province": "", 
            "city": birth_place or "", 
            "longitude": None, 
            "latitude": None
        }
        
        # 如果提供了出生地点，查找地理位置信息
        if birth_place:
            try:
                geo_info = location_service.get_location_info(birth_place)
                if geo_info:
                    location_info.update({
                        "province": geo_info.get("province", ""),
                        "city": geo_info.get("city", birth_place),
                        "longitude": geo_info.get("longitude"),
                        "latitude": geo_info.get("latitude")
                    })
                    logger.info(f"获取地理位置信息成功：{birth_place} -> {geo_info}")
            except Exception as e:
                logger.warning(f"获取地理位置信息失败：{e}")
        
        # 可选的真太阳时校正
        corrected_time = final_dt  # 默认使用原时间
        correction_info = None
        
        # 记录校正前的时间信息
        logger.info(f"=== 八字计算开始 ===")
        logger.info(f"原始出生时间: {final_dt}")
        logger.info(f"出生地点: {birth_place}")
        
        # 如果提供了出生地点，尝试进行真太阳时校正
        if birth_place and location_info.get("longitude"):
            try:
                correction_info = FiveElementsCalculator.get_solar_time_correction(final_dt, birth_place, location_info["longitude"])
                if correction_info.get("correction_applied", False):
                    corrected_time = correction_info["corrected_time"]
                    logger.info(f"=== 真太阳时校正详情 ===")
                    logger.info(f"出生地点: {birth_place}")
                    logger.info(f"地理坐标: 经度{location_info['longitude']:.4f}°, 纬度{location_info.get('latitude', 0):.4f}°")
                    logger.info(f"校正前时间: {final_dt}")
                    logger.info(f"校正后时间: {corrected_time}")
                    logger.info(f"经度时差: {correction_info.get('longitude_diff_minutes', 0):.2f}分钟")
                    logger.info(f"均时差: {correction_info.get('equation_of_time_minutes', 0):.2f}分钟")
                    logger.info(f"总时差: {correction_info.get('longitude_diff_minutes', 0) + correction_info.get('equation_of_time_minutes', 0):.2f}分钟")
                else:
                    logger.info(f"真太阳时校正未应用，使用原时间")
            except Exception as e:
                logger.warning(f"真太阳时校正失败，使用原时间：{e}")
                corrected_time = final_dt
        else:
            logger.info(f"未提供出生地点或经度信息，跳过真太阳时校正")
        
        # 如果有校正信息，添加到location_info中
        if correction_info:
            location_info.update({
                "longitude": correction_info.get("longitude"),
                "longitude_diff_minutes": correction_info.get("longitude_diff_minutes", 0),
                "equation_of_time_minutes": correction_info.get("equation_of_time_minutes", 0),
                "correction_applied": correction_info.get("correction_applied", False),
                "original_time": final_dt.isoformat() if correction_info.get("correction_applied") else None,
                "corrected_time": corrected_time.isoformat() if correction_info.get("correction_applied") else None
            })
        
        # 使用lunar_python进行精确八字计算
        from lunar_python import Lunar as Lunar6Tail, Solar as Solar6Tail
        
        # 使用校正后的时间进行计算
        solar_6tail = Solar6Tail.fromYmdHms(
            corrected_time.year, corrected_time.month, corrected_time.day,
            corrected_time.hour, corrected_time.minute, corrected_time.second
        )
        lunar_6tail_obj = solar_6tail.getLunar()
        eight_char_6tail_obj = lunar_6tail_obj.getEightChar()
        
        # 获取四柱干支（使用lunar_python确保准确性）
        
        year_gan = Bazi.safe_get_name(eight_char_6tail_obj.getYearGan())
        year_zhi = Bazi.safe_get_name(eight_char_6tail_obj.getYearZhi())
        month_gan = Bazi.safe_get_name(eight_char_6tail_obj.getMonthGan())
        month_zhi = Bazi.safe_get_name(eight_char_6tail_obj.getMonthZhi())
        day_gan = Bazi.safe_get_name(eight_char_6tail_obj.getDayGan())
        day_zhi = Bazi.safe_get_name(eight_char_6tail_obj.getDayZhi())
        hour_gan = Bazi.safe_get_name(eight_char_6tail_obj.getTimeGan())
        hour_zhi = Bazi.safe_get_name(eight_char_6tail_obj.getTimeZhi())

        # 详细记录四柱干支计算结果
        logger.info(f"=== 四柱干支计算结果 ===")
        logger.info(f"用于计算的时间: {corrected_time}")
        logger.info(f"年柱: {year_gan}{year_zhi}")
        logger.info(f"月柱: {month_gan}{month_zhi}")
        logger.info(f"日柱: {day_gan}{day_zhi}")
        logger.info(f"时柱: {hour_gan}{hour_zhi}")
        logger.info(f"八字: {year_gan}{year_zhi} {month_gan}{month_zhi} {day_gan}{day_zhi} {hour_gan}{hour_zhi}")
        
        # 如果进行了校正，记录对比信息
        if correction_info and correction_info.get("correction_applied", False):
            logger.info(f"=== 时间校正对比分析 ===")
            logger.info(f"校正前时间: {final_dt}")
            logger.info(f"校正后时间: {corrected_time}")
            logger.info(f"时间差: {(corrected_time - final_dt).total_seconds() / 60:.2f}分钟")
            
            # 如果时间差显著，可能影响时柱，进行对比计算
            time_diff_minutes = abs((corrected_time - final_dt).total_seconds() / 60)
            if time_diff_minutes > 30:  # 超过30分钟的校正
                logger.info(f"时间校正超过30分钟，可能影响时柱，进行对比计算")
                
                # 计算原时间的八字
                original_solar = Solar6Tail.fromYmdHms(
                    final_dt.year, final_dt.month, final_dt.day,
                    final_dt.hour, final_dt.minute, final_dt.second
                )
                original_lunar = original_solar.getLunar()
                original_eight_char = original_lunar.getEightChar()
                
                original_year_gan = safe_get_name(original_eight_char.getYearGan())
                original_year_zhi = safe_get_name(original_eight_char.getYearZhi())
                original_month_gan = safe_get_name(original_eight_char.getMonthGan())
                original_month_zhi = safe_get_name(original_eight_char.getMonthZhi())
                original_day_gan = safe_get_name(original_eight_char.getDayGan())
                original_day_zhi = safe_get_name(original_eight_char.getDayZhi())
                original_hour_gan = safe_get_name(original_eight_char.getTimeGan())
                original_hour_zhi = safe_get_name(original_eight_char.getTimeZhi())
                
                logger.info(f"原时间八字: {original_year_gan}{original_year_zhi} {original_month_gan}{original_month_zhi} {original_day_gan}{original_day_zhi} {original_hour_gan}{original_hour_zhi}")
                logger.info(f"校正后八字: {year_gan}{year_zhi} {month_gan}{month_zhi} {day_gan}{day_zhi} {hour_gan}{hour_zhi}")
                
                # 检查差异
                differences = []
                if f"{original_year_gan}{original_year_zhi}" != f"{year_gan}{year_zhi}":
                    differences.append(f"年柱: {original_year_gan}{original_year_zhi} → {year_gan}{year_zhi}")
                if f"{original_month_gan}{original_month_zhi}" != f"{month_gan}{month_zhi}":
                    differences.append(f"月柱: {original_month_gan}{original_month_zhi} → {month_gan}{month_zhi}")
                if f"{original_day_gan}{original_day_zhi}" != f"{day_gan}{day_zhi}":
                    differences.append(f"日柱: {original_day_gan}{original_day_zhi} → {day_gan}{day_zhi}")
                if f"{original_hour_gan}{original_hour_zhi}" != f"{hour_gan}{hour_zhi}":
                    differences.append(f"时柱: {original_hour_gan}{original_hour_zhi} → {hour_gan}{hour_zhi}")
                
                if differences:
                    logger.warning(f"真太阳时校正导致四柱变化: {'; '.join(differences)}")
                else:
                    logger.info(f"真太阳时校正未导致四柱变化")

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
            start_date, start_days, luck_pillars, start_age = FiveElementsCalculator.calculate_precise_dayun(
                final_dt, request_data.gender, year_gan, month_pillar
            )
            major_cycles = FiveElementsCalculator.format_dayun_info(start_age, luck_pillars, final_dt, day_gan)
            
            # 创建DaYun对象供高级分析使用
            for i, pillar in enumerate(luck_pillars):
                cycle_start_age = start_age + i * 10
                if hasattr(pillar, 'stem_branch'):
                    # pillar 是 DaYun 对象
                    dayun_gan = pillar.stem_branch.stem
                    dayun_zhi = pillar.stem_branch.branch
                    
                    dayun_obj = DaYun(
                        start_age=cycle_start_age,
                        stem_branch=StemBranch(dayun_gan, dayun_zhi),
                        end_age=cycle_start_age + 9
                    )
                else:
                    # pillar 是字符串格式（兼容旧格式）
                    pillar_str = str(pillar)
                    dayun_gan = pillar_str[0] if len(pillar_str) >= 2 else '甲'
                    dayun_zhi = pillar_str[1] if len(pillar_str) >= 2 else '子'
                    
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
            interactions = shen_sha_calculator.analyze_interactions(bazi_obj)
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
            
            current_year_gan = Bazi.safe_get_name(current_eight_char.getYearGan())
            current_year_zhi = Bazi.safe_get_name(current_eight_char.getYearZhi())
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
                start_age = int(cycle.get("age_start", cycle.get("start_age", 0)))
                end_age = start_age + 9
                if start_age <= current_age <= end_age:
                    current_dayun = cycle.get("pillar", cycle.get("gan_zhi", "未知"))
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
            bazi_obj, current_year, major_cycles, current_dayun_ten_god, 
            primary_favorable, primary_unfavorable
        )
        
        # 分析流年神煞 - 直接获取分析结果
        liunian_shensha_analysis = FiveElementsCalculator.analyze_liunian_shensha(
            bazi_obj, current_year
        )
        
        # 转换为列表格式以兼容analyzers.py的期望
        liunian_shensha = []
        # 添加有利神煞
        for shensha_info in liunian_shensha_analysis.get("favorable_shensha", []):
            liunian_shensha.append({
                "key": shensha_info["name"],
                "name": shensha_info["name"],
                "position": shensha_info["position"],
                "strength": shensha_info["strength"],
                "description": shensha_info["description"],
                "positive_tags": shensha_info.get("tags", []),
                "negative_tags": []
            })
        
        # 添加不利神煞
        for shensha_info in liunian_shensha_analysis.get("unfavorable_shensha", []):
            liunian_shensha.append({
                "key": shensha_info["name"],
                "name": shensha_info["name"],
                "position": shensha_info["position"],
                "strength": shensha_info["strength"],
                "description": shensha_info["description"],
                "positive_tags": [],
                "negative_tags": shensha_info.get("tags", [])
            })
        
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
            "shensha_analysis": liunian_shensha_analysis,
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
                # 即使lunar_python返回了纳音，也要应用标准化
                try:
                    # 使用神煞计算器的标准化方法
                    standardized_nayin_name, nayin_element_index = shen_sha_calculator.get_nayin_name_and_element(gan, zhi)
                    nayin_name_str = standardized_nayin_name
                except Exception as e:
                    logger.warning(f"纳音标准化失败 {pillar_name}: {e}")
                    # 获取五行索引
                    try:
                        nayin_element_index = shen_sha_calculator.get_nayin_element_index(gan, zhi)
                    except Exception as e2:
                        logger.warning(f"纳音五行索引获取失败 {pillar_name}: {e2}")
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
