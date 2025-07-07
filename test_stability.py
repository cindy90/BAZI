#!/usr/bin/env python3
"""
测试不同生日的完整功能 - 验证系统稳定性
"""
import requests
import json
from datetime import datetime

def test_multiple_birthdates():
    print("🎯 多生日测试 - 验证系统稳定性")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "测试案例1",
            "gender": "女",
            "birth_datetime": "1985-07-15T14:30:00+08:00",
            "birth_place": "上海"
        },
        {
            "name": "测试案例2", 
            "gender": "男",
            "birth_datetime": "1992-11-23T08:45:00+08:00",
            "birth_place": "广州"
        },
        {
            "name": "测试案例3",
            "gender": "女", 
            "birth_datetime": "1978-03-06T20:15:00+08:00",
            "birth_place": "深圳"
        },
        {
            "name": "测试案例4",
            "gender": "男",
            "birth_datetime": "2000-12-31T23:59:00+08:00", 
            "birth_place": "成都"
        }
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ {test_case['name']} ({test_case['gender']}, {test_case['birth_place']})")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/bazi/test-calculate",
                json={k: v for k, v in test_case.items() if k != 'name'},
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"   ❌ API调用失败: {response.status_code}")
                continue
            
            result = response.json()
            
            # 检查关键字段
            required_fields = [
                'bazi_characters', 'zodiac_sign', 'day_master_strength',
                'five_elements_score', 'na_yin', 'dz_cang_gan',
                'day_chang_sheng', 'year_chang_sheng', 'shen_sha_details',
                'interactions', 'major_cycles'
            ]
            
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print(f"   ❌ 缺失字段: {missing_fields}")
                continue
            
            # 验证数据完整性
            bazi_chars = result['bazi_characters']
            bazi_str = f"{bazi_chars['year_stem']}{bazi_chars['year_branch']} {bazi_chars['month_stem']}{bazi_chars['month_branch']} {bazi_chars['day_stem']}{bazi_chars['day_branch']} {bazi_chars['hour_stem']}{bazi_chars['hour_branch']}"
            
            print(f"   ✅ 八字: {bazi_str}")
            print(f"   ✅ 生肖: {result['zodiac_sign']}")
            print(f"   ✅ 日主强度: {result['day_master_strength']}")
            
            # 检查纳音
            na_yin = result['na_yin']
            na_yin_valid = all(
                isinstance(na_yin[key], list) and len(na_yin[key]) == 2
                for key in ['year_na_yin', 'month_na_yin', 'day_na_yin', 'hour_na_yin']
            )
            print(f"   {'✅' if na_yin_valid else '❌'} 纳音格式: {'正确' if na_yin_valid else '错误'}")
            
            # 检查五行百分比
            five_elements = result['five_elements_score']
            total_percentage = sum(float(v.rstrip('%')) for v in five_elements.values())
            print(f"   {'✅' if abs(total_percentage - 100) < 0.1 else '❌'} 五行百分比: {total_percentage:.1f}%")
            
            # 检查十二长生
            day_cs = result['day_chang_sheng']
            year_cs = result['year_chang_sheng']
            cs_valid = len(day_cs) == 4 and len(year_cs) == 4
            print(f"   {'✅' if cs_valid else '❌'} 十二长生: {'正确' if cs_valid else '错误'}")
            
            # 检查干支互动
            interactions = result['interactions']
            interaction_types = len([k for k, v in interactions.items() if isinstance(v, list)])
            print(f"   ✅ 干支互动: {interaction_types} 类")
            
            # 检查神煞
            shen_sha = result['shen_sha_details']
            print(f"   ✅ 神煞: {len(shen_sha)} 个")
            
            # 检查大运
            major_cycles = result['major_cycles']
            print(f"   ✅ 大运: {len(major_cycles)} 步")
            
            success_count += 1
            print(f"   🎉 测试通过!")
            
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
    
    print(f"\n📊 测试结果: {success_count}/{total_count} 通过")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 所有测试案例均通过，系统稳定性良好!")
        return True
    else:
        print("⚠️  部分测试案例失败，需要进一步检查")
        return False

if __name__ == "__main__":
    test_multiple_birthdates()
