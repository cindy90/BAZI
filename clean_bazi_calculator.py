#!/usr/bin/env python3
"""
清理 bazi_calculator.py 文件，移除冗余代码
"""

def clean_bazi_calculator():
    input_file = r"c:\Users\cindy\bazi_app\backend\app\services\bazi_calculator.py"
    output_file = r"c:\Users\cindy\bazi_app\backend\app\services\bazi_calculator_clean.py"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到冗余代码开始的位置
    clean_lines = []
    for i, line in enumerate(lines):
        if "precise_calculator = PreciseBaziCalculator()" in line:
            break
        clean_lines.append(line)
    
    # 写入清理后的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    
    print(f"清理完成：{len(clean_lines)} 行保留，{len(lines) - len(clean_lines)} 行删除")

if __name__ == "__main__":
    clean_bazi_calculator()
