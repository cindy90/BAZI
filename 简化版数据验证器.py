#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字命理案例数据质量验证脚本（简化版）
用于检查CSV模板中录入数据的完整性和准确性
"""

import csv
from datetime import datetime
import os

class SimpleBaziDataValidator:
    """简化的八字数据验证器（不依赖pandas）"""
    
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
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return None, None
            
        try:
            # 尝试不同的编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
            data = None
            headers = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        reader = csv.DictReader(f)
                        data = list(reader)
                        headers = reader.fieldnames
                    print(f"📁 读取文件成功: {file_path} (编码: {encoding})")
                    break
                except UnicodeDecodeError:
                    continue
            
            if data is None:
                print(f"❌ 无法读取文件，尝试了编码: {encodings}")
                return None, None
            
            print(f"📊 总案例数: {len(data)}")
            if headers:
                print(f"📋 总字段数: {len(headers)}")
            print("-" * 60)
            
            # 执行各项验证
            self.validate_basic_info(data, headers)
            self.validate_bazi_pillars(data)
            self.validate_wu_xing_scores(data)
            self.validate_dayun_info(data)
            self.validate_dates(data)
            
            print("-" * 60)
            print("✅ 数据质量验证完成！")
            
            return data, headers
            
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return None, None
    
    def validate_basic_info(self, data, headers):
        """验证基础信息"""
        print("🔍 验证基础信息...")
        
        # 检查必填字段
        required_fields = ['案例编号', '姓名', '性别', '阳历生日_年', '阳历生日_月', '阳历生日_日']
        
        for field in required_fields:
            if field in headers:
                missing_count = sum(1 for row in data if not row.get(field, '').strip())
                if missing_count > 0:
                    print(f"⚠️  {field}: {missing_count}个案例缺失")
                else:
                    print(f"✅ {field}: 完整")
            else:
                print(f"❌ 缺少必要字段: {field}")
        
        # 验证性别字段
        if '性别' in headers:
            invalid_genders = []
            for i, row in enumerate(data):
                gender = row.get('性别', '').strip()
                if gender and gender not in ['男', '女']:
                    invalid_genders.append(f"行{i+2}: {gender}")
            
            if invalid_genders:
                print(f"⚠️  性别字段有无效值:")
                for invalid in invalid_genders[:3]:
                    print(f"    {invalid}")
        
        # 验证年份范围
        if '阳历生日_年' in headers:
            invalid_years = []
            for i, row in enumerate(data):
                year_str = row.get('阳历生日_年', '').strip()
                if year_str:
                    try:
                        year = int(year_str)
                        if year < 1900 or year > 2100:
                            invalid_years.append(f"行{i+2}: {year}")
                    except ValueError:
                        invalid_years.append(f"行{i+2}: {year_str}(非数字)")
            
            if invalid_years:
                print(f"⚠️  年份超出合理范围(1900-2100):")
                for invalid in invalid_years[:3]:
                    print(f"    {invalid}")
        
        print()
    
    def validate_bazi_pillars(self, data):
        """验证八字四柱"""
        print("🔍 验证八字四柱...")
        
        pillar_fields = ['标准_年柱', '标准_月柱', '标准_日柱', '标准_时柱']
        
        for field in pillar_fields:
            invalid_pillars = []
            valid_count = 0
            
            for i, row in enumerate(data):
                pillar = row.get(field, '').strip()
                if pillar:
                    if self.is_valid_pillar(pillar):
                        valid_count += 1
                    else:
                        invalid_pillars.append(f"行{i+2}: {pillar}")
            
            if invalid_pillars:
                print(f"⚠️  {field}格式错误:")
                for invalid in invalid_pillars[:3]:  # 只显示前3个错误
                    print(f"    {invalid}")
                if len(invalid_pillars) > 3:
                    print(f"    ... 还有{len(invalid_pillars)-3}个错误")
            
            if valid_count > 0:
                print(f"✅ {field}: {valid_count}个有效干支")
        
        print()
    
    def validate_wu_xing_scores(self, data):
        """验证五行得分"""
        print("🔍 验证五行得分...")
        
        wu_xing_fields = [
            '标准_五行得分_木', '标准_五行得分_火', '标准_五行得分_土',
            '标准_五行得分_金', '标准_五行得分_水'
        ]
        
        # 检查每行的五行得分总和
        total_errors = []
        range_errors = []
        
        for i, row in enumerate(data):
            scores = []
            for field in wu_xing_fields:
                score_str = row.get(field, '').strip()
                if score_str:
                    try:
                        score = float(score_str)
                        scores.append(score)
                        
                        # 检查单个得分范围
                        if score < 0 or score > 100:
                            range_errors.append(f"行{i+2}: {field}={score}")
                    except ValueError:
                        range_errors.append(f"行{i+2}: {field}={score_str}(非数字)")
            
            # 检查总和
            if len(scores) == 5:
                total = sum(scores)
                if abs(total - 100) > 0.1:
                    total_errors.append(f"行{i+2}: 总和{total:.1f}")
        
        if total_errors:
            print("⚠️  五行得分总和异常（应为100.0）:")
            for error in total_errors[:3]:
                print(f"    {error}")
        
        if range_errors:
            print("⚠️  五行得分超出范围(0-100):")
            for error in range_errors[:3]:
                print(f"    {error}")
        
        if not total_errors and not range_errors:
            print("✅ 五行得分验证通过")
        
        print()
    
    def validate_dayun_info(self, data):
        """验证大运信息"""
        print("🔍 验证大运信息...")
        
        # 检查大运干支格式
        for i in range(1, 6):  # 检查前5个大运
            gan_zhi_field = f'标准_大运{i}_干支'
            age_field = f'标准_大运{i}_起运年龄'
            
            # 验证干支格式
            invalid_dayun = []
            valid_count = 0
            
            for j, row in enumerate(data):
                gan_zhi = row.get(gan_zhi_field, '').strip()
                if gan_zhi:
                    if self.is_valid_pillar(gan_zhi):
                        valid_count += 1
                    else:
                        invalid_dayun.append(f"行{j+2}: {gan_zhi}")
            
            if invalid_dayun:
                print(f"⚠️  {gan_zhi_field}格式错误:")
                for invalid in invalid_dayun[:2]:
                    print(f"    {invalid}")
            elif valid_count > 0:
                print(f"✅ {gan_zhi_field}: {valid_count}个有效")
            
            # 检查起运年龄
            invalid_ages = []
            for j, row in enumerate(data):
                age_str = row.get(age_field, '').strip()
                if age_str:
                    try:
                        age = int(age_str)
                        if age < 0 or age > 120:
                            invalid_ages.append(f"行{j+2}: {age}")
                    except ValueError:
                        invalid_ages.append(f"行{j+2}: {age_str}(非数字)")
            
            if invalid_ages:
                print(f"⚠️  {age_field}超出合理范围(0-120):")
                for invalid in invalid_ages[:2]:
                    print(f"    {invalid}")
        
        print()
    
    def validate_dates(self, data):
        """验证日期的合理性"""
        print("🔍 验证日期合理性...")
        
        invalid_dates = []
        
        for i, row in enumerate(data):
            try:
                year_str = row.get('阳历生日_年', '').strip()
                month_str = row.get('阳历生日_月', '').strip()
                day_str = row.get('阳历生日_日', '').strip()
                hour_str = row.get('阳历生日_时', '').strip() or '0'
                minute_str = row.get('阳历生日_分', '').strip() or '0'
                
                if year_str and month_str and day_str:
                    year = int(year_str)
                    month = int(month_str)
                    day = int(day_str)
                    hour = int(hour_str)
                    minute = int(minute_str)
                    
                    # 尝试创建日期对象来验证日期的有效性
                    datetime(year, month, day, hour, minute)
                        
            except (ValueError, TypeError):
                invalid_dates.append(f"行{i+2}: {year_str}-{month_str}-{day_str} {hour_str}:{minute_str}")
        
        if invalid_dates:
            print(f"⚠️  无效日期:")
            for invalid in invalid_dates[:3]:
                print(f"    {invalid}")
            if len(invalid_dates) > 3:
                print(f"    ... 还有{len(invalid_dates)-3}个无效日期")
        else:
            print("✅ 所有日期格式正确")
        
        print()
    
    def is_valid_pillar(self, pillar):
        """验证干支组合是否有效"""
        if not isinstance(pillar, str) or len(pillar) != 2:
            return False
        
        gan, zhi = pillar[0], pillar[1]
        return gan in self.gan and zhi in self.zhi
    
    def generate_summary_report(self, data, headers):
        """生成数据汇总报告"""
        print("\n📋 数据汇总统计:")
        print("-" * 40)
        
        # 案例总数
        total_cases = len(data)
        print(f"总案例数: {total_cases}")
        
        # 性别分布
        if '性别' in headers:
            male_count = sum(1 for row in data if row.get('性别', '').strip() == '男')
            female_count = sum(1 for row in data if row.get('性别', '').strip() == '女')
            print(f"性别分布: 男{male_count}个, 女{female_count}个")
        
        # 年代分布
        if '阳历生日_年' in headers:
            years = []
            for row in data:
                year_str = row.get('阳历生日_年', '').strip()
                if year_str:
                    try:
                        years.append(int(year_str))
                    except ValueError:
                        pass
            
            if years:
                min_year = min(years)
                max_year = max(years)
                print(f"年代范围: {min_year}年 - {max_year}年")
        
        # 数据完整性
        complete_cases = 0
        basic_fields = ['案例编号', '姓名', '性别', '标准_年柱', '标准_月柱', '标准_日柱', '标准_时柱']
        
        for row in data:
            if all(row.get(field, '').strip() for field in basic_fields if field in headers):
                complete_cases += 1
        
        completion_rate = (complete_cases / total_cases * 100) if total_cases > 0 else 0
        print(f"基础信息完整率: {completion_rate:.1f}% ({complete_cases}/{total_cases})")

def main():
    """主函数"""
    print("🎯 八字命理案例数据质量验证工具（简化版）")
    print("=" * 60)
    
    validator = SimpleBaziDataValidator()
    
    # 默认验证当前目录下的CSV文件
    csv_file = "八字命理案例数据模板.csv"
    
    result = validator.validate_csv_file(csv_file)
    
    if result and len(result) == 2:
        data, headers = result
        if data is not None:
            validator.generate_summary_report(data, headers)
    
    print("\n💡 提示:")
    print("1. 修复上述问题后重新运行验证")
    print("2. 确保五行得分总和为100%")
    print("3. 检查所有干支组合的正确性")
    print("4. 验证日期时间的合理性")

if __name__ == "__main__":
    main()
