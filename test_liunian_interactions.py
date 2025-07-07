#!/usr/bin/env python3
"""
流年互动分析功能测试脚本
测试新的 special_combinations 和 predicted_events 功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from backend.app.schemas.bazi import BaziCalculateRequest
from backend.app.services.bazi_calculator import calculate_bazi_data
import json
import asyncio

async def test_liunian_interactions():
    """测试流年互动分析功能"""
    print("=== 流年互动分析功能测试 ===\n")
    
    # 测试案例：选择一些有特殊互动关系的八字
    test_cases = [
        {
            "name": "案例1 - 天克地冲测试",
            "birth_datetime": datetime(1984, 2, 15, 14, 30),  # 甲子年丙寅月己卯日辛未时
            "gender": "男",
            "description": "测试2025年乙巳流年与命局的互动"
        },
        {
            "name": "案例2 - 岁运并临测试", 
            "birth_datetime": datetime(1985, 3, 20, 10, 15),  # 乙丑年己卯月癸酉日甲寅时
            "gender": "女",
            "description": "测试特殊组合情况"
        },
        {
            "name": "案例3 - 地支六合测试",
            "birth_datetime": datetime(1980, 11, 25, 16, 45),  # 庚申年丁亥月壬子日戊申时
            "gender": "男", 
            "description": "测试2025年乙巳与命局的合化关系"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"{i}. {case['name']}")
        print(f"   {case['description']}")
        print("-" * 60)
        
        try:
            # 创建请求
            request = BaziCalculateRequest(
                name=case['name'],
                birth_datetime=case['birth_datetime'],
                gender=case['gender'],
                birth_place="北京",
                is_solar_time=True,
                longitude=116.4,
                latitude=39.9,
                timezone_offset=8
            )
            
            # 计算八字
            result = await calculate_bazi_data(request)
            
            # 显示基本信息
            print(f"八字: {result.bazi_characters['year_stem']}{result.bazi_characters['year_branch']} "
                  f"{result.bazi_characters['month_stem']}{result.bazi_characters['month_branch']} "
                  f"{result.bazi_characters['day_stem']}{result.bazi_characters['day_branch']} "
                  f"{result.bazi_characters['hour_stem']}{result.bazi_characters['hour_branch']}")
            
            if result.current_year_fortune:
                fortune = result.current_year_fortune
                
                print(f"流年: {fortune['gan_zhi']} ({fortune['ten_god_relation']})")
                print(f"当前大运: {fortune.get('current_dayun', '未知')}")
                
                # 显示流年互动分析
                if 'liunian_interactions' in fortune:
                    interactions = fortune['liunian_interactions']
                    print(f"\n【流年互动分析】")
                    print(f"综合评估: {interactions.get('overall_assessment', '无')}")
                    
                    if interactions.get('harmonies'):
                        print(f"和谐关系: {'; '.join(interactions['harmonies'])}")
                    
                    if interactions.get('conflicts'): 
                        print(f"冲突关系: {'; '.join(interactions['conflicts'])}")
                    
                    if interactions.get('punishments'):
                        print(f"刑罚关系: {'; '.join(interactions['punishments'])}")
                    
                    if interactions.get('harms'):
                        print(f"相害关系: {'; '.join(interactions['harms'])}")
                    
                    if interactions.get('special_combinations'):
                        print(f"特殊组合: {'; '.join(interactions['special_combinations'])}")
                
                # 显示流年神煞
                if 'liunian_shensha' in fortune and fortune['liunian_shensha']:
                    print(f"\n【流年神煞】")
                    for shensha in fortune['liunian_shensha'][:3]:  # 只显示前3个
                        print(f"• {shensha['name']}: {shensha['description'][:30]}...")
                
                # 显示特殊组合分析
                if 'special_combinations' in fortune:
                    special = fortune['special_combinations']
                    print(f"\n【特殊组合判断】")
                    print(f"岁运并临: {'是' if special.get('sui_yun_bing_lin') else '否'}")
                    print(f"天克地冲: {'是' if special.get('tian_ke_di_chong') else '否'}")
                    print(f"岁运相冲: {'是' if special.get('sui_yun_xiang_chong') else '否'}")
                    
                    if special.get('special_warnings'):
                        print(f"特别提醒: {'; '.join(special['special_warnings'][:2])}")
                    
                    if special.get('favorable_combinations'):
                        print(f"有利组合: {'; '.join(special['favorable_combinations'][:2])}")
                
                # 显示详细预测事件
                if 'predicted_events' in fortune:
                    events = fortune['predicted_events']
                    print(f"\n【详细预测事件】")
                    
                    if events.get('career'):
                        print(f"事业预测: {events['career'][0]}")
                    
                    if events.get('wealth'):
                        print(f"财运预测: {events['wealth'][0]}")
                    
                    if events.get('health'):
                        print(f"健康预测: {events['health'][0]}")
                    
                    if events.get('relationship'):
                        print(f"感情预测: {events['relationship'][0]}")
            
            print("\n" + "="*80 + "\n")
            
        except Exception as e:
            print(f"计算失败: {e}")
            import traceback
            traceback.print_exc()
            print("\n" + "="*80 + "\n")

async def test_specific_interactions():
    """测试特定的互动关系"""
    print("=== 特定互动关系测试 ===\n")
    
    # 导入计算器进行单独测试
    from backend.app.services.calculators import FiveElementsCalculator
    from backend.app.services.core import Bazi, StemBranch
    
    # 创建测试八字：甲子年丙寅月己卯日辛未时
    test_bazi = Bazi(
        year=StemBranch("甲", "子"),
        month=StemBranch("丙", "寅"),
        day=StemBranch("己", "卯"),
        hour=StemBranch("辛", "未"),
        gender="男",
        birth_time=datetime(1984, 2, 15, 14, 30)
    )
    
    # 测试2025年乙巳流年
    liunian_gan = "乙"
    liunian_zhi = "巳"
    dayun_gan = "丁"
    dayun_zhi = "巳"
    
    print(f"命局: 甲子 丙寅 己卯 辛未")
    print(f"流年: {liunian_gan}{liunian_zhi}")
    print(f"大运: {dayun_gan}{dayun_zhi}")
    print("-" * 40)
    
    # 分析互动关系
    interactions = FiveElementsCalculator.analyze_liunian_interactions(
        test_bazi, liunian_gan, liunian_zhi, dayun_gan, dayun_zhi
    )
    
    print("【互动分析结果】")
    print(f"综合评估: {interactions['overall_assessment']}")
    
    if interactions['stem_interactions']:
        print(f"天干互动: {interactions['stem_interactions']}")
    
    if interactions['harmonies']:
        print(f"合化关系: {interactions['harmonies']}")
    
    if interactions['conflicts']:
        print(f"冲突关系: {interactions['conflicts']}")
    
    if interactions['punishments']:
        print(f"刑罚关系: {interactions['punishments']}")
    
    if interactions['harms']:
        print(f"相害关系: {interactions['harms']}")
    
    if interactions['special_combinations']:
        print(f"特殊组合: {interactions['special_combinations']}")
    
    print(f"\n统计: 合{len(interactions['harmonies'])}个, 冲{len(interactions['conflicts'])}个, "
          f"刑{len(interactions['punishments'])}个, 害{len(interactions['harms'])}个")

async def main():
    """主测试函数"""
    print("开始测试流年互动分析功能...\n")
    
    try:
        # 测试完整API集成
        await test_liunian_interactions()
        
        # 测试特定互动
        await test_specific_interactions()
        
        print("✅ 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
