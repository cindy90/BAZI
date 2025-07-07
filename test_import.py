#!/usr/bin/env python3
"""
测试 constants.py 导入问题
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("当前工作目录:", os.getcwd())
print("Python 路径:", sys.path[:3])

# 测试 1: 直接导入
try:
    from app.services.constants import TIANGAN
    print("✓ 测试1成功: 直接导入 constants.TIANGAN")
    print("  天干:", TIANGAN[:3])
except Exception as e:
    print("✗ 测试1失败:", e)
    import traceback
    traceback.print_exc()

# 测试 2: 模块导入
try:
    from app.services import constants
    print("✓ 测试2成功: 模块导入 constants")
    print("  天干:", constants.TIANGAN[:3])
except Exception as e:
    print("✗ 测试2失败:", e)
    import traceback
    traceback.print_exc()

# 测试 3: 相对导入模拟
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("constants", "backend/app/services/constants.py")
    constants_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(constants_module)
    print("✓ 测试3成功: 通过 importlib 导入")
    print("  天干:", constants_module.TIANGAN[:3])
except Exception as e:
    print("✗ 测试3失败:", e)
    import traceback
    traceback.print_exc()

# 测试 4: calculators.py 导入
try:
    from app.services.calculators import FiveElementsCalculator
    print("✓ 测试4成功: 导入 FiveElementsCalculator")
except Exception as e:
    print("✗ 测试4失败:", e)
    import traceback
    traceback.print_exc()

print("\n=== 文件存在性检查 ===")
files_to_check = [
    "backend/app/services/constants.py",
    "backend/app/services/calculators.py", 
    "backend/app/services/__init__.py"
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        print(f"✓ {file_path} 存在")
    else:
        print(f"✗ {file_path} 不存在")
