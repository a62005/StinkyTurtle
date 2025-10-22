import json
import os
import pyimgur
import importlib
import sys
from datetime import datetime

# 處理相對導入問題
try:
    from .time_utils import check_date
    from config.settings import IMGUR_CLIENT_ID, USE_LOCAL_IMAGE_SERVER
except ImportError:
    # 如果相對導入失敗，使用絕對導入
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.time_utils import check_date
    from config.settings import IMGUR_CLIENT_ID, USE_LOCAL_IMAGE_SERVER

script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im = pyimgur.Imgur(IMGUR_CLIENT_ID)

# 在 App Engine 環境中使用記憶體儲存
_img_data_cache = {
    'date': '2000-01-01',
    'imgurl': '',
    'method': 'imgur'
}

def get_img_data_path():
    """獲取圖片資料檔案路徑，在 App Engine 中使用 /tmp"""
    if os.environ.get('GAE_ENV', '').startswith('standard'):
        # App Engine 環境，使用 /tmp 目錄
        return '/tmp/img_data.json'
    else:
        # 本地環境
        return f"{script_directory}/config/img_data.json"

def load_img_data():
    """載入圖片資料"""
    global _img_data_cache
    
    if os.environ.get('GAE_ENV', '').startswith('standard'):
        # App Engine 環境，使用記憶體快取
        return _img_data_cache.copy()
    
    try:
        img_data_path = get_img_data_path()
        with open(img_data_path, 'r', encoding='utf-8') as r:
            return json.load(r)
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果文件不存在或格式錯誤，返回預設數據
        return {
            'date': '2000-01-01',
            'imgurl': '',
            'method': 'imgur'
        }

def save_img_data(img_data):
    """儲存圖片資料"""
    global _img_data_cache
    
    if os.environ.get('GAE_ENV', '').startswith('standard'):
        # App Engine 環境，更新記憶體快取
        _img_data_cache.update(img_data)
        print("📝 圖片資料已儲存到記憶體快取")
        return
    
    try:
        img_data_path = get_img_data_path()
        # 確保目錄存在
        os.makedirs(os.path.dirname(img_data_path), exist_ok=True)
        with open(img_data_path, 'w', encoding='utf-8') as w:
            json.dump(img_data, w)
        print(f"📝 圖片資料已儲存到: {img_data_path}")
    except Exception as e:
        print(f"⚠️ 無法儲存圖片資料: {e}")
        # 在本地環境也使用記憶體快取作為備用
        _img_data_cache.update(img_data)

def get_server_url():
    """獲取服務器 URL"""
    try:
        from pyngrok import ngrok
        tunnels = ngrok.get_tunnels()
        if tunnels:
            return tunnels[0].public_url
    except:
        pass
    return "http://localhost:8001"  # 備用 URL

def async_img_link(force_update=False):
    """
    獲取圖片連結
    Args:
        force_update: 是否強制更新圖片，預設為 False
    """
    img = f"{script_directory}/dataframe_image.png"
    
    # 使用新的載入函數
    imgData = load_img_data()
    
    date = imgData['date']
    
    # 檢查是否需要重新生成圖片
    use_method = "local" if USE_LOCAL_IMAGE_SERVER else "imgur"
    current_method = imgData.get('method', 'imgur')
    
    if not force_update and check_date(date) and use_method == current_method:
        link = imgData['imgurl']
        print(f"使用現有圖片連結: {link}")
    else:
        try:
            # print("開始重新生成圖片...")
            # # 重新生成圖片
            # print_data = importlib.import_module('print_data')  # 動態導入
            # importlib.reload(print_data)  # 重新加載模組
            # print_data.main()
            
            if USE_LOCAL_IMAGE_SERVER:
                # 使用本地服務器
                server_url = get_server_url()
                link = f"{server_url}/image/current"
                print(f"使用本地服務器: {link}")
            else:
                # 使用 Imgur
                uploaded_img = im.upload_image(img, title="Test by Turtle")
                link = uploaded_img.link
                print(f"使用 Imgur: {link}")
            
            imgData['date'] = datetime.now().strftime('%Y-%m-%d')
            imgData['imgurl'] = link
            imgData['method'] = use_method
            
            # 使用新的儲存函數
            save_img_data(imgData)
                
        except Exception as e:
            print(f"圖片生成失敗: {e}")
            # 返回現有連結或預設連結
            link = imgData.get('imgurl', '')
            if not link:
                if USE_LOCAL_IMAGE_SERVER:
                    server_url = get_server_url()
                    link = f"{server_url}/image/current"
                else:
                    link = "https://via.placeholder.com/800x600?text=Image+Not+Available"
    
    return link

def get_current_img_link():
    """獲取目前的圖片連結"""
    imgData = load_img_data()
    return imgData.get('imgurl', '')