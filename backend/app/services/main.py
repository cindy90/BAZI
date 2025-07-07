"""
八字计算主模块
包含主要的计算函数、API入口和算法实现
"""
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.schemas.bazi import BaziCalculateRequest, BaziCalculateResponse
from typing import Dict, Any, List, Optional, Union
import math
import json
import os

# --- 导入 6tail/lunar-python 库 ---
from lunar_python import Lunar as Lunar6Tail, Solar as Solar6Tail
from lunar_python.util import LunarUtil

# 导入其他模块
from .core import Bazi, StemBranch, DaYun, FortuneModel
from .calculators import ShenShaCalculator, FiveElementsCalculator
from .analyzers import AdvancedDayunAnalyzer, AdvancedEventEngine, EventDeductionEngine
from .prompt_manager import PromptManager
from .utils import (
    safe_get_name, safe_get_method_result, analyze_dayun_phase,
    self_calculate_ten_god, get_zhi_hidden_gan, 
    analyze_dayun_interaction_with_mingju, calculate_precise_dayun_start,
    get_location_info, get_solar_terms_for_year, calculate_precise_dayun,
    format_dayun_info, JIAZI
)


# 节气数据库（2023-2025年）
SOLAR_TERMS_DATA = {
    2023: {
        "立春": "2023-02-04 10:42", "雨水": "2023-02-19 06:34", "惊蛰": "2023-03-06 04:36", 
        "春分": "2023-03-21 05:24", "清明": "2023-04-05 09:13", "谷雨": "2023-04-20 16:14",
        "立夏": "2023-05-06 02:19", "小满": "2023-05-21 15:09", "芒种": "2023-06-06 06:18",
        "夏至": "2023-06-21 22:58", "小暑": "2023-07-07 16:31", "大暑": "2023-07-23 09:50",
        "立秋": "2023-08-08 02:23", "处暑": "2023-08-23 17:01", "白露": "2023-09-08 05:27",
        "秋分": "2023-09-23 14:50", "寒露": "2023-10-08 21:16", "霜降": "2023-10-24 00:21",
        "立冬": "2023-11-08 00:36", "小雪": "2023-11-22 22:03", "大雪": "2023-12-07 17:33",
        "冬至": "2023-12-22 11:27", "小寒": "2024-01-06 04:49", "大寒": "2024-01-20 22:07"
    },
    2024: {
        "立春": "2024-02-04 16:27", "雨水": "2024-02-19 12:13", "惊蛰": "2024-03-05 10:23",
        "春分": "2024-03-20 11:06", "清明": "2024-04-04 15:02", "谷雨": "2024-04-19 21:60",
        "立夏": "2024-05-05 08:10", "小满": "2024-05-20 20:59", "芒种": "2024-06-05 12:10",
        "夏至": "2024-06-21 04:51", "小暑": "2024-07-06 22:20", "大暑": "2024-07-22 15:44",
        "立秋": "2024-08-07 08:09", "处暑": "2024-08-22 22:55", "白露": "2024-09-07 11:11",
        "秋分": "2024-09-22 20:44", "寒露": "2024-10-08 03:00", "霜降": "2024-10-23 06:15",
        "立冬": "2024-11-07 06:20", "小雪": "2024-11-22 03:56", "大雪": "2024-12-06 23:17",
        "冬至": "2024-12-21 17:21", "小寒": "2025-01-05 10:33", "大寒": "2025-01-20 03:51"
    },
    2025: {
        "立春": "2025-02-03 22:10", "雨水": "2025-02-18 17:57", "惊蛰": "2025-03-05 16:07",
        "春分": "2025-03-20 16:49", "清明": "2025-04-04 20:48", "谷雨": "2025-04-20 03:55",
        "立夏": "2025-05-05 14:01", "小满": "2025-05-21 02:49", "芒种": "2025-06-05 18:06",
        "夏至": "2025-06-21 10:42", "小暑": "2025-07-07 04:05", "大暑": "2025-07-22 21:29",
        "立秋": "2025-08-07 13:53", "处暑": "2025-08-23 04:34", "白露": "2025-09-07 16:52",
        "秋分": "2025-09-23 02:19", "寒露": "2025-10-08 08:36", "霜降": "2025-10-23 11:51",
        "立冬": "2025-11-07 12:01", "小雪": "2025-11-22 09:35", "大雪": "2025-12-07 05:04",
        "冬至": "2025-12-21 23:03", "小寒": "2026-01-05 16:16", "大寒": "2026-01-20 09:34"
    }
}

# 六十甲子表
JIAZI_TABLE = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]


async def calculate_bazi_data(request_data: BaziCalculateRequest, quick_mode: bool = False) -> BaziCalculateResponse:
    """计算八字数据的主函数 - 简化版本"""
    
    try:
        final_dt = request_data.birth_datetime
        birth_place = request_data.birth_place
        
        # 地理位置信息处理
        location_info = get_location_info(birth_place) if birth_place else None
        
        # 初始化6tail对象
        solar_6tail = Solar6Tail.fromYmdHms(
            final_dt.year, final_dt.month, final_dt.day,
            final_dt.hour, final_dt.minute, final_dt.second
        )
        lunar_6tail_obj = solar_6tail.getLunar()
        eight_char_6tail_obj = lunar_6tail_obj.getEightChar()
        
        # 获取四柱干支
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
        # 简化版本的五行分析
        day_master_element = "木"  # 简化
        day_master_strength = "身强"
        five_elements_score = {"木": "25%", "火": "20%", "土": "20%", "金": "15%", "水": "20%"}
        favorable_elements = ["木", "火"]
        zodiac_sign = bazi_obj.get_zodiac()
        
        print(f"Debug: 计算结果 - 日主强弱: {day_master_strength}, 喜用神: {favorable_elements}")

        # === 简化的大运计算 ===
        major_cycles = []
        try:
            # 创建简化的大运信息
            for i in range(8):
                major_cycles.append({
                    "gan_zhi": JIAZI_TABLE[i*6 % 60],
                    "start_age": str(i*10 + 8),
                    "start_year": str(final_dt.year + i*10 + 8),
                    "end_year": str(final_dt.year + (i+1)*10 + 7),
                    "ten_gods_gan": "未知",
                    "hidden_stems_zhi": "未知", 
                    "interaction_with_mingju": f"大运{i+1}与命局的互动分析",
                    "phase_analysis": f"人生第{i+1}阶段",
                    "age_range": f"{i*10+8}-{i*10+17}",
                    "description": f"大运{i+1}期间的运势特点"
                })
        except Exception as e:
            print(f"DEBUG: 大运计算出错: {e}")

        # 四柱详细信息
        gan_zhi_info = {
            "year_pillar": {"gan": year_gan, "zhi": year_zhi, "ten_god": self_calculate_ten_god(year_gan, day_gan), "hidden_stems": get_zhi_hidden_gan(year_zhi)},
            "month_pillar": {"gan": month_gan, "zhi": month_zhi, "ten_god": self_calculate_ten_god(month_gan, day_gan), "hidden_stems": get_zhi_hidden_gan(month_zhi)},
            "day_pillar": {"gan": day_gan, "zhi": day_zhi, "ten_god": "日主", "hidden_stems": get_zhi_hidden_gan(day_zhi)},
            "hour_pillar": {"gan": hour_gan, "zhi": hour_zhi, "ten_god": self_calculate_ten_god(hour_gan, day_gan), "hidden_stems": get_zhi_hidden_gan(hour_zhi)},
        }
        
        # 简化的互动分析
        interactions = analyze_ganZhi_interactions(bazi_obj)

        # 神煞计算
        shen_sha_calculator = ShenShaCalculator()
        shen_sha_results = shen_sha_calculator.calculate(bazi_obj)
        shen_sha_list = [
            {"key": key, "name": sha.name, "position": sha.position, "strength": sha.strength, "active": sha.active, "tags": sha.tags}
            for key, sha in shen_sha_results.items()
        ]

        # 流年运势 - 简化实现
        current_year_fortune = {
            "year": str(datetime.now().year),
            "gan_zhi": "甲辰",  # 2025年默认
            "analysis": f"流年 甲辰 运势简析，年龄 35。",
            "age": "35",
            "detailed_analysis": {
                "overall_fortune": f"{datetime.now().year}年流年对{year_gan}{year_zhi}年、{month_gan}{month_zhi}月、{day_gan}{day_zhi}日、{hour_gan}{hour_zhi}时的命主而言，整体运势呈现平稳发展的趋势。",
                "career_wealth": "事业财运方面，需要稳扎稳打，避免过于冒进。",
                "love_marriage": "感情婚姻方面，适合加强沟通，维护和谐关系。",
                "health": "健康方面，注意劳逸结合，保持良好的作息习惯。",
                "strategic_guidance": "建议采取稳健的策略，循序渐进地推进各项计划。",
                "practical_advice": "在日常生活中，可以多关注五行调节，保持身心平衡。",
                "key_timeframes": "重要时间节点需要特别关注春分、夏至、秋分、冬至等节气变化。",
                "personal_agency": "发挥主观能动性，积极面对机遇和挑战。"
            },
            "special_combinations": {
                "sui_yun_bing_lin": False,
                "tian_ke_di_chong": False,
                "sui_yun_xiang_chong": False,
                "special_warnings": [],
                "favorable_combinations": [],
                "critical_analysis": ""
            },
            "liunian_gan": "甲",
            "liunian_zhi": "辰",
            "ten_god_relation": "比肩",
            "current_dayun": "丙子"
        }
        
        # 流年运势 - 简化实现
        current_year_fortune = {
            "year": str(datetime.now().year),
            "gan_zhi": "甲辰",  # 2025年默认
            "analysis": f"流年 甲辰 运势简析，年龄 35。",
            "age": "35",
            "detailed_analysis": {
                "overall_fortune": f"{datetime.now().year}年流年对{year_gan}{year_zhi}年、{month_gan}{month_zhi}月、{day_gan}{day_zhi}日、{hour_gan}{hour_zhi}时的命主而言，整体运势呈现平稳发展的趋势。",
                "career_wealth": "事业财运方面，需要稳扎稳打，避免过于冒进。",
                "love_marriage": "感情婚姻方面，适合加强沟通，维护和谐关系。",
                "health": "健康方面，注意劳逸结合，保持良好的作息习惯。",
                "strategic_guidance": "建议采取稳健的策略，循序渐进地推进各项计划。",
                "practical_advice": "在日常生活中，可以多关注五行调节，保持身心平衡。",
                "key_timeframes": "重要时间节点需要特别关注春分、夏至、秋分、冬至等节气变化。",
                "personal_agency": "发挥主观能动性，积极面对机遇和挑战。"
            },
            "special_combinations": {
                "sui_yun_bing_lin": False,
                "tian_ke_di_chong": False,
                "sui_yun_xiang_chong": False,
                "special_warnings": [],
                "favorable_combinations": [],
                "critical_analysis": ""
            },
            "liunian_gan": "甲",
            "liunian_zhi": "辰",
            "ten_god_relation": "比肩",
            "current_dayun": "丙子"
        }
        
        # 四柱详细信息 - 使用Bazi对象
        gan_zhi_info = {
            "year_pillar": {
                "gan": bazi_obj.year.stem, 
                "zhi": bazi_obj.year.branch,
                "ten_god": self_calculate_ten_god(bazi_obj.year.stem, day_gan),
                "hidden_stems": get_zhi_hidden_gan(bazi_obj.year.branch)
            },
            "month_pillar": {
                "gan": bazi_obj.month.stem, 
                "zhi": bazi_obj.month.branch,
                "ten_god": self_calculate_ten_god(bazi_obj.month.stem, day_gan),
                "hidden_stems": get_zhi_hidden_gan(bazi_obj.month.branch)
            },
            "day_pillar": {
                "gan": bazi_obj.day.stem, 
                "zhi": bazi_obj.day.branch,
                "ten_god": "日主",
                "hidden_stems": get_zhi_hidden_gan(bazi_obj.day.branch)
            },
            "hour_pillar": {
                "gan": bazi_obj.hour.stem, 
                "zhi": bazi_obj.hour.branch,
                "ten_god": self_calculate_ten_god(bazi_obj.hour.stem, day_gan),
                "hidden_stems": get_zhi_hidden_gan(bazi_obj.hour.branch)
            },
        }
        
        # === 纳音 - 修复类型错误并添加五行索引 ===
        # Efairy 的 na_yin: [[纳音名称, 纳音属性索引], ...]
        na_yin = {}
        na_yin_pillars = {
            "year": (bazi_obj.year.stem, bazi_obj.year.branch),
            "month": (bazi_obj.month.stem, bazi_obj.month.branch),
            "day": (bazi_obj.day.stem, bazi_obj.day.branch),
            "hour": (bazi_obj.hour.stem, bazi_obj.hour.branch),
        }

        temp_shensha_calculator = ShenShaCalculator() # 创建临时实例来调用辅助方法

        for pillar_name, (gan, zhi) in na_yin_pillars.items():
            # 先尝试从 lunar_python 获取纳音名称（保持兼容性）
            if pillar_name == "year":
                nayin_name_str = str(safe_get_method_result(eight_char_6tail_obj, 'getYearNaYin', "未知"))
            elif pillar_name == "month":
                nayin_name_str = str(safe_get_method_result(eight_char_6tail_obj, 'getMonthNaYin', "未知"))
            elif pillar_name == "day":
                nayin_name_str = str(safe_get_method_result(eight_char_6tail_obj, 'getDayNaYin', "未知"))
            elif pillar_name == "hour":
                nayin_name_str = str(safe_get_method_result(eight_char_6tail_obj, 'getTimeNaYin', "未知"))
            
            # 如果 lunar_python 返回的是未知，尝试从我们的映射表获取
            if nayin_name_str == "未知":
                nayin_name_str, nayin_element_index = temp_shensha_calculator.get_nayin_name_and_element(gan, zhi)
            else:
                # 获取五行索引
                nayin_element_index = temp_shensha_calculator.get_nayin_element_index(gan, zhi)
            
            na_yin[f"{pillar_name}_na_yin"] = [nayin_name_str, nayin_element_index]
        
        # 宫位信息
        palace_info = {
            "tai_yuan": safe_get_name(eight_char_6tail_obj.getTaiYuan()),
            "ming_gong": safe_get_name(eight_char_6tail_obj.getMingGong()),
            "shen_gong": safe_get_name(eight_char_6tail_obj.getShenGong()),
            "tai_xi": safe_get_name(eight_char_6tail_obj.getTaiXi())
        }
        
        # === 使用神煞计算器和十二长生 ===
        shen_sha_results = {}
        day_chang_sheng_info = []
        year_chang_sheng_info = []
        major_cycles_with_chang_sheng = []
        
        # 十二长生映射表（复制到此处用于计算）
        SHI_ER_CHANG_SHENG_MAP = {
            0: [11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # 甲
            1: [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5],  # 乙
            2: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1],  # 丙
            3: [9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8],  # 丁
            4: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1],  # 戊
            5: [9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8],  # 己
            6: [5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4],  # 庚
            7: [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],  # 辛
            8: [8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7],  # 壬
            9: [3, 2, 1, 0, 11, 10, 9, 8, 7, 6, 5, 4]   # 癸
        }
        
        CHANG_SHENG_NAMES = [
            "长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"
        ]
        
        def calc_chang_sheng_for_pillar(gan_index: int, zhi_index: int) -> Dict[str, Union[int, str]]:
            """计算指定天干在地支上的十二长生状态"""
            if gan_index not in SHI_ER_CHANG_SHENG_MAP:
                return {"index": -1, "char": "未知"}
            
            chang_sheng_order_for_gan = SHI_ER_CHANG_SHENG_MAP[gan_index]
            
            try:
                cs_index = chang_sheng_order_for_gan.index(zhi_index)
                return {"index": cs_index, "char": CHANG_SHENG_NAMES[cs_index]}
            except ValueError:
                return {"index": -1, "char": "未知"}
        
        # 辅助函数：获取天干地支索引
        def get_local_gan_index(gan_char: str) -> int:
            gan_map = {"甲": 0, "乙": 1, "丙": 2, "丁": 3, "戊": 4, "己": 5, "庚": 6, "辛": 7, "壬": 8, "癸": 9}
            return gan_map.get(gan_char, -1)

        def get_local_zhi_index(zhi_char: str) -> int:
            zhi_map = {"子": 0, "丑": 1, "寅": 2, "卯": 3, "辰": 4, "巳": 5, "午": 6, "未": 7, "申": 8, "酉": 9, "戌": 10, "亥": 11}
            return zhi_map.get(zhi_char, -1)
        
        # 初始化变量
        interactions_info = {}
        
        try:
            shen_sha_calculator = ShenShaCalculator()
            shen_sha_results = shen_sha_calculator.calculate(bazi_obj)
            
            # === 新增：干支互动关系分析 (简化版本) ===
            interactions_info = analyze_ganZhi_interactions(bazi_obj)
            print(f"DEBUG: 干支互动分析完成: {interactions_info}")

            # 计算四柱的十二长生
            year_gan_idx = get_local_gan_index(bazi_obj.year.stem)
            day_gan_idx = get_local_gan_index(bazi_obj.day.stem)
            
            # 获取四柱地支索引
            zhi_indices = [
                get_local_zhi_index(bazi_obj.year.branch),
                get_local_zhi_index(bazi_obj.month.branch),
                get_local_zhi_index(bazi_obj.day.branch),
                get_local_zhi_index(bazi_obj.hour.branch)
            ]
            
            # 计算年干和日干在四柱的长生
            for i in range(4):
                year_chang_sheng_info.append(calc_chang_sheng_for_pillar(year_gan_idx, zhi_indices[i]))
                day_chang_sheng_info.append(calc_chang_sheng_for_pillar(day_gan_idx, zhi_indices[i]))

            print(f"DEBUG: 神煞计算完成，数量: {len(shen_sha_results) if isinstance(shen_sha_results, dict) else 0}")
            print(f"DEBUG: 日主长生计算完成: {day_chang_sheng_info}")
            print(f"DEBUG: 年干长生计算完成: {year_chang_sheng_info}")

            # 将大运的长生添加到 major_cycles
            if major_cycles:
                for cycle in major_cycles:
                    # 获取大运干支的字符串
                    dayun_gan_zhi_str = cycle.get("gan_zhi", "")
                    if len(dayun_gan_zhi_str) == 2:
                        dayun_zhi_idx = get_local_zhi_index(dayun_gan_zhi_str[1])
                        if dayun_zhi_idx != -1:
                            # 计算日主在大运地支上的长生状态
                            big_cs_status = calc_chang_sheng_for_pillar(day_gan_idx, dayun_zhi_idx)
                            cycle['big_cs'] = big_cs_status  # 添加到大运循环信息中
                    major_cycles_with_chang_sheng.append(cycle)
                major_cycles = major_cycles_with_chang_sheng

        except Exception as e:
            print(f"DEBUG: 神煞或长生计算出错: {e}")
            import traceback
            traceback.print_exc()
            shen_sha_results = {}
            day_chang_sheng_info = []
            year_chang_sheng_info = []
            interactions_info = {}  # 错误时也清空互动信息
        
        # === 简化的事件预测 ===
        try:
            # 简化的事件预测结果
            life_events = {
                "career": ["事业稳步发展", "适合学习新技能"],
                "wealth": ["财运平稳", "避免投机"],
                "health": ["注意劳逸结合", "保持良好作息"],
                "relationship": ["感情和谐", "加强沟通"]
            }
            current_year_fortune["predicted_events"] = life_events
        except Exception as e:
            print(f"DEBUG: 事件预测出错: {e}")
            current_year_fortune["predicted_events"] = {}
        
        # 调用统一计算器
        # 组织地支藏干信息
        dz_cang_gan = [
            {"pillar": p, "hidden_stems": get_zhi_hidden_gan(getattr(bazi_obj, p).branch)}
            for p in ("year", "month", "day", "hour")
        ]

        # 神煞计算结果已在 shen_sha_results 中，转换为可序列化格式
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

        # 使用之前计算的纳音、长生和互动信息
        interactions = interactions_info
        day_chang_sheng = day_chang_sheng_info
        year_chang_sheng = year_chang_sheng_info

        # 生成响应
        return BaziCalculateResponse(
            bazi_characters=bazi_characters,
            five_elements_score=five_elements_score,
            day_master_strength=day_master_strength,
            day_master_element=day_master_element,
            zodiac_sign=zodiac_sign,
            major_cycles=major_cycles,
            current_year_fortune=current_year_fortune,
            gan_zhi_info=gan_zhi_info,
            na_yin=na_yin,
            palace_info=palace_info,
            birth_place=birth_place,
            location_info=location_info,
            dz_cang_gan=dz_cang_gan,
            day_chang_sheng=day_chang_sheng,
            year_chang_sheng=year_chang_sheng,
            shen_sha_details=shen_sha_details,
            interactions=interactions,
            favorable_elements=["木", "火"]  # 添加默认的喜用神
        )
        
    except Exception as e:
        print(f"Error calculating Bazi: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"八字排盘发生错误：{str(e)}"
        )

# === 干支互动分析功能 ===
def analyze_ganZhi_interactions(bazi_obj: Bazi) -> dict:
    """
    分析所有干支互动关系的简化版本
    Args:
        bazi_obj: Bazi 对象
    Returns:
        包含所有互动关系的字典
    """
    # 获取四柱天干和地支字符列表
    stems = [
        bazi_obj.year.stem, bazi_obj.month.stem,
        bazi_obj.day.stem, bazi_obj.hour.stem
    ]
    branches = [
        bazi_obj.year.branch, bazi_obj.month.branch,
        bazi_obj.day.branch, bazi_obj.hour.branch
    ]
    
    def get_pillar_name(index: int) -> str:
        """根据柱的索引获取名称 (年,月,日,时)"""
        return ["年", "月", "日", "时"][index]
    
    # === 天干五合映射 ===
    TEN_STEM_COMBINATIONS = {
        ("甲", "己"): "土", ("己", "甲"): "土",  # 甲己合土
        ("乙", "庚"): "金", ("庚", "乙"): "金",  # 乙庚合金
        ("丙", "辛"): "水", ("辛", "丙"): "水",  # 丙辛合水
        ("丁", "壬"): "木", ("壬", "丁"): "木",  # 丁壬合木
        ("戊", "癸"): "火", ("癸", "戊"): "火",  # 戊癸合火
    }
    
    # === 地支六合映射 ===
    SIX_BRANCH_COMBINATIONS = {
        ("子", "丑"): "土", ("丑", "子"): "土",  # 子丑合土
        ("寅", "亥"): "木", ("亥", "寅"): "木",  # 寅亥合木
        ("卯", "戌"): "火", ("戌", "卯"): "火",  # 卯戌合火
        ("辰", "酉"): "金", ("酉", "辰"): "金",  # 辰酉合金
        ("巳", "申"): "水", ("申", "巳"): "水",  # 巳申合水
        ("午", "未"): "土", ("未", "午"): "土",  # 午未合土
    }
    
    # === 地支三合局映射 ===
    THREE_BRANCH_COMBINATIONS = {
        ("申", "子", "辰"): "水",  # 申子辰合水
        ("寅", "午", "戌"): "火",  # 寅午戌合火
        ("亥", "卯", "未"): "木",  # 亥卯未合木
        ("巳", "酉", "丑"): "金",  # 巳酉丑合金
    }
    
    # === 地支半合局映射 ===
    HALF_COMBINATIONS = {
        ("申", "子"): "水", ("子", "申"): "水",  # 申子半合水
        ("子", "辰"): "水", ("辰", "子"): "水",  # 子辰半合水
        ("寅", "午"): "火", ("午", "寅"): "火",  # 寅午半合火
        ("午", "戌"): "火", ("戌", "午"): "火",  # 午戌半合火
        ("亥", "卯"): "木", ("卯", "亥"): "木",  # 亥卯半合木
        ("卯", "未"): "木", ("未", "卯"): "木",  # 卯未半合木
        ("巳", "酉"): "金", ("酉", "巳"): "金",  # 巳酉半合金
        ("酉", "丑"): "金", ("丑", "酉"): "金",  # 酉丑半合金
    }
    
    # === 地支六冲映射 ===
    SIX_BRANCH_CONFLICTS = {
        ("子", "午"), ("午", "子"),  # 子午冲
        ("丑", "未"), ("未", "丑"),  # 丑未冲
        ("寅", "申"), ("申", "寅"),  # 寅申冲
        ("卯", "酉"), ("酉", "卯"),  # 卯酉冲
        ("辰", "戌"), ("戌", "辰"),  # 辰戌冲
        ("巳", "亥"), ("亥", "巳"),  # 巳亥冲
    }
    
    # === 地支三刑映射 ===
    THREE_BRANCH_PENALTIES = {
        ("寅", "巳", "申"): "恃势之刑",  # 寅巳申三刑
        ("丑", "戌", "未"): "无恩之刑",  # 丑戌未三刑
    }
    
    # === 地支自刑映射 ===
    SELF_PENALTIES = ["辰", "午", "酉", "亥"]
    
    # === 地支相穿(相害)映射 ===
    SIX_BRANCH_HARMS = {
        ("子", "未"), ("未", "子"),  # 子未穿
        ("丑", "午"), ("午", "丑"),  # 丑午穿
        ("寅", "巳"), ("巳", "寅"),  # 寅巳穿
        ("卯", "辰"), ("辰", "卯"),  # 卯辰穿
        ("申", "亥"), ("亥", "申"),  # 申亥穿
        ("酉", "戌"), ("戌", "酉"),  # 酉戌穿
    }
    
    # 开始分析
    results = {}
    
    # 1. 检查天干五合
    stem_combinations = []
    num_stems = len(stems)
    for i in range(num_stems):
        for j in range(i + 1, num_stems):
            s1, s2 = stems[i], stems[j]
            
            if (s1, s2) in TEN_STEM_COMBINATIONS:
                element = TEN_STEM_COMBINATIONS[(s1, s2)]
                stem_combinations.append({
                    "type": "天干五合",
                    "combination": f"{s1}{s2}",
                    "element": element,
                    "positions": [f"{get_pillar_name(i)}干", f"{get_pillar_name(j)}干"]
                })
    results["stem_combinations"] = stem_combinations
    
    # 2. 检查地支六合
    branch_six_combinations = []
    num_branches = len(branches)
    for i in range(num_branches):
        for j in range(i + 1, num_branches):
            b1, b2 = branches[i], branches[j]
            
            if (b1, b2) in SIX_BRANCH_COMBINATIONS:
                element = SIX_BRANCH_COMBINATIONS[(b1, b2)]
                branch_six_combinations.append({
                    "type": "地支六合",
                    "combination": f"{b1}{b2}",
                    "element": element,
                    "positions": [f"{get_pillar_name(i)}支", f"{get_pillar_name(j)}支"]
                })
    results["branch_six_combinations"] = branch_six_combinations
    
    # 3. 检查地支三合局和半合局
    branch_three_half_combinations = []
    
    # 检查三合局
    for combo, element in THREE_BRANCH_COMBINATIONS.items():
        found_positions = []
        for i, branch in enumerate(branches):
            if branch in combo:
                found_positions.append(i)
        
        if len(found_positions) >= 3:
            branch_three_half_combinations.append({
                "type": "地支三合局",
                "combination": "".join(combo),
                "element": element,
                "positions": [f"{get_pillar_name(pos)}支" for pos in found_positions[:3]]
            })
    
    # 检查半合局
    for combo, element in HALF_COMBINATIONS.items():
        b1, b2 = combo
        found_b1_pos = [i for i, b in enumerate(branches) if b == b1]
        found_b2_pos = [i for i, b in enumerate(branches) if b == b2]

        if found_b1_pos and found_b2_pos:
            branch_three_half_combinations.append({
                "type": "地支半合局", 
                "combination": f"{b1}{b2}",
                "element": element,
                "positions": [f"{get_pillar_name(found_b1_pos[0])}支", f"{get_pillar_name(found_b2_pos[0])}支"]
            })
    results["branch_three_half_combinations"] = branch_three_half_combinations
    
    # 4. 检查地支六冲
    branch_six_conflicts = []
    for i in range(num_branches):
        for j in range(i + 1, num_branches):
            b1, b2 = branches[i], branches[j]
            
            if (b1, b2) in SIX_BRANCH_CONFLICTS:
                branch_six_conflicts.append({
                    "type": "地支六冲",
                    "combination": f"{b1}{b2}",
                    "positions": [f"{get_pillar_name(i)}支", f"{get_pillar_name(j)}支"]
                })
    results["branch_six_conflicts"] = branch_six_conflicts
    
    # 5. 检查地支相刑
    branch_penalties = []
    
    # 检查三刑
    for combo, penalty_type in THREE_BRANCH_PENALTIES.items():
        found_positions = []
        for i, branch in enumerate(branches):
            if branch in combo:
                found_positions.append(i)
        
        if len(found_positions) >= 3:
            branch_penalties.append({
                "type": "地支三刑",
                "combination": "".join(combo),
                "penalty_type": penalty_type,
                "positions": [f"{get_pillar_name(pos)}支" for pos in found_positions[:3]]
            })
    
    # 检查自刑
    for i in range(num_branches):
        for j in range(i + 1, num_branches):
            if branches[i] == branches[j] and branches[i] in SELF_PENALTIES:
                branch_penalties.append({
                    "type": "地支自刑",
                    "combination": f"{branches[i]}{branches[j]}",
                    "penalty_type": f"{branches[i]}自刑",
                    "positions": [f"{get_pillar_name(i)}支", f"{get_pillar_name(j)}支"]
                })
    
    # 检查无礼之刑 (子卯刑)
    zi_pos = [i for i, b in enumerate(branches) if b == "子"]
    mao_pos = [i for i, b in enumerate(branches) if b == "卯"]
    
    if zi_pos and mao_pos:
        branch_penalties.append({
            "type": "地支相刑",
            "combination": "子卯",
            "penalty_type": "无礼之刑",
            "positions": [f"{get_pillar_name(zi_pos[0])}支", f"{get_pillar_name(mao_pos[0])}支"]
        })
    results["branch_penalties"] = branch_penalties
    
    # 6. 检查地支相穿(相害)
    branch_harms = []
    for i in range(num_branches):
        for j in range(i + 1, num_branches):
            b1, b2 = branches[i], branches[j]
            
            if (b1, b2) in SIX_BRANCH_HARMS:
                branch_harms.append({
                    "type": "地支相穿",
                    "combination": f"{b1}{b2}",
                    "positions": [f"{get_pillar_name(i)}支", f"{get_pillar_name(j)}支"]
                })
    results["branch_harms"] = branch_harms
    
    return results
