# backend/app/schemas/iching.py
"""
易经算卦相关的 Pydantic 模型
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class IChingDivinationRequest(BaseModel):
    """易经算卦请求模型"""
    
    question: str = Field(..., description="占卜问题", min_length=1, max_length=500)
    divination_method: str = Field(
        default="coins", 
        description="算卦方式：coins(掷币法)、yarrow(蓍草法)、time(时间起卦)、number(数字起卦)"
    )
    divination_time: Optional[datetime] = Field(None, description="算卦时间，用于时间起卦法")
    numbers: Optional[List[int]] = Field(None, description="数字序列，用于数字起卦法")
    birth_info: Optional[Dict[str, Any]] = Field(None, description="生辰信息，用于个人化解读")
    
    # 兼容旧版本字段
    method: Optional[str] = Field("coins", description="摇卦方法，可为'coins'或'manual_numbers'")
    manual_numbers: Optional[List[int]] = Field(None, description="如果method为'manual_numbers'，则提供六个数字列表")
    gender: Optional[str] = Field(None, description="问卦者的性别，可为'男'或'女'")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "今年事业发展如何？",
                "divination_method": "coins",
                "datetime": "2025-06-24T10:30:00",
                "numbers": [6, 8, 9],
                "birth_info": {
                    "year": 1990,
                    "month": 6,
                    "day": 15
                }
            }
        }

class HexagramLine(BaseModel):
    """爻线模型"""
    number: int = Field(..., ge=1, le=6, description="爻的序号，1到6")
    value: int = Field(..., description="爻的数值，6(老阴), 7(少阳), 8(少阴), 9(老阳)")
    yin_yang: str = Field(..., description="阴或阳")
    is_changing: bool = Field(..., description="是否为变爻 (值是6或9)")
    description: Optional[str] = Field(None, description="爻辞（这爻的解释）")

class Hexagram(BaseModel):
    """卦象模型"""
    
    number: int = Field(..., description="卦序号(1-64)")
    name: str = Field(..., description="卦名")
    chinese_name: str = Field(..., description="中文卦名") 
    upper_trigram: str = Field(..., description="上卦")
    lower_trigram: str = Field(..., description="下卦")
    binary: str = Field(..., description="二进制表示")
    lines: List[str] = Field(..., description="六爻组成")

class HexagramData(BaseModel):
    """卦象数据模型（兼容旧版本）"""
    name: str = Field(..., description="卦名 (例如 '乾为天')")
    number: int = Field(..., description="卦序 (例如 1)")
    upper_trigram: str = Field(..., description="上卦 (例如 '乾')")
    lower_trigram: str = Field(..., description="下卦 (例如 '坤')")
    image: str = Field(..., description="卦象（例如 '天行健'）")
    judgment: str = Field(..., description="卦辞（对本卦的整体解释）")
    lines: List[HexagramLine] = Field(..., description="包含六个 HexagramLine 对象的列表")

class YaoLine(BaseModel):
    """爻辞模型"""
    
    position: int = Field(..., description="爻位(1-6)")
    name: str = Field(..., description="爻名")
    text: str = Field(..., description="爻辞")
    interpretation: str = Field(..., description="爻辞解释")
    is_changing: bool = Field(default=False, description="是否为变爻")

class IChingInterpretation(BaseModel):
    """易经解读模型"""
    
    overall_meaning: str = Field(..., description="卦象总体含义")
    judgment: str = Field(..., description="卦辞")
    image: str = Field(..., description="象辞")
    fortune_analysis: str = Field(..., description="运势分析")
    advice: str = Field(..., description="建议指导")
    time_analysis: str = Field(..., description="时机分析")
    relationship_analysis: Optional[str] = Field(None, description="人际关系分析")
    career_analysis: Optional[str] = Field(None, description="事业分析")
    wealth_analysis: Optional[str] = Field(None, description="财运分析")

class IChingDivinationResponse(BaseModel):
    """易经算卦响应模型"""
    
    question: str = Field(..., description="原始问题")
    divination_method: Optional[str] = Field(None, description="使用的算卦方法")
    divination_time: Optional[datetime] = Field(None, description="算卦时间")
    
    # 主卦信息
    primary_hexagram: HexagramData = Field(..., description="主卦")
    primary_yao_lines: Optional[List[YaoLine]] = Field(None, description="主卦爻辞")
    
    # 变卦信息（如果有变爻）
    changing_hexagram: Optional[HexagramData] = Field(None, description="变卦")
    changing_yao_lines: Optional[List[YaoLine]] = Field(None, description="变卦爻辞")
    
    # 解读分析
    interpretation: Optional[IChingInterpretation] = Field(None, description="卦象解读")
    
    # 兼容旧版本字段
    changing_lines_descriptions: List[str] = Field(default=[], description="所有变爻的爻辞列表")
    summary_analysis: str = Field(default="", description="综合分析结果")
    
    # 变爻分析
    changing_lines_analysis: Optional[str] = Field(None, description="变爻分析")
    
    # 综合建议
    final_guidance: Optional[str] = Field(None, description="综合指导建议")
    
    # AI增强分析字段
    ai_enhanced_analysis: Optional[str] = Field(None, description="AI增强分析，预留给未来的AI分析功能")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "今年事业发展如何？",
                "divination_method": "coins",
                "divination_time": "2025-06-24T10:30:00",
                "primary_hexagram": {
                    "name": "乾为天",
                    "number": 1,
                    "upper_trigram": "乾",
                    "lower_trigram": "乾",
                    "image": "天行健，君子以自强不息",
                    "judgment": "乾：元，亨，利，贞",
                    "lines": []
                },
                "summary_analysis": "当前运势极佳，事业发展正逢其时，建议积极行动",
                "changing_lines_descriptions": []
            }
        }