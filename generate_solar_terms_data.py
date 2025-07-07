#!/usr/bin/env python3
"""
生成完整的节气数据文件
使用 lunar_python 库生成从 1900 年到 2050 年的完整节气数据
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "backend"))

def generate_solar_terms_data():
    """生成完整的节气数据"""
    print("开始生成节气数据...")
    
    try:
        # 导入 lunar_python
        from lunar_python import Solar as Solar6Tail
        
        # 24个节气的名称（按年份顺序）
        solar_terms = [
            "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
            "立夏", "小满", "芒种", "夏至", "小暑", "大暑", 
            "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
            "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
        ]
        
        # 生成数据的年份范围
        start_year = 1900
        end_year = 2050
        
        solar_terms_data = {}
        
        for year in range(start_year, end_year + 1):
            print(f"正在生成 {year} 年的节气数据...")
            
            year_data = {}
            
            # 生成该年份的所有节气
            for month in range(1, 13):
                for day in range(1, 32):
                    try:
                        # 创建Solar对象
                        solar = Solar6Tail.fromYmd(year, month, day)
                        lunar = solar.getLunar()
                        
                        # 获取节气
                        jie_qi = lunar.getJieQi()
                        if jie_qi and jie_qi in solar_terms:
                            # 格式化时间
                            time_str = f"{year}-{month:02d}-{day:02d} {solar.getHour():02d}:{solar.getMinute():02d}"
                            year_data[jie_qi] = time_str
                            
                    except Exception as e:
                        # 忽略无效日期（如2月30日）
                        continue
            
            # 处理跨年的小寒和大寒
            # 小寒和大寒通常在次年1月，需要特殊处理
            for month in [1, 2]:
                for day in range(1, 32):
                    try:
                        next_year = year + 1 if month <= 2 else year
                        solar = Solar6Tail.fromYmd(next_year, month, day)
                        lunar = solar.getLunar()
                        
                        jie_qi = lunar.getJieQi()
                        if jie_qi in ["小寒", "大寒"]:
                            # 这些节气属于前一年的节气周期
                            time_str = f"{next_year}-{month:02d}-{day:02d} {solar.getHour():02d}:{solar.getMinute():02d}"
                            year_data[jie_qi] = time_str
                            
                    except Exception as e:
                        continue
            
            # 确保每年都有24个节气
            if len(year_data) >= 20:  # 允许一些容错
                solar_terms_data[str(year)] = year_data
            else:
                print(f"警告: {year} 年只找到 {len(year_data)} 个节气")
        
        # 保存到JSON文件
        output_file = project_root / "backend" / "solar_terms_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(solar_terms_data, f, ensure_ascii=False, indent=2)
        
        print(f"节气数据已生成并保存到: {output_file}")
        print(f"生成了 {len(solar_terms_data)} 年的节气数据")
        
        # 验证几个关键年份
        test_years = [1900, 1950, 1980, 1985, 1988, 1990, 1992, 2000, 2024, 2050]
        for test_year in test_years:
            if str(test_year) in solar_terms_data:
                year_data = solar_terms_data[str(test_year)]
                print(f"验证 {test_year} 年: 包含 {len(year_data)} 个节气")
                # 显示立春和冬至作为示例
                if "立春" in year_data:
                    print(f"  立春: {year_data['立春']}")
                if "冬至" in year_data:
                    print(f"  冬至: {year_data['冬至']}")
            else:
                print(f"警告: 未找到 {test_year} 年的数据")
        
        return True
        
    except ImportError as e:
        print(f"错误: 无法导入 lunar_python 库: {e}")
        print("请确保已安装 lunar_python: pip install lunar-python")
        return False
    except Exception as e:
        print(f"生成节气数据时发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def alternative_generate_solar_terms_data():
    """备用方案：使用算法生成基础节气数据"""
    print("使用备用方案生成节气数据...")
    
    # 基础的节气计算（简化版）
    # 这个方案基于天文学算法，但精度较低
    
    solar_terms_data = {}
    
    # 节气在一年中的大致天数（简化计算）
    solar_terms_days = {
        "立春": 34,   # 2月4日左右
        "雨水": 49,   # 2月19日左右
        "惊蛰": 65,   # 3月5日左右
        "春分": 79,   # 3月20日左右
        "清明": 95,   # 4月4日左右
        "谷雨": 110,  # 4月19日左右
        "立夏": 125,  # 5月5日左右
        "小满": 141,  # 5月21日左右
        "芒种": 157,  # 6月6日左右
        "夏至": 172,  # 6月21日左右
        "小暑": 188,  # 7月7日左右
        "大暑": 204,  # 7月23日左右
        "立秋": 220,  # 8月8日左右
        "处暑": 235,  # 8月23日左右
        "白露": 251,  # 9月8日左右
        "秋分": 266,  # 9月23日左右
        "寒露": 282,  # 10月8日左右
        "霜降": 297,  # 10月23日左右
        "立冬": 313,  # 11月8日左右
        "小雪": 328,  # 11月23日左右
        "大雪": 343,  # 12月8日左右
        "冬至": 358,  # 12月23日左右
    }
    
    # 生成 1900-2050 年的数据
    for year in range(1900, 2051):
        if year % 10 == 0:
            print(f"正在生成 {year} 年的节气数据...")
            
        year_data = {}
        
        # 判断是否为闰年
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        
        for term, day_of_year in solar_terms_days.items():
            # 简单的日期计算
            try:
                start_date = datetime(year, 1, 1)
                term_date = start_date + timedelta(days=day_of_year - 1)
                
                # 调整闰年
                if is_leap and day_of_year > 59:  # 3月1日之后
                    term_date = term_date + timedelta(days=1)
                
                # 格式化为字符串
                time_str = term_date.strftime("%Y-%m-%d %H:%M")
                year_data[term] = time_str
                
            except Exception as e:
                continue
        
        # 处理跨年的小寒和大寒
        try:
            # 小寒（大约1月5日）
            xiaopan_date = datetime(year + 1, 1, 5, 12, 0)
            year_data["小寒"] = xiaopan_date.strftime("%Y-%m-%d %H:%M")
            
            # 大寒（大约1月20日）
            dahan_date = datetime(year + 1, 1, 20, 12, 0)
            year_data["大寒"] = dahan_date.strftime("%Y-%m-%d %H:%M")
            
        except Exception as e:
            pass
        
        solar_terms_data[str(year)] = year_data
    
    # 保存到JSON文件
    output_file = project_root / "backend" / "solar_terms_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(solar_terms_data, f, ensure_ascii=False, indent=2)
    
    print(f"备用节气数据已生成并保存到: {output_file}")
    print(f"生成了 {len(solar_terms_data)} 年的节气数据")
    
    return True


if __name__ == "__main__":
    print("节气数据生成器")
    print("=" * 50)
    
    # 首先尝试使用 lunar_python 生成精确数据
    success = generate_solar_terms_data()
    
    if not success:
        print("\n尝试使用备用方案...")
        success = alternative_generate_solar_terms_data()
    
    if success:
        print("\n✅ 节气数据生成完成！")
        print("现在可以重新运行八字计算测试了。")
    else:
        print("\n❌ 节气数据生成失败！")
        print("请检查错误信息并重试。")
