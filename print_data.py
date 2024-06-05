# import sys
# print(f"paht {sys.path}")
# sys.path.append('/yfpy/google')
# sys.path.append('/yfpy/quickstart')
from yfpy.google import sheet
from yfpy.quickstart import quickstart
import time
from datetime import datetime, timedelta
import pandas as pd
import dataframe_image as dfi

def get_today():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def get_all_data(week, today):
    # try:
        print("獲取當週資料中...")
        data = quickstart.get_all_data(week, today)
        print("當週資料獲取成功！")
        return data
    # except Exception as e:
    #     print(e)
    #     print("獲取當週資料失敗　><")

def get_today_data(date, week):
    # try:
        print("獲取當天資料中...")
        data = quickstart.get_today_all_data(date, week)
        print("當天資料獲取成功！")
        return data
    # except Exception as e:
    #     print(e)
    #     print("獲取當天資料失敗　><")
        

def write_data(week, week_data, today_data):
    # try:
        print("資料寫入中...")
        sheet.start(week, week_data, today_data)
        print("資料寫入成功!")
    # except Exception as e:
    #     print(e)
    #     print("資料寫入失敗 ><")

def calculate_weeks(end_date):
    start_date = '2023-10-23'
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    difference = end_date - start_date
    weeks = difference.days // 7
    return weeks + 1

def main():
    week = calculate_weeks(get_today()) - 1
    today = get_today()
    print(f"第{week}週")
    week_data = get_all_data(week, today)
    today_data = get_today_data(today, week)
    write_data(week, week_data, today_data)
    print("資料完成囉，拜拜啦～")

main()

print("等2分鐘資料同步")
time.sleep(120)


# 读取Excel文件
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRWHJVgpuaJeOILIPf1B3KRDGwbGzS0BTnRshtYfl3hk7A-6sLGJ_6Y7QronBsSjXM5ITkXYaDiTB4l/pub?output=xlsx'

df = pd.read_excel(url)  # 替换为您的Excel文件路径
df.fillna('', inplace=True)
df.index += 1
df = df.applymap(lambda x: '{:.0f}'.format(x) if isinstance(x, float) and x.is_integer() else x)

def remove_trailing_zeros(x):
    if isinstance(x, float):
        return '{:0.3g}'.format(x)
    return x

df = df.applymap(remove_trailing_zeros)

styled_df = df.style.set_properties(**{'text-align': 'center'})
# 将DataFrame保存为图像
dfi.export(styled_df, 'dataframe_image.png', max_cols=-1)