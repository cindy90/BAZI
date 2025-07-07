#!/usr/bin/env python3
"""
专门测试干支互动关系功能
"""
import requests
import json

def test_interactions():
    print("🎯 干支互动关系测试")
    print("=" * 60)
    
    # 测试数据 - 选择一个有明显互动关系的八字
    test_data = {
        "gender": "男", 
        "birth_datetime": "1990-04-29T12:00:00+08:00",
        "birth_place": "北京"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/bazi/test-calculate",
            json=test_data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ API调用失败: {response.status_code}")
            return False
        
        result = response.json()
        
        # 获取互动关系数据
        interactions = result.get('interactions', {})
        
        if not interactions:
            print("❌ 未找到互动关系数据")
            return False
        
        print("🔍 互动关系分析结果:")
        print(f"   八字: 庚午 庚辰 甲子 庚午")
        print()
        
        # 分析各种互动关系
        categories = [
            ('stem_combinations', '天干五合', '🌸'),
            ('branch_six_combinations', '地支六合', '🤝'),
            ('branch_three_half_combinations', '地支三合/半合', '🔺'),
            ('branch_six_conflicts', '地支六冲', '⚡'),
            ('branch_penalties', '地支相刑', '⚔️'),
            ('branch_harms', '地支相穿', '🗡️')
        ]
        
        total_interactions = 0
        
        for key, name, emoji in categories:
            items = interactions.get(key, [])
            count = len(items)
            total_interactions += count
            
            print(f"{emoji} {name}: {count} 个")
            
            if items:
                for item in items:
                    combo = item.get('combination', '未知')
                    element = item.get('element', '')
                    positions = item.get('positions', [])
                    penalty_type = item.get('penalty_type', '')
                    
                    if element:
                        print(f"   - {combo} 化 {element} ({' '.join(positions)})")
                    elif penalty_type:
                        print(f"   - {combo} {penalty_type} ({' '.join(positions)})")
                    else:
                        print(f"   - {combo} ({' '.join(positions)})")
        
        print()
        print(f"📊 总计互动关系: {total_interactions} 个")
        
        # 检验具体预期的互动关系
        print()
        print("🔬 具体互动关系验证:")
        
        # 庚午庚辰甲子庚午 应该有的互动
        expected_interactions = []
        
        # 午和子应该冲
        conflicts = interactions.get('branch_six_conflicts', [])
        zi_wu_conflict = any('子午' in item.get('combination', '') or '午子' in item.get('combination', '') for item in conflicts)
        print(f"   ✅ 子午冲: {'检测到' if zi_wu_conflict else '未检测到'}")
        
        # 辰和子应该有半合水
        three_half = interactions.get('branch_three_half_combinations', [])
        chen_zi_half = any('辰子' in item.get('combination', '') or '子辰' in item.get('combination', '') for item in three_half)
        print(f"   ✅ 子辰半合水: {'检测到' if chen_zi_half else '未检测到'}")
        
        # 午自刑
        penalties = interactions.get('branch_penalties', [])
        wu_self = any('午午' in item.get('combination', '') for item in penalties)
        print(f"   ✅ 午自刑: {'检测到' if wu_self else '未检测到'}")
        
        if total_interactions > 0:
            print("🎉 干支互动关系功能正常!")
            return True
        else:
            print("⚠️  干支互动关系数据为空")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_interactions()
