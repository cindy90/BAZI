#!/usr/bin/env python3
"""
Test API endpoint directly
"""
import requests
import json
from datetime import datetime

def test_api_endpoint():
    print("🌐 Testing API endpoint directly...")
    
    # Test data
    test_data = {
        "gender": "男",
        "birth_datetime": "1990-04-29T12:00:00+08:00",
        "birth_place": "北京"
    }
    
    # Test the endpoint
    url = "http://localhost:8000/api/v1/bazi/test-calculate"
    
    try:
        print(f"📡 Sending POST request to: {url}")
        print(f"📦 Data: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            url, 
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print(f"🎯 Response keys: {list(result.keys())}")
            if 'bazi_characters' in result:
                print(f"🔮 八字: {result['bazi_characters']}")
            if 'day_chang_sheng' in result:
                print(f"🌸 日主长生: {result['day_chang_sheng']}")
        else:
            print(f"❌ API call failed!")
            print(f"📝 Response text: {response.text}")
            
            # Try to get more detailed error info
            try:
                error_detail = response.json()
                print(f"🔍 Error details: {json.dumps(error_detail, ensure_ascii=False, indent=2)}")
            except:
                print("🔍 Could not parse error as JSON")
                
    except requests.exceptions.RequestException as e:
        print(f"🌐 Network error: {e}")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

if __name__ == "__main__":
    test_api_endpoint()
