from datetime import datetime, timedelta
from config.settings import TARGET_TIME, DRAFT_TIME

def check_date(date: str) -> bool:
    if not date:
        return False
    # 獲取當前日期並將其格式化為字符串
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 將輸入的日期與當前日期進行比較
    return date == current_date

def is_time_between(start_time_str='00:00', end_time_str='14:00'):
    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()
    
    # 如果開始時間小於結束時間，則檢查當前時間是否在這個範圍內 
    if start_time < end_time:
        return start_time <= datetime.now().time() <= end_time
    # 如果開始時間大於結束時間，則檢查當前時間是否在這個範圍內
    else:
        return datetime.now().time() >= start_time or datetime.now().time() <= end_time

def time_until_target():
    # 設定未來的時間點，例如 "10/07 22:00"
    future_time_str = TARGET_TIME

    # 取得當前年份，並將未來的時間點轉換為 datetime 對象
    current_year = datetime.now().year
    future_time = datetime.strptime(f"{current_year}/{future_time_str}", "%Y/%m/%d %H:%M")

    # 取得當前時間
    now = datetime.now()

    # 計算剩餘時間
    remaining_time = future_time - now

    # 如果指定的時間已經過去，返回0時間
    if remaining_time.total_seconds() < 0:
        remaining_time = timedelta(0)

    # 格式化為 dd hh:mm:ss
    days = remaining_time.days
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"距離開打 \n倒數 {days:02d}天 {hours:02d}小時 {minutes:02d}分 {seconds:02d}秒"

def time_until_draft():
    # 設定未來的時間點，例如 "10/07 22:00"
    future_time_str = DRAFT_TIME

    # 取得當前年份，並將未來的時間點轉換為 datetime 對象
    current_year = datetime.now().year
    future_time = datetime.strptime(f"{current_year}/{future_time_str}", "%Y/%m/%d %H:%M")

    # 取得當前時間
    now = datetime.now()

    # 計算剩餘時間
    remaining_time = future_time - now

    # 如果指定的時間已經過去，返回0時間
    if remaining_time.total_seconds() < 0:
        remaining_time = timedelta(0)

    # 格式化為 dd hh:mm:ss
    days = remaining_time.days
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"距離選秀 \n倒數 {days:02d}天 {hours:02d}小時 {minutes:02d}分 {seconds:02d}秒"