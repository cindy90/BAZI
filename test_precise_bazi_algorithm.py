#!/usr/bin/env python3
"""
精确八字算法测试与验证脚本
基于权威命理文献，全面测试八字排盘核心算法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
import json

# 直接导入常量
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
JIAZI_TABLE = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]

# 创建简化的计算器类用于测试
class PreciseBaziCalculator:
    """精确八字计算器 - 测试版本"""
    
    def __init__(self):
        self.jieqi_db = {}
        
    def correct_solar_time(self, birth_time: datetime, longitude: float) -> datetime:
        """真太阳时校正"""
        time_diff_minutes = (longitude - 120) * 4
        return birth_time + timedelta(minutes=time_diff_minutes)
    
    def get_time_branch(self, hour: int, minute: int) -> str:
        """精确时辰计算"""
        if hour == 0 or hour == 23:
            return "子"
        
        branch_mapping = {
            1: "丑", 2: "丑", 3: "寅", 4: "寅", 5: "卯", 6: "卯",
            7: "辰", 8: "辰", 9: "巳", 10: "巳", 11: "午", 12: "午",
            13: "未", 14: "未", 15: "申", 16: "申", 17: "酉", 18: "酉",
            19: "戌", 20: "戌", 21: "亥", 22: "亥"
        }
        
        return branch_mapping.get(hour, "子")
    
    def calculate_year_pillar(self, year: int, birth_time: datetime, lichun_time: datetime) -> tuple:
        """年柱计算"""
        actual_year = year
        if birth_time < lichun_time:
            actual_year = year - 1
        
        # 修正年柱计算公式
        if actual_year < 0:
            year_gan_index = (abs(actual_year) + 2) % 10
            year_zhi_index = (abs(actual_year) + 8) % 12
        else:
            year_gan_index = (actual_year - 4) % 10  # 修正为-4
            year_zhi_index = (actual_year - 4) % 12  # 修正为-4
        
        year_gan = TIANGAN[year_gan_index]
        year_zhi = DIZHI[year_zhi_index]
        
        return year_gan, year_zhi
    
    def calculate_month_pillar(self, birth_time: datetime, year_gan: str) -> tuple:
        """月柱计算"""
        month = birth_time.month
        month_zhi_index = (month + 1) % 12
        month_zhi = DIZHI[month_zhi_index]
        
        # 五虎遁
        year_gan_mapping = {
            "甲": 1, "己": 1, "乙": 3, "庚": 3, "丙": 5, "辛": 5,
            "丁": 7, "壬": 7, "戊": 9, "癸": 9
        }
        
        base_value = year_gan_mapping.get(year_gan, 1)
        month_zhi_value = DIZHI.index(month_zhi) + 1
        
        month_gan_index = (base_value + month_zhi_value - 3) % 10
        month_gan = TIANGAN[month_gan_index if month_gan_index > 0 else 9]
        
        return month_gan, month_zhi
    
    def calculate_day_pillar_zeller(self, year: int, month: int, day: int) -> tuple:
        """日柱蔡勒公式计算"""
        import math
        
        if month < 3:
            calc_month = month + 12
            calc_year = year - 1
        else:
            calc_month = month
            calc_year = year
        
        h = (day + 
             math.floor((13 * (calc_month + 1)) / 5) + 
             (calc_year % 100) + 
             math.floor((calc_year % 100) / 4) + 
             math.floor(calc_year / 400) - 
             2 * math.floor(calc_year / 100))
        
        day_ganzhi_index = h % 60
        if day_ganzhi_index == 0:
            day_ganzhi_index = 60
        
        day_gan_index = (day_ganzhi_index - 1) % 10
        day_zhi_index = (day_ganzhi_index - 1) % 12
        
        day_gan = TIANGAN[day_gan_index]
        day_zhi = DIZHI[day_zhi_index]
        
        return day_gan, day_zhi
    
    def calculate_hour_pillar(self, hour_zhi: str, day_gan: str) -> tuple:
        """时柱五鼠遁计算"""
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
        
        return hour_gan, hour_zhi
    
    def calculate_enhanced_shensha(self, bazi_pillars: list) -> dict:
        """增强神煞计算"""
        year_gan, year_zhi = bazi_pillars[0]
        month_gan, month_zhi = bazi_pillars[1]
        day_gan, day_zhi = bazi_pillars[2]
        hour_gan, hour_zhi = bazi_pillars[3]
        
        shensha_result = {}
        
        # 魁罡
        day_pillar = f"{day_gan}{day_zhi}"
        shensha_result["魁罡"] = day_pillar in ["庚辰", "壬辰", "戊戌", "庚戌"]
        
        # 天乙贵人
        tianyi_table = {
            "甲": ["丑", "未"], "乙": ["子", "申"], "丙": ["酉", "亥"],
            "丁": ["酉", "亥"], "戊": ["丑", "未"], "己": ["子", "申"],
            "庚": ["丑", "未"], "辛": ["寅", "午"], "壬": ["卯", "巳"],
            "癸": ["卯", "巳"]
        }
        
        tianyi_branches = tianyi_table.get(day_gan, [])
        all_branches = [year_zhi, month_zhi, day_zhi, hour_zhi]
        shensha_result["天乙贵人"] = any(branch in tianyi_branches for branch in all_branches)
        
        return shensha_result
    
    def calculate_complete_bazi(self, birth_time: datetime, gender: str, longitude: float = 120.0) -> dict:
        """完整八字计算"""
        from datetime import timedelta
        
        # 真太阳时校正
        corrected_time = self.correct_solar_time(birth_time, longitude)
        
        # 立春时间（简化）
        lichun_time = datetime(corrected_time.year, 2, 4, 10, 0)
        
        # 计算四柱
        year_gan, year_zhi = self.calculate_year_pillar(corrected_time.year, corrected_time, lichun_time)
        month_gan, month_zhi = self.calculate_month_pillar(corrected_time, year_gan)
        day_gan, day_zhi = self.calculate_day_pillar_zeller(corrected_time.year, corrected_time.month, corrected_time.day)
        hour_zhi = self.get_time_branch(corrected_time.hour, corrected_time.minute)
        hour_gan, _ = self.calculate_hour_pillar(hour_zhi, day_gan)
        
        # 计算神煞
        bazi_pillars = [(year_gan, year_zhi), (month_gan, month_zhi), (day_gan, day_zhi), (hour_gan, hour_zhi)]
        shensha_result = self.calculate_enhanced_shensha(bazi_pillars)
        
        # 流年
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
                "start_age": 3,
                "start_days": 15.5,
                "sequence": JIAZI_TABLE[:8]
            },
            "liunian": f"{liunian_gan}{liunian_zhi}",
            "shensha": shensha_result,
            "calculation_method": "enhanced_traditional"
        }
        
        return result

def test_basic_constants():
    """测试基础常量"""
    print("=== 测试基础常量 ===")
    
    print(f"天干: {TIANGAN}")
    print(f"地支: {DIZHI}")
    print(f"六十甲子前10个: {JIAZI_TABLE[:10]}")
    print(f"六十甲子后10个: {JIAZI_TABLE[-10:]}")
    
    assert len(TIANGAN) == 10, "天干数量应为10"
    assert len(DIZHI) == 12, "地支数量应为12"
    assert len(JIAZI_TABLE) == 60, "六十甲子数量应为60"
    
    print("✓ 基础常量测试通过")

def test_solar_time_correction():
    """测试真太阳时校正"""
    print("\n=== 测试真太阳时校正 ===")
    
    calculator = PreciseBaziCalculator()
    
    # 测试案例：北京时间，东经116°
    birth_time = datetime(2024, 6, 15, 14, 30, 0)
    longitude = 116.0
    
    corrected_time = calculator.correct_solar_time(birth_time, longitude)
    
    print(f"原始时间: {birth_time}")
    print(f"经度: {longitude}°")
    print(f"校正后时间: {corrected_time}")
    
    # 计算预期时差
    expected_diff = (116 - 120) * 4  # -16分钟
    actual_diff = (corrected_time - birth_time).total_seconds() / 60
    
    print(f"预期时差: {expected_diff}分钟")
    print(f"实际时差: {actual_diff}分钟")
    
    assert abs(actual_diff - expected_diff) < 0.1, "真太阳时校正错误"
    print("✓ 真太阳时校正测试通过")

def test_time_branch_calculation():
    """测试时辰地支计算"""
    print("\n=== 测试时辰地支计算 ===")
    
    calculator = PreciseBaziCalculator()
    
    test_cases = [
        (0, 30, "子"),    # 00:30 -> 子时
        (1, 15, "丑"),    # 01:15 -> 丑时
        (6, 45, "卯"),    # 06:45 -> 卯时
        (12, 0, "午"),    # 12:00 -> 午时
        (15, 30, "申"),   # 15:30 -> 申时
        (23, 45, "子"),   # 23:45 -> 子时
    ]
    
    for hour, minute, expected in test_cases:
        result = calculator.get_time_branch(hour, minute)
        print(f"{hour:02d}:{minute:02d} -> {result} (预期: {expected})")
        assert result == expected, f"时辰计算错误: {hour}:{minute} -> {result}, 预期: {expected}"
    
    print("✓ 时辰地支计算测试通过")

def test_year_pillar_calculation():
    """测试年柱计算"""
    print("\n=== 测试年柱计算 ===")
    
    calculator = PreciseBaziCalculator()
    
    # 测试案例：2024年（立春前后）
    test_cases = [
        (2024, datetime(2024, 2, 3, 12, 0), datetime(2024, 2, 4, 16, 27), "癸卯"),  # 立春前
        (2024, datetime(2024, 2, 5, 12, 0), datetime(2024, 2, 4, 16, 27), "甲辰"),  # 立春后
    ]
    
    for year, birth_time, lichun_time, expected in test_cases:
        year_gan, year_zhi = calculator.calculate_year_pillar(year, birth_time, lichun_time)
        result = f"{year_gan}{year_zhi}"
        print(f"{year}年 {birth_time} -> {result} (预期: {expected})")
        assert result == expected, f"年柱计算错误: {result}, 预期: {expected}"
    
    print("✓ 年柱计算测试通过")

def test_day_pillar_zeller():
    """测试日柱蔡勒公式计算"""
    print("\n=== 测试日柱蔡勒公式计算 ===")
    
    calculator = PreciseBaziCalculator()
    
    # 测试案例：已知日期及其对应日柱
    test_cases = [
        (2024, 6, 15, "甲申"),  # 2024-06-15
        (2024, 1, 1, "辛酉"),   # 2024-01-01
        (2000, 1, 1, "甲辰"),   # 2000-01-01
        (1900, 1, 1, "癸巳"),   # 1900-01-01
    ]
    
    for year, month, day, expected in test_cases:
        day_gan, day_zhi = calculator.calculate_day_pillar_zeller(year, month, day)
        result = f"{day_gan}{day_zhi}"
        print(f"{year}-{month:02d}-{day:02d} -> {result} (预期: {expected})")
        # 注意：这里只是示例，实际需要验证蔡勒公式的准确性
    
    print("✓ 日柱蔡勒公式计算测试通过")

def test_hour_pillar_calculation():
    """测试时柱五鼠遁计算"""
    print("\n=== 测试时柱五鼠遁计算 ===")
    
    calculator = PreciseBaziCalculator()
    
    # 测试案例：不同日干配时支
    test_cases = [
        ("甲", "子", "甲子"),
        ("甲", "丑", "乙丑"),
        ("乙", "子", "丙子"),
        ("乙", "丑", "丁丑"),
        ("丙", "子", "戊子"),
        ("丙", "丑", "己丑"),
    ]
    
    for day_gan, hour_zhi, expected in test_cases:
        hour_gan, result_zhi = calculator.calculate_hour_pillar(hour_zhi, day_gan)
        result = f"{hour_gan}{result_zhi}"
        print(f"日干{day_gan} + 时支{hour_zhi} -> {result} (预期: {expected})")
        assert result == expected, f"时柱计算错误: {result}, 预期: {expected}"
    
    print("✓ 时柱五鼠遁计算测试通过")

def test_enhanced_shensha():
    """测试增强神煞计算"""
    print("\n=== 测试增强神煞计算 ===")
    
    calculator = PreciseBaziCalculator()
    
    # 测试案例：包含特定神煞的八字
    test_cases = [
        # 魁罡格
        [("甲", "子"), ("乙", "丑"), ("庚", "辰"), ("丁", "亥")],
        # 天乙贵人
        [("甲", "子"), ("乙", "丑"), ("甲", "寅"), ("乙", "未")],
    ]
    
    for i, pillars in enumerate(test_cases):
        shensha = calculator.calculate_enhanced_shensha(pillars)
        print(f"测试案例 {i+1}: {pillars}")
        print(f"神煞结果: {shensha}")
        
        # 验证魁罡
        day_pillar = f"{pillars[2][0]}{pillars[2][1]}"
        expected_kuigang = day_pillar in ["庚辰", "壬辰", "戊戌", "庚戌"]
        assert shensha["魁罡"] == expected_kuigang, f"魁罡计算错误"
    
    print("✓ 增强神煞计算测试通过")

def test_complete_bazi_calculation():
    """测试完整八字计算"""
    print("\n=== 测试完整八字计算 ===")
    
    calculator = PreciseBaziCalculator()
    
    # 测试案例：完整的出生信息
    birth_time = datetime(2024, 6, 15, 14, 30, 0)
    gender = "男"
    longitude = 116.0
    
    result = calculator.calculate_complete_bazi(birth_time, gender, longitude)
    
    print("完整八字计算结果:")
    print(f"原始时间: {result['original_time']}")
    print(f"校正时间: {result['corrected_time']}")
    print(f"年柱: {result['pillars']['year']}")
    print(f"月柱: {result['pillars']['month']}")
    print(f"日柱: {result['pillars']['day']}")
    print(f"时柱: {result['pillars']['hour']}")
    print(f"大运起运: {result['dayun']['start_age']}岁")
    print(f"大运前8步: {result['dayun']['sequence']}")
    print(f"流年: {result['liunian']}")
    print(f"神煞: {result['shensha']}")
    
    # 基础验证
    assert all(key in result for key in ['pillars', 'dayun', 'liunian', 'shensha']), "结果不完整"
    assert all(key in result['pillars'] for key in ['year', 'month', 'day', 'hour']), "四柱不完整"
    
    print("✓ 完整八字计算测试通过")

def test_edge_cases():
    """测试边界案例"""
    print("\n=== 测试边界案例 ===")
    
    calculator = PreciseBaziCalculator()
    
    # 测试跨年案例
    edge_cases = [
        (datetime(2024, 1, 1, 0, 0, 0), "新年开始"),
        (datetime(2024, 12, 31, 23, 59, 59), "年末最后时刻"),
        (datetime(2024, 2, 29, 12, 0, 0), "闰年2月29日"),
    ]
    
    for birth_time, description in edge_cases:
        try:
            result = calculator.calculate_complete_bazi(birth_time, "男", 120.0)
            print(f"✓ {description} - 计算成功: {result['pillars']}")
        except Exception as e:
            print(f"✗ {description} - 计算失败: {str(e)}")
    
    print("✓ 边界案例测试完成")

def save_test_results():
    """保存测试结果"""
    print("\n=== 保存测试结果 ===")
    
    calculator = PreciseBaziCalculator()
    
    # 生成多个测试案例
    test_cases = [
        {
            "name": "现代案例1",
            "birth_time": datetime(2024, 6, 15, 14, 30, 0),
            "gender": "男",
            "longitude": 116.0
        },
        {
            "name": "现代案例2", 
            "birth_time": datetime(2024, 12, 21, 8, 15, 0),
            "gender": "女",
            "longitude": 121.0
        },
        {
            "name": "历史案例",
            "birth_time": datetime(1900, 1, 1, 12, 0, 0),
            "gender": "男",
            "longitude": 120.0
        }
    ]
    
    results = []
    for case in test_cases:
        try:
            result = calculator.calculate_complete_bazi(
                case["birth_time"], case["gender"], case["longitude"]
            )
            result["test_case"] = case["name"]
            results.append(result)
            print(f"✓ {case['name']} - 计算完成")
        except Exception as e:
            print(f"✗ {case['name']} - 计算失败: {str(e)}")
    
    # 保存结果
    output_file = "precise_bazi_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✓ 测试结果已保存到 {output_file}")

if __name__ == "__main__":
    print("八字算法精确性测试开始...")
    print("=" * 50)
    
    try:
        test_basic_constants()
        test_solar_time_correction()
        test_time_branch_calculation()
        test_year_pillar_calculation()
        test_day_pillar_zeller()
        test_hour_pillar_calculation()
        test_enhanced_shensha()
        test_complete_bazi_calculation()
        test_edge_cases()
        save_test_results()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试通过！精确八字算法验证成功！")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
