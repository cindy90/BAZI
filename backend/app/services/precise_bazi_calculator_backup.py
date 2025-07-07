"""
真太阳时校正模块 - 专注于经度时差和均时差校正
配合 lunar_python 使用，提供精确的时间校正功能
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
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
    def get_precise_longitude(city_name: str = None, province: str = None) -> float:
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
    def calculate_precise_bazi_with_lunar(birth_time: datetime, longitude: float = None, 
                                         city_name: str = None) -> Dict[str, any]:
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
def get_solar_time_correction(birth_time: datetime, city_name: str = None, 
                             longitude: float = None) -> Dict[str, any]:
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


def apply_solar_time_correction(birth_time: datetime, city_name: str = None, 
                               longitude: float = None) -> datetime:
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
    def get_precise_longitude(city_name: str = None, province: str = None) -> float:
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
            minute: 分钟
            
        Returns:
            对应的地支
        """
        # 时辰划分表（23:00-00:59为子时等）
        time_ranges = [
            (23, 0, 59, "子"),   # 23:00-00:59
            (1, 0, 59, "丑"),    # 01:00-02:59
            (3, 0, 59, "寅"),    # 03:00-04:59
            (5, 0, 59, "卯"),    # 05:00-06:59
            (7, 0, 59, "辰"),    # 07:00-08:59
            (9, 0, 59, "巳"),    # 09:00-10:59
            (11, 0, 59, "午"),   # 11:00-12:59
            (13, 0, 59, "未"),   # 13:00-14:59
            (15, 0, 59, "申"),   # 15:00-16:59
            (17, 0, 59, "酉"),   # 17:00-18:59
            (19, 0, 59, "戌"),   # 19:00-20:59
            (21, 0, 59, "亥")    # 21:00-22:59
        ]
        
        # 特殊处理子时（跨日）
        if hour == 0:
            return "子"
        elif hour == 23:
            return "子"
        
        # 其他时辰
        for start_hour, start_min, end_min, branch in time_ranges:
            if start_hour <= hour <= start_hour + 1:
                if hour == start_hour and minute >= start_min:
                    return branch
                elif hour == start_hour + 1 and minute <= end_min:
                    return branch
        
        # 默认处理
        branch_mapping = {
            1: "丑", 2: "丑", 3: "寅", 4: "寅", 5: "卯", 6: "卯",
            7: "辰", 8: "辰", 9: "巳", 10: "巳", 11: "午", 12: "午",
            13: "未", 14: "未", 15: "申", 16: "申", 17: "酉", 18: "酉",
            19: "戌", 20: "戌", 21: "亥", 22: "亥"
        }
        
        return branch_mapping.get(hour, "子")
    
    def calculate_year_pillar(self, year: int, birth_time: datetime, lichun_time: datetime) -> Tuple[str, str]:
        """年柱计算（立春分界）
        
        Args:
            year: 年份
            birth_time: 出生时间
            lichun_time: 立春精确时间
            
        Returns:
            (年干, 年支)
        """
        # 判断是否在立春之前
        actual_year = year
        if birth_time < lichun_time:
            actual_year = year - 1
            logger.info(f"出生时间在立春前，年柱使用{actual_year}年")
        
        # 年柱计算公式（修正版）
        if actual_year < 0:  # 公元前年份
            year_gan_index = (abs(actual_year) + 2) % 10
            year_zhi_index = (abs(actual_year) + 8) % 12
        else:
            year_gan_index = (actual_year - 4) % 10  # 修正为-4
            year_zhi_index = (actual_year - 4) % 12  # 修正为-4
        
        # 转换为实际干支
        year_gan = TIANGAN[year_gan_index]
        year_zhi = DIZHI[year_zhi_index]
        
        logger.info(f"年柱计算: {actual_year}年 -> {year_gan}{year_zhi}")
        
        return year_gan, year_zhi
    
    def calculate_month_pillar(self, birth_time: datetime, year_gan: str) -> Tuple[str, str]:
        """月柱计算（精确节气分界）
        
        Args:
            birth_time: 出生时间
            year_gan: 年干
            
        Returns:
            (月干, 月支)
        """
        # 月支判定（基于节气）
        month = birth_time.month
        
        # 默认月支序数
        month_zhi_index = (month + 1) % 12
        
        # TODO: 这里需要加入精确节气时间判断
        # if 出生时间 < 当月节气精确时间:
        #     month_zhi_index = (month_zhi_index - 2) % 12 + 1
        
        month_zhi = DIZHI[month_zhi_index]
        
        # 月干五虎遁公式
        year_gan_mapping = {
            "甲": 1, "己": 1,   # 甲/己→丙(1)
            "乙": 3, "庚": 3,   # 乙/庚→戊(3)
            "丙": 5, "辛": 5,   # 丙/辛→庚(5)
            "丁": 7, "壬": 7,   # 丁/壬→壬(7)
            "戊": 9, "癸": 9    # 戊/癸→甲(9)
        }
        
        base_value = year_gan_mapping.get(year_gan, 1)
        month_zhi_value = DIZHI.index(month_zhi) + 1
        
        month_gan_index = (base_value + month_zhi_value - 3) % 10
        month_gan = TIANGAN[month_gan_index if month_gan_index > 0 else 9]
        
        logger.info(f"月柱计算: {month}月 -> {month_gan}{month_zhi}")
        
        return month_gan, month_zhi
    
    def calculate_day_pillar_zeller(self, year: int, month: int, day: int) -> Tuple[str, str]:
        """日柱计算（蔡勒公式）
        
        Args:
            year: 年
            month: 月
            day: 日
            
        Returns:
            (日干, 日支)
        """
        # 蔡勒公式变体
        if month < 3:
            calc_month = month + 12
            calc_year = year - 1
        else:
            calc_month = month
            calc_year = year
        
        # 蔡勒公式
        h = (day + 
             math.floor((13 * (calc_month + 1)) / 5) + 
             (calc_year % 100) + 
             math.floor((calc_year % 100) / 4) + 
             math.floor(calc_year / 400) - 
             2 * math.floor(calc_year / 100))
        
        # 计算干支序数
        day_ganzhi_index = h % 60
        if day_ganzhi_index == 0:
            day_ganzhi_index = 60  # 癸亥
        
        # 转换为天干地支
        day_gan_index = (day_ganzhi_index - 1) % 10
        day_zhi_index = (day_ganzhi_index - 1) % 12
        
        day_gan = TIANGAN[day_gan_index]
        day_zhi = DIZHI[day_zhi_index]
        
        logger.info(f"日柱蔡勒公式计算: {year}-{month}-{day} -> {day_gan}{day_zhi}")
        
        return day_gan, day_zhi
    
    def calculate_hour_pillar(self, hour_zhi: str, day_gan: str) -> Tuple[str, str]:
        """时柱计算（五鼠遁）
        
        Args:
            hour_zhi: 时支
            day_gan: 日干
            
        Returns:
            (时干, 时支)
        """
        # 五鼠遁公式：以甲、己日见甲子时为例
        day_gan_mapping = {
            "甲": 0, "己": 0,  # 甲己日从甲子时开始
            "乙": 2, "庚": 2,  # 乙庚日从丙子时开始
            "丙": 4, "辛": 4,  # 丙辛日从戊子时开始
            "丁": 6, "壬": 6,  # 丁壬日从庚子时开始
            "戊": 8, "癸": 8   # 戊癸日从壬子时开始
        }
        
        base_gan_index = day_gan_mapping.get(day_gan, 0)
        hour_zhi_index = DIZHI.index(hour_zhi)
        
        # 计算时干索引
        hour_gan_index = (base_gan_index + hour_zhi_index) % 10
        hour_gan = TIANGAN[hour_gan_index]
        
        logger.info(f"时柱五鼠遁计算: 日干{day_gan} + 时支{hour_zhi} -> {hour_gan}{hour_zhi}")
        
        return hour_gan, hour_zhi
    
    def calculate_dayun_precise(self, birth_time: datetime, gender: str, year_gan: str, 
                               month_pillar: str) -> Tuple[int, List[str], float]:
        """精确大运计算
        
        Args:
            birth_time: 出生时间
            gender: 性别
            year_gan: 年干
            month_pillar: 月柱
            
        Returns:
            (起运年龄, 大运列表, 起运天数)
        """
        # 1. 判断阴阳年
        yang_gans = ["甲", "丙", "戊", "庚", "壬"]
        is_yang_year = year_gan in yang_gans
        
        # 2. 判断顺逆排
        is_male = (gender == "男")
        is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
        
        # 3. 计算到节气的距离（简化版，实际需要精确节气数据）
        # TODO: 实现精确节气查询
        
        # 临时使用估算值
        start_days = 15.5  # 假设距离节气15.5天
        start_months = start_days * 4  # 1天=4个月
        start_age = int(start_months / 12)
        
        # 4. 生成大运干支序列
        try:
            month_index = JIAZI_TABLE.index(month_pillar)
        except ValueError:
            month_index = 0
        
        dayun_list = []
        for i in range(10):
            if is_forward:
                pillar_index = (month_index + i + 1) % 60
            else:
                pillar_index = (month_index - i - 1 + 60) % 60
            dayun_list.append(JIAZI_TABLE[pillar_index])
        
        logger.info(f"大运计算: {'顺排' if is_forward else '逆排'}, 起运{start_age}岁")
        
        return start_age, dayun_list, start_days
    
    def calculate_enhanced_shensha(self, bazi_pillars: List[Tuple[str, str]]) -> Dict[str, bool]:
        """增强神煞计算
        
        Args:
            bazi_pillars: [(年干,年支), (月干,月支), (日干,日支), (时干,时支)]
            
        Returns:
            神煞字典
        """
        year_gan, year_zhi = bazi_pillars[0]
        month_gan, month_zhi = bazi_pillars[1]
        day_gan, day_zhi = bazi_pillars[2]
        hour_gan, hour_zhi = bazi_pillars[3]
        
        shensha_result = {}
        
        # 1. 魁罡（强化）
        day_pillar = f"{day_gan}{day_zhi}"
        shensha_result["魁罡"] = day_pillar in ["庚辰", "壬辰", "戊戌", "庚戌"]
        
        # 2. 天乙贵人
        tianyi_table = {
            "甲": ["丑", "未"], "乙": ["子", "申"], "丙": ["酉", "亥"],
            "丁": ["酉", "亥"], "戊": ["丑", "未"], "己": ["子", "申"],
            "庚": ["丑", "未"], "辛": ["寅", "午"], "壬": ["卯", "巳"],
            "癸": ["卯", "巳"]
        }
        
        tianyi_branches = tianyi_table.get(day_gan, [])
        all_branches = [year_zhi, month_zhi, day_zhi, hour_zhi]
        shensha_result["天乙贵人"] = any(branch in tianyi_branches for branch in all_branches)
        
        # 3. 将星（年支/日支查）
        jiangxing_table = {
            "寅": "午", "午": "午", "戌": "午",  # 寅午戌见午
            "申": "子", "子": "子", "辰": "子",  # 申子辰见子
            "巳": "酉", "酉": "酉", "丑": "酉",  # 巳酉丑见酉
            "亥": "卯", "卯": "卯", "未": "卯"   # 亥卯未见卯
        }
        
        jiangxing_position = jiangxing_table.get(year_zhi)
        shensha_result["将星"] = jiangxing_position in all_branches if jiangxing_position else False
        
        # 4. 劫煞（三合绝位）
        jiesha_table = {
            "申": "巳", "子": "巳", "辰": "巳",  # 申子辰见巳
            "寅": "亥", "午": "亥", "戌": "亥",  # 寅午戌见亥
            "巳": "寅", "酉": "寅", "丑": "寅",  # 巳酉丑见寅
            "亥": "申", "卯": "申", "未": "申"   # 亥卯未见申
        }
        
        jiesha_position = jiesha_table.get(day_zhi)
        shensha_result["劫煞"] = jiesha_position in all_branches if jiesha_position else False
        
        logger.info(f"神煞计算结果: {shensha_result}")
        
        return shensha_result
    
    def calculate_complete_bazi(self, birth_time: datetime, gender: str, 
                               longitude: float = 120.0) -> Dict:
        """完整八字计算
        
        Args:
            birth_time: 出生时间
            gender: 性别
            longitude: 经度（用于真太阳时校正）
            
        Returns:
            完整的八字数据
        """
        # 1. 真太阳时校正
        corrected_time = self.correct_solar_time(birth_time, longitude)
        
        # 2. 立春时间（简化，实际需要精确数据）
        lichun_time = datetime(corrected_time.year, 2, 4, 10, 0)  # 简化处理
        
        # 3. 计算四柱
        year_gan, year_zhi = self.calculate_year_pillar(
            corrected_time.year, corrected_time, lichun_time
        )
        
        month_gan, month_zhi = self.calculate_month_pillar(corrected_time, year_gan)
        
        day_gan, day_zhi = self.calculate_day_pillar_zeller(
            corrected_time.year, corrected_time.month, corrected_time.day
        )
        
        hour_zhi = self.get_time_branch(corrected_time.hour, corrected_time.minute)
        hour_gan, _ = self.calculate_hour_pillar(hour_zhi, day_gan)
        
        # 4. 计算大运
        month_pillar = f"{month_gan}{month_zhi}"
        start_age, dayun_list, start_days = self.calculate_dayun_precise(
            corrected_time, gender, year_gan, month_pillar
        )
        
        # 5. 计算神煞
        bazi_pillars = [
            (year_gan, year_zhi),
            (month_gan, month_zhi),
            (day_gan, day_zhi),
            (hour_gan, hour_zhi)
        ]
        shensha_result = self.calculate_enhanced_shensha(bazi_pillars)
        
        # 6. 流年计算
        current_year = datetime.now().year
        liunian_gan_index = (current_year - 3) % 10
        liunian_zhi_index = (current_year - 3) % 12
        liunian_gan = TIANGAN[liunian_gan_index if liunian_gan_index > 0 else 9]
        liunian_zhi = DIZHI[liunian_zhi_index if liunian_zhi_index > 0 else 11]
        
        result = {
            "original_time": birth_time,
            "corrected_time": corrected_time,
            "longitude": longitude,
            "pillars": {
                "year": f"{year_gan}{year_zhi}",
                "month": f"{month_gan}{month_zhi}",
                "day": f"{day_gan}{day_zhi}",
                "hour": f"{hour_gan}{hour_zhi}"
            },
            "dayun": {
                "start_age": start_age,
                "start_days": start_days,
                "sequence": dayun_list[:8]
            },
            "liunian": f"{liunian_gan}{liunian_zhi}",
            "shensha": shensha_result,
            "calculation_method": "enhanced_traditional"
        }
        
        logger.info(f"完整八字计算完成: {result['pillars']}")
        
        return result
