import json
import os
import pyimgur
import importlib
import sys
from datetime import datetime

# 處理相對導入問題
try:
    from .time_utils import check_date
    from config.settings import IMGUR_CLIENT_ID
except ImportError:
    # 如果相對導入失敗，使用絕對導入
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.time_utils import check_date
    from config.settings import IMGUR_CLIENT_ID

script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im = pyimgur.Imgur(IMGUR_CLIENT_ID)

def async_img_link():
    img = f"{script_directory}/dataframe_image.png"
    with open(f"{script_directory}/config/img_data.json", 'r', encoding='utf-8') as r:
        imgData = json.load(r)
    date = imgData['date']
    if check_date(date):
        link = imgData['imgurl']
    else:
        print_data = importlib.import_module('print_data')  # 動態導入
        importlib.reload(print_data)  # 重新加載模組
        print_data.main()
        uploaded_img = im.upload_image(img, title="Test by Turtle")
        link = uploaded_img.link
        imgData['date'] = datetime.now().strftime('%Y-%m-%d')
        imgData['imgurl'] = link
        # 再以寫入模式打開文件，寫入數據
        with open(f"{script_directory}/config/img_data.json", 'w', encoding='utf-8') as w:
            json.dump(imgData, w)
    return link

def get_current_img_link():
    with open(f"{script_directory}/config/img_data.json", 'r', encoding='utf-8') as r:
        imgData = json.load(r)
        return imgData['imgurl']