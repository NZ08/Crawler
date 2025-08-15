"""
孙杨比赛成绩数据处理脚本
该脚本用于处理从World Aquatics API下载的原始JSON数据，
提取关键比赛信息并转换为CSV格式便于分析。
"""

import json
import pandas as pd

# 读取JSON文件
# 使用不带时间戳的标准文件名
with open('SUN Yang_原始数据.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 提取需要的数据字段
# 从原始JSON中获取比赛结果数组
results = data['Results']
extracted_data = []

# 遍历所有比赛记录，提取感兴趣的字段
for result in results:
    # 提取所需的字段到一个字典中
    # 这些字段包括比赛名次、项目、用时、赛事名称和日期
    extracted_result = {
        '名次': result.get('Rank'),         # 比赛排名
        '比赛项目': result.get('DisciplineName'),  # 比赛项目名称
        '比赛用时': result.get('Time'),      # 完成时间
        '赛事': result.get('CompetitionName'),  # 赛事名称
        '比赛时间': result.get('Date')       # 比赛日期
    }
    extracted_data.append(extracted_result)

# 创建DataFrame将数据转换为表格形式
df = pd.DataFrame(extracted_data)

# 保存为CSV文件
# 使用标准文件名，不带时间戳
df.to_csv('孙杨比赛成绩数据.csv', index=False, encoding='utf-8-sig')

print("数据已成功提取并保存为 '孙杨比赛成绩数据.csv'") 