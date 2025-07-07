import requests
import json

def test_major_cycles_structure():
    """测试大运结构的完整性"""
    url = "http://localhost:8000/api/v1/bazi/test-calculate"
    
    data = {
        "name": "测试用户",
        "gender": "男",
        "birth_year": 1990,
        "birth_month": 4,
        "birth_day": 29,
        "birth_hour": 10,
        "birth_minute": 30,
        "birth_datetime": "1990-04-29T10:30:00",
        "is_solar_time": True,
        "birth_place": "北京市"
    }
    
    try:
        print("🚀 测试大运结构完整性...")
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            major_cycles = result.get('major_cycles', [])
            
            print(f"✅ API调用成功!")
            print(f"📊 大运数量: {len(major_cycles)}")
            
            if major_cycles:
                # 检查第一个大运的结构
                first_cycle = major_cycles[0]
                print(f"\n🎯 第一个大运结构:")
                print(json.dumps(first_cycle, ensure_ascii=False, indent=2))
                
                # 验证必需字段
                required_fields = ['gan_zhi', 'start_age', 'start_year', 'end_year']
                missing_fields = []
                for field in required_fields:
                    if field not in first_cycle:
                        missing_fields.append(field)
                
                if missing_fields:
                    print(f"❌ 缺少必需字段: {missing_fields}")
                else:
                    print(f"✅ 必需字段完整")
                
                # 检查干支是否合理
                if 'gan_zhi' in first_cycle:
                    gan_zhi = first_cycle['gan_zhi']
                    if len(gan_zhi) == 2 and not gan_zhi.startswith('大运'):
                        print(f"✅ 干支格式正确: {gan_zhi}")
                    else:
                        print(f"⚠️ 干支格式可能有问题: {gan_zhi}")
                
                # 检查年龄递增
                print(f"\n📈 大运年龄序列:")
                for i, cycle in enumerate(major_cycles[:4]):
                    start_age = cycle.get('start_age', 'N/A')
                    gan_zhi = cycle.get('gan_zhi', 'N/A')
                    print(f"  大运 {i+1}: {gan_zhi} (起运年龄: {start_age})")
                
            else:
                print("❌ 大运列表为空")
                
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求出错: {e}")

if __name__ == "__main__":
    test_major_cycles_structure()
