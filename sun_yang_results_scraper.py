"""
World Aquatics运动员比赛记录爬虫

该脚本用于从World Aquatics(国际泳联)官网获取指定运动员的比赛记录数据，
处理数据并保存为JSON和Excel格式，同时显示基本的统计信息。

作者: 爬虫开发者
版本: 1.0
"""

import requests
import json
import pandas as pd
from datetime import datetime
import os

def fetch_athlete_results(athlete_id):
    """
    获取运动员比赛结果数据
    
    通过World Aquatics API获取指定运动员的全部比赛记录，
    使用自定义请求头以模拟浏览器行为，避免被API阻止。
    
    Args:
        athlete_id: 运动员ID，可从World Aquatics官网运动员页面URL中获取
    
    Returns:
        JSON格式的比赛结果数据，若请求失败则返回None
    """
    url = f"https://api.worldaquatics.com/fina/athletes/{athlete_id}/results"
    
    # 设置请求头以模拟浏览器访问，降低被反爬的可能性
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.worldaquatics.com/"
    }
    
    try:
        # 发送GET请求获取数据
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果请求失败则抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def process_results(data):
    """
    处理获取到的比赛结果数据
    
    从API返回的JSON数据中提取关键信息，转换为结构化的DataFrame格式，
    便于后续分析和保存。
    
    Args:
        data: JSON格式的比赛结果数据
    
    Returns:
        处理后的数据DataFrame和运动员姓名的元组，若数据格式错误则返回None
    """
    # 检查数据有效性
    if not data or "Results" not in data:
        print("数据格式错误或没有比赛结果")
        return None
    
    results = data["Results"]
    athlete_name = data.get("FullName", "Unknown")
    
    # 提取需要的字段，构建结构化数据列表
    processed_data = []
    for result in results:
        processed_result = {
            "比赛名称": result.get("CompetitionName", ""),  # 赛事全称
            "比赛类型": result.get("CompetitionType", ""),  # 赛事类型(如奥运会、世锦赛等)
            "项目": result.get("DisciplineName", ""),      # 比赛项目
            "阶段": result.get("PhaseName", ""),          # 比赛阶段(预赛、决赛等)
            "排名": result.get("Rank", ""),              # 最终排名
            "奖牌": result.get("MedalTag", ""),          # 奖牌类型(G=金牌,S=银牌,B=铜牌)
            "时间": result.get("Time", ""),              # 比赛用时
            "日期": result.get("Date", ""),              # 比赛日期
            "城市": result.get("CompetitionCity", ""),    # 比赛举办城市
            "国家": result.get("CompetitionCountry", ""), # 比赛举办国家
            "俱乐部/国家队": result.get("ClubName", result.get("NAT", "")),  # 代表队伍
            "记录类型": result.get("RecordType", ""),      # 是否破纪录(WR=世界纪录等)
            "分数": result.get("Points", ""),            # FINA积分
            "年龄": result.get("AthleteResultAge", "")    # 运动员当时年龄
        }
        processed_data.append(processed_result)
    
    # 返回处理后的DataFrame和运动员姓名
    return pd.DataFrame(processed_data), athlete_name

def save_to_excel(df, athlete_name):
    """
    将数据保存为Excel文件
    
    使用pandas的to_excel方法将处理后的数据保存为Excel格式。
    
    Args:
        df: 数据DataFrame
        athlete_name: 运动员名字
    """
    # 生成不带时间戳的固定文件名
    filename = f"{athlete_name}_比赛记录.xlsx"
    
    # 保存为Excel文件
    df.to_excel(filename, index=False)
    print(f"数据已保存至 {filename}")

def save_to_json(data, athlete_name):
    """
    将原始JSON数据保存为文件
    
    保存API返回的原始数据，以便后续可能的再处理或作为备份。
    使用UTF-8编码确保中文正确显示。
    
    Args:
        data: JSON数据
        athlete_name: 运动员名字
    """
    # 生成不带时间戳的固定文件名
    filename = f"{athlete_name}_原始数据.json"
    
    # 保存为JSON文件，ensure_ascii=False确保中文正确显示
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"原始数据已保存至 {filename}")

def main():
    """
    主函数，控制整个程序的执行流程
    
    定义目标运动员ID，获取数据，处理并保存结果，显示基本统计信息
    """
    athlete_id = "1017653"  # 孙杨的ID
    print(f"正在获取运动员ID {athlete_id} 的比赛数据...")
    
    # 获取数据
    data = fetch_athlete_results(athlete_id)
    
    if data:
        # 保存原始数据
        athlete_name = data.get("FullName", "Unknown")
        save_to_json(data, athlete_name)
        
        # 处理并保存为Excel
        df, athlete_name = process_results(data)
        if df is not None:
            save_to_excel(df, athlete_name)
            
            # 显示基本统计信息
            print(f"\n获取到 {len(df)} 条比赛记录")
            print(f"比赛时间范围: {df['日期'].min()} - {df['日期'].max()}")
            
            # 计算奖牌数量
            medals = df['奖牌'].value_counts().to_dict()
            print("\n奖牌统计:")
            print(f"金牌 (G): {medals.get('G', 0)}")  # G代表金牌
            print(f"银牌 (S): {medals.get('S', 0)}")  # S代表银牌
            print(f"铜牌 (B): {medals.get('B', 0)}")  # B代表铜牌

# 当脚本直接运行时(而非被导入时)执行main函数
if __name__ == "__main__":
    main() 