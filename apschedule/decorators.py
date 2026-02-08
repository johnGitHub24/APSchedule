"""
裝飾器 - Annotation 方式定義排程任務

這個模組提供了裝飾器功能，讓使用者可以用裝飾器語法來定義排程任務。
裝飾器是 Python 的一個強大特性，可以讓程式碼更簡潔和優雅。

裝飾器說明：
- 裝飾器是一個函數，接受一個函數作為參數，並返回一個新函數
- 使用 @decorator 語法可以將裝飾器應用到函數上
- functools.wraps 可以保留原函數的元資料（名稱、文檔等）
"""
# 從 functools 模組匯入 wraps 函數
# wraps 用於保留被裝飾函數的元資料（名稱、文檔字串等）
# 這樣裝飾後的函數看起來就像原函數一樣
from functools import wraps

# 從 typing 模組匯入型別提示
# Callable: 可呼叫物件型別（函數、方法等）
# Optional: 可選型別（可以是某個型別或 None）
from typing import Callable, Optional

# 從 APScheduler 匯入間隔觸發器
# IntervalTrigger 用於定義固定間隔執行的任務（例如：每 5 秒執行一次）
from apscheduler.triggers.interval import IntervalTrigger

# 從 APScheduler 匯入 Cron 觸發器
# CronTrigger 用於定義基於 Cron 表達式的任務（例如：每天 9 點執行）
from apscheduler.triggers.cron import CronTrigger

# 從 datetime 模組匯入 timedelta（雖然這裡沒用到，但保留以備未來使用）
from datetime import timedelta

# 匯入 logging 模組用於記錄日誌
import logging

# 建立一個 logger 物件，用於記錄這個模組的日誌
logger = logging.getLogger(__name__)

# 全域排程器實例（由使用者設定）
# 這個變數用於儲存全域的排程器實例
# 當使用裝飾器時，任務會自動註冊到這個排程器中
# None 表示尚未設定全域排程器
_global_scheduler = None


def set_global_scheduler(scheduler):
    """
    設定全域排程器
    
    這個函數用於設定全域的排程器實例。
    設定後，使用裝飾器定義的任務會自動註冊到這個排程器中。
    
    Args:
        scheduler: SchedulerManager 實例
            - 必須是 SchedulerManager 或類似的物件
            - 必須有 add_job() 方法
    """
    # 使用 global 關鍵字聲明要修改全域變數
    # 如果不使用 global，Python 會認為這是一個區域變數
    global _global_scheduler
    
    # 將傳入的排程器實例儲存到全域變數中
    _global_scheduler = scheduler


def scheduled_job(trigger, id: Optional[str] = None, name: Optional[str] = None, **kwargs):
    """
    通用排程任務裝飾器
    
    這是一個裝飾器工廠函數，返回一個裝飾器。
    它接受觸發器和其他參數，然後返回一個可以應用到函數上的裝飾器。
    
    Args:
        trigger: 觸發器物件
            - IntervalTrigger: 間隔觸發（例如：每 5 秒執行一次）
            - CronTrigger: Cron 表達式觸發（例如：每天 9 點執行）
            - DateTrigger: 指定日期時間觸發（只執行一次）
        id: 任務的唯一識別碼
            - 如果為 None，會自動使用函數的模組名和函數名作為 ID
            - 例如：'__main__.my_function'
        name: 任務的名稱（可選，用於顯示）
            - 如果為 None，會使用函數名作為名稱
        **kwargs: 其他參數
            - 這些參數會傳遞給 SchedulerManager.add_job() 方法
            - 例如：args, kwargs, replace_existing 等
    
    Returns:
        裝飾器函數
    
    使用範例：
        @scheduled_job(trigger=IntervalTrigger(seconds=5), id='my_job')
        def my_function():
            print("執行任務")
    """
    # 定義裝飾器函數
    # 這個函數接受一個函數作為參數，並返回一個新函數
    def decorator(func: Callable):
        # 使用 @wraps 裝飾器保留原函數的元資料
        # 這樣裝飾後的函數會保留原函數的名稱、文檔字串等
        @wraps(func)
        def wrapper(*args, **func_kwargs):
            # 包裝函數：直接呼叫原函數並返回結果
            # *args 和 **func_kwargs 用於傳遞任意參數給原函數
            return func(*args, **func_kwargs)
        
        # 如果全域排程器已設定，自動註冊任務
        if _global_scheduler is not None:
            # 如果沒有提供任務 ID，則自動產生一個
            # 使用函數的模組名和函數名作為 ID
            # func.__module__ 是函數所在的模組名
            # func.__name__ 是函數的名稱
            job_id = id or f"{func.__module__}.{func.__name__}"
            
            # 如果沒有提供任務名稱，則使用函數名作為名稱
            job_name = name or func.__name__
            
            # 呼叫排程器的 add_job 方法註冊任務
            # 任務會在排程器啟動後自動執行
            _global_scheduler.add_job(
                func=func,          # 要執行的函數
                trigger=trigger,    # 觸發器（決定何時執行）
                id=job_id,          # 任務 ID
                name=job_name,      # 任務名稱
                **kwargs            # 其他參數
            )
            
            # 記錄資訊日誌，表示任務已透過裝飾器註冊
            logger.info(f"任務已透過裝飾器註冊: {job_id}")
        
        # 返回包裝後的函數
        # 這個函數可以像原函數一樣被呼叫
        return wrapper
    
    # 返回裝飾器函數
    # 這樣就可以使用 @scheduled_job(...) 語法了
    return decorator


def interval_job(seconds: int = 0, 
                 minutes: int = 0, 
                 hours: int = 0,
                 id: Optional[str] = None,
                 name: Optional[str] = None,
                 **kwargs):
    """
    間隔時間任務裝飾器
    
    這是一個便利函數，用於建立間隔觸發的任務。
    它會自動建立 IntervalTrigger，然後呼叫 scheduled_job 裝飾器。
    
    Args:
        seconds: 間隔的秒數
            - 例如：5 表示每 5 秒執行一次
            - 預設為 0（不使用秒數）
        minutes: 間隔的分鐘數
            - 例如：10 表示每 10 分鐘執行一次
            - 預設為 0（不使用分鐘數）
        hours: 間隔的小時數
            - 例如：1 表示每 1 小時執行一次
            - 預設為 0（不使用小時數）
        id: 任務的唯一識別碼（可選）
        name: 任務的名稱（可選）
        **kwargs: 其他參數（會傳遞給 scheduled_job）
    
    Returns:
        裝飾器函數
    
    使用範例：
        @interval_job(seconds=5, id='my_job')
        def my_function():
            print("每 5 秒執行一次")
    """
    # 建立間隔觸發器
    # IntervalTrigger 會根據設定的時間間隔觸發任務執行
    # 例如：IntervalTrigger(seconds=5) 表示每 5 秒執行一次
    trigger = IntervalTrigger(seconds=seconds, minutes=minutes, hours=hours)
    
    # 呼叫 scheduled_job 裝飾器並返回
    # 這樣就建立了一個間隔觸發的任務裝飾器
    return scheduled_job(trigger=trigger, id=id, name=name, **kwargs)


def cron_job(year: Optional[str] = None,
             month: Optional[str] = None,
             day: Optional[str] = None,
             week: Optional[str] = None,
             day_of_week: Optional[str] = None,
             hour: Optional[str] = None,
             minute: Optional[str] = None,
             second: Optional[str] = None,
             id: Optional[str] = None,
             name: Optional[str] = None,
             **kwargs):
    """
    Cron 任務裝飾器
    
    這是一個便利函數，用於建立 Cron 表達式觸發的任務。
    它會自動建立 CronTrigger，然後呼叫 scheduled_job 裝飾器。
    
    Cron 表達式說明：
    - Cron 是一種時間表達式，用於定義任務的執行時間
    - 每個欄位可以是數字、範圍（1-5）、列表（1,3,5）或萬用字元（*）
    - 例如：hour='9' 表示每天 9 點執行
    - 例如：day_of_week='mon' 表示每週一執行
    
    Args:
        year: 年（例如：'2024' 或 '2024-2025'）
        month: 月（1-12 或 'jan'-'dec'）
        day: 日（1-31）
        week: 週（1-53）
        day_of_week: 星期幾（0-6 或 'mon'-'sun'）
            - 0 或 'mon' 表示星期一
            - 6 或 'sun' 表示星期日
        hour: 時（0-23）
        minute: 分（0-59）
        second: 秒（0-59）
        id: 任務的唯一識別碼（可選）
        name: 任務的名稱（可選）
        **kwargs: 其他參數（會傳遞給 scheduled_job）
    
    Returns:
        裝飾器函數
    
    使用範例：
        @cron_job(hour=9, minute=0, id='daily_job')
        def daily_task():
            print("每天 9 點執行")
    """
    # 建立 Cron 觸發器
    # CronTrigger 會根據設定的 Cron 表達式觸發任務執行
    # 例如：CronTrigger(hour=9, minute=0) 表示每天 9 點執行
    trigger = CronTrigger(
        year=year,              # 年
        month=month,            # 月
        day=day,                # 日
        week=week,              # 週
        day_of_week=day_of_week,  # 星期幾
        hour=hour,              # 時
        minute=minute,          # 分
        second=second           # 秒
    )
    
    # 呼叫 scheduled_job 裝飾器並返回
    # 這樣就建立了一個 Cron 觸發的任務裝飾器
    return scheduled_job(trigger=trigger, id=id, name=name, **kwargs)
