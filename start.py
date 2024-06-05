import sys
sys.path.append('/yfpy/google')
sys.path.append('/yfpy/quickstart')
# from yfpy.google import sheet
# from yfpy.quickstart import quickstart
import time
from datetime import datetime, timedelta
import pandas as pd
import dataframe_image as dfi
import requests

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
      
# def get_data(week): 
#     try:
#         print("獲取資料中...")
#         data = quickstart.get_all_data(week)
#         print("資料獲取成功！")
#         return data
#     except Exception as e:
#         print(e)
#         print("獲取資料失敗　><")
        

# def write_data(week, data):
#     try:
#         print("寫入資料中...")
#         sheet.start(week, data)
#         print("寫入資料成功!")
#     except Exception as e:
#         print(e)
#         print("寫入資料失敗 ><")

# def main():
#     week = "6"
#     data = get_data(week)
#     write_data(week, data)
#     print("資料完成囉，拜拜啦～")
#     time.sleep(3)

# main()

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


def send_notify(token, msg, filepath=None, stickerPackageId=None, stickerId=None):
    payload = {'message': msg}
    headers = {
        "Authorization": "Bearer " + token
     }
    if stickerPackageId and stickerId:
        payload['stickerPackageId'] = stickerPackageId
        payload['stickerId'] = stickerId

    if filepath:
        attachment = {'imageFile': open(filepath, 'rb')}
        print(attachment)
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload, files=attachment)
    else:
        print("attachment")
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code, r.text

# Test line notify

# 臭烏龜聯賽
token = "Ao7pCGAeIeLluPxy4mQGXv1jhK7tVY29Arc31QuG2Z7"

# 我要發大財
token = "yrjISonW7S5g5F9xTjuLCs6cpimSdoiIQ8OmiNTaMec"
send_notify(token=token, msg='戰績出來啦', filepath='dataframe_image.png', stickerPackageId='', stickerId='')