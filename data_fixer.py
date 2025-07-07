#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据修复器 - 修复CSV中的数据错误
"""

import csv
import pandas as pd
from datetime import datetime

class DataFixer:
    """数据修复器"""
    
    def __init__(self):
        self.tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 手动修复数据
        self.manual_fixes = {
            '19': {  # 乔治·布什
                '标准_时柱': '壬午（天河水）',  # 12点为午时，根据日柱壬戌推算
                'notes': '时柱根据12点午时推算'
            },
            '41': {  # 董仒舒
                '标准_日柱': '乙未（砂中金）',  # 修正"乙不"为"乙未"
                'notes': '修正日柱录入错误'
            }
        }
    
    def fix_csv_data(self, input_file='八字命理案例数据.csv', output_file='八字命理案例数据_修复版.csv'):
        """修复CSV数据"""
        print("🔧 开始修复CSV数据...")
        
        try:
            # 读取原始数据
            df = pd.read_csv(input_file, encoding='utf-8-sig')
            
            # 应用手动修复
            for case_id, fixes in self.manual_fixes.items():
                case_index = int(case_id) - 1  # 转换为0-based索引
                
                if case_index < len(df):
                    print(f"📝 修复案例 {case_id}: {df.iloc[case_index]['姓名']}")
                    
                    for column, new_value in fixes.items():
                        if column != 'notes':
                            old_value = df.iloc[case_index][column]
                            df.at[case_index, column] = new_value
                            print(f"  {column}: {old_value} -> {new_value}")
            
            # 保存修复后的数据
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"✅ 修复完成，保存为: {output_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ 修复失败: {e}")
            return False
    
    def verify_fixes(self, file_path='八字命理案例数据_修复版.csv'):
        """验证修复结果"""
        print("\n🔍 验证修复结果...")
        
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            for case_id in self.manual_fixes.keys():
                case_index = int(case_id) - 1
                
                if case_index < len(df):
                    name = df.iloc[case_index]['姓名']
                    print(f"\n📋 案例 {case_id}: {name}")
                    
                    # 检查四柱
                    pillars = ['年柱', '月柱', '日柱', '时柱']
                    for pillar in pillars:
                        col = f'标准_{pillar}'
                        value = df.iloc[case_index][col]
                        print(f"  {pillar}: {value}")
            
            return True
            
        except Exception as e:
            print(f"❌ 验证失败: {e}")
            return False

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 八字数据修复器")
    print("=" * 60)
    
    fixer = DataFixer()
    
    # 修复数据
    if fixer.fix_csv_data():
        # 验证修复结果
        fixer.verify_fixes()
        print("\n✅ 数据修复完成！")
    else:
        print("\n❌ 数据修复失败！")

if __name__ == "__main__":
    main()
