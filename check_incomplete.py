#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# 读取验证报告
with open('complete_validation_report_20250704_132116.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 查看不完整案例的详细信息
incomplete_cases = ['19', '41', '66', '69', '74', '84', '88']

print("不完整案例详情:")
print("=" * 50)

for case_id in incomplete_cases:
    case = data['cases'][case_id]
    print(f'案例{case_id} ({case["name"]}):')
    comp = case['completeness']
    for key, value in comp.items():
        if not value:
            print(f'  缺失: {key}')
    print()
