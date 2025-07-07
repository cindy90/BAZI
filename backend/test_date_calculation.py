#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日期计算测试
"""

from datetime import datetime
from lunar_python import Lunar as Lunar6Tail, Solar as Solar6Tail

def test_date_calculation():
    """测试1940年11月27日的八字计算"""
    print("=== 1940年11月27日 8:00 八字计算测试 ===")
    
    # 测试时间
    test_time = datetime(1940, 11, 27, 8, 0, 0)
    print(f"测试时间: {test_time}")
    
    # 使用lunar_python计算
    solar_6tail = Solar6Tail.fromYmdHms(
        test_time.year, test_time.month, test_time.day,
        test_time.hour, test_time.minute, test_time.second
    )
    lunar_6tail_obj = solar_6tail.getLunar()
    eight_char_6tail_obj = lunar_6tail_obj.getEightChar()
    
    # 获取四柱干支
    year_gan = eight_char_6tail_obj.getYearGan()
    year_zhi = eight_char_6tail_obj.getYearZhi()
    month_gan = eight_char_6tail_obj.getMonthGan()
    month_zhi = eight_char_6tail_obj.getMonthZhi()
    day_gan = eight_char_6tail_obj.getDayGan()
    day_zhi = eight_char_6tail_obj.getDayZhi()
    hour_gan = eight_char_6tail_obj.getTimeGan()
    hour_zhi = eight_char_6tail_obj.getTimeZhi()
    
    print(f"年柱: {year_gan}{year_zhi}")
    print(f"月柱: {month_gan}{month_zhi}")
    print(f"日柱: {day_gan}{day_zhi}")
    print(f"时柱: {hour_gan}{hour_zhi}")
    print(f"八字: {year_gan}{year_zhi} {month_gan}{month_zhi} {day_gan}{day_zhi} {hour_gan}{hour_zhi}")
    
    # 金标准对比
    gold_standard = "庚辰 丁亥 丁酉 甲辰"
    system_result = f"{year_gan}{year_zhi} {month_gan}{month_zhi} {day_gan}{day_zhi} {hour_gan}{hour_zhi}"
    
    print(f"\n金标准: {gold_standard}")
    print(f"系统计算: {system_result}")
    print(f"匹配情况: {'✓ 匹配' if system_result == gold_standard else '❌ 不匹配'}")
    
    # 获取农历信息
    lunar_month = lunar_6tail_obj.getMonth()
    lunar_day = lunar_6tail_obj.getDay()
    lunar_year = lunar_6tail_obj.getYear()
    
    print(f"\n农历信息:")
    print(f"农历年: {lunar_year}")
    print(f"农历月: {lunar_month}")
    print(f"农历日: {lunar_day}")
    
    # 测试时区调整
    print(f"\n=== 时区调整测试 ===")
    
    # 旧金山时间 (PST -8小时)
    sf_time = datetime(1940, 11, 27, 8, 0, 0)  # 旧金山当地时间
    utc_time = datetime(1940, 11, 27, 16, 0, 0)  # 对应UTC时间
    beijing_time = datetime(1940, 11, 28, 0, 0, 0)  # 对应北京时间
    
    print(f"旧金山时间: {sf_time}")
    print(f"对应UTC时间: {utc_time}")
    print(f"对应北京时间: {beijing_time}")
    
    # 用UTC时间计算
    solar_utc = Solar6Tail.fromYmdHms(
        utc_time.year, utc_time.month, utc_time.day,
        utc_time.hour, utc_time.minute, utc_time.second
    )
    lunar_utc = solar_utc.getLunar()
    eight_char_utc = lunar_utc.getEightChar()
    
    utc_bazi = f"{eight_char_utc.getYearGan()}{eight_char_utc.getYearZhi()} {eight_char_utc.getMonthGan()}{eight_char_utc.getMonthZhi()} {eight_char_utc.getDayGan()}{eight_char_utc.getDayZhi()} {eight_char_utc.getTimeGan()}{eight_char_utc.getTimeZhi()}"
    
    print(f"UTC时间计算八字: {utc_bazi}")
    
    # 用北京时间计算
    solar_beijing = Solar6Tail.fromYmdHms(
        beijing_time.year, beijing_time.month, beijing_time.day,
        beijing_time.hour, beijing_time.minute, beijing_time.second
    )
    lunar_beijing = solar_beijing.getLunar()
    eight_char_beijing = lunar_beijing.getEightChar()
    
    beijing_bazi = f"{eight_char_beijing.getYearGan()}{eight_char_beijing.getYearZhi()} {eight_char_beijing.getMonthGan()}{eight_char_beijing.getMonthZhi()} {eight_char_beijing.getDayGan()}{eight_char_beijing.getDayZhi()} {eight_char_beijing.getTimeGan()}{eight_char_beijing.getTimeZhi()}"
    
    print(f"北京时间计算八字: {beijing_bazi}")
    
    # 分析哪种时间更接近金标准
    print(f"\n=== 对比分析 ===")
    print(f"金标准:     {gold_standard}")
    print(f"旧金山时间: {system_result}")
    print(f"UTC时间:    {utc_bazi}")
    print(f"北京时间:   {beijing_bazi}")
    
    if utc_bazi == gold_standard:
        print("✓ UTC时间与金标准匹配")
    elif beijing_bazi == gold_standard:
        print("✓ 北京时间与金标准匹配")
    else:
        print("❌ 没有时间版本与金标准匹配")

if __name__ == "__main__":
    test_date_calculation()
