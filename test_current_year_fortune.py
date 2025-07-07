import requests
import json
import sys

def test_current_year_fortune():
    """测试当年运势功能"""
    
    # 测试数据
    test_data = {
        'name': '测试用户',
        'gender': '女',
        'birth_datetime': '1990-04-29T10:30:00+08:00',
        'birth_place': '北京',
        'is_solar_time': True
    }
    
    print("=" * 50)
    print("测试当年运势功能")
    print("=" * 50)
    
    try:
        print("🚀 发送API请求...")
        response = requests.post(
            'http://localhost:8000/api/v1/bazi/calculate-test',
            headers={'Content-Type': 'application/json'},
            json=test_data,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            
            # 检查当年运势字段
            current_year_fortune = result.get('current_year_fortune')
            
            if current_year_fortune:
                print("✅ current_year_fortune字段存在!")
                print(f"📅 年份: {current_year_fortune.get('year', '未知')}")
                print(f"🔮 干支: {current_year_fortune.get('gan_zhi', '未知')}")
                print(f"⭐ 十神: {current_year_fortune.get('ten_god', '未知')}")
                print(f"📝 基础分析: {current_year_fortune.get('analysis', '无')[:100]}...")
                
                # 检查详细分析
                detailed_analysis = current_year_fortune.get('detailed_analysis', {})
                if detailed_analysis:
                    print("✅ detailed_analysis字段存在!")
                    analysis_fields = [
                        'overall_fortune', 'career_wealth', 'love_marriage', 
                        'health', 'strategic_guidance', 'practical_advice'
                    ]
                    
                    for field in analysis_fields:
                        value = detailed_analysis.get(field, '无')
                        print(f"  📋 {field}: {value[:50]}...")
                        
                    # 检查特殊组合
                    special_combinations = current_year_fortune.get('special_combinations', {})
                    if special_combinations:
                        print("✅ special_combinations字段存在!")
                        print(f"  🔥 岁运并临: {special_combinations.get('sui_yun_bing_lin', False)}")
                        print(f"  ⚡ 天克地冲: {special_combinations.get('tian_ke_di_chong', False)}")
                else:
                    print("❌ detailed_analysis字段不存在或为空")
                    
            else:
                print("❌ current_year_fortune字段不存在!")
                print("📋 响应中的字段:", list(result.keys()))
                
                # 保存响应到文件以便调试
                with open('api_response_debug.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print("📄 完整响应已保存到 api_response_debug.json")
                
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("请确保后端服务器在 http://localhost:8000 运行")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 发生异常: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    test_current_year_fortune()
