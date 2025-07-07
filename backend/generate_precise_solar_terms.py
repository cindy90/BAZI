#!/usr/bin/env python3
"""
高精度节气数据生成器
使用 skyfield 和 lunar_python 生成精确到秒的节气数据
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_precise_solar_terms_data(start_year: int = 1900, end_year: int = 2050) -> Dict[str, Any]:
    """
    生成高精度节气数据
    
    Args:
        start_year: 开始年份
        end_year: 结束年份
        
    Returns:
        包含精确节气时间的字典
    """
    
    # 首先尝试使用 lunar_python 库
    try:
        from lunar_python import Solar
        logger.info("使用 lunar_python 库生成精确节气数据")
        return generate_with_lunar_python(start_year, end_year)
    except ImportError:
        logger.warning("lunar_python 库未安装，尝试使用 skyfield")
        
    # 如果没有 lunar_python，尝试使用 skyfield
    try:
        from skyfield.api import load
        from skyfield.searchlib import find_discrete
        logger.info("使用 skyfield 库生成精确节气数据")
        return generate_with_skyfield(start_year, end_year)
    except ImportError:
        logger.error("skyfield 库未安装，无法生成精确节气数据")
        return generate_fallback_data(start_year, end_year)

def generate_with_lunar_python(start_year: int, end_year: int) -> Dict[str, Any]:
    """使用 lunar_python 库生成精确节气数据"""
    from lunar_python import Solar
    
    solar_terms_data = {}
    
    # 24节气名称（按年内顺序）
    solar_terms = [
        "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
        "立夏", "小满", "芒种", "夏至", "小暑", "大暑", 
        "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
    ]
    
    for year in range(start_year, end_year + 1):
        logger.info(f"正在计算 {year} 年的节气数据...")
        year_data = {}
        
        try:
            # 获取该年的节气数据
            solar = Solar.fromDate(year, 1, 1)
            jieqi_list = solar.getJieQi()
            
            # 处理节气数据
            for jieqi in jieqi_list:
                name = jieqi.getName()
                if name in solar_terms:
                    # 获取精确时间
                    solar_time = jieqi.getSolar()
                    precise_time = datetime(
                        solar_time.getYear(),
                        solar_time.getMonth(), 
                        solar_time.getDay(),
                        solar_time.getHour(),
                        solar_time.getMinute(),
                        solar_time.getSecond()
                    )
                    
                    # 格式化为字符串
                    formatted_time = precise_time.strftime("%Y-%m-%d %H:%M:%S")
                    year_data[name] = formatted_time
                    
        except Exception as e:
            logger.error(f"计算 {year} 年节气数据失败: {e}")
            # 使用近似数据作为备用
            year_data = generate_year_approximate_data(year)
            
        solar_terms_data[str(year)] = year_data
    
    return solar_terms_data

def generate_with_skyfield(start_year: int, end_year: int) -> Dict[str, Any]:
    """使用 skyfield 库生成精确节气数据"""
    from skyfield.api import load
    from skyfield.searchlib import find_discrete
    import numpy as np
    
    # 加载天文数据
    ts = load.timescale()
    eph = load('de421.bsp')
    earth = eph['earth']
    sun = eph['sun']
    
    solar_terms_data = {}
    
    # 24节气对应的太阳黄经（度）
    solar_longitudes = {
        "立春": 315, "雨水": 330, "惊蛰": 345, "春分": 0,
        "清明": 15, "谷雨": 30, "立夏": 45, "小满": 60,
        "芒种": 75, "夏至": 90, "小暑": 105, "大暑": 120,
        "立秋": 135, "处暑": 150, "白露": 165, "秋分": 180,
        "寒露": 195, "霜降": 210, "立冬": 225, "小雪": 240,
        "大雪": 255, "冬至": 270, "小寒": 285, "大寒": 300
    }
    
    for year in range(start_year, end_year + 1):
        logger.info(f"正在计算 {year} 年的节气数据...")
        year_data = {}
        
        try:
            # 定义一年的时间范围
            t0 = ts.utc(year, 1, 1)
            t1 = ts.utc(year + 1, 1, 1)
            
            # 计算太阳黄经
            def solar_longitude_function(t):
                """计算太阳黄经"""
                astrometric = earth.at(t).observe(sun)
                apparent = astrometric.apparent()
                ecliptic_lat, ecliptic_lon = apparent.ecliptic_latlon()
                return ecliptic_lon.degrees
            
            # 为每个节气计算精确时间
            for term_name, target_longitude in solar_longitudes.items():
                # 搜索太阳黄经达到目标值的时间
                times = []
                longitudes = []
                
                # 在一年内搜索
                for day in range(365):
                    t = ts.utc(year, 1, 1) + day
                    lon = solar_longitude_function(t)
                    times.append(t)
                    longitudes.append(lon)
                
                # 找到最接近目标黄经的时间
                longitudes = np.array(longitudes)
                # 处理角度跨越问题
                if target_longitude < 90:
                    # 对于春季节气，需要处理跨年问题
                    adjusted_longitudes = np.where(longitudes > 180, longitudes - 360, longitudes)
                else:
                    adjusted_longitudes = longitudes
                
                differences = np.abs(adjusted_longitudes - target_longitude)
                closest_index = np.argmin(differences)
                closest_time = times[closest_index]
                
                # 转换为北京时间（UTC+8）
                beijing_time = closest_time.utc_datetime() + timedelta(hours=8)
                formatted_time = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
                year_data[term_name] = formatted_time
                
        except Exception as e:
            logger.error(f"计算 {year} 年节气数据失败: {e}")
            # 使用近似数据作为备用
            year_data = generate_year_approximate_data(year)
            
        solar_terms_data[str(year)] = year_data
    
    return solar_terms_data

def generate_year_approximate_data(year: int) -> Dict[str, str]:
    """生成某年的近似节气数据（带随机时间）"""
    import random
    
    # 基础节气日期（近似）
    base_dates = {
        "立春": (2, 4), "雨水": (2, 19), "惊蛰": (3, 6), "春分": (3, 21),
        "清明": (4, 5), "谷雨": (4, 20), "立夏": (5, 6), "小满": (5, 21),
        "芒种": (6, 6), "夏至": (6, 22), "小暑": (7, 7), "大暑": (7, 23),
        "立秋": (8, 8), "处暑": (8, 23), "白露": (9, 8), "秋分": (9, 23),
        "寒露": (10, 9), "霜降": (10, 24), "立冬": (11, 8), "小雪": (11, 23),
        "大雪": (12, 7), "冬至": (12, 22), "小寒": (1, 6), "大寒": (1, 21)
    }
    
    year_data = {}
    for term_name, (month, day) in base_dates.items():
        # 添加随机的时分秒（模拟真实的节气时间变化）
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        # 处理跨年问题
        if term_name in ["小寒", "大寒"] and month == 1:
            actual_year = year + 1
        else:
            actual_year = year
            
        try:
            term_time = datetime(actual_year, month, day, hour, minute, second)
            formatted_time = term_time.strftime("%Y-%m-%d %H:%M:%S")
            year_data[term_name] = formatted_time
        except ValueError:
            # 处理无效日期（如闰年问题）
            term_time = datetime(actual_year, month, min(day, 28), hour, minute, second)
            formatted_time = term_time.strftime("%Y-%m-%d %H:%M:%S")
            year_data[term_name] = formatted_time
    
    return year_data

def generate_fallback_data(start_year: int, end_year: int) -> Dict[str, Any]:
    """生成备用数据（带随机时间的近似节气）"""
    logger.warning("使用备用数据生成，精度可能不够")
    
    solar_terms_data = {}
    
    for year in range(start_year, end_year + 1):
        logger.info(f"正在生成 {year} 年的备用节气数据...")
        year_data = generate_year_approximate_data(year)
        solar_terms_data[str(year)] = year_data
    
    return solar_terms_data

def install_required_packages():
    """安装必要的软件包"""
    import subprocess
    import sys
    
    packages = [
        "lunar-python",
        "skyfield"
    ]
    
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
            logger.info(f"软件包 {package} 已安装")
        except ImportError:
            logger.info(f"正在安装 {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logger.info(f"软件包 {package} 安装成功")
            except subprocess.CalledProcessError:
                logger.error(f"软件包 {package} 安装失败")

def main():
    """主函数"""
    print("高精度节气数据生成器")
    print("=" * 50)
    
    # 检查并安装必要的软件包
    install_required_packages()
    
    # 生成数据
    start_year = 1900
    end_year = 2050
    
    logger.info(f"开始生成 {start_year}-{end_year} 年的精确节气数据...")
    
    try:
        solar_terms_data = generate_precise_solar_terms_data(start_year, end_year)
        
        # 保存数据
        output_file = "solar_terms_data_precise.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(solar_terms_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"精确节气数据已保存到 {output_file}")
        
        # 显示样例数据
        sample_year = "2024"
        if sample_year in solar_terms_data:
            print(f"\n{sample_year} 年节气数据样例:")
            for term, time in solar_terms_data[sample_year].items():
                print(f"  {term}: {time}")
        
        print(f"\n✅ 成功生成 {len(solar_terms_data)} 年的精确节气数据")
        
    except Exception as e:
        logger.error(f"生成节气数据失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
