# backend/app/api/v1/iching.py
"""
易经算卦 API 路由
提供易经六十四卦的算卦和解卦功能
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
from datetime import datetime

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.iching import IChingDivinationRequest, IChingDivinationResponse
from app.services.iching_calculator import perform_iching_divination

router = APIRouter(prefix="/iching", tags=["易经算卦"])

@router.post("/divine", response_model=IChingDivinationResponse)
async def divine_iching(
    request: IChingDivinationRequest,
    current_user: Any = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    易经算卦
    
    根据用户提供的问题和算卦方式进行易经占卜，返回卦象和解读。
    需要用户登录才能使用。
    
    Args:
        request: 算卦请求数据，包含问题、算卦方式等信息
        current_user: 当前登录用户（通过依赖注入获取）
        db: 数据库会话（通过依赖注入获取）
    
    Returns:
        IChingDivinationResponse: 包含卦象、爻辞、解读等完整算卦结果
    
    Raises:
        HTTPException: 当算卦过程中发生错误时抛出
    """
    try:
        # 调用易经算卦服务
        divination_result = await perform_iching_divination(request)
        return divination_result
        
    except HTTPException as e:
        # 重新抛出服务层的 HTTPException
        print(f"易经算卦 HTTPException: Status={e.status_code}, Detail={e.detail}")
        raise e
        
    except Exception as e:
        # 捕获其他未知错误并转换为 HTTP 500 错误
        print(f"易经算卦发生未知错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"易经算卦发生未知错误: {str(e)}"
        )

@router.get("/hexagrams")
async def get_hexagram_list(
    current_user: Any = Depends(get_current_user)
):
    """
    获取六十四卦列表
    
    返回完整的易经六十四卦基本信息，供用户参考。
    
    Returns:
        dict: 包含六十四卦的基本信息
    """
    try:
        # 这里可以返回六十四卦的基本信息
        # 暂时返回简化版本，后续可以扩展
        return {
            "message": "六十四卦列表功能",
            "description": "此功能可用于获取完整的易经六十四卦信息",
            "status": "coming_soon"
        }
        
    except Exception as e:
        print(f"获取卦象列表错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取卦象列表发生错误: {str(e)}"
        )

@router.post("/test-divine", response_model=dict)
async def test_divine_iching(request: IChingDivinationRequest):
    """
    测试易经算卦功能 (无需认证)
    
    用于测试易经算卦服务是否正常工作，不需要用户认证。
    """
    try:
        # 调用易经算卦服务
        divination_result = await perform_iching_divination(request)
        
        return {
            "status": "success",
            "message": "易经算卦测试成功",
            "result": divination_result.model_dump()
        }
        
    except Exception as e:
        print(f"测试易经算卦错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"测试易经算卦发生错误: {str(e)}"
        )