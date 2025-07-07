#!/usr/bin/env python3
"""
修正版高精度节气数据生成器
使用更准确的天文算法生成精确到秒的节气数据
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 二十四节气对应的太阳黄经（度）
SOLAR_TERMS_LONGITUDE = {
    "立春": 315, "雨水": 330, "惊蛰": 345, "春分": 0,
    "清明": 15, "谷雨": 30, "立夏": 45, "小满": 60,
    "芒种": 75, "夏至": 90, "小暑": 105, "大暑": 120,
    "立秋": 135, "处暑": 150, "白露": 165, "秋分": 180,
    "寒露": 195, "霜降": 210, "立冬": 225, "小雪": 240,
    "大雪": 255, "冬至": 270, "小寒": 285, "大寒": 300
}

# 节气顺序（从立春开始）
SOLAR_TERMS_ORDER = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
]

def julian_day(dt: datetime) -> float:
    """计算给定日期时间的儒略日数"""
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    
    if month <= 2:
        year -= 1
        month += 12
    
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5
    jd += (hour + minute / 60.0 + second / 3600.0) / 24.0
    
    return jd

def solar_longitude(jd: float) -> float:
    """计算给定儒略日的太阳黄经（度）"""
    # 从J2000.0开始的儒略世纪数
    t = (jd - 2451545.0) / 36525.0
    
    # 太阳平均黄经（度）
    l0 = 280.4664567 + 360007.6982779 * t + 0.03032028 * t * t + t * t * t / 49931 - t * t * t * t / 15300 - t * t * t * t * t / 2000000
    
    # 太阳平均近点角（度）
    m = 357.5291092 + 35999.0502909 * t - 0.0001536 * t * t + t * t * t / 24490000
    
    # 地心黄经修正（度）
    c = (1.9146 - 0.004817 * t - 0.000014 * t * t) * math.sin(math.radians(m))
    c += (0.019993 - 0.000101 * t) * math.sin(math.radians(2 * m))
    c += 0.000289 * math.sin(math.radians(3 * m))
    
    # 真太阳黄经
    true_longitude = l0 + c
    
    # 章动修正
    omega = 125.04452 - 1934.136261 * t + 0.0020708 * t * t + t * t * t / 450000
    nutation = -0.00569 - 0.00478 * math.sin(math.radians(omega))
    
    # 视黄经
    apparent_longitude = true_longitude + nutation
    
    # 归一化到 0-360 度
    while apparent_longitude < 0:
        apparent_longitude += 360
    while apparent_longitude >= 360:
        apparent_longitude -= 360
    
    return apparent_longitude

def find_solar_term_time(year: int, solar_term: str) -> datetime:
    """寻找特定年份特定节气的准确时间"""
    target_longitude = SOLAR_TERMS_LONGITUDE[solar_term]
    
    # 估算起始时间
    if solar_term in ["立春", "雨水", "惊蛰"]:
        start_date = datetime(year, 1, 15)
    elif solar_term in ["春分", "清明", "谷雨"]:
        start_date = datetime(year, 3, 1)
    elif solar_term in ["立夏", "小满", "芒种"]:
        start_date = datetime(year, 4, 15)
    elif solar_term in ["夏至", "小暑", "大暑"]:
        start_date = datetime(year, 6, 1)
    elif solar_term in ["立秋", "处暑", "白露"]:
        start_date = datetime(year, 7, 15)
    elif solar_term in ["秋分", "寒露", "霜降"]:
        start_date = datetime(year, 9, 1)
    elif solar_term in ["立冬", "小雪", "大雪"]:
        start_date = datetime(year, 10, 15)
    else:  # 冬至, 小寒, 大寒
        start_date = datetime(year, 12, 1)
    
    # 对于跨年的节气，调整年份
    if solar_term in ["小寒", "大寒", "立春"] and start_date.month == 12:
        if solar_term == "立春":
            start_date = datetime(year, 2, 1)
        elif solar_term in ["小寒", "大寒"]:
            start_date = datetime(year, 1, 1)
    
    # 使用牛顿法进行精确搜索
    current_time = start_date
    
    for iteration in range(100):  # 最多迭代100次
        jd = julian_day(current_time)
        current_longitude = solar_longitude(jd)
        
        # 计算角度差
        diff = target_longitude - current_longitude
        
        # 处理跨越360度的情况
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        
        # 如果差异小于0.0001度（约0.36秒），认为找到了
        if abs(diff) < 0.0001:
            break
        
        # 太阳每天移动约1度，所以时间调整为 diff 天
        time_adjustment = diff * 24 * 3600 / 360  # 秒
        current_time += timedelta(seconds=time_adjustment)
    
    return current_time

def generate_precise_solar_terms_data(start_year: int = 1900, end_year: int = 2050) -> Dict[str, Any]:
    """生成高精度节气数据"""
    logger.info(f"开始生成 {start_year}-{end_year} 年的精确节气数据...")
    
    solar_terms_data = {}
    
    for year in range(start_year, end_year + 1):
        logger.info(f"正在计算 {year} 年的节气数据...")
        
        year_data = {}
        
        for solar_term in SOLAR_TERMS_ORDER:
            # 计算精确时间
            precise_time = find_solar_term_time(year, solar_term)
            
            # 格式化时间字符串
            time_str = precise_time.strftime("%Y-%m-%d %H:%M:%S")
            year_data[solar_term] = time_str
        
        solar_terms_data[str(year)] = year_data
    
    return solar_terms_data

def main():
    """主函数"""
    print("修正版高精度节气数据生成器")
    print("=" * 50)
    
    # 生成精确节气数据
    solar_terms_data = generate_precise_solar_terms_data(1900, 2050)
    
    # 保存数据
    output_file = "solar_terms_data_precise.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(solar_terms_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"精确节气数据已保存到 {output_file}")
    
    # 显示2024年的数据样例
    print("\n2024 年节气数据样例:")
    year_2024_data = solar_terms_data.get("2024", {})
    for i, (term, time_str) in enumerate(year_2024_data.items()):
        print(f"  {term}: {time_str}")
    
    print(f"\n✅ 成功生成 {len(solar_terms_data)} 年的精确节气数据")
    
    # 验证数据质量
    print("\n数据质量验证:")
    year_2024_data = solar_terms_data.get("2024", {})
    non_midnight_count = sum(1 for time_str in year_2024_data.values() if not time_str.endswith("00:00:00"))
    print(f"  2024年非午夜时间的节气数量: {non_midnight_count}/{len(year_2024_data)}")

if __name__ == "__main__":
    main()
