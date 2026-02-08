"""
基本 APScheduler 範例
展示 Schedule/Job/APScheduler 的基本用法

這個範例展示了如何使用 APScheduler 建立和執行排程任務。
它包含了三種常見的使用方式：
1. 簡單的間隔觸發任務
2. 帶參數的任務
3. Cron 表達式觸發的任務

學習重點：
- 如何建立 BlockingScheduler
- 如何使用 IntervalTrigger 和 CronTrigger
- 如何新增任務到排程器
- 如何啟動和停止排程器
"""
# 從 APScheduler 匯入阻塞式排程器
# BlockingScheduler 會阻塞主執行緒，直到排程器停止
# 適合用於簡單的腳本或單執行緒應用
from apscheduler.schedulers.blocking import BlockingScheduler

# 從 APScheduler 匯入間隔觸發器
# IntervalTrigger 用於定義固定間隔執行的任務
# 例如：每 5 秒、每 10 分鐘、每 1 小時執行一次
from apscheduler.triggers.interval import IntervalTrigger

# 從 APScheduler 匯入 Cron 觸發器
# CronTrigger 用於定義基於 Cron 表達式的任務
# Cron 是一種時間表達式，可以定義複雜的執行時間
# 例如：每天 9 點、每週一、每月 1 號等
from apscheduler.triggers.cron import CronTrigger

# 從 datetime 模組匯入 datetime 類別
# datetime 用於處理日期和時間
# datetime.now() 可以取得當前時間
from datetime import datetime

# 匯入 time 模組（雖然這個範例中沒有使用，但保留以備未來使用）
# time 模組提供了時間相關的功能
import time


def job_function():
    """
    簡單的任務函數
    
    這是一個沒有參數的任務函數，會在排程器觸發時執行。
    它會列印當前時間和一個訊息。
    
    任務函數說明：
    - 任務函數可以是任何可呼叫的 Python 物件（函數、方法等）
    - 函數可以接受參數，參數可以透過 args 和 kwargs 傳遞
    - 如果函數拋出異常，APScheduler 會記錄錯誤但不會停止排程器
    """
    # 使用 f-string 格式化字串
    # datetime.now() 取得當前時間
    # strftime('%Y-%m-%d %H:%M:%S') 將時間格式化為 '2024-01-01 12:00:00' 格式
    # %Y: 四位數年份（例如：2024）
    # %m: 兩位數月份（01-12）
    # %d: 兩位數日期（01-31）
    # %H: 24 小時制小時（00-23）
    # %M: 分鐘（00-59）
    # %S: 秒（00-59）
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行基本任務")


def job_with_params(name, age):
    """
    帶參數的任務函數
    
    這個任務函數接受兩個參數：name（姓名）和 age（年齡）。
    這些參數會在新增任務時透過 args 或 kwargs 傳遞。
    
    Args:
        name: 姓名（字串）
        age: 年齡（整數）
    
    參數傳遞說明：
    - 可以使用 args 傳遞位置參數：args=['張三', 25]
    - 可以使用 kwargs 傳遞關鍵字參數：kwargs={'name': '張三', 'age': 25}
    - args 和 kwargs 可以同時使用
    """
    # 列印當前時間和傳入的參數
    # f-string 可以在字串中嵌入 Python 表達式
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {name}, 年齡: {age}")


def main():
    """
    主函數
    
    這個函數展示了如何使用 APScheduler 建立和執行排程任務。
    它包含了三種常見的使用方式。
    """
    # 建立阻塞式排程器實例
    # BlockingScheduler() 建立一個新的排程器
    # 阻塞式排程器會阻塞主執行緒，直到排程器停止
    # 這意味著 scheduler.start() 後面的程式碼不會執行，直到排程器停止
    scheduler = BlockingScheduler()
    
    # ========== 方式1: 使用 add_job 方法新增簡單的間隔觸發任務 ==========
    # 每 5 秒執行一次
    # scheduler.add_job() 是新增任務的主要方法
    scheduler.add_job(
        job_function,                      # func: 要執行的函數
        trigger=IntervalTrigger(seconds=5),  # trigger: 觸發器，定義何時執行
        id='job_1',                        # id: 任務的唯一識別碼
        name='每5秒執行的任務'              # name: 任務的名稱（用於顯示）
    )
    # IntervalTrigger(seconds=5) 表示每 5 秒執行一次
    # 也可以使用 minutes=1 表示每 1 分鐘，hours=1 表示每 1 小時
    
    # ========== 方式2: 新增帶參數的任務 ==========
    # 每 10 秒執行一次，帶參數
    scheduler.add_job(
        job_with_params,                   # func: 要執行的函數
        trigger=IntervalTrigger(seconds=10), # trigger: 每 10 秒觸發一次
        args=['張三', 25],                 # args: 傳遞給函數的位置參數（列表）
        id='job_2',                        # id: 任務 ID
        name='帶參數的任務'                 # name: 任務名稱
    )
    # args=['張三', 25] 會將 '張三' 和 25 作為位置參數傳遞給 job_with_params
    # 相當於呼叫：job_with_params('張三', 25)
    # 也可以使用 kwargs={'name': '張三', 'age': 25} 來傳遞關鍵字參數
    
    # ========== 方式3: 使用 Cron 表達式 ==========
    # 每分鐘的第 30 秒執行
    scheduler.add_job(
        job_function,                      # func: 要執行的函數
        trigger=CronTrigger(second=30),   # trigger: Cron 觸發器
        id='job_3',                        # id: 任務 ID
        name='Cron任務'                     # name: 任務名稱
    )
    # CronTrigger(second=30) 表示每分鐘的第 30 秒執行
    # 其他 Cron 範例：
    # - CronTrigger(hour=9, minute=0)  # 每天 9 點執行
    # - CronTrigger(day_of_week='mon', hour=9)  # 每週一 9 點執行
    # - CronTrigger(day=1, hour=0)  # 每月 1 號 0 點執行
    
    # 列印提示訊息
    print("排程器已啟動，按 Ctrl+C 停止...")
    print("任務列表:")
    
    # 取得所有已註冊的任務
    # scheduler.get_jobs() 返回一個包含所有 Job 物件的列表
    for job in scheduler.get_jobs():
        # 列印每個任務的 ID 和名稱
        # job.id 是任務的唯一識別碼
        # job.name 是任務的顯示名稱
        print(f"  - {job.id}: {job.name}")
    
    # 使用 try-except 來處理鍵盤中斷
    try:
        # 啟動排程器
        # scheduler.start() 會開始執行已註冊的任務
        # 對於 BlockingScheduler，這會阻塞主執行緒
        # 排程器會持續運行，直到被停止（例如：按 Ctrl+C）
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # 捕獲鍵盤中斷（Ctrl+C）或系統退出異常
        # KeyboardInterrupt: 當使用者按 Ctrl+C 時拋出
        # SystemExit: 當程式正常退出時拋出
        print("\n排程器已停止")
        
        # 關閉排程器
        # scheduler.shutdown() 會停止排程器並清理資源
        # wait=True 表示等待正在執行的任務完成（預設值）
        scheduler.shutdown()


# Python 的主程式入口
# 當這個檔案被直接執行時（不是被匯入），會執行 main() 函數
# __name__ 是 Python 的內建變數：
# - 如果檔案被直接執行，__name__ 的值為 '__main__'
# - 如果檔案被匯入，__name__ 的值為檔案名（不含副檔名）
if __name__ == '__main__':
    # 呼叫主函數
    main()
