"""
時區工具模組
提供統一的時區處理功能
"""
from datetime import datetime, timezone, timedelta

# 定義台北時區 (GMT+8)
TAIPEI_TZ = timezone(timedelta(hours=8))

def get_taipei_now():
    """獲取台北時間的當前時間"""
    return datetime.now(TAIPEI_TZ)

def get_taipei_today():
    """獲取台北時間的今天日期字符串"""
    return get_taipei_now().strftime('%Y-%m-%d')

def get_taipei_yesterday():
    """獲取台北時間的昨天日期字符串"""
    yesterday = get_taipei_now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def format_taipei_time(dt=None, format_str='%Y-%m-%d %H:%M:%S %Z'):
    """格式化台北時間"""
    if dt is None:
        dt = get_taipei_now()
    elif dt.tzinfo is None:
        # 如果沒有時區資訊，假設是台北時間
        dt = dt.replace(tzinfo=TAIPEI_TZ)
    elif dt.tzinfo != TAIPEI_TZ:
        # 轉換到台北時區
        dt = dt.astimezone(TAIPEI_TZ)
    
    return dt.strftime(format_str)

def utc_to_taipei(utc_dt):
    """將 UTC 時間轉換為台北時間"""
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(TAIPEI_TZ)

def taipei_to_utc(taipei_dt):
    """將台北時間轉換為 UTC 時間"""
    if taipei_dt.tzinfo is None:
        taipei_dt = taipei_dt.replace(tzinfo=TAIPEI_TZ)
    return taipei_dt.astimezone(timezone.utc)