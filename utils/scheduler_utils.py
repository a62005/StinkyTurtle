from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import atexit
import sys
import os

# 處理相對導入問題
try:
    from .image_utils import async_img_link
    from config.settings import SCHEDULE_TIME
except ImportError:
    # 如果相對導入失敗，使用絕對導入
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.image_utils import async_img_link
    from config.settings import SCHEDULE_TIME

def job():
    """排程任務：更新圖片"""
    try:
        print(f"開始執行排程任務... at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # 強制更新圖片
        async_img_link(force_update=True)
        print(f"排程任務執行完成 at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"排程任務執行失敗: {e}")

def start_scheduler():
    """啟動排程器"""
    try:
        scheduler = BackgroundScheduler()
        
        # 解析時間 (格式: "13:50")
        hour, minute = map(int, SCHEDULE_TIME.split(':'))
        
        # 添加每日定時任務
        scheduler.add_job(
            func=job,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_update',
            name='每日圖片更新',
            replace_existing=True
        )
        
        # 啟動排程器
        scheduler.start()
        print(f"排程器已啟動，將在每天 {SCHEDULE_TIME} 執行更新任務")
        
        # 確保程序退出時關閉排程器
        atexit.register(lambda: scheduler.shutdown())
        
        return scheduler
    except Exception as e:
        print(f"排程器啟動失敗: {e}")
        return None