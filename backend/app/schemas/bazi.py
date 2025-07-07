# backend/app/schemas/bazi.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class BaziCalculateRequest(BaseModel):
    name: Optional[str] = Field(None, description="姓名", max_length=50)
    gender: str = Field(..., description="性别", pattern="^(男|女)$")
    # 注意：datetime 应该接收 ISO 8601 格式的字符串，FastAPI/Pydantic 会自动解析
    birth_datetime: datetime = Field(..., description="出生日期时间，包含时区信息。格式如 '2000-01-01T12:30:00+08:00'")
    is_solar_time: bool = Field(True, description="是否使用真太阳时校准")
    # 添加出生地点相关字段
    birth_place: Optional[str] = Field(None, description="出生地点（城市名）", max_length=100)
    longitude: Optional[float] = Field(None, description="出生地经度", ge=-180, le=180)
    latitude: Optional[float] = Field(None, description="出生地纬度", ge=-90, le=90)
    timezone_offset: Optional[float] = Field(None, description="时区偏移（小时）", ge=-12, le=12)

class BaziCalculateResponse(BaseModel):
    bazi_characters: Dict[str, str] = Field(..., description="八字天干地支，如 { 'year_stem': '甲', 'year_branch': '子', 'day_stem': '庚', 'day_branch': '午', ... }")
    five_elements_score: Dict[str, str] = Field(..., description="五行得分（百分比格式），如 { '金': '19%', '木': '14%', '水': '14%', '火': '20%', '土': '34%' }")
    day_master_strength: str = Field(..., description="日主旺衰，如 '偏弱', '偏旺'")
    day_master_element: str = Field(..., description="日主五行")
    zodiac_sign: str = Field(..., description="生肖")
    major_cycles: List[Dict[str, Any]] = Field([], description="大运信息列表，每项包含开始年份，干支，天干十神，地支藏干，五行变化，互动关系，趋势分析等完整信息")
    current_year_fortune: Optional[Dict[str, Any]] = Field(None, description="当年运势简要分析，例如 { 'year': 2025, 'gan_zhi': '乙巳', 'analysis': '...' }")
    gan_zhi_info: Dict[str, Any] = Field(..., description="四柱干支的详细信息，包含十神、藏干、纳音等")
    na_yin: Dict[str, List[Union[str, int]]] = Field(..., description="四柱纳音，现在包含名称和五行索引，如 { 'year_na_yin': ['海中金', 3], ... }")
    palace_info: Dict[str, Any] = Field(..., description="宫位信息，包含胎元、命宫、身宫、胎息及其纳音、方位等，以及完整的十二宫位系统")
    birth_place: Optional[str] = Field(None, description="出生地点")
    location_info: Optional[Dict[str, Any]] = Field(None, description="出生地点相关信息，包含地理坐标、真太阳时偏移等")
    # === 新增字段：地支藏干 ===
    dz_cang_gan: Optional[List[Dict[str, Any]]] = Field(None, description="地支藏干详细信息，如 [{'pillar':'year','hidden_stems':['癸','辛','戊']}, ...]")
    
    # === 新增字段：十二长生和神煞 ===
    day_chang_sheng: Optional[List[Dict[str, Any]]] = Field(None, description="日主在四柱的十二长生状态，如 [{'index': 4, 'char': '帝旺'}, ...]")
    year_chang_sheng: Optional[List[Dict[str, Any]]] = Field(None, description="年干在四柱的十二长生状态，如 [{'index': 0, 'char': '长生'}, ...]")
    shen_sha_details: Optional[List[Dict[str, Any]]] = Field(None, description="详细神煞结果列表，包含各种神煞的位置、强度和状态信息")
    
    # === 新增字段：干支互动关系 ===
    interactions: Optional[Dict[str, Any]] = Field(None, description="干支互动关系分析结果，包含天干五合、地支六合、三合、半合、六冲、相刑、相穿等")
    # === 新增字段：喜用神五行 ===
    favorable_elements: List[str] = Field(..., description="喜用神五行")
    
    # === 新增字段：综合分析结果 ===
    comprehensive_favorable_analysis: Optional[Dict[str, Any]] = Field(None, description="综合分析结果，包含基础分析、调候分析、通关分析、病药分析、格局分析和最终预测")
    
    # 可以在这里添加更多你希望展示的八字细节，如神煞、格局等