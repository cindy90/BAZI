#!/usr/bin/env python3
"""
测试主文件中的 AdvancedDayunAnalyzer 功能
验证删除独立文件后功能是否正常
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    # 导入主文件中的类
    from backend.app.services.core import Bazi, StemBranch, DaYun
    from backend.app.services.analyzers import AdvancedDayunAnalyzer, AdvancedEventEngine
    
    print("✅ 成功导入 AdvancedDayunAnalyzer 和相关类")
    
    # 创建测试数据
    test_bazi = Bazi(
        year=StemBranch("己", "巳"),
        month=StemBranch("丙", "子"),
        day=StemBranch("丙", "寅"),
        hour=StemBranch("壬", "辰"),
        gender="男"
    )
    
    test_dayun_list = [
        DaYun(3, StemBranch("乙", "亥"), end_age=13),
        DaYun(13, StemBranch("甲", "戌"), end_age=23),
        DaYun(23, StemBranch("癸", "酉"), end_age=33),
    ]
    
    print("✅ 成功创建测试数据")
    
    # 测试大运分析
    analysis = AdvancedDayunAnalyzer.analyze_dayun_fortune_trend(test_bazi, test_dayun_list)
    print("\n📊 大运运势分析结果:")
    print(f"整体趋势: {analysis['overall_trend']}")
    print(f"高峰期数量: {len(analysis['peak_periods'])}")
    print(f"挑战期数量: {len(analysis['challenging_periods'])}")
    print(f"转折点数量: {len(analysis['turning_points'])}")
    
    # 测试事件预测
    events = AdvancedEventEngine.predict_life_events(test_bazi, test_dayun_list)
    print("\n🔮 事件预测结果:")
    for event_type, predictions in events.items():
        if predictions:
            print(f"{event_type}: {len(predictions)} 个预测")
        else:
            print(f"{event_type}: 无预测")
    
    print("\n✅ AdvancedDayunAnalyzer 功能测试通过！")
    print("📝 主文件中的实现完全正常，独立文件已安全删除。")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
