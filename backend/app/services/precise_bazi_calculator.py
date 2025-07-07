"""
真太阳时校正模块 - 专注于经度时差和均时差校正
配合 lunar_python 使用，提供精确的时间校正功能
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging

logger = logging.getLogger(__name__)

class PreciseBaziCalculator:
    """精确时间校正器 - 专注于真太阳时校正"""
    
    def __init__(self):
        pass
    
    @staticmethod
    def correct_solar_time(birth_time: datetime, longitude: float) -> datetime:
        """真太阳时校正
        
        Args:
            birth_time: 出生时间（当地时间）
            longitude: 经度（东经为正，西经为负）
            
        Returns:
            校正后的真太阳时
        """
        # 1. 经度时差校正
        # 时差（分钟） = (当地经度 - 120) × 4
        longitude_diff_minutes = (longitude - 120) * 4
        
        # 2. 均时差校正（简化版本）
        # 均时差是地球椭圆轨道和地轴倾斜造成的时差
        equation_of_time_minutes = PreciseBaziCalculator._calculate_equation_of_time(birth_time)
        
        # 3. 总时差
        total_diff_minutes = longitude_diff_minutes + equation_of_time_minutes
        
        # 4. 应用校正
        corrected_time = birth_time + timedelta(minutes=total_diff_minutes)
        
        logger.info(f"真太阳时校正: 经度{longitude}°, 经度时差{longitude_diff_minutes:.1f}分钟, 均时差{equation_of_time_minutes:.1f}分钟")
        logger.info(f"原时间: {birth_time}, 校正后: {corrected_time}")
        
        return corrected_time
    
    @staticmethod
    def _calculate_equation_of_time(date: datetime) -> float:
        """计算均时差（分钟）
        
        Args:
            date: 日期时间
            
        Returns:
            均时差（分钟）
        """
        # 计算一年中的天数
        day_of_year = date.timetuple().tm_yday
        
        # 简化的均时差计算公式
        # 基于傅里叶级数近似
        B = 2 * math.pi * (day_of_year - 81) / 365
        
        # 均时差公式（分钟）
        E = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
        
        return E
    
    @staticmethod
    def get_precise_longitude(city_name: Optional[str] = None, province: Optional[str] = None) -> float:
        """获取城市精确经度
        
        Args:
            city_name: 城市名称
            province: 省份名称
            
        Returns:
            经度（东经为正）
        """
        # 主要城市经度数据库
        city_coordinates = {
            "北京": 116.4074,
            "上海": 121.4737,
            "广州": 113.2644,
            "深圳": 114.0579,
            "杭州": 120.1551,
            "南京": 118.7969,
            "武汉": 114.2619,
            "成都": 104.0668,
            "西安": 108.9402,
            "重庆": 106.5516,
            "天津": 117.2008,
            "沈阳": 123.4315,
            "长沙": 112.9388,
            "济南": 117.0009,
            "郑州": 113.6401,
            "哈尔滨": 126.6366,
            "昆明": 102.8329,
            "南昌": 115.8921,
            "福州": 119.3063,
            "石家庄": 114.5149,
            "太原": 112.5489,
            "呼和浩特": 111.7519,
            "长春": 125.3245,
            "南宁": 108.3669,
            "银川": 106.2309,
            "兰州": 103.8236,
            "西宁": 101.7782,
            "乌鲁木齐": 87.6177,
            "拉萨": 91.1322,
            "台北": 121.5598,
            "香港": 114.1694,
            "澳门": 113.5491
        }
        
        if city_name and city_name in city_coordinates:
            return city_coordinates[city_name]
        
        # 默认返回东八区标准经度
        return 120.0
    
    @staticmethod
    def calculate_precise_bazi_with_lunar(birth_time: datetime, longitude: Optional[float] = None, 
                                         city_name: Optional[str] = None) -> Dict[str, Any]:
        """
        使用真太阳时校正配合 lunar_python 计算精确八字
        
        Args:
            birth_time: 出生时间（当地时间）
            longitude: 经度（优先使用）
            city_name: 城市名称（用于获取经度）
            
        Returns:
            包含校正信息的八字数据
        """
        try:
            # 获取经度
            if longitude is None:
                longitude = PreciseBaziCalculator.get_precise_longitude(city_name)
            
            # 真太阳时校正
            corrected_time = PreciseBaziCalculator.correct_solar_time(birth_time, longitude)
            
            # 返回校正信息，让调用者使用 lunar_python 计算八字
            return {
                "original_time": birth_time,
                "corrected_time": corrected_time,
                "longitude": longitude,
                "longitude_diff_minutes": (longitude - 120) * 4,
                "equation_of_time_minutes": PreciseBaziCalculator._calculate_equation_of_time(birth_time),
                "city_name": city_name,
                "correction_applied": True
            }
            
        except Exception as e:
            logger.error(f"真太阳时校正失败: {e}")
            return {
                "original_time": birth_time,
                "corrected_time": birth_time,
                "longitude": longitude or 120.0,
                "longitude_diff_minutes": 0,
                "equation_of_time_minutes": 0,
                "city_name": city_name,
                "correction_applied": False,
                "error": str(e)
            }


# 便捷函数，用于与现有系统集成
def get_solar_time_correction(birth_time: datetime, city_name: Optional[str] = None, 
                             longitude: Optional[float] = None) -> Dict[str, Any]:
    """
    获取真太阳时校正信息
    
    Args:
        birth_time: 出生时间
        city_name: 城市名称
        longitude: 精确经度
        
    Returns:
        校正信息字典
    """
    return PreciseBaziCalculator.calculate_precise_bazi_with_lunar(
        birth_time, longitude, city_name
    )


def apply_solar_time_correction(birth_time: datetime, city_name: Optional[str] = None, 
                               longitude: Optional[float] = None) -> datetime:
    """
    应用真太阳时校正，返回校正后的时间
    
    Args:
        birth_time: 出生时间
        city_name: 城市名称
        longitude: 精确经度
        
    Returns:
        校正后的时间
    """
    if longitude is None:
        longitude = PreciseBaziCalculator.get_precise_longitude(city_name)
    
    return PreciseBaziCalculator.correct_solar_time(birth_time, longitude)


# 测试函数
def test_solar_time_correction():
    """测试真太阳时校正功能"""
    print("=== 真太阳时校正测试 ===")
    
    # 测试用例1：北京时间
    birth_time = datetime(1990, 5, 15, 14, 30, 0)
    print(f"原始时间: {birth_time}")
    
    # 北京校正
    beijing_corrected = apply_solar_time_correction(birth_time, "北京")
    print(f"北京校正后: {beijing_corrected}")
    
    # 上海校正
    shanghai_corrected = apply_solar_time_correction(birth_time, "上海")
    print(f"上海校正后: {shanghai_corrected}")
    
    # 新疆校正
    xinjiang_corrected = apply_solar_time_correction(birth_time, "乌鲁木齐")
    print(f"新疆校正后: {xinjiang_corrected}")
    
    # 获取详细校正信息
    correction_info = get_solar_time_correction(birth_time, "北京")
    print(f"\n=== 北京校正详情 ===")
    for key, value in correction_info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    test_solar_time_correction()
