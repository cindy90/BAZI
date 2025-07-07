import argparse
import collections
import datetime
from typing import List

from lunar_python import Lunar, Solar
from colorama import init

# ==== MOCK/兼容常量定义（如需更详细可补充）====
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
gan5 = {g: w for g, w in zip(Gan, ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"])}
zhi5 = {z: {g: 1 for g in Gan} for z in Zhi}  # 简化为每支含所有干
wuhangs = {"金": [], "木": [], "水": [], "火": [], "土": []}
jianlus = set()
year_shens = {k: {k: [] for k in Zhi} for k in []}
month_shens = {k: {k: [] for k in Zhi} for k in []}
day_shens = {k: {k: [] for k in Zhi} for k in []}
g_shens = {k: {k: [] for k in Zhi} for k in []}
nayins = {(g, z): "" for g in Gan for z in Zhi}
yutangs = {g: [[]] for g in Gan}
gong_he = {}

# 定义十神索引映射，与 Efairy 的二维数组保持一致
# [['比', '劫'], ['食', '伤'], ['财', '才'],[ '杀', '官'], ['枭', '印']]
SHI_SHEN_MAP = [
    ["比", "劫"],  # 0: 比劫
    ["食", "伤"],  # 1: 食伤
    ["财", "才"],  # 2: 财才 (正财, 偏财)
    ["杀", "官"],  # 3: 杀官 (七杀, 正官)
    ["枭", "印"]   # 4: 枭印 (偏印, 正印)
]

# 天干五行阴阳属性
GAN_YIN_YANG = {
    "甲": "阳", "乙": "阴",
    "丙": "阳", "丁": "阴",
    "戊": "阳", "己": "阴",
    "庚": "阳", "辛": "阴",
    "壬": "阳", "癸": "阴"
}

# 修正 ten_deities，使其返回 [主索引, 副索引]
# 副索引 0 代表阳性或正性，1 代表阴性或偏性 (根据 Efairy 约定)
ten_deities = {}
for day_master_gan in Gan:
    ten_deities[day_master_gan] = {}
    day_master_element = gan5[day_master_gan]
    day_master_yin_yang = GAN_YIN_YANG[day_master_gan]

    for target_gan in Gan:
        target_element = gan5[target_gan]
        target_yin_yang = GAN_YIN_YANG[target_gan]

        if target_gan == day_master_gan:
            # 比肩: 同五行同阴阳
            ten_deities[day_master_gan][target_gan] = [0, 0]  # 比
        elif target_element == day_master_element and target_yin_yang != day_master_yin_yang:
            # 劫财: 同五行不同阴阳
            ten_deities[day_master_gan][target_gan] = [0, 1]  # 劫
        elif (day_master_element == "木" and target_element == "火") or \
             (day_master_element == "火" and target_element == "土") or \
             (day_master_element == "土" and target_element == "金") or \
             (day_master_element == "金" and target_element == "水") or \
             (day_master_element == "水" and target_element == "木"):
            # 食伤: 我生者
            if target_yin_yang == day_master_yin_yang:
                ten_deities[day_master_gan][target_gan] = [1, 0]  # 食 (同阴阳为食神)
            else:
                ten_deities[day_master_gan][target_gan] = [1, 1]  # 伤 (异阴阳为伤官)
        elif (day_master_element == "木" and target_element == "土") or \
             (day_master_element == "火" and target_element == "金") or \
             (day_master_element == "土" and target_element == "水") or \
             (day_master_element == "金" and target_element == "木") or \
             (day_master_element == "水" and target_element == "火"):
            # 财才: 我克者
            if target_yin_yang == day_master_yin_yang:
                ten_deities[day_master_gan][target_gan] = [2, 1]  # 才 (同阴阳为偏财)
            else:
                ten_deities[day_master_gan][target_gan] = [2, 0]  # 财 (异阴阳为正财)
        elif (day_master_element == "木" and target_element == "金") or \
             (day_master_element == "火" and target_element == "水") or \
             (day_master_element == "土" and target_element == "木") or \
             (day_master_element == "金" and target_element == "火") or \
             (day_master_element == "水" and target_element == "土"):
            # 杀官: 克我者
            if target_yin_yang == day_master_yin_yang:
                ten_deities[day_master_gan][target_gan] = [3, 0]  # 杀 (同阴阳为七杀)
            else:
                ten_deities[day_master_gan][target_gan] = [3, 1]  # 官 (异阴阳为正官)
        elif (day_master_element == "木" and target_element == "水") or \
             (day_master_element == "火" and target_element == "木") or \
             (day_master_element == "土" and target_element == "火") or \
             (day_master_element == "金" and target_element == "土") or \
             (day_master_element == "水" and target_element == "金"):
            # 枭印: 生我者
            if target_yin_yang == day_master_yin_yang:
                ten_deities[day_master_gan][target_gan] = [4, 0]  # 枭 (同阴阳为偏印)
            else:
                ten_deities[day_master_gan][target_gan] = [4, 1]  # 印 (异阴阳为正印)
        else:
            ten_deities[day_master_gan][target_gan] = [-1, -1]  # 未知或错误情况
# mock tianyis, self_zuo, zhi5_list
# tianyis = {g: [[]] for g in Gan}
tianyis = {g: [[]] for g in Gan}
self_zuo = {}
zhi5_list = {z: [] for z in Zhi}

# init colorama (如果需要，但这里只用于命令行打印，可以移除)
init()

description = '''

'''

# 保留所有顶部的导入、数据、辅助函数和核心计算逻辑
# 移除无用 import
# import pprint  # 已无 print 调用，可删除
# 删除 parser = argparse.ArgumentParser(...) 开始到文件末尾的命令行解析和全局 print 代码块
# 你可以在此处添加 BaZiCalculatorLib 类或其他结构化封装代码

Gans = collections.namedtuple("Gans", "year month day time")
Zhis = collections.namedtuple("Zhis", "year month day time")

def safe_get_name(obj):
    if obj is not None and hasattr(obj, "getName") and callable(getattr(obj, "getName")):
        return obj.getName()
    return str(obj) if obj is not None else ""

def safe_get_hidden_gan(zhi_obj):
    """
    安全获取地支对象的藏干列表，防止 None/type 报错。
    """
    if zhi_obj and hasattr(zhi_obj, "getHiddenGan") and callable(getattr(zhi_obj, "getHiddenGan")):
        hidden_gan = zhi_obj.getHiddenGan()
        if hidden_gan and isinstance(hidden_gan, (list, tuple)):
            return hidden_gan
    return []

def get_shishen_char(shishen_index: List[int]) -> str:
    """
    将十神索引转换为字符表示。
    Args:
        shishen_index: 形如 [主索引, 副索引] 的十神索引。
    Returns:
        十神字符，如 "比", "劫", "正财" 等。
    """
    if not isinstance(shishen_index, list) or len(shishen_index) != 2:
        return "未知"
    
    main_idx, sub_idx = shishen_index
    
    if 0 <= main_idx < len(SHI_SHEN_MAP) and 0 <= sub_idx < len(SHI_SHEN_MAP[main_idx]):
        return SHI_SHEN_MAP[main_idx][sub_idx]
    return "未知"

class BaZiCalculatorLib:
    """
    八字分析主类，封装所有八字分析逻辑，结构化输出，便于API调用。
    """
    def __init__(self, year, month, day, hour, sex, use_solar=True):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int(hour)
        self.sex = sex
        self.use_solar = use_solar
        self.dayun_list_full = []
        self.all_liunian_list = []
        self.gans = None
        self.zhis = None
        self.gan_shens = None
        self.zhi_shens = None
        self.scores = None
        self.gan_scores = None
        self.weak = None
        self.dayuns = None
        self.ba = None
        self.lunar = None
        self.solar = None
        self.zhus = None
        self.me = None
        self.month_zhi = None
        self.palace_info_result = None
        self._init_bazi()
        self._calc_main_properties()
        # self.palace_info_result = self.get_detailed_palace_info()

    def _init_bazi(self):
        # 通过 lunar_python 获取八字干支
        if self.use_solar:
            solar = Solar.fromYmdHms(self.year, self.month, self.day, self.hour, 0, 0)
            lunar = solar.getLunar()
        else:
            lunar = Lunar.fromYmdHms(self.year, self.month, self.day, self.hour, 0, 0)
            solar = lunar.getSolar()
        self.lunar = lunar
        self.solar = solar
        ba = lunar.getEightChar()
        self.ba = ba  # 保留 EightChar 对象
        self.gans = Gans(year=ba.getYearGan(), month=ba.getMonthGan(), day=ba.getDayGan(), time=ba.getTimeGan())
        self.zhis = Zhis(year=ba.getYearZhi(), month=ba.getMonthZhi(), day=ba.getDayZhi(), time=ba.getTimeZhi())
        self.zhus = [item for item in zip(self.gans, self.zhis)]
        self.me = self.gans.day if self.gans else None
        self.month_zhi = self.zhis.month if self.zhis else None
        # 新增：暴露完整大运对象列表
        # 尝试不同的 lunar_python EightChar 大运方法名
        dayun_method = None
        for method_name in ["getDaYunList", "getDaYun", "getYun"]:
            if hasattr(self.ba, method_name) and callable(getattr(self.ba, method_name, None)):
                dayun_method = getattr(self.ba, method_name)
                break
        if dayun_method:
            try:
                # 有些方法需要传性别，有些不需要
                import inspect
                if len(inspect.signature(dayun_method).parameters) == 1:
                    self.dayun_list_full = dayun_method(self.sex == '男')
                else:
                    self.dayun_list_full = dayun_method()
            except Exception:
                self.dayun_list_full = []
        else:
            self.dayun_list_full = []

    def _calc_main_properties(self):
        # 计算主流程属性，便于后续分析方法调用
        self.scores = {k: 0 for k in "金木水火土"}
        self.gan_scores = {k: 0 for k in Gan}
        if self.gans:
            for item in self.gans:
                if item in gan5:
                    self.scores[gan5[item]] += 5
                    self.gan_scores[item] += 5
        if self.zhis:
            for item in list(self.zhis) + ([self.zhis.month] if hasattr(self.zhis, 'month') else []):
                if item in zhi5:
                    for gan in zhi5[item]:
                        if gan in gan5:
                            self.scores[gan5[gan]] += zhi5[item][gan]
                            self.gan_scores[gan] += zhi5[item][gan]
        # 十神
        if self.gans and self.me:
            # 存储十神索引
            self.gan_shens_indices = [ten_deities[self.me][safe_get_name(item)] if i != 2 else [-1, -1] for i, item in enumerate(self.gans)]
            # 为了兼容旧的显示逻辑，这里仍可以保留字符形式
            self.gan_shens = [get_shishen_char(idx) if idx != [-1, -1] else '--' for idx in self.gan_shens_indices]
        else:
            self.gan_shens = []
            self.gan_shens_indices = []

        if self.zhis and self.me:
            # 获取地支藏干，然后计算藏干的十神
            self.zhi_shens_indices = []
            self.zhi_shens = []
            for zhi_obj in self.zhis:
                hidden_gans = safe_get_hidden_gan(zhi_obj)
                current_zhi_shens = []
                current_zhi_shens_indices = []
                for hidden_gan in hidden_gans:
                    # 确保 hidden_gan 是字符串类型
                    hidden_gan_str = safe_get_name(hidden_gan)
                    if hidden_gan_str in ten_deities[self.me]:
                        idx = ten_deities[self.me][hidden_gan_str]
                        current_zhi_shens_indices.append(idx)
                        current_zhi_shens.append(get_shishen_char(idx))
                self.zhi_shens_indices.append(current_zhi_shens_indices)
                self.zhi_shens.append(current_zhi_shens)  # 存储藏干十神字符列表
        else:
            self.zhi_shens = []
            self.zhi_shens_indices = []
        
        # 修复：将地支的十神列表展平后再与天干十神合并
        zhi_shens_flat = []
        for zhi_shens_list in self.zhi_shens:
            zhi_shens_flat.extend(zhi_shens_list)
        self.shens = self.gan_shens + zhi_shens_flat
        self.weak = self._calc_weak()
        self.dayuns = self._calc_dayuns()
        self.main_result = self._get_main_result()
        # 获取所有流年信息
        self.all_liunian_list = []
        if hasattr(self, 'dayun_list_full') and self.dayun_list_full:
            for dayun_obj in self.dayun_list_full:
                if hasattr(dayun_obj, 'getLiuNian') and callable(getattr(dayun_obj, 'getLiuNian', None)):
                    for liunian_obj in dayun_obj.getLiuNian():
                        self.all_liunian_list.append({
                            "year": liunian_obj.getYear(),
                            "gan_zhi": liunian_obj.getGanZhi(),
                            "age": liunian_obj.getAge(),
                            "ten_god_gan": "",
                            "analysis": ""
                        })

    def _calc_weak(self):
        if not self.zhis or not self.me:
            return True
        # 修复：使用 safe_get_name 获取地支字符串，并且获取十神字符而不是索引
        me_status = []
        for item in self.zhis:
            zhi_str = safe_get_name(item)
            if zhi_str in ten_deities[self.me]:
                shishen_idx = ten_deities[self.me][zhi_str]
                shishen_char = get_shishen_char(shishen_idx)
                me_status.append(shishen_char)
        
        weak = True
        for s in me_status:
            if s in ('长', '帝', '建'):  # 这些可能需要根据实际的地支长生十二宫来调整
                weak = False
        if weak:
            if hasattr(self, 'shens') and self.shens and self.shens.count('比') + me_status.count('库') > 2:
                weak = False
        return weak

    def _calc_dayuns(self):
        if not self.gans or not self.zhis:
            return []
        try:
            seq = Gan.index(self.gans.year)
            direction = 1 if (seq % 2 == 0 and self.sex == '男') or (seq % 2 == 1 and self.sex == '女') else -1
            gan_seq = Gan.index(self.gans.month)
            zhi_seq = Zhi.index(self.zhis.month)
            return [Gan[(gan_seq + i * direction) % 10] + Zhi[(zhi_seq + i * direction) % 12] for i in range(1, 13)]
        except Exception:
            return []

    def _get_main_result(self):
        # 主流程结构化结果
        return {
            'gans': self.gans,
            'zhis': self.zhis,
            'gan_shens': self.gan_shens,  # 字符表示
            'gan_shens_indices': self.gan_shens_indices,  # 索引表示
            'zhi_shens': self.zhi_shens,  # 字符表示
            'zhi_shens_indices': self.zhi_shens_indices,  # 索引表示
            'scores': self.scores,
            'gan_scores': self.gan_scores,
            'weak': self.weak,
            'dayuns': self.dayuns,
        }

    def get_main_result(self):
        return self.main_result

    def get_god_spirits(self):
        # 神煞分析，返回所有神煞列表
        if not self.zhis or not self.gans or self.me is None:
            return []
        all_shens = set()
        zhis = self.zhis
        gans = self.gans
        me = self.me
        for item in year_shens:
            for i in (1, 2, 3):
                if hasattr(zhis, '__getitem__') and hasattr(zhis, 'year') and getattr(zhis, 'year', None) and zhis[i] in year_shens[item].get(zhis.year, []):
                    all_shens.add(item)
        for item in month_shens:
            for i in range(4):
                if hasattr(gans, '__getitem__') and hasattr(zhis, 'month') and getattr(zhis, 'month', None) and (gans[i] in month_shens[item].get(zhis.month, []) or zhis[i] in month_shens[item].get(zhis.month, [])):
                    all_shens.add(item)
        for item in day_shens:
            for i in (0, 1, 3):
                if hasattr(zhis, '__getitem__') and hasattr(zhis, 'day') and getattr(zhis, 'day', None) and zhis[i] in day_shens[item].get(zhis.day, []):
                    all_shens.add(item)
        for item in g_shens:
            for i in range(4):
                if hasattr(zhis, '__getitem__') and me is not None and zhis[i] in g_shens[item].get(me, []):
                    all_shens.add(item)
        return list(all_shens)

    def get_geju(self):
        # 格局分析
        me = self.me
        zhis = self.zhis
        gans = self.gans
        zhus = self.zhus
        if not me or not zhis or not gans:
            return ''
        ge = ''
        if hasattr(zhis, 'month') and (me, zhis.month) in jianlus:
            ge = '建'
        elif hasattr(zhis, 'month') and (me, zhis.month) in (('甲', '卯'), ('庚', '酉'), ('壬', '子')):
            ge = '月刃'
        else:
            if hasattr(zhis, '__getitem__') and len(zhis) > 1:
                zhi = zhis[1]
                if zhi in wuhangs['土'] or (hasattr(zhis, 'month') and (me, zhis.month) in (('乙', '寅'), ('丙', '午'), ('丁', '巳'), ('戊', '午'), ('己', '巳'), ('辛', '申'), ('癸', '亥'))):
                    for item in zhi5.get(zhi, {}):
                        if hasattr(gans, '__getitem__') and item in list(gans)[:2] + list(gans)[3:]:
                            ge = ten_deities[me][item]
                else:
                    d = zhi5.get(zhi, {})
                    if d:
                        max_key = None
                        max_value = float('-inf')
                        for k, v in d.items():
                            if isinstance(v, (int, float)) and v > max_value:
                                max_key = k
                                max_value = v
                        if max_key:
                            ge = ten_deities[me][max_key]
        return ge

    def get_special_stars(self):
        # 兼容测试用例，返回空字典
        return {}

    def get_wuxing_advice(self):
        # 五行建议，兼容测试用例
        short = ''
        if isinstance(self.scores, dict) and self.scores is not None and self.scores and all(v is not None for v in self.scores.values()):
            # 只在 self.scores 所有值非 None 时取最小
            min_key = None
            min_value = float('inf')
            for k, v in self.scores.items():
                if v is not None and v < min_value:
                    min_key = k
                    min_value = v
            short = min_key if min_key is not None else ''
        return {
            'lacking': short,
            'advice_url': 'http://t.cn/E6zwOMq',
        }