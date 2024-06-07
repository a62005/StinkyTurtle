import pygsheets
import pandas as pd
import requests
import re
import os
import glob
import ast



sheet_app_script_url = 'https://script.google.com/macros/s/AKfycbyv4E1rzC5cutjXj1Zc_kmg9bXwjDWO5SYDwSdxsY8PePJkFcfeW0qi07mRZg57lt4K/exec'
current_dir = f"{os.getcwd()}/config/"
file_path = glob.glob(os.path.join(current_dir, 'player_name.txt'))[0]
player_list_str = open(file_path, 'r').read()
player_list = ast.literal_eval(player_list_str)


#根據數字拿到對應的英文字母
def col_num_to_letter(n):
   string = ""
   while n > 0:
       n, remainder = divmod(n - 1, 26)
       string = chr(65 + remainder) + string
   return string


#設定表格文字置中
def set_sheet_text_center(ws):
  all_values = ws.get_all_values()
  last_row_with_values = max((index for index, row in enumerate(all_values, start=1) if any(row)), default=0)
  last_col_with_values = max((index for index, row in enumerate(zip(*all_values), start=1) if any(row)), default=0)
  range = f"A1:{col_num_to_letter(last_col_with_values)}{last_row_with_values}"
  # Get the range of cells you want to center
  cell_range = ws.range(range)


  # Set the horizontal alignment to 'CENTER'
  for row in cell_range:
     for cell in row:
        cell.set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)

def get_previous_week_name(week):
    # 從字符串中提取出數字 N
    match = re.search(r'\d+', week)
    if match is None:
        return week

    # 將 N 轉換為整數，然後減 1
    n = int(match.group())
    previous_week = n - 1

    # 返回 "第(N-1)週" 的字符串
    return f"第{previous_week}週"
 
#連線到表格
def connect_to_sheet(sheet_name):
  gc = pygsheets.authorize(service_account_file='google_auth.json')


  survey_url = 'https://docs.google.com/spreadsheets/d/1pqLJtUbeKy91C8dSKsagFsNE_MJWb5g4p-FpLRHtY3c/edit#gid=0'
  sh = gc.open_by_url(survey_url)

  try:
     ws = sh.worksheet_by_title(sheet_name)
     ws.clear()
     return ws
  except:
      week_name = get_previous_week_name(sheet_name)
   
      ws = sh.worksheet_by_title(week_name)
      new_ws = ws.copy_to(sh.id)
      new_ws.title = sheet_name

      sh.del_worksheet(ws)
      return new_ws

def parse_name_id(id):
   return player_list.get(id, id) 

def parse_data_name(data):
   keys = data.keys()
   result = {}
   for key in keys:
      result[parse_name_id(key)] = data[key]\
   
   return result

def set_data(ws, mData, col):
   count = 1
   col_num = 1
   keys = mData.keys()
   for key in keys:
      data = parse_data_name(mData[key])
      if key == 'FG%' or key == 'FT%':
         df = pd.DataFrame(list(data.values()), columns=[key])
         row_num = col
         start = col_num_to_letter(col_num) + str(row_num)
         ws.set_dataframe(df, start)
         col_num += 1
      else:
         df = pd.DataFrame(list(data.items()), columns=[' ' * count, key])
         row_num = col  # Row number starting from 1
         start = col_num_to_letter(col_num) + str(row_num)
         ws.set_dataframe(df, start)
         count += 1
         col_num += 2


#將資料寫入表格
def set_data_in_sheet(ws, mData, today_data):
   set_data(ws, mData, 1)
   set_data(ws, today_data, len(player_list) + 4)

def call_app_script(ws, sheet_name):  
   # result = ws.execute_function('autoSetWidthFromPython', sheet_name)
   params = {
      'method': 'autoSetWidthFromPython',
      'name': sheet_name
   }
   result = requests.get(sheet_app_script_url, params=params)

#開始寫入表格
def start(week, data, today_data):
   sheet_name = f"第{week}週"
   ws = connect_to_sheet(sheet_name)
   set_data_in_sheet(ws, data, today_data)
   call_app_script(ws, sheet_name)
#   set_sheet_text_center(ws)\


# week = 6
# data = {
#    'name': {
#         'a': '0',
#         'b': '1'
#    },
#    'age': {
#          'c': '2',
#          'd': '3'
#    },
#    'test': {
#          'e': '4',
#          'f': '5'
#    }
# }



