from fastapi import HTTPException, status
from app.schemas.iching import (
    IChingDivinationRequest,
    IChingDivinationResponse,
    HexagramData,
    HexagramLine
)
import random
import logging
from iching import iching
from typing import List, Optional, Any, Dict

# 64卦完整数据库
HEXAGRAM_DATABASE = {
    1: {"name": "乾", "judgment": "乾：元，亨，利，贞。", "image": "天行健，君子以自强不息。", "upper": "乾", "lower": "乾"},
    2: {"name": "坤", "judgment": "坤：元，亨，利牝马之贞。君子有攸往，先迷后得主，利西南得朋，东北丧朋。安贞，吉。", "image": "地势坤，君子以厚德载物。", "upper": "坤", "lower": "坤"},
    3: {"name": "屯", "judgment": "屯：元，亨，利，贞，勿用，有攸往，利建侯。", "image": "云雷，屯；君子以经纶。", "upper": "坎", "lower": "震"},
    4: {"name": "蒙", "judgment": "蒙：亨。匪我求童蒙，童蒙求我。初噬告，再三渎，渎则不告。利贞。", "image": "山下出泉，蒙；君子以果行育德。", "upper": "艮", "lower": "坎"},
    5: {"name": "需", "judgment": "需：有孚，光亨，贞吉。利涉大川。", "image": "云上于天，需；君子以饮食宴乐。", "upper": "坎", "lower": "乾"},
    6: {"name": "讼", "judgment": "讼：有孚，窒。惕中吉。终凶。利见大人，不利涉大川。", "image": "天与水违行，讼；君子以作事谋始。", "upper": "乾", "lower": "坎"},
    7: {"name": "师", "judgment": "师：贞，丈人，吉无咎。", "image": "地中有水，师；君子以容民畜众。", "upper": "坤", "lower": "坎"},
    8: {"name": "比", "judgment": "比：吉。原筮元永贞，无咎。不宁方来，后夫凶。", "image": "水在地上，比；先王以建万国，亲诸侯。", "upper": "坎", "lower": "坤"},
    # 为了简化，这里只列出前8卦，实际应用中可以扩展到64卦
}

# 八卦基本信息
TRIGRAM_INFO = {
    "乾": {"binary": "111", "element": "金", "nature": "天", "attribute": "刚健"},
    "坤": {"binary": "000", "element": "土", "nature": "地", "attribute": "柔顺"},
    "震": {"binary": "100", "element": "木", "nature": "雷", "attribute": "动"},
    "巽": {"binary": "011", "element": "木", "nature": "风", "attribute": "顺"},
    "坎": {"binary": "010", "element": "水", "nature": "水", "attribute": "险"},
    "离": {"binary": "101", "element": "火", "nature": "火", "attribute": "明"},
    "艮": {"binary": "001", "element": "土", "nature": "山", "attribute": "止"},
    "兑": {"binary": "110", "element": "金", "nature": "泽", "attribute": "悦"}
}

def extract_hexagram_data(yao_values: List[int], use_simple_method: bool = True) -> HexagramData:
    """
    从六爻值生成完整的卦象数据
    
    Args:
        yao_values: 六爻值列表 [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
        use_simple_method: 是否使用简化方法（不依赖外部库）
        
    Returns:
        HexagramData: 填充完整信息的卦象数据
    """
    try:
        print(f"DEBUG: extract_hexagram_data 输入爻值: {yao_values}")
        
        # 1. 计算上下卦八卦
        def calculate_trigram(trigram_lines):
            """根据三个爻计算八卦"""
            # 将爻值转换为二进制 (阳爻=1, 阴爻=0)
            binary_str = ""
            for line_value in trigram_lines:
                binary_str += "1" if line_value in [7, 9] else "0"
            
            # 八卦映射表（从下到上）
            trigram_map = {
                "000": "坤",  # ☷ 坤为地
                "001": "艮",  # ☶ 艮为山
                "010": "坎",  # ☵ 坎为水
                "011": "巽",  # ☴ 巽为风
                "100": "震",  # ☳ 震为雷
                "101": "离",  # ☲ 离为火
                "110": "兑",  # ☱ 兑为泽
                "111": "乾"   # ☰ 乾为天
            }
            
            return trigram_map.get(binary_str, "未知")
        
        # 计算下卦（初爻、二爻、三爻）和上卦（四爻、五爻、六爻）
        lower_trigram_lines = yao_values[:3]  # 下三爻
        upper_trigram_lines = yao_values[3:]  # 上三爻
        
        lower_trigram = calculate_trigram(lower_trigram_lines)
        upper_trigram = calculate_trigram(upper_trigram_lines)
        
        print(f"DEBUG: 下卦={lower_trigram}, 上卦={upper_trigram}")
        
        # 2. 根据上下卦组合计算卦序
        def get_hexagram_number(upper_tri, lower_tri):
            """根据上下卦计算64卦序号"""
            # 完整的64卦映射表
            hexagram_map = {
                ("乾", "乾"): 1, ("乾", "兑"): 43, ("乾", "离"): 14, ("乾", "震"): 34,
                ("乾", "巽"): 9, ("乾", "坎"): 5, ("乾", "艮"): 26, ("乾", "坤"): 11,
                ("兑", "乾"): 58, ("兑", "兑"): 58, ("兑", "离"): 38, ("兑", "震"): 54,
                ("兑", "巽"): 61, ("兑", "坎"): 60, ("兑", "艮"): 41, ("兑", "坤"): 19,
                ("离", "乾"): 13, ("离", "兑"): 49, ("离", "离"): 30, ("离", "震"): 55,
                ("离", "巽"): 37, ("离", "坎"): 63, ("离", "艮"): 22, ("离", "坤"): 36,
                ("震", "乾"): 25, ("震", "兑"): 17, ("震", "离"): 21, ("震", "震"): 51,
                ("震", "巽"): 42, ("震", "坎"): 3, ("震", "艮"): 27, ("震", "坤"): 24,
                ("巽", "乾"): 44, ("巽", "兑"): 28, ("巽", "离"): 50, ("巽", "震"): 32,
                ("巽", "巽"): 57, ("巽", "坎"): 48, ("巽", "艮"): 18, ("巽", "坤"): 46,
                ("坎", "乾"): 6, ("坎", "兑"): 47, ("坎", "离"): 64, ("坎", "震"): 40,
                ("坎", "巽"): 59, ("坎", "坎"): 29, ("坎", "艮"): 4, ("坎", "坤"): 7,
                ("艮", "乾"): 33, ("艮", "兑"): 31, ("艮", "离"): 56, ("艮", "震"): 62,
                ("艮", "巽"): 53, ("艮", "坎"): 39, ("艮", "艮"): 52, ("艮", "坤"): 15,
                ("坤", "乾"): 12, ("坤", "兑"): 45, ("坤", "离"): 35, ("坤", "震"): 16,
                ("坤", "巽"): 20, ("坤", "坎"): 8, ("坤", "艮"): 23, ("坤", "坤"): 2
            }
            return hexagram_map.get((upper_tri, lower_tri), 0)
        
        hexagram_number = get_hexagram_number(upper_trigram, lower_trigram)
        
        # 3. 获取卦名和卦辞
        def get_hexagram_info(number):
            """根据卦序获取卦名和卦辞"""
            # 简化的卦名数据库（前32卦）
            gua_names = {
                1: "乾为天", 2: "坤为地", 3: "水雷屯", 4: "山水蒙", 5: "水天需", 6: "天水讼", 7: "地水师", 8: "水地比",
                9: "风天小畜", 10: "天泽履", 11: "地天泰", 12: "天地否", 13: "天火同人", 14: "火天大有", 15: "地山谦", 16: "雷地豫",
                17: "泽雷随", 18: "山风蛊", 19: "地泽临", 20: "风地观", 21: "火雷噬嗑", 22: "山火贲", 23: "山地剥", 24: "地雷复",
                25: "天雷无妄", 26: "山天大畜", 27: "山雷颐", 28: "泽风大过", 29: "坎为水", 30: "离为火", 31: "泽山咸", 32: "雷风恒",
                33: "天山遁", 34: "雷天大壮", 35: "火地晋", 36: "地火明夷", 37: "风火家人", 38: "火泽睽", 39: "水山蹇", 40: "雷水解",
                41: "山泽损", 42: "风雷益", 43: "泽天夬", 44: "天风姤", 45: "泽地萃", 46: "地风升", 47: "泽水困", 48: "水风井",
                49: "泽火革", 50: "火风鼎", 51: "震为雷", 52: "艮为山", 53: "风山渐", 54: "雷泽归妹", 55: "雷火丰", 56: "火山旅",
                57: "巽为风", 58: "兑为泽", 59: "风水涣", 60: "水泽节", 61: "风泽中孚", 62: "雷山小过", 63: "水火既济", 64: "火水未济"
            }
            
            gua_judgments = {
                1: "乾：元，亨，利，贞。", 2: "坤：元，亨，利牝马之贞。君子有攸往，先迷后得主，利西南得朋，东北丧朋。安贞，吉。",
                3: "屯：元，亨，利，贞，勿用，有攸往，利建侯。", 4: "蒙：亨。匪我求童蒙，童蒙求我。初噬告，再三渎，渎则不告。利贞。",
                5: "需：有孚，光亨，贞吉。利涉大川。", 6: "讼：有孚，窒。惕中吉。终凶。利见大人，不利涉大川。",
                7: "师：贞，丈人，吉无咎。", 8: "比：吉。原筮元永贞，无咎。不宁方来，后夫凶。"
                # 可以继续扩展到64卦
            }
            
            name = gua_names.get(number, f"{upper_trigram}{lower_trigram}卦")
            judgment = gua_judgments.get(number, f"{name}的卦辞暂缺")
            
            return name, judgment
        
        hexagram_name, judgment_text = get_hexagram_info(hexagram_number)
        
        # 4. 构建卦象描述
        trigram_nature = {
            "乾": "天", "坤": "地", "震": "雷", "巽": "风",
            "坎": "水", "离": "火", "艮": "山", "兑": "泽"
        }
        upper_nature = trigram_nature.get(upper_trigram, upper_trigram)
        lower_nature = trigram_nature.get(lower_trigram, lower_trigram)
        image_text = f"{upper_nature}上{lower_nature}下，{hexagram_name}"
        
        # 5. 构建六爻线数据
        lines = []
        line_descriptions = [
            "初爻：事物开始，基础阶段，需谨慎行事",
            "二爻：辅助之位，中正之道，宜柔顺",
            "三爻：人道之始，多忧之位，当慎重",
            "四爻：近君之位，多惧之时，宜谨慎",
            "五爻：君王之位，中正当位，大吉之象",
            "上爻：极致之位，物极必反，宜知止"
        ]
        
        for idx in range(6):
            yao_value = yao_values[idx]
            line_number = idx + 1
            
            # 判断阴阳
            yin_yang = "阳" if yao_value in [7, 9] else "阴"
            
            # 判断是否为变爻
            is_changing = yao_value in [6, 9]
            
            # 构建爻辞描述
            base_description = line_descriptions[idx]
            if is_changing:
                if yao_value == 9:  # 老阳
                    base_description += "（老阳变阴，刚极必变）"
                else:  # 老阴
                    base_description += "（老阴变阳，柔极必刚）"
            
            lines.append(HexagramLine(
                number=line_number,
                value=yao_value,
                yin_yang=yin_yang,
                is_changing=is_changing,
                description=base_description
            ))
        
        print(f"DEBUG: 成功解析卦象 - 卦名:{hexagram_name}, 卦序:{hexagram_number}")
        
        return HexagramData(
            name=hexagram_name,
            number=hexagram_number,
            upper_trigram=upper_trigram,
            lower_trigram=lower_trigram,
            image=image_text,
            judgment=judgment_text,
            lines=lines
        )
        
    except Exception as e:
        logging.error(f"解析卦象数据失败: {e}")
        # 返回默认卦象数据
        return HexagramData(
            name="解析失败",
            number=0,
            upper_trigram="未知",
            lower_trigram="未知",
            image="卦象解析失败",
            judgment="卦辞解析失败",
            lines=[
                HexagramLine(
                    number=i+1,
                    value=yao_values[i] if i < len(yao_values) else 7,
                    yin_yang="阳" if (yao_values[i] if i < len(yao_values) else 7) in [7, 9] else "阴",
                    is_changing=(yao_values[i] if i < len(yao_values) else 7) in [6, 9],
                    description=f"第{i+1}爻：解析失败"
                ) for i in range(6)
            ]
        )

def prepare_ai_analysis_context(primary_hexagram: HexagramData, changing_hexagram: Optional[HexagramData], 
                               question: str, yao_values: List[int], changing_lines: List[int]) -> str:
    """
    为AI增强分析准备上下文信息
    
    Args:
        primary_hexagram: 主卦数据
        changing_hexagram: 变卦数据（可选）
        question: 用户问题
        yao_values: 六爻值
        changing_lines: 变爻位置列表
        
    Returns:
        str: AI分析的上下文信息（当前返回空字符串，待后续AI集成）
    """
    try:
        # 准备AI分析所需的结构化上下文
        context_data = {
            "question": question,
            "primary_hexagram": {
                "name": primary_hexagram.name,
                "number": primary_hexagram.number,
                "upper_trigram": primary_hexagram.upper_trigram,
                "lower_trigram": primary_hexagram.lower_trigram,
                "judgment": primary_hexagram.judgment
            },
            "changing_hexagram": {
                "name": changing_hexagram.name,
                "number": changing_hexagram.number,
                "judgment": changing_hexagram.judgment
            } if changing_hexagram else None,
            "yao_analysis": {
                "yao_values": yao_values,
                "changing_lines": changing_lines,
                "changing_count": len(changing_lines)
            },
            "divination_type": "有变爻" if changing_lines else "无变爻"
        }
        
        # TODO: 在此处集成AI分析服务
        # 可以调用外部AI API（如OpenAI、Claude等）进行深度分析
        # ai_response = call_ai_analysis_service(context_data)
        # return ai_response
        
        # 目前返回空字符串，保留AI分析接口
        return ""
        
    except Exception as e:
        logging.warning(f"准备AI分析上下文失败: {e}")
        return ""

async def perform_iching_divination(request_data: IChingDivinationRequest) -> IChingDivinationResponse:
    try:
        # 1. 生成六爻
        if request_data.method == "manual_numbers":
            if not request_data.manual_numbers or len(request_data.manual_numbers) != 6:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="manual_numbers 必须为6个数字")
            for n in request_data.manual_numbers:
                if n not in [6, 7, 8, 9]:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="每个爻值必须为6,7,8,9")
            yao_values = request_data.manual_numbers
        else:
            # 使用iching库生成六爻
            yao_values = iching.sixYao()
        
        print(f"DEBUG: 生成的六爻: {yao_values}")
        
        # 2. 不再使用 ichingshifa，直接用我们的方法解析卦象
        
        # 3. 主卦填充 - 使用新的 extract_hexagram_data 函数
        print(f"DEBUG: 开始解析主卦，爻值: {yao_values}")
        primary_hexagram = extract_hexagram_data(yao_values)
        print(f"DEBUG: 主卦解析完成 - {primary_hexagram.name}")
        
        # 4. 变卦判断与填充（增强版）
        changing_hexagram = None
        changing_lines_descriptions = []
        
        # 精确判断变爻
        changing_lines = [i+1 for i, v in enumerate(yao_values) if v in [6, 9]]
        has_changing_lines = len(changing_lines) > 0
        
        print(f"DEBUG: 检测到变爻位置: {changing_lines}")
        
        if has_changing_lines:
            # 生成变卦爻值
            transformed_yao_values = []
            for yao_val in yao_values:
                if yao_val == 9:  # 老阳变少阴
                    transformed_yao_values.append(8)
                elif yao_val == 6:  # 老阴变少阳
                    transformed_yao_values.append(7)
                else:  # 7, 8 保持不变
                    transformed_yao_values.append(yao_val)
            
            print(f"DEBUG: 变卦爻值: {transformed_yao_values}")
            
            # 使用 extract_hexagram_data 填充 changing_hexagram
            changing_hexagram = extract_hexagram_data(transformed_yao_values)
            print(f"DEBUG: 变卦解析完成 - {changing_hexagram.name}")
        
        # 5. 提取变爻爻辞
        for line in primary_hexagram.lines:
            if line.is_changing:
                changing_lines_descriptions.append(line.description)
        
        # 6. summary_analysis 填充（增强版结构化分析）
        summary_parts = []
        
        # 1. 卦象基本信息
        summary_parts.append(f"卦象解析：{primary_hexagram.name}（第{primary_hexagram.number}卦），{primary_hexagram.upper_trigram}上{primary_hexagram.lower_trigram}下")
        
        # 2. 主卦卦辞
        summary_parts.append(f"本卦卦辞：{primary_hexagram.judgment}")
        
        # 3. 变卦信息（如果存在）
        if changing_hexagram:
            summary_parts.append(f"变卦：{changing_hexagram.name}（第{changing_hexagram.number}卦），卦辞：{changing_hexagram.judgment}")
        
        # 4. 变爻详细解读（如果非空）
        if changing_lines_descriptions:
            summary_parts.append(f"变爻解读（共{len(changing_lines_descriptions)}个变爻）：{'；'.join(changing_lines_descriptions)}")
        
        # 5. 八卦组合特性
        if primary_hexagram.upper_trigram != "未知" and primary_hexagram.lower_trigram != "未知":
            trigram_meanings = {
                "乾": "天、刚健", "坤": "地、柔顺", "震": "雷、动", "巽": "风、顺",
                "坎": "水、险", "离": "火、明", "艮": "山、止", "兑": "泽、悦"
            }
            upper_meaning = trigram_meanings.get(primary_hexagram.upper_trigram, primary_hexagram.upper_trigram)
            lower_meaning = trigram_meanings.get(primary_hexagram.lower_trigram, primary_hexagram.lower_trigram)
            summary_parts.append(f"八卦组合：上{upper_meaning}，下{lower_meaning}")
        
        # 6. 基本运势分析
        if has_changing_lines:
            summary_parts.append(f"运势变化：有{len(changing_lines)}个变爻，局势正在发生变化，需要灵活应对")
        else:
            summary_parts.append("运势稳定：无变爻，当前局势相对稳定")
        
        # 组合成完整的 summary_analysis
        summary_analysis = "。".join(summary_parts) + "。"
        
        # 7. AI增强分析预留框架
        ai_enhanced_analysis = prepare_ai_analysis_context(
            primary_hexagram=primary_hexagram,
            changing_hexagram=changing_hexagram,
            question=request_data.question,
            yao_values=yao_values,
            changing_lines=changing_lines
        )
        
        # 8. 返回完整的 IChingDivinationResponse
        return IChingDivinationResponse(
            question=request_data.question,
            divination_method=request_data.divination_method,
            divination_time=request_data.divination_time,
            primary_hexagram=primary_hexagram,
            changing_hexagram=changing_hexagram,
            changing_lines_descriptions=changing_lines_descriptions,
            summary_analysis=summary_analysis,
            primary_yao_lines=None,
            changing_yao_lines=None,
            interpretation=None,
            changing_lines_analysis=None,
            final_guidance=None,
            ai_enhanced_analysis=ai_enhanced_analysis  # 使用AI分析结果
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"易经算卦失败: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"易经算卦失败: {str(e)}") 