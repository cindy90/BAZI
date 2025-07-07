"""
八字计算模块 - 模块化版本
整合核心功能，保持向后兼容
"""

# 主要计算函数
from .main import calculate_bazi_data

# 核心数据结构
from .core import Bazi, StemBranch, DaYun, ShenSha, FortuneModel

# 计算引擎
from .calculators import ShenShaCalculator, FiveElementsCalculator

# 分析引擎
from .analyzers import (
    EventDeductionEngine, 
    AdvancedDayunAnalyzer, 
    AdvancedEventEngine
)

# 提示管理器
from .prompt_manager import PromptManager

# 工具函数
from .utils import (
    safe_get_name, safe_get_method_result, analyze_dayun_phase,
    self_calculate_ten_god, get_zhi_hidden_gan, 
    analyze_dayun_interaction_with_mingju, calculate_precise_dayun_start,
    get_location_info, get_solar_terms_for_year, calculate_precise_dayun,
    format_dayun_info, JIAZI
)

# 向后兼容性导出
__all__ = [
    # 主函数
    'calculate_bazi_data',
    
    # 核心类
    'Bazi', 'StemBranch', 'DaYun', 'ShenSha', 'FortuneModel',
    
    # 计算器
    'ShenShaCalculator', 'FiveElementsCalculator',
    
    # 分析器  
    'EventDeductionEngine', 'AdvancedDayunAnalyzer', 'AdvancedEventEngine',
    
    # 提示管理器
    'PromptManager',
    
    # 工具函数
    'safe_get_name', 'safe_get_method_result', 'analyze_dayun_phase',
    'self_calculate_ten_god', 'get_zhi_hidden_gan', 
    'analyze_dayun_interaction_with_mingju', 'calculate_precise_dayun_start',
    'get_location_info', 'get_solar_terms_for_year', 'calculate_precise_dayun',
    'format_dayun_info', 'JIAZI'
]
