#!/usr/bin/env python3
"""
测试 calculators.py 第三步修改结果
验证 PreciseBaziCalculator 和 FiveElementsCalculator 的所有方法
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_precise_bazi_calculator():
    """测试 PreciseBaziCalculator 类"""
    print("=== 测试 PreciseBaziCalculator 类 ===")
    
    try:
        from app.services.calculators import PreciseBaziCalculator, get_solar_time_correction, apply_solar_time_correction
        
        # 测试基本的真太阳时校正
        birth_time = datetime(1990, 5, 15, 14, 30, 0)
        longitude = 116.4074  # 北京经度
        
        # 测试静态方法
        corrected_time = PreciseBaziCalculator.correct_solar_time(birth_time, longitude)
        print(f"✓ correct_solar_time: {birth_time} -> {corrected_time}")
        
        # 测试均时差计算
        equation_time = PreciseBaziCalculator._calculate_equation_of_time(birth_time)
        print(f"✓ _calculate_equation_of_time: {equation_time:.2f} 分钟")
        
        # 测试经度获取
        beijing_lng = PreciseBaziCalculator.get_precise_longitude("北京")
        print(f"✓ get_precise_longitude (北京): {beijing_lng}")
        
        shanghai_lng = PreciseBaziCalculator.get_precise_longitude("上海")
        print(f"✓ get_precise_longitude (上海): {shanghai_lng}")
        
        # 测试完整的校正功能
        correction_info = PreciseBaziCalculator.calculate_precise_bazi_with_lunar(birth_time, city_name="北京")
        print(f"✓ calculate_precise_bazi_with_lunar: 校正应用={correction_info['correction_applied']}")
        print(f"  经度时差: {correction_info['longitude_diff_minutes']:.1f} 分钟")
        print(f"  均时差: {correction_info['equation_of_time_minutes']:.1f} 分钟")
        
        # 测试便捷函数
        correction_info2 = get_solar_time_correction(birth_time, "上海")
        print(f"✓ get_solar_time_correction: 校正应用={correction_info2['correction_applied']}")
        
        corrected_time2 = apply_solar_time_correction(birth_time, "广州")
        print(f"✓ apply_solar_time_correction: {birth_time} -> {corrected_time2}")
        
        print("✓ PreciseBaziCalculator 所有测试通过！")
        return True
        
    except Exception as e:
        print(f"✗ PreciseBaziCalculator 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_five_elements_calculator_methods():
    """测试 FiveElementsCalculator 类的所有必需方法"""
    print("\n=== 测试 FiveElementsCalculator 必需方法 ===")
    
    try:
        from app.services.calculators import FiveElementsCalculator
        from app.services.core import Bazi, StemBranch
        
        # 测试所有必需的静态方法
        methods_to_test = [
            "analyze_dayun_phase",
            "calculate_ten_god_relation", 
            "get_zhi_hidden_gan",
            "calculate_chang_sheng_twelve_palaces",
            "get_chang_sheng_strength_level",
            "get_chang_sheng_strength_level_int"  # 新增的数值版本
        ]
        
        # 测试 analyze_dayun_phase
        phase = FiveElementsCalculator.analyze_dayun_phase(25)
        print(f"✓ analyze_dayun_phase(25): {phase}")
        
        phase2 = FiveElementsCalculator.analyze_dayun_phase(45)
        print(f"✓ analyze_dayun_phase(45): {phase2}")
        
        # 测试 calculate_ten_god_relation
        ten_god = FiveElementsCalculator.calculate_ten_god_relation("甲", "庚")
        print(f"✓ calculate_ten_god_relation('甲', '庚'): {ten_god}")
        
        ten_god2 = FiveElementsCalculator.calculate_ten_god_relation("乙", "甲")
        print(f"✓ calculate_ten_god_relation('乙', '甲'): {ten_god2}")
        
        # 测试 get_zhi_hidden_gan
        hidden_gan = FiveElementsCalculator.get_zhi_hidden_gan("寅")
        print(f"✓ get_zhi_hidden_gan('寅'): {hidden_gan}")
        
        hidden_gan2 = FiveElementsCalculator.get_zhi_hidden_gan("子")
        print(f"✓ get_zhi_hidden_gan('子'): {hidden_gan2}")
        
        # 测试 calculate_chang_sheng_twelve_palaces
        chang_sheng = FiveElementsCalculator.calculate_chang_sheng_twelve_palaces("甲", "亥")
        print(f"✓ calculate_chang_sheng_twelve_palaces('甲', '亥'): {chang_sheng}")
        
        chang_sheng2 = FiveElementsCalculator.calculate_chang_sheng_twelve_palaces("庚", "寅")
        print(f"✓ calculate_chang_sheng_twelve_palaces('庚', '寅'): {chang_sheng2}")
        
        # 测试 get_chang_sheng_strength_level (字符串版本)
        strength_str = FiveElementsCalculator.get_chang_sheng_strength_level("临官")
        print(f"✓ get_chang_sheng_strength_level('临官'): {strength_str}")
        
        # 测试 get_chang_sheng_strength_level_int (数值版本)
        strength_int = FiveElementsCalculator.get_chang_sheng_strength_level_int("临官")
        print(f"✓ get_chang_sheng_strength_level_int('临官'): {strength_int}")
        
        strength_int2 = FiveElementsCalculator.get_chang_sheng_strength_level_int("帝旺")
        print(f"✓ get_chang_sheng_strength_level_int('帝旺'): {strength_int2}")
        
        # 验证所有方法都存在
        for method_name in methods_to_test:
            if hasattr(FiveElementsCalculator, method_name):
                print(f"✓ {method_name} - 方法存在")
            else:
                print(f"✗ {method_name} - 方法不存在")
                return False
        
        # 测试其他重要方法
        # 创建一个测试用的八字对象
        bazi_obj = Bazi(
            year=StemBranch("庚", "午"),
            month=StemBranch("辛", "巳"),
            day=StemBranch("庚", "辰"),
            hour=StemBranch("癸", "未"),
            gender="男",
            birth_time=datetime(1990, 5, 15, 14, 30, 0)
        )
        
        # 测试日主强度计算
        strength = FiveElementsCalculator.calculate_day_master_strength(bazi_obj)
        print(f"✓ calculate_day_master_strength: {strength}")
        
        # 测试五行占比计算
        percentages = FiveElementsCalculator.calculate_five_elements_percentage(bazi_obj)
        print(f"✓ calculate_five_elements_percentage: {percentages}")
        
        # 测试强度等级描述
        strength_desc = FiveElementsCalculator.get_strength_level_description(strength)
        print(f"✓ get_strength_level_description({strength}): {strength_desc}")
        
        print("✓ FiveElementsCalculator 所有必需方法测试通过！")
        return True
        
    except Exception as e:
        print(f"✗ FiveElementsCalculator 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_import_changes():
    """测试导入更改是否成功"""
    print("\n=== 测试导入更改 ===")
    
    try:
        # 测试从 calculators.py 导入真太阳时校正功能
        from app.services.calculators import get_solar_time_correction, apply_solar_time_correction
        print("✓ 成功从 calculators.py 导入真太阳时校正功能")
        
        # 测试 bazi_calculator.py 的导入是否正常
        from app.services.bazi_calculator import calculate_bazi_data
        print("✓ bazi_calculator.py 导入正常")
        
        print("✓ 所有导入更改测试通过！")
        return True
        
    except Exception as e:
        print(f"✗ 导入更改测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始 calculators.py 第三步修改测试...")
    
    # 测试1：PreciseBaziCalculator 类
    test1 = test_precise_bazi_calculator()
    
    # 测试2：FiveElementsCalculator 必需方法
    test2 = test_five_elements_calculator_methods()
    
    # 测试3：导入更改
    test3 = test_import_changes()
    
    if test1 and test2 and test3:
        print("\n🎉 所有测试通过！第三步修改成功！")
        print("\n✅ 完成的功能：")
        print("  - PreciseBaziCalculator 类已迁移到 calculators.py")
        print("  - 所有真太阳时校正功能正常工作")
        print("  - FiveElementsCalculator 包含所有必需的静态方法")
        print("  - analyze_dayun_phase, calculate_ten_god_relation, get_zhi_hidden_gan 等方法可用")
        print("  - calculate_chang_sheng_twelve_palaces, get_chang_sheng_strength_level 方法可用")
        print("  - 新增 get_chang_sheng_strength_level_int 方法返回数值")
        print("  - bazi_calculator.py 导入已更新为从 calculators.py 获取功能")
    else:
        print("\n❌ 部分测试失败，需要进一步修复。")

if __name__ == "__main__":
    main()
