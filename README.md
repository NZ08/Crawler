# Crawler
# 游泳运动员比赛记录爬虫 | Swimmer Competition Records Scraper

这个Python脚本用于爬取World Aquatics（国际泳联）官网上的运动员比赛记录数据。
This Python script scrapes athlete competition records from the World Aquatics official website.

## 功能 | Features

- 从World Aquatics API获取指定运动员的比赛记录 | Fetch competition records for specific athletes from World Aquatics API
- 将原始JSON数据保存为文件 | Save raw JSON data to a file
- 将处理后的比赛数据保存为Excel文件 | Save processed competition data as Excel file
- 显示基本的比赛和奖牌统计信息 | Display basic competition and medal statistics

## 系统要求 | Requirements

- Python 3.8+
- 依赖库：requests, pandas, openpyxl, python-dateutil, numpy

## 使用方法 | Usage

1. 安装所需依赖 | Install required dependencies:

```
pip install -r requirements.txt
```

2. 运行主脚本 | Run the main script:

```
python sun_yang_results_scraper.py
```

3. 处理数据脚本 | Process data script (optional):

```
python process_data.py
```

## 自定义设置 | Custom Settings

如果要爬取其他运动员的数据，请修改`sun_yang_results_scraper.py`脚本中的`main()`函数里的`athlete_id`参数:

To scrape data for other athletes, modify the `athlete_id` parameter in the `main()` function of `sun_yang_results_scraper.py`:

```python
def main():
    athlete_id = "YOUR_ATHLETE_ID"  # 修改为目标运动员的ID | Change to target athlete's ID
    # ...
```

运动员ID可以从World Aquatics官网的运动员页面URL中获取。

Athlete IDs can be found in the URL of the athlete's page on the World Aquatics official website.

## 输出文件 | Output Files

脚本会生成两个文件 | The script generates two files:

1. `{运动员姓名}_原始数据.json` - 包含API返回的原始JSON数据 | Contains raw JSON data returned by the API
2. `{运动员姓名}_比赛记录.xlsx` - 包含处理后的比赛记录数据表格 | Contains processed competition records in table format

## 文件说明 | File Description

- `sun_yang_results_scraper.py` - 主脚本，用于获取和处理数据 | Main script for fetching and processing data
- `process_data.py` - 示例脚本，演示如何处理已保存的JSON数据 | Example script showing how to process saved JSON data
- `requirements.txt` - 依赖库列表 | List of dependencies

## 注意事项 | Notes

- 请合理使用此脚本，不要频繁请求API以避免IP被封 | Please use this script reasonably and avoid frequent API requests to prevent IP blocking
- 尊重World Aquatics的数据使用政策 | Respect World Aquatics' data usage policy
- 本脚本仅用于学习和研究目的 | This script is for learning and research purposes only 
