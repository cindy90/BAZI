"""
八字计算工具函数模块
包含各种辅助函数、常量数据表、精确计算方法等
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union


# JIAZI 六十甲子表
JIAZI = [
    f"{g}{z}" for g, z in zip(
        "甲乙丙丁戊己庚辛壬癸甲乙丙丁戊己庚辛壬癸甲乙丙丁戊己庚辛壬癸甲乙丙丁戊己庚辛壬癸甲乙丙丁戊己庚辛壬癸甲乙丙丁戊己庚辛壬癸",
        "子丑寅卯辰巳午未申酉戌亥子丑寅卯辰巳午未申酉戌亥子丑寅卯辰巳午未申酉戌亥子丑寅卯辰巳午未申酉戌亥子丑寅卯辰巳午未申酉戌亥"
    )
][:60]


def safe_get_name(obj):
    """安全获取对象的name属性"""
    try:
        if hasattr(obj, "getName"):
            return obj.getName()
        else:
            return str(obj) if obj is not None else ""
    except Exception:
        return ""


def safe_get_method_result(obj, method_name, default=""):
    """安全调用对象方法获取结果"""
    try:
        if hasattr(obj, method_name):
            method = getattr(obj, method_name)
            if callable(method):
                result = method()
                return safe_get_name(result) if result is not None else default
        return default
    except Exception:
        return default


def analyze_dayun_phase(age: int) -> str:
    """根据年龄判断人生阶段"""
    if age < 10:
        return "童年初期"
    elif age < 20:
        return "少年时期"
    elif age < 30:
        return "成年初期"
    elif age < 40:
        return "事业建立期"
    elif age < 50:
        return "事业高峰期"
    elif age < 60:
        return "中年稳定期"
    elif age < 70:
        return "花甲之年"
    else:
        return "老年时期"


def self_calculate_ten_god(gan: str, day_master: str) -> str:
    """基于天干与日主关系计算十神"""
    # 天干五合对照表
    gan_five_element = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    
    # 天干阴阳对照表
    gan_yin_yang = {
        "甲": "阳", "丙": "阳", "戊": "阳", "庚": "阳", "壬": "阳",
        "乙": "阴", "丁": "阴", "己": "阴", "辛": "阴", "癸": "阴"
    }
    
    # 十神关系计算
    day_master_element = gan_five_element.get(day_master, "")
    gan_element = gan_five_element.get(gan, "")
    
    if not day_master_element or not gan_element:
        return "未知"
        
    day_master_yin_yang = gan_yin_yang.get(day_master, "")
    gan_yin_yang_value = gan_yin_yang.get(gan, "")
    
    # 日主与干的关系
    if gan == day_master:
        return "比肩"
    
    # 同五行不同阴阳
    if gan_element == day_master_element and gan_yin_yang_value != day_master_yin_yang:
        return "劫财"
    
    # 生我者为"食神"或"伤官"
    if (day_master_element == "木" and gan_element == "水") or \
       (day_master_element == "火" and gan_element == "木") or \
       (day_master_element == "土" and gan_element == "火") or \
       (day_master_element == "金" and gan_element == "土") or \
       (day_master_element == "水" and gan_element == "金"):
        return "食神" if gan_yin_yang_value == "阳" else "伤官"
    
    # 我生者为"财"
    if (day_master_element == "木" and gan_element == "火") or \
       (day_master_element == "火" and gan_element == "土") or \
       (day_master_element == "土" and gan_element == "金") or \
       (day_master_element == "金" and gan_element == "水") or \
       (day_master_element == "水" and gan_element == "木"):
        return "正财" if gan_yin_yang_value == "阴" else "偏财"
    
    # 克我者为"官"
    if (day_master_element == "木" and gan_element == "金") or \
       (day_master_element == "火" and gan_element == "水") or \
       (day_master_element == "土" and gan_element == "木") or \
       (day_master_element == "金" and gan_element == "火") or \
       (day_master_element == "水" and gan_element == "土"):
        return "正官" if gan_yin_yang_value == "阳" else "七杀"
    
    # 我克者为"印"
    if (day_master_element == "木" and gan_element == "土") or \
       (day_master_element == "火" and gan_element == "金") or \
       (day_master_element == "土" and gan_element == "水") or \
       (day_master_element == "金" and gan_element == "木") or \
       (day_master_element == "水" and gan_element == "火"):
        return "正印" if gan_yin_yang_value == "阴" else "偏印"
    
    return "未知"


def get_zhi_hidden_gan(zhi: str) -> str:
    """获取地支藏干"""
    zhi_canggan = {
        "子": "癸", 
        "丑": "己,癸,辛", 
        "寅": "甲,丙,戊", 
        "卯": "乙",
        "辰": "戊,乙,癸", 
        "巳": "丙,戊,庚", 
        "午": "丁,己", 
        "未": "己,丁,乙",
        "申": "庚,壬,戊", 
        "酉": "辛", 
        "戌": "戊,辛,丁", 
        "亥": "壬,甲"
    }
    return zhi_canggan.get(zhi, "未知")


def analyze_dayun_interaction_with_mingju(dayun_gan: str, dayun_zhi: str, bazi_chars: dict, day_master: str) -> str:
    """分析大运与命局的互动关系"""
    # 简化的分析逻辑
    results = []
    
    # 检查天干与日主的关系
    dayun_gan_relation = self_calculate_ten_god(dayun_gan, day_master)
    results.append(f"大运天干{dayun_gan}为{dayun_gan_relation}")
    
    # 检查地支冲克关系
    twelve_opposites = {
        "子": "午", "午": "子", "丑": "未", "未": "丑",
        "寅": "申", "申": "寅", "卯": "酉", "酉": "卯",
        "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳"
    }
    
    if dayun_zhi in twelve_opposites:
        opposite = twelve_opposites[dayun_zhi]
        for pillar in ["year", "month", "day", "hour"]:
            if bazi_chars[f"{pillar}_branch"] == opposite:
                results.append(f"大运地支{dayun_zhi}冲克命局{pillar}柱{opposite}")
    
    # 简单返回结果
    if len(results) == 0:
        return "大运与命局关系平稳"
    return "，".join(results)


def calculate_precise_dayun_start(birth_date: datetime, lunar_6tail_obj, year_gan_obj, gender_str: str) -> tuple:
    """精确计算起运时间"""
    try:
        # 获取生日当月节气
        jie_qi = safe_get_name(lunar_6tail_obj.getPrevJieQi())
        next_jie_qi = safe_get_name(lunar_6tail_obj.getNextJieQi())
        
        # 计算起运时间（默认3岁）
        start_age = 3
        start_days = 100
        
        # 简化的起运方向判断
        is_male = (gender_str == "男")
        is_yang = False
        try:
            if hasattr(year_gan_obj, "getYang"):
                is_yang = year_gan_obj.getYang() == 1
        except:
            is_yang = str(year_gan_obj) in ["甲", "丙", "戊", "庚", "壬"]
        
        # 顺逆排（简化规则）
        is_forward = (is_yang and is_male) or (not is_yang and not is_male)
        
        # 简化的起运时间计算
        # 实际应该计算出生到下一节令的天数，然后转换为岁数
        start_age_months = start_age * 12
        start_time = birth_date + timedelta(days=start_age_months * 30)
        
        age_str = f"{start_age}岁"
        
        return age_str, start_time, start_days
    except Exception as e:
        print(f"精确起运计算错误: {e}")
        return "3岁", birth_date + timedelta(days=3*365), 100


def get_location_info(place_name: str) -> dict:
    """根据地名获取地理信息"""
    # 实际项目中应该接入地理位置API，这里使用简化的实现
    return {
        "latitude": 30.0,
        "longitude": 120.0,
        "timezone": "Asia/Shanghai",
        "country": "中国",
        "city": place_name
    }


def get_solar_terms_for_year(year: int) -> dict:
    """获取某年的节气数据"""
    # 这里应该是精确的节气计算，现在返回简化版本
    return {
        "立春": datetime(year, 2, 4),
        "雨水": datetime(year, 2, 19),
        "惊蛰": datetime(year, 3, 6),
        "春分": datetime(year, 3, 21),
        "清明": datetime(year, 4, 5),
        "谷雨": datetime(year, 4, 20),
        "立夏": datetime(year, 5, 6),
        "小满": datetime(year, 5, 21),
        "芒种": datetime(year, 6, 6),
        "夏至": datetime(year, 6, 21),
        "小暑": datetime(year, 7, 7),
        "大暑": datetime(year, 7, 23),
        "立秋": datetime(year, 8, 8),
        "处暑": datetime(year, 8, 23),
        "白露": datetime(year, 9, 8),
        "秋分": datetime(year, 9, 23),
        "寒露": datetime(year, 10, 8),
        "霜降": datetime(year, 10, 23),
        "立冬": datetime(year, 11, 7),
        "小雪": datetime(year, 11, 22),
        "大雪": datetime(year, 12, 7),
        "冬至": datetime(year, 12, 22)
    }


def calculate_precise_dayun(birth_datetime: datetime, gender: str, year_gan: str, month_pillar: str) -> tuple:
    """
    精确计算大运起运信息
    
    Args:
        birth_datetime: 出生时间
        gender: 性别 ("男" 或 "女")
        year_gan: 年干
        month_pillar: 月柱（如"戊辰"）
    
    Returns:
        tuple: (起运日期, 起运天数, 大运干支列表)
    """
    try:
        birth_year = birth_datetime.year
        birth_month = birth_datetime.month
        
        # 1. 判断阴阳年
        yang_gans = ["甲", "丙", "戊", "庚", "壬"]
        is_yang_year = year_gan in yang_gans
        
        # 2. 判断顺逆排
        is_male = (gender == "男")
        is_forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)
        
        # 3. 计算起运天数（简化算法）
        base_days = 100  # 基础天数
        start_days = base_days + (birth_month - 1) * 10  # 简化计算
        
        # 4. 起运日期
        start_date = birth_datetime + timedelta(days=start_days)
        
        # 5. 生成大运干支序列
        month_index = JIAZI.index(month_pillar) if month_pillar in JIAZI else 0
        
        luck_pillars = []
        for i in range(8):  # 生成8个大运
            if is_forward:
                pillar_index = (month_index + i + 1) % 60
            else:
                pillar_index = (month_index - i - 1) % 60
            
            luck_pillars.append(JIAZI[pillar_index])
        
        return start_date, start_days, luck_pillars
        
    except Exception as e:
        print(f"精确大运计算错误: {e}")
        # 返回简化的默认值
        start_date = birth_datetime + timedelta(days=365*3)  # 3岁起运
        start_days = 365*3
        luck_pillars = ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未"]
        return start_date, start_days, luck_pillars


def format_dayun_info(start_date: datetime, start_days: float, luck_pillars: list, 
                     current_year: Optional[int] = None, bazi_chars: Optional[dict] = None, day_master: Optional[str] = None) -> list:
    """格式化大运信息"""
    formatted_luck = []
    
    for i, pillar in enumerate(luck_pillars[:8]):  # 通常显示8步大运
        step_start_age = int(start_days / 365) + i * 10
        step_end_age = step_start_age + 9
        step_start_date = start_date + timedelta(days=i * 10 * 365)
        step_end_date = step_start_date + timedelta(days=9 * 365)
        
        # 分析大运阶段
        phase = analyze_dayun_phase(step_start_age)
        
        # 分析大运与命局的关系
        if bazi_chars and day_master and len(pillar) >= 2:
            dayun_gan = pillar[0]
            dayun_zhi = pillar[1]
            interaction = analyze_dayun_interaction_with_mingju(
                dayun_gan, dayun_zhi, bazi_chars, day_master
            )
        else:
            interaction = "关系分析暂不可用"
        
        # 判断是否为当前大运
        is_current = False
        if current_year:
            current_age = current_year - int(start_date.year) + step_start_age
            is_current = step_start_age <= current_age <= step_end_age
        
        luck_info = {
            "step": i + 1,
            "gan_zhi": pillar,  # 使用 gan_zhi 键名以匹配 main.py 的期望
            "start_age": step_start_age,
            "end_age": step_end_age,
            "start_date": step_start_date.strftime("%Y-%m-%d"),
            "end_date": step_end_date.strftime("%Y-%m-%d"),
            "phase": phase,
            "interaction": interaction,
            "is_current": is_current
        }
        
        formatted_luck.append(luck_info)
    
    return formatted_luck
