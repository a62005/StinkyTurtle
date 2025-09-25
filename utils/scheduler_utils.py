import schedule
import time
import threading
from datetime import datetime
from .image_utils import async_img_link
from config.settings import SCHEDULE_TIME

def job():
    async_img_link()

def run_schedule():
    schedule.every().day.at(SCHEDULE_TIME).do(job)
    
    while True:
        print(f"Running... at {datetime.now().strftime('%m-%d %H:%M:%S')}")
        schedule.run_pending()
        time.sleep(300)

def start_scheduler():
    """啟動排程器"""
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.daemon = True  # 設置為守護線程，使其在主程序退出時自動終止
    schedule_thread.start()
    return schedule_thread