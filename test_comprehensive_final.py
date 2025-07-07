#!/usr/bin/env python3
"""
Comprehensive test of all new features
"""
import requests
import json

def test_comprehensive_features():
    print("🎯 八字系统功能完整性测试")
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
        
        # Test core functionality
        print("1️⃣ 核心八字功能:")
        bazi_chars = result.get('bazi_characters', {})
        print(f"   📅 八字: {bazi_chars.get('year_stem', '')}{bazi_chars.get('year_branch', '')} {bazi_chars.get('month_stem', '')}{bazi_chars.get('month_branch', '')} {bazi_chars.get('day_stem', '')}{bazi_chars.get('day_branch', '')} {bazi_chars.get('hour_stem', '')}{bazi_chars.get('hour_branch', '')}")
        print(f"   🐲 生肖: {result.get('zodiac_sign', '未知')}")
        print(f"   💪 日主强度: {result.get('day_master_strength', '未知')}")
        
        # Test new Chang Sheng functionality
        print("\n2️⃣ 十二长生功能:")
        day_cs = result.get('day_chang_sheng', [])
        year_cs = result.get('year_chang_sheng', [])
        
        print(f"   🌸 日主长生: {[cs.get('char', '未知') for cs in day_cs]}")
        print(f"   🎋 年干长生: {[cs.get('char', '未知') for cs in year_cs]}")
        
        # Test major cycles with Chang Sheng
        print("\n3️⃣ 大运长生功能:")
        major_cycles = result.get('major_cycles', [])
        print(f"   📊 大运数量: {len(major_cycles)}")
        
        if major_cycles:
            first_cycle = major_cycles[0]
            big_cs = first_cycle.get('big_cs', {})
            print(f"   🔮 第一大运: {first_cycle.get('gan_zhi', '未知')} - 长生: {big_cs.get('char', '未知')}")
        
        # Test ShenSha functionality
        print("\n4️⃣ 神煞功能:")
        shensha = result.get('shen_sha_details', [])
        if shensha:
            shensha_count = len(shensha)
            print(f"   ⭐ 神煞数量: {shensha_count}")
            if shensha_count > 0:
                sample_shensha = shensha[0]
                print(f"   🌟 示例神煞: {sample_shensha.get('name', '未知')} - {sample_shensha.get('position', '未知')}")
        else:
            print("   ⚠️  神煞数据为空")
        
        # Test additional features
        print("\n5️⃣ 其他功能:")
        print(f"   🏠 出生地: {result.get('birth_place', '未知')}")
        print(f"   🏛️  宫位信息: {'✅' if result.get('palace_info') else '❌'}")
        print(f"   🎵 纳音: {'✅' if result.get('na_yin') else '❌'}")
        print(f"   🔥 五行得分: {'✅' if result.get('five_elements_score') else '❌'}")
        
        # Overall assessment
        print("\n📊 功能完整性评估:")
        core_features = all([
            result.get('bazi_characters'),
            result.get('zodiac_sign'),
            result.get('day_master_strength')
        ])
        
        changsheng_features = all([
            result.get('day_chang_sheng'),
            result.get('year_chang_sheng'),
            major_cycles and major_cycles[0].get('big_cs')
        ])
        
        shensha_features = bool(result.get('shen_sha_details'))
        
        print(f"   ✅ 核心八字功能: {'通过' if core_features else '失败'}")
        print(f"   ✅ 十二长生功能: {'通过' if changsheng_features else '失败'}")
        print(f"   ✅ 神煞计算功能: {'通过' if shensha_features else '失败'}")
        
        overall_pass = core_features and changsheng_features and shensha_features
        print(f"\n🎉 总体评估: {'🟢 全部功能正常' if overall_pass else '🟡 部分功能需要改进'}")
        
        return overall_pass
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    test_comprehensive_features()
