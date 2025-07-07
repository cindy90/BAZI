#!/usr/bin/env python3
"""
Test the no-response-model endpoint
"""
import requests

def test_no_response_model():
    data = {
        "gender": "男",
        "birth_datetime": "1990-04-29T12:00:00+08:00",
        "birth_place": "北京"
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/bazi/test-no-response-model",
        json=data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success! Response has {len(result)} fields")
        print(f"Key fields present: {['bazi_characters' in result, 'day_chang_sheng' in result, 'shen_sha_details' in result]}")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    test_no_response_model()
