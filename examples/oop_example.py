"""
OOP 設計範例
展示如何使用 SchedulerManager 和 JobHandler

這個範例展示了如何使用物件導向的方式來管理排程任務。
它使用了 JobHandler 來封裝任務的執行邏輯和統計資訊。

學習重點：
- 如何使用 SchedulerManager 管理排程器
- 如何使用 JobHandler 封裝任務邏輯
- 如何使用 JobRegistry 管理多個任務處理器
- 如何追蹤任務的執行統計資訊
"""
# 匯入 sys 模組
# sys 模組提供了與 Python 直譯器互動的功能
import sys

# 匯入 os 模組（雖然這個範例中沒有使用，但保留以備未來使用）
import os

# 從 pathlib 模組匯入 Path 類別
# Path 提供了跨平台的檔案路徑操作功能
from pathlib import Path

# 添加專案根目錄到 Python 模組搜尋路徑
# 這樣就可以匯入專案中的模組了
# __file__ 是當前檔案的路徑
# Path(__file__) 將字串路徑轉換為 Path 物件
# .parent 取得父目錄（examples 目錄）
# .parent 再次取得父目錄（專案根目錄）
project_root = Path(__file__).parent.parent

# sys.path.insert(0, ...) 將路徑插入到搜尋路徑的最前面
# 0 表示插入到列表的最前面（優先搜尋）
sys.path.insert(0, str(project_root))

# 從 apschedule 模組匯入需要的類別
# SchedulerManager: 排程器管理器，用於管理排程器
# JobHandler: 任務處理器，用於封裝任務的執行邏輯
# JobRegistry: 任務註冊表，用於管理多個任務處理器
from apschedule import SchedulerManager, JobHandler, JobRegistry

# 從 APScheduler 匯入間隔觸發器
# IntervalTrigger 用於定義固定間隔執行的任務
from apscheduler.triggers.interval import IntervalTrigger

# 從 datetime 模組匯入 datetime 類別
# datetime 用於處理日期和時間
from datetime import datetime

# 匯入 time 模組（雖然這個範例中沒有使用，但保留以備未來使用）
import time

# 匯入 logging 模組用於記錄日誌
import logging

# 設定日誌的基本配置
# basicConfig() 用於設定日誌系統的基本配置
logging.basicConfig(
    level=logging.INFO,  # 設定日誌級別為 INFO（資訊級別）
    # 設定日誌格式
    # %(asctime)s: 時間戳記
    # %(name)s: logger 的名稱
    # %(levelname)s: 日誌級別
    # %(message)s: 日誌訊息
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def task_1():
    """
    任務1: 簡單的任務
    
    這是一個沒有參數的簡單任務函數。
    它會在執行時列印當前時間和任務名稱。
    """
    # 使用 f-string 格式化字串並列印
    # datetime.now() 取得當前時間
    # strftime('%Y-%m-%d %H:%M:%S') 將時間格式化為 '2024-01-01 12:00:00' 格式
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行任務1")


def task_2(name: str, value: int):
    """
    任務2: 帶參數的任務
    
    這是一個接受兩個參數的任務函數。
    這些參數會在建立 JobHandler 時透過 kwargs 傳遞。
    
    Args:
        name: 名稱（字串）
        value: 數值（整數）
    """
    # 列印當前時間和傳入的參數
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行任務2: {name}, 值: {value}")


def task_3():
    """
    任務3: 另一個任務
    
    這是第三個任務函數，用於展示多個任務的管理。
    """
    # 列印當前時間和任務名稱
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行任務3")


def main():
    """
    主函數
    
    這個函數展示了如何使用 OOP 方式管理排程任務。
    它包含以下步驟：
    1. 建立排程器管理器和任務註冊表
    2. 建立任務處理器並註冊
    3. 將任務處理器包裝成可執行的函數
    4. 新增任務到排程器
    5. 啟動排程器並顯示統計資訊
    """
    # ========== 步驟1: 建立排程器管理器和任務註冊表 ==========
    
    # 建立排程器管理器實例
    # scheduler_type='blocking' 指定使用阻塞式排程器
    # BlockingScheduler 會阻塞主執行緒，直到排程器停止
    scheduler_manager = SchedulerManager(scheduler_type='blocking')
    
    # 建立任務註冊表實例
    # JobRegistry 用於管理多個任務處理器
    # 它提供了統一的註冊、查詢和統計功能
    registry = JobRegistry()
    
    # ========== 步驟2: 建立任務處理器 ==========
    
    # 建立第一個任務處理器
    # JobHandler 封裝了任務的執行邏輯和統計資訊
    handler1 = JobHandler(
        job_id='task_1',      # 任務的唯一識別碼
        name='任務1',          # 任務的顯示名稱
        func=task_1            # 要執行的函數
    )
    
    # 建立第二個任務處理器（帶參數）
    # 注意：傳遞給任務函數的參數應該放在 kwargs 中
    # 這些參數會在執行任務時傳遞給函數
    handler2 = JobHandler(
        job_id='task_2',       # 任務的唯一識別碼
        name='任務2',          # 任務的顯示名稱
        func=task_2,           # 要執行的函數
        # 以下是傳遞給 task_2 函數的參數（透過 kwargs）
        # 這些參數會在 handler2.execute() 時傳遞給 task_2
        value=100              # 傳遞給 task_2 的 value 參數
    )
    # 注意：這裡的 name='測試' 是傳遞給 task_2 函數的參數
    # 它與 JobHandler 的 name='任務2' 參數不同
    # JobHandler 的 name 是任務的顯示名稱
    # 而 kwargs 中的 name 是傳遞給函數的參數
    
    # 建立第三個任務處理器
    handler3 = JobHandler(
        job_id='task_3',       # 任務的唯一識別碼
        name='任務3',          # 任務的顯示名稱
        func=task_3            # 要執行的函數
    )
    
    # ========== 步驟3: 註冊任務處理器 ==========
    
    # 將任務處理器註冊到註冊表中
    # 註冊後，可以透過註冊表查詢和管理任務處理器
    registry.register(handler1)
    registry.register(handler2)
    registry.register(handler3)
    
    # ========== 步驟4: 將任務處理器包裝成可執行的函數 ==========
    
    # 定義包裝函數，用於執行任務處理器
    # 這些函數會在排程器觸發時被呼叫
    def wrapped_task_1():
        """
        包裝函數1: 執行第一個任務處理器
        
        這個函數會在排程器觸發時被呼叫。
        它會呼叫 handler1.execute() 來執行任務並更新統計資訊。
        """
        # 呼叫任務處理器的 execute() 方法
        # execute() 會執行任務函數並更新統計資訊
        handler1.execute()
    
    def wrapped_task_2():
        """
        包裝函數2: 執行第二個任務處理器
        
        這個函數會在排程器觸發時被呼叫。
        它會呼叫 handler2.execute() 來執行任務。
        注意：handler2 已經在建立時設定了參數（name='測試', value=100）
        所以 execute() 不需要額外的參數。
        """
        # 呼叫任務處理器的 execute() 方法
        # handler2 的參數已經在建立時設定，所以不需要傳遞參數
        handler2.execute()
    
    def wrapped_task_3():
        """
        包裝函數3: 執行第三個任務處理器
        
        這個函數會在排程器觸發時被呼叫。
        """
        # 呼叫任務處理器的 execute() 方法
        handler3.execute()
    
    # ========== 步驟5: 新增任務到排程器 ==========
    
    # 新增第一個任務到排程器
    # 使用包裝函數作為要執行的函數
    scheduler_manager.add_job(
        func=wrapped_task_1,                   # 要執行的函數（包裝函數）
        trigger=IntervalTrigger(seconds=5),    # 觸發器：每 5 秒執行一次
        id='task_1',                           # 任務 ID（與 handler1 的 job_id 相同）
        name='任務1'                            # 任務名稱（用於顯示）
    )
    
    # 新增第二個任務到排程器
    scheduler_manager.add_job(
        func=wrapped_task_2,                   # 要執行的函數（包裝函數）
        trigger=IntervalTrigger(seconds=10),   # 觸發器：每 10 秒執行一次
        id='task_2',                           # 任務 ID
        name='任務2'                            # 任務名稱
    )
    
    # 新增第三個任務到排程器
    scheduler_manager.add_job(
        func=wrapped_task_3,                   # 要執行的函數（包裝函數）
        trigger=IntervalTrigger(seconds=15),   # 觸發器：每 15 秒執行一次
        id='task_3',                           # 任務 ID
        name='任務3'                            # 任務名稱
    )
    
    # ========== 步驟6: 顯示任務列表並啟動排程器 ==========
    
    # 列印提示訊息
    print("排程器已啟動，按 Ctrl+C 停止...")
    print("\n任務列表:")
    
    # 取得所有已註冊的任務並列印
    # scheduler_manager.get_jobs() 返回所有任務的列表
    for job in scheduler_manager.get_jobs():
        # 列印每個任務的 ID 和名稱
        # job.id 是任務的唯一識別碼
        # job.name 是任務的顯示名稱
        print(f"  - {job.id}: {job.name}")
    
    # 使用 try-except 來處理鍵盤中斷
    try:
        # 啟動排程器
        # scheduler_manager.start() 會開始執行已註冊的任務
        # 對於 BlockingScheduler，這會阻塞主執行緒
        # 排程器會持續運行，直到被停止（例如：按 Ctrl+C）
        scheduler_manager.start()
    except (KeyboardInterrupt, SystemExit):
        # 捕獲鍵盤中斷（Ctrl+C）或系統退出異常
        # KeyboardInterrupt: 當使用者按 Ctrl+C 時拋出
        # SystemExit: 當程式正常退出時拋出
        
        # 列印停止訊息
        print("\n\n排程器已停止")
        print("\n任務統計:")
        
        # 取得所有任務的統計資訊
        # registry.get_stats() 返回一個字典，包含所有任務的統計資訊
        stats = registry.get_stats()
        
        # 遍歷所有任務的統計資訊並列印
        # stats.items() 返回 (job_id, stat_dict) 的元組列表
        for job_id, stat in stats.items():
            # 列印任務的基本資訊
            print(f"\n{stat['name']} (ID: {stat['job_id']}):")
            
            # 列印執行次數
            # execution_count 記錄任務執行了多少次
            print(f"  執行次數: {stat['execution_count']}")
            
            # 列印錯誤次數
            # error_count 記錄任務執行失敗了多少次
            print(f"  錯誤次數: {stat['error_count']}")
            
            # 列印最後執行時間
            # last_execution_time 記錄任務最後一次執行的時間
            print(f"  最後執行時間: {stat['last_execution_time']}")
        
        # 停止排程器
        # scheduler_manager.stop() 會停止排程器並清理資源
        scheduler_manager.stop()


# Python 的主程式入口
# 當這個檔案被直接執行時（不是被匯入），會執行 main() 函數
# __name__ 是 Python 的內建變數：
# - 如果檔案被直接執行，__name__ 的值為 '__main__'
# - 如果檔案被匯入，__name__ 的值為檔案名（不含副檔名）
if __name__ == '__main__':
    # 呼叫主函數
    main()
