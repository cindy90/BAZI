#!/usr/bin/env python3
"""
Test the enhanced Nayin functionality
"""
import requests
import json

def test_nayin_functionality():
    print("🎯 测试纳音五行索引功能")
    print("=" * 60)
    
    # Test data
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
        
        # Check Nayin information
        print("📊 纳音信息检查:")
        na_yin = result.get('na_yin', {})
        
        for pillar_name in ['year', 'month', 'day', 'hour']:
            key = f"{pillar_name}_na_yin"
            if key in na_yin:
                nayin_data = na_yin[key]
                
                # Check if it's the new format [name, index] or old format string
                if isinstance(nayin_data, list) and len(nayin_data) == 2:
                    nayin_name, nayin_index = nayin_data
                    print(f"   ✅ {pillar_name.upper()}柱纳音: {nayin_name} (五行索引: {nayin_index})")
                    
                    # Validate index range (0-4 for Efairy)
                    if isinstance(nayin_index, int) and 0 <= nayin_index <= 4:
                        element_names = ["木", "火", "土", "金", "水"]
                        print(f"      🌟 五行: {element_names[nayin_index]}")
                    else:
                        print(f"      ⚠️  五行索引异常: {nayin_index}")
                else:
                    print(f"   ⚠️  {pillar_name.upper()}柱纳音格式旧版: {nayin_data}")
            else:
                print(f"   ❌ 缺少 {pillar_name.upper()}柱纳音")
        
        # Check if the format matches Efairy expectations
        print("\n🎯 Efairy 兼容性检查:")
        all_new_format = True
        for pillar_name in ['year', 'month', 'day', 'hour']:
            key = f"{pillar_name}_na_yin"
            if key in na_yin:
                nayin_data = na_yin[key]
                if not (isinstance(nayin_data, list) and len(nayin_data) == 2):
                    all_new_format = False
                    break
        
        if all_new_format:
            print("   ✅ 纳音格式符合 Efairy 标准 (包含名称和五行索引)")
        else:
            print("   ⚠️  纳音格式部分兼容，建议进一步优化")
        
        # Test specific Ganzhi combinations
        print("\n🔬 特定干支纳音测试:")
        bazi_chars = result.get('bazi_characters', {})
        if bazi_chars:
            year_ganzhi = f"{bazi_chars.get('year_stem', '')}{bazi_chars.get('year_branch', '')}"
            month_ganzhi = f"{bazi_chars.get('month_stem', '')}{bazi_chars.get('month_branch', '')}"
            day_ganzhi = f"{bazi_chars.get('day_stem', '')}{bazi_chars.get('day_branch', '')}"
            hour_ganzhi = f"{bazi_chars.get('hour_stem', '')}{bazi_chars.get('hour_branch', '')}"
            
            print(f"   📅 八字: {year_ganzhi} {month_ganzhi} {day_ganzhi} {hour_ganzhi}")
            
            # Check if specific combinations match expected values
            expected_mappings = {
                "庚午": "路旁土",
                "庚辰": "白蜡金", 
                "甲子": "海中金"
            }
            
            test_combinations = [
                ("年柱", year_ganzhi, na_yin.get('year_na_yin')),
                ("月柱", month_ganzhi, na_yin.get('month_na_yin')),
                ("日柱", day_ganzhi, na_yin.get('day_na_yin')),
                ("时柱", hour_ganzhi, na_yin.get('hour_na_yin'))
            ]
            
            for pillar, ganzhi, nayin_result in test_combinations:
                if ganzhi in expected_mappings:
                    expected_nayin = expected_mappings[ganzhi]
                    if isinstance(nayin_result, list) and len(nayin_result) >= 1:
                        actual_nayin = nayin_result[0]
                        if actual_nayin == expected_nayin:
                            print(f"   ✅ {pillar} {ganzhi}: {actual_nayin} (正确)")
                        else:
                            print(f"   ❌ {pillar} {ganzhi}: 期望 {expected_nayin}, 实际 {actual_nayin}")
                    else:
                        print(f"   ⚠️  {pillar} {ganzhi}: 格式异常 {nayin_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_nayin_functionality()
