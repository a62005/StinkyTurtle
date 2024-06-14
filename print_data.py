import sys
sys.path.append(f'{sys.path[0]}/yfpy/google')
sys.path.append(f'{sys.path[0]}/yfpy/quickstart')
import sheet
import quickstart
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

def remove_trailing_zeros(x):
    if isinstance(x, float):
        return '{:0.3g}'.format(x)
    return x

def parse_data_to_img_from_xml():
    # 读取Excel文件
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRWHJVgpuaJeOILIPf1B3KRDGwbGzS0BTnRshtYfl3hk7A-6sLGJ_6Y7QronBsSjXM5ITkXYaDiTB4l/pub?output=xlsx'

    df = pd.read_excel(url)  # 替换为您的Excel文件路径
    df.fillna('', inplace=True)
    df.index += 1
    df = df.applymap(lambda x: '{:.0f}'.format(x) if isinstance(x, float) and x.is_integer() else x)
    df = df.applymap(remove_trailing_zeros)

    styled_df = df.style.set_properties(**{'text-align': 'center'})
    # 将DataFrame保存为图像
    dfi.export(styled_df, 'dataframe_image.png', max_cols=-1)

def main():
    league_info = quickstart.get_league_info()
    if league_info.is_finished == 1:
        print("聯賽已結束")
        return
    week = league_info.current_week
    today = league_info.end_date
    # today = get_today()
    print(f"第{week}週  第{today}天")
    week_data = get_all_data(week, today)
    today_data = get_today_data(today, week)
    write_data(week, week_data, today_data)
    print("等2分鐘資料同步")
    time.sleep(120)
    parse_data_to_img_from_xml()
    print("資料完成囉，拜拜啦～")