#!/usr/bin/env python3
"""
獨立的圖片更新腳本，可以被 cron job 調用
使用方法：python scripts/update_image.py
"""
import sys
import os

# 添加項目根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.image_utils import async_img_link
from datetime import datetime

if __name__ == "__main__":
    try:
        print(f"開始更新圖片... at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        async_img_link()
        print(f"圖片更新完成 at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"圖片更新失敗: {e}")
        sys.exit(1)