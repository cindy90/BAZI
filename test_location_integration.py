#!/usr/bin/env python3
"""
测试地理位置服务集成的脚本
验证 LocationService 与 bazi_calculator 的集成效果
"""

import sys
import os
import asyncio
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "backend"))

from backend.app.services.location_service import LocationService
from backend.app.services.bazi_calculator import calculate_bazi_data
from backend.app.schemas.bazi import BaziCalculateRequest

async def test_location_service():
    """测试地理位置服务"""
    print("=" * 50)
    print("测试地理位置服务")
    print("=" * 50)
    
    location_service = LocationService()
    
    # 测试城市列表
    test_cities = [
        "北京", "上海", "广州", "深圳", "杭州", "南京", "武汉", "成都", "西安", "重庆",
        "天津", "沈阳", "长沙", "济南", "郑州", "哈尔滨", "昆明", "南昌", "福州",
        "石家庄", "太原", "呼和浩特", "长春", "南宁", "银川", "兰州", "西宁", "乌鲁木齐",
        "拉萨", "海口", "贵阳", "香港", "澳门", "苏州", "无锡", "宁波", "温州",
        "青岛", "烟台", "佛山", "东莞", "大连", "厦门", "泉州", "洛阳", "开封",
        "江门", "中山", "珠海", "汕头", "湛江", "茂名", "肇庆", "惠州", "韶关",
        "汕尾", "河源", "阳江", "清远", "潮州", "揭阳", "云浮", "梅州", "潮州市",
        "揭阳市", "云浮市", "梅州市", "台山", "新会", "开平", "恩平", "鹤山",
        "高要", "四会", "陆丰", "兴宁", "普宁", "罗定", "连州", "英德", "廉江",
        "雷州", "吴川", "高州", "化州", "信宜", "高明", "三水", "新兴", "郁南",
        "封开", "德庆", "怀集", "广宁", "四会", "台山", "新会", "开平", "恩平",
        "鹤山", "南海", "顺德", "高明", "三水", "花都", "从化", "增城", "番禺",
        "南沙", "萝岗", "黄埔", "白云", "天河", "越秀", "荔湾", "海珠", "哈尔滨市",
        "七台河", "鹤岗", "双鸭山", "鸡西", "牡丹江", "佳木斯", "大庆", "伊春",
        "黑河", "绥化", "齐齐哈尔"
    ]
    
    success_count = 0
    fail_count = 0
    
    for city in test_cities:
        try:
            info = location_service.get_location_info(city)
            if info:
                print(f"✓ {city}: {info['province']}{info['city']} ({info['longitude']:.4f}°E, {info['latitude']:.4f}°N)")
                success_count += 1
            else:
                print(f"✗ {city}: 未找到地理位置信息")
                fail_count += 1
        except Exception as e:
            print(f"✗ {city}: 查询失败 - {e}")
            fail_count += 1
    
    print(f"\n地理位置服务测试结果: 成功 {success_count}, 失败 {fail_count}")
    
    # 测试模糊匹配
    print("\n" + "=" * 50)
    print("测试模糊匹配")
    print("=" * 50)
    
    fuzzy_tests = [
        "北京市", "上海市", "广州市", "深圳市", "杭州市",
        "南京市", "武汉市", "成都市", "西安市", "重庆市",
        "江苏", "浙江", "广东", "山东", "河北", "河南",
        "湖南", "湖北", "四川", "陕西", "福建", "江西",
        "安徽", "辽宁", "吉林", "黑龙江", "内蒙古", "新疆",
        "西藏", "青海", "甘肃", "宁夏", "海南", "贵州",
        "云南", "广西", "山西", "香港特别行政区", "澳门特别行政区"
    ]
    
    for test_name in fuzzy_tests:
        try:
            info = location_service.get_location_info(test_name)
            if info:
                print(f"✓ {test_name}: {info['province']}{info['city']} ({info['longitude']:.4f}°E, {info['latitude']:.4f}°N)")
            else:
                print(f"✗ {test_name}: 未找到地理位置信息")
        except Exception as e:
            print(f"✗ {test_name}: 查询失败 - {e}")


async def test_bazi_integration():
    """测试八字计算与地理位置服务的集成"""
    print("\n" + "=" * 50)
    print("测试八字计算与地理位置服务的集成")
    print("=" * 50)
    
    # 测试用例
    test_cases = [
        {
            "name": "张三",
            "gender": "男",
            "birth_datetime": datetime(1990, 5, 15, 10, 30, 0),
            "birth_place": "北京",
            "description": "北京出生，测试基本功能"
        },
        {
            "name": "李四",
            "gender": "女", 
            "birth_datetime": datetime(1985, 8, 20, 14, 45, 0),
            "birth_place": "上海",
            "description": "上海出生，测试真太阳时校正"
        },
        {
            "name": "王五",
            "gender": "男",
            "birth_datetime": datetime(1992, 12, 10, 6, 20, 0),
            "birth_place": "广州",
            "description": "广州出生，测试南方城市"
        },
        {
            "name": "赵六",
            "gender": "女",
            "birth_datetime": datetime(1988, 3, 25, 18, 15, 0),
            "birth_place": "乌鲁木齐",
            "description": "乌鲁木齐出生，测试西部城市大经度差"
        },
        {
            "name": "陈七",
            "gender": "男",
            "birth_datetime": datetime(1995, 7, 8, 12, 0, 0),
            "birth_place": "不存在的城市",
            "description": "测试无效地名处理"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- 测试案例 {i}: {case['description']} ---")
        
        try:
            # 创建请求对象
            request = BaziCalculateRequest(
                name=case["name"],
                gender=case["gender"],
                birth_datetime=case["birth_datetime"],
                birth_place=case["birth_place"],
                is_solar_time=True,
                longitude=None,
                latitude=None,
                timezone_offset=None
            )
            
            # 调用计算函数
            result = await calculate_bazi_data(request)
            
            # 输出结果
            print(f"姓名: {case['name']}")
            print(f"性别: {case['gender']}")
            print(f"出生时间: {case['birth_datetime']}")
            print(f"出生地点: {case['birth_place']}")
            print(f"八字: {result.bazi_characters.get('year_stem', '')}{result.bazi_characters.get('year_branch', '')} "
                  f"{result.bazi_characters.get('month_stem', '')}{result.bazi_characters.get('month_branch', '')} "
                  f"{result.bazi_characters.get('day_stem', '')}{result.bazi_characters.get('day_branch', '')} "
                  f"{result.bazi_characters.get('hour_stem', '')}{result.bazi_characters.get('hour_branch', '')}")
            
            # 地理位置信息
            if result.location_info:
                print(f"地理位置信息:")
                print(f"  省份: {result.location_info.get('province', '未知')}")
                print(f"  城市: {result.location_info.get('city', '未知')}")
                if result.location_info.get('longitude') and result.location_info.get('latitude'):
                    print(f"  经纬度: {result.location_info['longitude']:.4f}°E, {result.location_info['latitude']:.4f}°N")
                
                # 真太阳时校正信息
                if result.location_info.get('correction_applied'):
                    print(f"  真太阳时校正: 已应用")
                    print(f"  经度时差: {result.location_info.get('longitude_diff_minutes', 0):.1f}分钟")
                    print(f"  均时差: {result.location_info.get('equation_of_time_minutes', 0):.1f}分钟")
                    if result.location_info.get('original_time'):
                        print(f"  校正前时间: {result.location_info['original_time']}")
                    if result.location_info.get('corrected_time'):
                        print(f"  校正后时间: {result.location_info['corrected_time']}")
                else:
                    print(f"  真太阳时校正: 未应用")
            else:
                print("地理位置信息: 无")
            
            print("✓ 计算成功")
            
        except Exception as e:
            print(f"✗ 计算失败: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """主函数"""
    print("地理位置服务集成测试")
    print("=" * 50)
    
    # 测试地理位置服务
    await test_location_service()
    
    # 测试八字计算集成
    await test_bazi_integration()
    
    print("\n" + "=" * 50)
    print("所有测试完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
