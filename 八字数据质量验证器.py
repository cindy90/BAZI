#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字命理案例数据质量验证脚本
用于检查Excel模板中录入数据的完整性和准确性
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

class BaziDataValidator:
    """八字数据验证器"""
    
    def __init__(self):
        # 天干地支定义
        self.gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 五行定义
        self.wu_xing = ['木', '火', '土', '金', '水']
        
        # 十神定义
        self.shi_shen = ['比肩', '劫财', '食神', '伤官', '偏财', '正财', '七杀', '正官', '偏印', '正印']
        
        # 旺衰定义
        self.wang_shuai = ['极弱', '身弱', '中和', '身旺', '极旺']
        
    def validate_csv_file(self, file_path):
        """验证CSV文件中的数据"""
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            print(f"📁 读取文件成功: {file_path}")
            print(f"📊 总案例数: {len(df)}")
            print(f"📋 总字段数: {len(df.columns)}")
            print("-" * 60)
            
            # 执行各项验证
            self.validate_basic_info(df)
            self.validate_bazi_pillars(df)
            self.validate_wu_xing_scores(df)
            self.validate_dayun_info(df)
            self.validate_dates(df)
            
            print("-" * 60)
            print("✅ 数据质量验证完成！")
            
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
    
    def validate_basic_info(self, df):
        """验证基础信息"""
        print("🔍 验证基础信息...")
        
        # 检查必填字段
        required_fields = ['案例编号', '姓名', '性别', '阳历生日_年', '阳历生日_月', '阳历生日_日']
        
        for field in required_fields:
            if field in df.columns:
                missing_count = df[field].isna().sum()
                if missing_count > 0:
                    print(f"⚠️  {field}: {missing_count}个案例缺失")
                else:
                    print(f"✅ {field}: 完整")
            else:
                print(f"❌ 缺少必要字段: {field}")
        
        # 验证性别字段
        if '性别' in df.columns:
            invalid_gender = df[~df['性别'].isin(['男', '女'])]['性别'].dropna()
            if len(invalid_gender) > 0:
                print(f"⚠️  性别字段有无效值: {invalid_gender.unique()}")
        
        # 验证年份范围
        if '阳历生日_年' in df.columns:
            # 转换为数值，处理非数值数据
            numeric_years = pd.to_numeric(df['阳历生日_年'], errors='coerce')
            invalid_years = numeric_years[(numeric_years < 1900) | (numeric_years > 2100)].dropna()
            if len(invalid_years) > 0:
                print(f"⚠️  年份超出合理范围(1900-2100): {invalid_years.values}")
        
        # 验证月份范围
        if '阳历生日_月' in df.columns:
            numeric_months = pd.to_numeric(df['阳历生日_月'], errors='coerce')
            invalid_months = numeric_months[(numeric_months < 1) | (numeric_months > 12)].dropna()
            if len(invalid_months) > 0:
                print(f"⚠️  月份超出范围(1-12): {invalid_months.values}")
        
        # 验证日期范围
        if '阳历生日_日' in df.columns:
            numeric_days = pd.to_numeric(df['阳历生日_日'], errors='coerce')
            invalid_days = numeric_days[(numeric_days < 1) | (numeric_days > 31)].dropna()
            if len(invalid_days) > 0:
                print(f"⚠️  日期超出范围(1-31): {invalid_days.values}")
        
        print()
    
    def validate_bazi_pillars(self, df):
        """验证八字四柱"""
        print("🔍 验证八字四柱...")
        
        pillar_fields = ['标准_年柱', '标准_月柱', '标准_日柱', '标准_时柱']
        
        for field in pillar_fields:
            if field in df.columns:
                invalid_pillars = []
                for idx, pillar in df[field].dropna().items():
                    if not self.is_valid_pillar(pillar):
                        invalid_pillars.append(f"行{idx+2}: {pillar}")
                
                if invalid_pillars:
                    print(f"⚠️  {field}格式错误:")
                    for invalid in invalid_pillars[:5]:  # 只显示前5个错误
                        print(f"    {invalid}")
                    if len(invalid_pillars) > 5:
                        print(f"    ... 还有{len(invalid_pillars)-5}个错误")
                else:
                    valid_count = df[field].dropna().count()
                    print(f"✅ {field}: {valid_count}个有效干支")
        
        print()
    
    def validate_wu_xing_scores(self, df):
        """验证五行得分"""
        print("🔍 验证五行得分...")
        
        wu_xing_fields = [
            '标准_五行得分_木', '标准_五行得分_火', '标准_五行得分_土',
            '标准_五行得分_金', '标准_五行得分_水'
        ]
        
        # 检查每行的五行得分总和
        if all(field in df.columns for field in wu_xing_fields):
            for idx, row in df.iterrows():
                scores = [row[field] for field in wu_xing_fields if pd.notna(row[field])]
                if len(scores) == 5:
                    total = sum(scores)
                    if abs(total - 100) > 0.1:
                        print(f"⚠️  行{idx+2}: 五行得分总和为{total:.1f}，应为100.0")
                
                # 检查单个得分范围
                for field in wu_xing_fields:
                    score = row[field]
                    if pd.notna(score) and (score < 0 or score > 100):
                        print(f"⚠️  行{idx+2}: {field}={score}，超出0-100范围")
        
        # 检查旺衰字段
        if '标准_日主旺衰' in df.columns:
            invalid_wang_shuai = df[~df['标准_日主旺衰'].isin(self.wang_shuai + [np.nan])]['标准_日主旺衰'].dropna()
            if len(invalid_wang_shuai) > 0:
                print(f"⚠️  日主旺衰有无效值: {invalid_wang_shuai.unique()}")
        
        print()
    
    def validate_dayun_info(self, df):
        """验证大运信息"""
        print("🔍 验证大运信息...")
        
        # 检查大运干支格式
        for i in range(1, 6):  # 检查前5个大运
            gan_zhi_field = f'标准_大运{i}_干支'
            age_field = f'标准_大运{i}_起运年龄'
            
            if gan_zhi_field in df.columns:
                invalid_dayun = []
                for idx, gan_zhi in df[gan_zhi_field].dropna().items():
                    if not self.is_valid_pillar(gan_zhi):
                        invalid_dayun.append(f"行{idx+2}: {gan_zhi}")
                
                if invalid_dayun:
                    print(f"⚠️  {gan_zhi_field}格式错误:")
                    for invalid in invalid_dayun[:3]:
                        print(f"    {invalid}")
                else:
                    valid_count = df[gan_zhi_field].dropna().count()
                    if valid_count > 0:
                        print(f"✅ {gan_zhi_field}: {valid_count}个有效")
            
            # 检查起运年龄的合理性
            if age_field in df.columns:
                invalid_ages = df[(df[age_field] < 0) | (df[age_field] > 120)][age_field].dropna()
                if len(invalid_ages) > 0:
                    print(f"⚠️  {age_field}超出合理范围(0-120): {invalid_ages.values}")
        
        print()
    
    def validate_dates(self, df):
        """验证日期的合理性"""
        print("🔍 验证日期合理性...")
        
        date_fields = ['阳历生日_年', '阳历生日_月', '阳历生日_日', '阳历生日_时', '阳历生日_分']
        
        if all(field in df.columns for field in date_fields):
            invalid_dates = []
            
            for idx, row in df.iterrows():
                try:
                    year = int(row['阳历生日_年']) if pd.notna(row['阳历生日_年']) else None
                    month = int(row['阳历生日_月']) if pd.notna(row['阳历生日_月']) else None
                    day = int(row['阳历生日_日']) if pd.notna(row['阳历生日_日']) else None
                    hour = int(row['阳历生日_时']) if pd.notna(row['阳历生日_时']) else 0
                    minute = int(row['阳历生日_分']) if pd.notna(row['阳历生日_分']) else 0
                    
                    if year and month and day:
                        # 尝试创建日期对象来验证日期的有效性
                        datetime(year, month, day, hour, minute)
                        
                except (ValueError, TypeError):
                    invalid_dates.append(f"行{idx+2}: {year}-{month}-{day} {hour}:{minute}")
            
            if invalid_dates:
                print(f"⚠️  无效日期:")
                for invalid in invalid_dates[:5]:
                    print(f"    {invalid}")
                if len(invalid_dates) > 5:
                    print(f"    ... 还有{len(invalid_dates)-5}个无效日期")
            else:
                print("✅ 所有日期格式正确")
        
        print()
    
    def is_valid_pillar(self, pillar):
        """验证干支组合是否有效"""
        if not isinstance(pillar, str):
            return False
        
        # 跳过缺失数据
        if pillar in ['缺', '未知', '', 'nan', 'NaN']:
            return True  # 缺失数据不算错误，跳过验证
        
        # 提取干支（移除括号内容）
        import re
        text = re.sub(r'（.*?）', '', pillar)
        text = re.sub(r'\(.*?\)', '', text)
        
        # 检查是否包含有效的干支组合
        for gan in self.gan:
            for zhi in self.zhi:
                if gan + zhi in text:
                    return True
        
        return False
    
    def generate_report(self, file_path, output_path=None):
        """生成数据质量报告"""
        if output_path is None:
            output_path = file_path.replace('.csv', '_质量报告.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("八字命理案例数据质量报告\n")
            f.write("=" * 40 + "\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"数据文件: {file_path}\n\n")
            
            # 这里可以添加更详细的报告内容
            f.write("详细验证结果请查看控制台输出。\n")
        
        print(f"📋 质量报告已保存到: {output_path}")

def main():
    """主函数"""
    print("🎯 八字命理案例数据质量验证工具")
    print("=" * 60)
    
    validator = BaziDataValidator()
    
    # 默认验证当前目录下的CSV文件
    csv_file = "八字命理案例数据.csv"
    
    try:
        validator.validate_csv_file(csv_file)
        validator.generate_report(csv_file)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {csv_file}")
        print("请确保CSV文件在当前目录下，或修改文件路径。")
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")

if __name__ == "__main__":
    main()
