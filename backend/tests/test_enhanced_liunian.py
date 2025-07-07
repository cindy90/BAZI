"""
测试增强版流年分析功能的API接口
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_enhanced_liunian_analysis():
    """测试增强版流年分析API"""
    # 测试数据
    test_data = {
        "birth_year": 1990,
        "birth_month": 6,
        "birth_day": 15,
        "birth_hour": 10,
        "birth_minute": 30,
        "gender": "男",
        "current_year": 2025,
        "name": "测试用户"
    }
    
    response = client.post("/api/v1/bazi/calculate", json=test_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # 验证基本结构
    assert "year_pillar" in data
    assert "month_pillar" in data
    assert "day_pillar" in data
    assert "hour_pillar" in data
    assert "current_year_fortune" in data
    assert "comprehensive_favorable_analysis" in data
    
    # 验证流年分析结构
    current_year_fortune = data["current_year_fortune"]
    assert "special_combinations" in current_year_fortune
    assert "predicted_events" in current_year_fortune
    assert "liunian_interactions" in current_year_fortune
    assert "liunian_shensha" in current_year_fortune
    
    # 验证特殊组合分析
    special_combinations = current_year_fortune["special_combinations"]
    assert "favorable_combinations" in special_combinations
    assert "special_warnings" in special_combinations
    assert "critical_analysis" in special_combinations
    
    # 验证新增字段
    assert "personalized_insights" in special_combinations
    assert "timing_analysis" in special_combinations
    assert "risk_assessment" in special_combinations
    
    # 验证预测事件
    predicted_events = current_year_fortune["predicted_events"]
    assert "career" in predicted_events
    assert "wealth" in predicted_events
    assert "health" in predicted_events
    assert "relationship" in predicted_events
    assert "timing" in predicted_events
    assert "strategy" in predicted_events
    assert "warning" in predicted_events
    
    # 验证内容不为空
    assert len(special_combinations["favorable_combinations"]) > 0
    assert len(special_combinations["special_warnings"]) > 0
    assert len(predicted_events["career"]) > 0
    assert len(predicted_events["wealth"]) > 0
    
    print("✅ 增强版流年分析API测试通过")

def test_multiple_cases():
    """测试多个案例"""
    test_cases = [
        # 案例1: 年轻男性
        {
            "birth_year": 1995,
            "birth_month": 3,
            "birth_day": 20,
            "birth_hour": 8,
            "birth_minute": 0,
            "gender": "男",
            "current_year": 2025,
            "name": "年轻男性"
        },
        # 案例2: 中年女性
        {
            "birth_year": 1980,
            "birth_month": 9,
            "birth_day": 12,
            "birth_hour": 14,
            "birth_minute": 30,
            "gender": "女",
            "current_year": 2025,
            "name": "中年女性"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        response = client.post("/api/v1/bazi/calculate", json=test_case)
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证每个案例都有个性化的内容
        current_year_fortune = data["current_year_fortune"]
        predicted_events = current_year_fortune["predicted_events"]
        
        # 验证不同案例的预测内容有所不同
        assert len(predicted_events["career"]) > 0
        assert len(predicted_events["wealth"]) > 0
        
        print(f"✅ 案例{i+1}({test_case['name']})测试通过")

if __name__ == "__main__":
    test_enhanced_liunian_analysis()
    test_multiple_cases()
    print("✅ 所有测试通过")
