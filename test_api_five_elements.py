import requests
import json

def test_api_five_elements_percentage():
    """通过API测试五行百分比功能"""
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
        print("🚀 测试五行百分比API...")
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # 检查五行得分字段
            five_elements = result.get('five_elements_score', {})
            print(f"✅ API调用成功!")
            print(f"📊 五行得分: {five_elements}")
            
            # 验证是否为百分比格式
            total_percentage = 0
            for element, score_str in five_elements.items():
                if isinstance(score_str, str) and score_str.endswith('%'):
                    percentage_value = float(score_str.rstrip('%'))
                    total_percentage += percentage_value
                    print(f"  {element}: {score_str} ({percentage_value}%)")
                else:
                    print(f"  ❌ {element}: {score_str} (不是百分比格式)")
            
            print(f"\n🎯 总和: {total_percentage:.1f}%")
            
            if abs(total_percentage - 100.0) < 0.1:
                print("✅ 百分比总和验证通过! (100%)")
            else:
                print(f"❌ 百分比总和验证失败: {total_percentage}%")
                
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求出错: {e}")

if __name__ == "__main__":
    test_api_five_elements_percentage()
