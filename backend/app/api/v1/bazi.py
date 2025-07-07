# backend/app/api/v1/bazi.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session # 尽管不直接用db，但get_current_user可能需要
from typing import Any, Dict, Optional
from pydantic import BaseModel
import asyncio
from datetime import datetime

from ...db.session import get_db # get_current_user依赖它
from ...schemas.bazi import BaziCalculateRequest, BaziCalculateResponse
from app.services.bazi_calculator import calculate_bazi_data
from app.services.core import Bazi, StemBranch
from app.services.analyzers import AdvancedDayunAnalyzer
from app.core.dependencies import get_current_user # 导入认证依赖

# 导入DeepSeek服务
try:
    from app.services.deepseek_service import DeepSeekService
    deepseek_service = DeepSeekService()
    DEEPSEEK_AVAILABLE = True
    print("DeepSeek service imported successfully")
except ImportError as e:
    DEEPSEEK_AVAILABLE = False
    print(f"DeepSeek service import failed: {e}")
    deepseek_service = None

router = APIRouter(prefix="/bazi", tags=["八字算命"])

@router.post("/calculate", response_model=BaziCalculateResponse)
async def calculate_bazi_chart(
    request: BaziCalculateRequest,
    current_user: Any = Depends(get_current_user), # 确保用户已登录
    db: Session = Depends(get_db) # 即使这里不直接用db，get_current_user依赖它
):
    """
    根据出生信息计算八字排盘（快速模式）。
    """
    try:
        # 调用八字计算服务（默认使用快速模式）
        bazi_result = await calculate_bazi_data(request, quick_mode=True)
        return bazi_result
    except HTTPException as e:
        # 重新抛出服务层可能抛出的HTTPException
        print(f"HTTPException caught in bazi_api: Status={e.status_code}, Detail={e.detail}")
        raise e
    except Exception as e:
        print(f"八字排盘发生未知错误: {e}")
        # 捕获其他未知错误
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"八字排盘发生未知错误: {e}"
        )

# 添加测试用的无认证端点
@router.post("/test-calculate")  # Removed response_model temporarily
async def test_calculate_bazi_chart(
    request: BaziCalculateRequest
):
    """
    测试用八字排盘端点，无需认证。
    """
    try:
        print(f"🚀 API: 收到请求 - {request}")
        # 调用八字计算服务（启用快速模式）
        print("🔄 API: 开始计算...")
        bazi_result = await calculate_bazi_data(request, quick_mode=True)
        print(f"✅ API: 计算成功 - 类型: {type(bazi_result)}")
        
        # 手动转换为字典以避免Pydantic响应模型验证问题
        result_dict = {}
        for field_name in bazi_result.__dict__.keys():
            result_dict[field_name] = getattr(bazi_result, field_name)
        
        return result_dict
    except HTTPException as e:
        # 重新抛出服务层可能抛出的HTTPException
        print(f"❌ HTTPException caught in test bazi_api: Status={e.status_code}, Detail={e.detail}")
        raise e
    except Exception as e:
        print(f"💥 测试八字排盘发生未知错误: {e}")
        import traceback
        traceback.print_exc()
        # 捕获其他未知错误
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"测试八字排盘发生未知错误: {e}"
        )

# 新增的测试端点
@router.post("/calculate-test", response_model=BaziCalculateResponse)
async def calculate_bazi_chart_test(
    request: BaziCalculateRequest
):
    """
    根据出生信息计算八字排盘（测试版本，无需认证）。
    """
    try:
        # 调用八字计算服务（默认使用快速模式）
        bazi_result = await calculate_bazi_data(request, quick_mode=True)
        return bazi_result
    except HTTPException as e:
        # 重新抛出服务层可能抛出的HTTPException
        print(f"HTTPException caught in bazi_api: Status={e.status_code}, Detail={e.detail}")
        raise e
    except Exception as e:
        print(f"八字排盘发生未知错误: {e}")
        # 捕获其他未知错误
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器内部错误: {str(e)}"
        )

# 添加快速计算端点（需要认证）
@router.post("/calculate-quick", response_model=BaziCalculateResponse)
async def calculate_bazi_chart_quick(
    request: BaziCalculateRequest,
    current_user: Any = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    快速八字排盘端点，跳过耗时的AI分析。
    """
    try:
        # 调用八字计算服务（启用快速模式）
        bazi_result = await calculate_bazi_data(request, quick_mode=True)
        return bazi_result
    except HTTPException as e:
        # 重新抛出服务层可能抛出的HTTPException
        print(f"HTTPException caught in quick bazi_api: Status={e.status_code}, Detail={e.detail}")
        raise e
    except Exception as e:
        print(f"快速八字排盘发生未知错误: {e}")
        # 捕获其他未知错误
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"快速八字排盘发生未知错误: {e}"
        )

# 详细分析请求模型
class DetailedAnalysisRequest(BaseModel):
    bazi_data: Dict[str, Any]
    year: str

# 详细分析响应模型
class DetailedAnalysisResponse(BaseModel):
    detailed_analysis: Dict[str, str]
    status: str = "success"
    processing_time: Optional[float] = None

@router.post("/generate-detailed-analysis", response_model=DetailedAnalysisResponse)
async def generate_detailed_analysis(
    request: DetailedAnalysisRequest
):
    """
    生成详细的AI运势分析，专门用于异步调用。
    支持从快速八字计算结果进行深度分析。
    """
    import time
    start_time = time.time()
    
    try:
        if not DEEPSEEK_AVAILABLE or deepseek_service is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI分析服务暂时不可用"
            )
          # 调用DeepSeek服务生成详细分析
        detailed_analysis = await deepseek_service.generate_detailed_fortune_analysis(
            request.bazi_data,
            request.year
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        return DetailedAnalysisResponse(
            detailed_analysis=detailed_analysis,
            status="success",
            processing_time=processing_time
        )
        
    except HTTPException as e:
        # 重新抛出HTTP异常
        raise e
    except Exception as e:
        print(f"生成详细分析发生未知错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成详细分析发生未知错误: {e}"
        )

# 大运详细分析测试端点
@router.post("/calculate-dayun-test", response_model=BaziCalculateResponse)
async def calculate_bazi_chart_dayun_test(
    request: BaziCalculateRequest,
    timeout_seconds: int = 120  # 增加超时时间到120秒，确保AI分析有足够时间完成
):
    """
    大运详细分析测试端点（无需认证，有超时控制）
    注意：此端点包含AI分析，可能需要较长时间完成
    """
    try:
        print(f"收到大运测试请求: {request}")
        # 为AI分析设置充足的超时时间
        print(f"Starting detailed analysis with {timeout_seconds}s timeout...")
        result = await asyncio.wait_for(
            calculate_bazi_data(request, quick_mode=False), 
            timeout=timeout_seconds
        )
        print("✅ Detailed analysis completed successfully")
        return result
    except asyncio.TimeoutError:
        # 超时时回退到快速模式，但仍提供基础的详细分析
        print(f"❌ Detailed analysis timed out after {timeout_seconds}s, falling back to quick mode")
        result = await calculate_bazi_data(request, quick_mode=True)
          # 为超时情况提供基础的详细分析
        if hasattr(result, 'current_year_fortune') and result.current_year_fortune:
            # 生成基础详细分析作为降级方案
            basic_detailed_analysis = {
                "overall_analysis": f"{result.current_year_fortune.get('analysis', '')}。由于网络原因暂时无法提供AI深度分析，以上为基础运势分析。",
                "note": "AI分析超时，已降级为基础分析版本",
                "retry_available": True
            }
            result.current_year_fortune['detailed_analysis'] = basic_detailed_analysis
        
        return result
    except Exception as e:
        print(f"Dayun test calculation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"大运分析失败: {str(e)}"
        )

# 大运详细分析端点（无超时限制）
@router.post("/calculate-dayun-full", response_model=BaziCalculateResponse)
async def calculate_bazi_chart_dayun_full(
    request: BaziCalculateRequest
):
    """
    大运详细分析端点（无需认证，无超时限制）
    包含完整的AI分析，可能需要较长时间完成
    """
    try:
        print("🚀 Starting full detailed analysis (no timeout)...")
        result = await calculate_bazi_data(request, quick_mode=False)
        print("✅ Full detailed analysis completed successfully")
        
        # 检查和统计AI分析情况
        ai_count = 0
        total_cycles = len(result.major_cycles) if hasattr(result, 'major_cycles') else 0
        
        if hasattr(result, 'major_cycles'):
            for cycle in result.major_cycles:
                if (cycle.get('trend') or cycle.get('advice') or cycle.get('deep_analysis')):
                    ai_count += 1
        
        print(f"📊 AI Analysis Status: {ai_count}/{total_cycles} cycles have AI content")
        return result
        
    except Exception as e:
        print(f"❌ Full dayun analysis error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"大运详细分析失败: {str(e)}"
        )

# 当年运势AI分析端点
@router.post("/current-year-ai-analysis")
async def generate_current_year_ai_analysis(
    request: BaziCalculateRequest,
    force_ai: bool = True
):
    """
    专门生成当年运势的AI分析
    可以单独调用，不影响基础八字计算
    """
    try:
        # 先获取基础八字数据（快速模式）
        basic_result = await calculate_bazi_data(request, quick_mode=True)
        
        if not DEEPSEEK_AVAILABLE:
            return {
                "success": False,
                "message": "DeepSeek服务不可用",
                "detailed_analysis": {
                    "overall_analysis": "AI服务暂时不可用，请稍后重试。",
                    "note": "DeepSeek服务未配置或无法连接"
                }
            }
        
        # 调用AI分析服务
        service = deepseek_service if DEEPSEEK_AVAILABLE else None
        if service:
            bazi_data_for_analysis = {
                "bazi_characters": basic_result.bazi_characters,
                "five_elements_score": basic_result.five_elements_score,
                "day_master_strength": basic_result.day_master_strength,
                "day_master_element": basic_result.day_master_element,
                "zodiac_sign": basic_result.zodiac_sign,
                "current_year_fortune": basic_result.current_year_fortune,
                "major_cycles": basic_result.major_cycles
            }
            
            detailed_analysis = await service.generate_detailed_fortune_analysis(
                bazi_data_for_analysis, 
                str(datetime.now().year)
            )
            
            return {
                "success": True,
                "message": "AI分析生成成功",
                "detailed_analysis": detailed_analysis,
                "current_year_fortune": basic_result.current_year_fortune
            }
        else:
            return {
                "success": False,
                "message": "AI服务初始化失败",
                "detailed_analysis": {
                    "overall_analysis": "AI服务初始化失败，请联系管理员。"
                }
            }
            
    except Exception as e:
        print(f"Current year AI analysis error: {e}")
        return {
            "success": False,
            "message": f"AI分析失败: {str(e)}",
            "detailed_analysis": {
                "overall_analysis": "AI分析过程中发生错误，请稍后重试。",
                "error": str(e)
            }
        }

# 单个大运AI分析端点
@router.post("/single-dayun-analysis")
async def generate_single_dayun_analysis(
    request: BaziCalculateRequest,
    cycle_gan_zhi: str,
    cycle_start_year: str,
    cycle_end_year: str
):
    """
    为单个大运生成详细分析
    """
    try:
        # 先获取基础八字数据
        basic_result = await calculate_bazi_data(request, quick_mode=True)
        
        # 计算年龄范围
        birth_year = request.birth_datetime.year
        start_age = int(cycle_start_year) - birth_year
        end_age = int(cycle_end_year) - birth_year
        
        # 导入分析类
        from app.services.core import Bazi, StemBranch
        from app.services.analyzers import AdvancedDayunAnalyzer
        
        # 构建八字对象
        year_stem, year_branch = basic_result.bazi_characters["year_stem"], basic_result.bazi_characters["year_branch"]
        month_stem, month_branch = basic_result.bazi_characters["month_stem"], basic_result.bazi_characters["month_branch"]
        day_stem, day_branch = basic_result.bazi_characters["day_stem"], basic_result.bazi_characters["day_branch"]
        hour_stem, hour_branch = basic_result.bazi_characters["hour_stem"], basic_result.bazi_characters["hour_branch"]
        
        bazi_obj = Bazi(
            year=StemBranch(year_stem, year_branch),
            month=StemBranch(month_stem, month_branch),
            day=StemBranch(day_stem, day_branch),
            hour=StemBranch(hour_stem, hour_branch),
            gender=request.gender,
            birth_time=request.birth_datetime
        )
        
        # 使用新的分析方法
        cycle_analysis = AdvancedDayunAnalyzer.analyze_single_dayun(
            bazi_obj, cycle_gan_zhi, start_age, end_age
        )
        
        # 如果需要AI分析，可以补充
        ai_analysis = ""
        if DEEPSEEK_AVAILABLE:
            try:
                service = deepseek_service
                cycle_info = {
                    "gan_zhi": cycle_gan_zhi,
                    "start_year": cycle_start_year,
                    "end_year": cycle_end_year,
                    "age_range": {"start": start_age, "end": end_age}
                }
                prompt = build_single_dayun_prompt(basic_result, cycle_info)
                ai_analysis = await service.generate_dayun_analysis(prompt, cycle_info)
            except Exception as e:
                print(f"AI analysis error: {e}")
                ai_analysis = "AI分析暂时不可用"
        
        # 合并分析结果
        if ai_analysis:
            cycle_analysis["ai_analysis"] = ai_analysis
        
        return {
            "success": True,
            "message": f"大运 {cycle_gan_zhi} 分析生成成功",
            "analysis": cycle_analysis  # 改为 analysis 以匹配前端期望的结构
        }
            
    except Exception as e:
        print(f"Single dayun analysis error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"大运分析失败: {str(e)}",
            "analysis": {  # 改为 analysis 以匹配前端期望的结构
                "gan_zhi": cycle_gan_zhi,
                "trend": "分析失败",
                "advice": f"大运分析过程中发生错误：{str(e)}",
                "deep_analysis": f"错误详情：{str(e)}",
                "error": str(e)
            }
        }

def build_single_dayun_prompt(bazi_result, cycle_info):
    """构建单个大运分析的提示词"""
    
    # 提取关键信息
    bazi_chars = bazi_result.bazi_characters
    year_pillar = f"{bazi_chars.get('year_stem', '')}{bazi_chars.get('year_branch', '')}"
    month_pillar = f"{bazi_chars.get('month_stem', '')}{bazi_chars.get('month_branch', '')}"
    day_pillar = f"{bazi_chars.get('day_stem', '')}{bazi_chars.get('day_branch', '')}"
    hour_pillar = f"{bazi_chars.get('hour_stem', '')}{bazi_chars.get('hour_branch', '')}"
    
    day_master = bazi_result.day_master_element
    day_strength = bazi_result.day_master_strength
    zodiac = bazi_result.zodiac_sign
    
    # 五行得分
    five_elements = bazi_result.five_elements_score
    elements_str = "、".join([f"{k}:{v}" for k, v in five_elements.items()])
    
    cycle_gan_zhi = cycle_info.get('gan_zhi', '')
    start_year = cycle_info.get('start_year', '')
    end_year = cycle_info.get('end_year', '')
    
    prompt = f"""请作为资深八字命理师，为以下命盘的特定大运进行专业分析：

【命盘信息】
- 四柱干支：{year_pillar}年 {month_pillar}月 {day_pillar}日 {hour_pillar}时
- 日主五行：{day_master}（{day_strength}）
- 生肖属相：{zodiac}
- 五行分布：{elements_str}

【目标大运】
- 大运干支：{cycle_gan_zhi}
- 运行时期：{start_year}年-{end_year}年

【分析要求】
请针对这个特定大运进行深度分析，包含以下方面：

1. **大运特征分析**
   - 分析{cycle_gan_zhi}大运的五行属性和基本特征
   - 与原命盘的生克关系和互动影响
   - 这个大运的整体吉凶性质

2. **十年运势走向**
   - 前期（{start_year}-{int(start_year)+3}年）运势特点
   - 中期（{int(start_year)+4}-{int(start_year)+6}年）发展状况  
   - 后期（{int(start_year)+7}-{end_year}年）收获阶段

3. **具体领域影响**
   - 事业发展：职业机遇、升迁可能、事业转换
   - 财富状况：收入变化、投资理财、财运起伏
   - 感情婚姻：情感机遇、婚姻状况、人际关系
   - 健康状况：身体变化、易患疾病、养生重点

4. **实用指导建议**
   - 这十年的发展策略和重点方向
   - 需要特别注意的时间节点
   - 趋吉避凶的具体方法
   - 五行调节和环境配置建议

请提供详细且实用的分析，字数控制在800-1200字，语言专业但通俗易懂。"""

    return prompt

# 调试大运互动分析的专用端点
@router.post("/debug-dayun-interaction", response_model=BaziCalculateResponse)
async def debug_dayun_interaction_endpoint(
    request: BaziCalculateRequest
):
    """
    调试大运互动分析的专用端点（无需认证，完整模式）
    """
    try:
        print("=== 调试大运互动分析端点被调用 ===")
        result = await calculate_bazi_data(request, quick_mode=False)
        print("=== 大运互动分析端点处理完成 ===")
        return result
    except Exception as e:
        print(f"调试大运互动分析发生错误: {e}")
        import traceback
        print(f"错误追踪: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"调试大运互动分析失败: {str(e)}"
        )

# 临时调试端点
@router.get("/debug-test")
async def debug_test():
    """
    临时调试端点，用于测试路由是否正常工作
    """
    return {"status": "ok", "message": "路由工作正常"}

@router.post("/debug-post")
async def debug_post(data: dict):
    """
    临时调试POST端点
    """
    return {"status": "ok", "received_data": data}

# 扩展的八字计算请求模型，支持外部参考起运信息
class BaziCalculateWithReferenceRequest(BaseModel):
    """支持外部参考起运信息的八字计算请求"""
    bazi_request: BaziCalculateRequest
    reference_start_age: Optional[str] = None  # 例如："8年0月4天16时"
    reference_start_date: Optional[str] = None  # 例如："1998年5月3日"

@router.post("/test-calculate-with-reference", response_model=BaziCalculateResponse)
async def test_calculate_bazi_with_reference(
    request: BaziCalculateWithReferenceRequest
):
    """
    测试用八字排盘端点，支持外部参考起运信息，无需认证。
    """
    try:
        # 调用八字计算服务
        bazi_result = await calculate_bazi_data(
            request.bazi_request,
            quick_mode=False
        )
        return bazi_result
    except HTTPException as e:
        print(f"HTTPException caught in test bazi_api with reference: Status={e.status_code}, Detail={e.detail}")
        raise e
    except Exception as e:
        print(f"测试八字排盘（含参考）发生未知错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"测试八字排盘（含参考）发生未知错误: {e}"
        )

@router.post("/master-fortune-analysis")
async def generate_master_fortune_analysis_endpoint(
    request: BaziCalculateRequest,
    target_year: int = 2025
):
    """
    生成命理大师级全面运势分析
    """
    try:
        # 获取基础八字数据
        basic_result = await calculate_bazi_data(request, quick_mode=False)
        
        # 构建八字对象
        year_stem, year_branch = basic_result.bazi_characters["year_stem"], basic_result.bazi_characters["year_branch"]
        month_stem, month_branch = basic_result.bazi_characters["month_stem"], basic_result.bazi_characters["month_branch"]
        day_stem, day_branch = basic_result.bazi_characters["day_stem"], basic_result.bazi_characters["day_branch"]
        hour_stem, hour_branch = basic_result.bazi_characters["hour_stem"], basic_result.bazi_characters["hour_branch"]
        
        bazi_obj = Bazi(
            year=StemBranch(year_stem, year_branch),
            month=StemBranch(month_stem, month_branch),
            day=StemBranch(day_stem, day_branch),
            hour=StemBranch(hour_stem, hour_branch),
            gender=request.gender,
            birth_time=request.birth_datetime
        )
        
        # 准备分析数据
        analysis_data = {
            "day_master_strength": basic_result.day_master_strength,
            "day_master_element": basic_result.day_master_element,
            "five_elements_score": basic_result.five_elements_score,
            "major_cycles": basic_result.major_cycles,
            "zodiac_sign": basic_result.zodiac_sign,
            "palace_info": basic_result.palace_info
        }
        
        # 生成大师级分析
        try:
            if deepseek_service is None:
                raise ValueError("DeepSeek service not available")
                
            service = deepseek_service
            master_analysis = await service.generate_master_fortune_analysis(
                bazi_obj, analysis_data, target_year
            )
            
            return {
                "success": True,
                "message": f"{target_year}年命理大师级分析生成成功",
                "analysis_type": "master_level",
                "target_year": target_year,
                "fortune_analysis": master_analysis
            }
            
        except Exception as e:
            print(f"Master analysis error: {e}")
            import traceback
            traceback.print_exc()
            # 返回基础分析作为备用
            return {
                "success": True,
                "message": "返回基础运势分析",
                "analysis_type": "basic_fallback", 
                "target_year": target_year,
                "fortune_analysis": {
                    "overall_fortune": {
                        "summary": f"{target_year}年整体运势平稳，适合稳中求进",
                        "score": "75",
                        "key_themes": ["稳定发展", "机遇把握"]
                    }
                }
            }
            
    except Exception as e:
        print(f"Master fortune analysis endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"分析失败: {str(e)}",
            "error": str(e)
        }

@router.post("/dayun-deep-analysis")
async def generate_dayun_deep_analysis_endpoint(
    request: BaziCalculateRequest,
    dayun_gan_zhi: str,
    start_age: int,
    end_age: int
):
    """
    生成大运周期深度分析
    """
    try:
        # 获取基础八字数据
        basic_result = await calculate_bazi_data(request, quick_mode=False)
        
        # 构建八字对象
        year_stem, year_branch = basic_result.bazi_characters["year_stem"], basic_result.bazi_characters["year_branch"]
        month_stem, month_branch = basic_result.bazi_characters["month_stem"], basic_result.bazi_characters["month_branch"]
        day_stem, day_branch = basic_result.bazi_characters["day_stem"], basic_result.bazi_characters["day_branch"]
        hour_stem, hour_branch = basic_result.bazi_characters["hour_stem"], basic_result.bazi_characters["hour_branch"]
        
        bazi_obj = Bazi(
            year=StemBranch(year_stem, year_branch),
            month=StemBranch(month_stem, month_branch),
            day=StemBranch(day_stem, day_branch),
            hour=StemBranch(hour_stem, hour_branch),
            gender=request.gender,
            birth_time=request.birth_datetime
        )
        
        # 准备大运信息
        dayun_info = {
            "gan_zhi": dayun_gan_zhi,
            "start_age": start_age,
            "end_age": end_age
        }
        
        # 准备分析数据
        analysis_data = {
            "day_master_strength": basic_result.day_master_strength,
            "day_master_element": basic_result.day_master_element,
            "five_elements_score": basic_result.five_elements_score
        }
        
        # 生成深度大运分析
        try:
            if deepseek_service is None:
                raise ValueError("DeepSeek service not available")
                
            service = deepseek_service
            dayun_analysis = await service.generate_dayun_deep_analysis(
                bazi_obj, dayun_info, analysis_data
            )
            
            return {
                "success": True,
                "message": f"大运 {dayun_gan_zhi} 深度分析生成成功",
                "analysis_type": "deep_dayun",
                "dayun_info": dayun_info,
                "dayun_analysis": dayun_analysis
            }
            
        except Exception as e:
            print(f"Deep dayun analysis error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "message": f"大运深度分析失败: {str(e)}",
                "error": str(e)
            }
            
    except Exception as e:
        print(f"Dayun deep analysis endpoint error: {e}")
        return {
            "success": False,
            "message": f"分析失败: {str(e)}",
            "error": str(e)
        }

@router.post("/test-simple")
async def test_simple_bazi():
    """
    最简单的测试端点，检查基础功能
    """
    try:
        # Test imports
        from app.schemas.bazi import BaziCalculateRequest
        from app.services.bazi_calculator import calculate_bazi_data
        
        return {"status": "ok", "message": "导入成功"}
    except Exception as e:
        return {"status": "error", "message": f"导入失败: {e}"}

@router.post("/test-model")
async def test_model_validation(request: BaziCalculateRequest):
    """
    测试Pydantic模型验证
    """
    try:
        return {
            "status": "ok", 
            "message": "模型验证成功",
            "received_data": {
                "gender": request.gender,
                "birth_datetime": request.birth_datetime.isoformat(),
                "birth_place": request.birth_place
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"模型验证失败: {e}"}

@router.post("/test-calculation")
async def test_calculation(request: BaziCalculateRequest):
    """
    测试实际计算功能
    """
    try:
        from app.services.bazi_calculator import calculate_bazi_data
        
        print(f"🚀 测试计算: 收到请求 - {request}")
        
        # 尝试调用计算函数
        result = await calculate_bazi_data(request, quick_mode=True)
        
        print(f"✅ 计算成功: {type(result)}")
        
        return {
            "status": "ok", 
            "message": "计算成功",
            "result_type": str(type(result)),
            "result_keys": list(result.__dict__.keys()) if hasattr(result, '__dict__') else "No __dict__"
        }
    except Exception as e:
        print(f"❌ 计算失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error", 
            "message": f"计算失败: {e}",
            "error_type": str(type(e))
        }

@router.post("/test-full-response", response_model=BaziCalculateResponse)
async def test_full_response(request: BaziCalculateRequest):
    """
    测试完整响应，使用response_model
    """
    try:
        from app.services.bazi_calculator import calculate_bazi_data
        
        print(f"🚀 测试完整响应: 收到请求")
        
        # 调用计算函数
        result = await calculate_bazi_data(request, quick_mode=True)
        
        print(f"✅ 计算成功，准备返回...")
        
        # 直接返回结果，让FastAPI处理序列化
        return result
        
    except Exception as e:
        print(f"❌ 计算失败: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"计算失败: {e}"
        )

@router.post("/test-debug-result")
async def test_debug_result(request: BaziCalculateRequest):
    """
    调试响应数据，查看哪个字段有问题
    """
    try:
        from app.services.bazi_calculator import calculate_bazi_data
        import json
        
        # 调用计算函数
        result = await calculate_bazi_data(request, quick_mode=True)
        
        # 尝试将每个字段单独序列化
        debug_info = {}
        
        for field_name in result.__dict__.keys():
            try:
                field_value = getattr(result, field_name)
                # 尝试JSON序列化
                json.dumps(field_value, ensure_ascii=False, default=str)
                debug_info[field_name] = {"status": "ok", "type": str(type(field_value))}
            except Exception as e:
                debug_info[field_name] = {"status": "error", "error": str(e), "type": str(type(field_value))}
        
        return {
            "status": "debug_completed",
            "field_analysis": debug_info
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

@router.post("/test-no-response-model")
async def test_no_response_model(request: BaziCalculateRequest):
    """
    测试不使用response_model的响应
    """
    try:
        from app.services.bazi_calculator import calculate_bazi_data
        
        # 调用计算函数
        result = await calculate_bazi_data(request, quick_mode=True)
        
        # 手动转换为字典
        result_dict = {}
        for field_name in result.__dict__.keys():
            result_dict[field_name] = getattr(result, field_name)
        
        return result_dict
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}