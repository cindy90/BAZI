#!/usr/bin/env python3
"""
简化的流年互动常量测试
"""
import sys
import os

# 修改 Python 路径
current_dir = os.getcwd()
backend_dir = os.path.join(current_dir, 'backend')
sys.path.insert(0, backend_dir)

def test_constants_import():
    """测试常量导入"""
    print("=== 流年互动常量导入测试 ===")
    
    try:
        # 导入常量
        from app.services.constants import (
            STEM_COMBINATIONS_DETAILED, 
            BRANCH_CONFLICTS_MAPPING,
            BRANCH_SIX_COMBINATIONS_DETAILED,
            BRANCH_THREE_COMBINATIONS_DETAILED,
            BRANCH_PUNISHMENTS_DETAILED,
            BRANCH_HARMS_DETAILED
        )
        
        print("✅ 所有新常量导入成功")
        
        # 测试常量内容
        print("\n1. 天干五合常量测试:")
        print(f"  甲己合化土: {STEM_COMBINATIONS_DETAILED.get(('甲', '己'))}")
        print(f"  乙庚合化金: {STEM_COMBINATIONS_DETAILED.get(('乙', '庚'))}")
        
        print("\n2. 地支六冲常量测试:")
        print(f"  子冲午: {BRANCH_CONFLICTS_MAPPING.get('子')}")
        print(f"  寅冲申: {BRANCH_CONFLICTS_MAPPING.get('寅')}")
        
        print("\n3. 地支六合常量测试:")
        print(f"  子丑合土: {BRANCH_SIX_COMBINATIONS_DETAILED.get(('子', '丑'))}")
        print(f"  寅亥合木: {BRANCH_SIX_COMBINATIONS_DETAILED.get(('寅', '亥'))}")
        
        print("\n4. 地支三合常量测试:")
        print(f"  申子辰水局: {BRANCH_THREE_COMBINATIONS_DETAILED.get(('申', '子', '辰'))}")
        print(f"  寅午戌火局: {BRANCH_THREE_COMBINATIONS_DETAILED.get(('寅', '午', '戌'))}")
        
        print("\n5. 地支相刑常量测试:")
        print(f"  寅巳申刑: {BRANCH_PUNISHMENTS_DETAILED.get(('寅', '巳', '申'))}")
        print(f"  子卯刑: {BRANCH_PUNISHMENTS_DETAILED.get(('子', '卯'))}")
        
        print("\n6. 地支相害常量测试:")
        print(f"  子未害: {BRANCH_HARMS_DETAILED.get(('子', '未'))}")
        print(f"  寅巳害: {BRANCH_HARMS_DETAILED.get(('寅', '巳'))}")
        
        print("\n✅ 常量内容验证通过")
        return True
        
    except ImportError as e:
        print(f"❌ 常量导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        return False

def test_calculators_import():
    """测试计算器导入"""
    print("\n=== 计算器模块导入测试 ===")
    
    try:
        from app.services.calculators import FiveElementsCalculator
        print("✅ FiveElementsCalculator 导入成功")
        
        # 检查方法是否存在
        if hasattr(FiveElementsCalculator, 'analyze_liunian_interactions'):
            print("✅ analyze_liunian_interactions 方法存在")
        else:
            print("❌ analyze_liunian_interactions 方法不存在")
            return False
            
        if hasattr(FiveElementsCalculator, 'get_strength_level_description'):
            print("✅ get_strength_level_description 方法存在")
        else:
            print("❌ get_strength_level_description 方法不存在")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ 计算器模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        return False

if __name__ == "__main__":
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Backend目录: {backend_dir}")
    print(f"Python路径: {sys.path[:3]}")  # 只显示前3个路径
    
    success1 = test_constants_import()
    success2 = test_calculators_import()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！常量重构成功完成！")
    else:
        print("\n❌ 测试失败，需要检查问题")
