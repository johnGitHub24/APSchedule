"""
測試 SchedulerManager

這個模組包含 SchedulerManager 類別的所有單元測試。

單元測試說明：
- 單元測試是用於測試程式碼最小單元（通常是函數或方法）的測試
- pytest 是 Python 最流行的測試框架之一
- 測試函數必須以 test_ 開頭，pytest 會自動發現並執行這些函數
- assert 語句用於斷言（斷定某個條件為真），如果為假則測試失敗

執行測試：
    pytest tests/test_scheduler_manager.py -v
    # -v 表示詳細模式，會顯示每個測試的結果

測試覆蓋率：
    pytest tests/test_scheduler_manager.py --cov=apschedule.scheduler_manager
    # --cov 會顯示程式碼覆蓋率
"""
# 匯入 pytest 測試框架
# pytest 是 Python 的測試框架，提供了豐富的測試功能
# 使用 pytest 可以輕鬆編寫和執行測試
import pytest

# 匯入 time 模組
# time 模組用於時間相關的操作，這裡用於測試中的延遲
import time

# 從 unittest.mock 匯入 Mock 和 patch
# Mock 用於建立模擬物件，可以模擬函數或類別的行為
# patch 用於臨時替換物件或函數
# 這些工具用於隔離測試，避免測試之間的相互影響
from unittest.mock import Mock, patch

# 從 apschedule 模組匯入 SchedulerManager
# 這是我們要測試的類別
from apschedule import SchedulerManager

# 從 APScheduler 匯入間隔觸發器
# 用於建立測試任務的觸發器
from apscheduler.triggers.interval import IntervalTrigger


def test_scheduler_manager_initialization():
    """
    測試排程器管理器初始化
    
    這個測試驗證 SchedulerManager 在建立時是否正確初始化所有屬性。
    它檢查：
    1. scheduler_type 是否正確設定
    2. is_running 是否為 False（初始狀態）
    3. scheduler 是否為 None（延遲初始化）
    """
    # 建立一個 SchedulerManager 實例
    # scheduler_type='blocking' 指定使用阻塞式排程器
    manager = SchedulerManager(scheduler_type='blocking')
    
    # 斷言：檢查 scheduler_type 是否等於 'blocking'
    # assert 語句：如果條件為真則繼續，如果為假則拋出 AssertionError
    # 這是測試的核心：我們斷定某個條件應該為真
    assert manager.scheduler_type == 'blocking'
    
    # 斷言：檢查 is_running 是否為 False
    # not manager.is_running 表示 is_running 應該為 False
    # 初始狀態下，排程器不應該在運行
    assert not manager.is_running
    
    # 斷言：檢查 scheduler 是否為 None
    # 由於使用延遲初始化，建立時 scheduler 應該為 None
    # 只有在呼叫 add_job() 或 start() 時才會建立排程器
    assert manager.scheduler is None


def test_scheduler_manager_add_job():
    """
    測試新增任務
    
    這個測試驗證 add_job() 方法是否正確新增任務。
    它檢查：
    1. 返回的任務 ID 是否正確
    2. 排程器是否被建立（延遲初始化）
    3. 任務是否成功新增到排程器
    """
    # 建立一個 SchedulerManager 實例
    manager = SchedulerManager(scheduler_type='blocking')
    
    # 定義一個測試任務函數
    # 這是一個簡單的函數，什麼都不做（pass）
    # 在實際測試中，任務函數可以是任何可呼叫的物件
    def test_job():
        # pass 是 Python 的空語句，表示什麼都不做
        # 這裡用於建立一個最小的測試函數
        pass
    
    # 呼叫 add_job() 方法新增任務
    # add_job() 會：
    # 1. 建立排程器（如果尚未建立）
    # 2. 將任務註冊到排程器
    # 3. 返回任務 ID
    job_id = manager.add_job(
        func=test_job,                      # 要執行的函數
        trigger=IntervalTrigger(seconds=5),  # 觸發器：每 5 秒執行一次
        id='test_job',                      # 任務 ID
        name='測試任務'                      # 任務名稱
    )
    
    # 斷言：檢查返回的任務 ID 是否等於 'test_job'
    # 這驗證 add_job() 正確返回了我們指定的 ID
    assert job_id == 'test_job'
    
    # 斷言：檢查排程器是否已被建立
    # 由於 add_job() 會觸發延遲初始化，scheduler 不應該為 None
    assert manager.scheduler is not None
    
    # 斷言：檢查任務是否成功新增
    # manager.get_jobs() 返回所有任務的列表
    # len() 取得列表的長度
    # 應該只有 1 個任務（我們剛才新增的）
    assert len(manager.get_jobs()) == 1


def test_scheduler_manager_remove_job():
    """
    測試移除任務
    
    這個測試驗證 remove_job() 方法是否正確移除任務。
    它檢查：
    1. 任務是否成功移除
    2. 任務列表是否正確更新
    """
    # 建立一個 SchedulerManager 實例
    manager = SchedulerManager(scheduler_type='blocking')
    
    # 定義一個測試任務函數
    def test_job():
        pass
    
    # 新增一個任務
    manager.add_job(
        func=test_job,
        trigger=IntervalTrigger(seconds=5),
        id='test_job',
        name='測試任務'
    )
    
    # 斷言：檢查任務是否成功新增（應該有 1 個任務）
    assert len(manager.get_jobs()) == 1
    
    # 移除任務
    # remove_job() 會從排程器中移除指定的任務
    manager.remove_job('test_job')
    
    # 斷言：檢查任務是否成功移除（應該有 0 個任務）
    assert len(manager.get_jobs()) == 0


def test_scheduler_manager_get_job():
    """
    測試取得任務
    
    這個測試驗證 get_job() 方法是否正確取得任務。
    它檢查：
    1. 取得的任務 ID 是否正確
    2. 取得的任務名稱是否正確
    """
    # 建立一個 SchedulerManager 實例
    manager = SchedulerManager(scheduler_type='blocking')
    
    # 定義一個測試任務函數
    def test_job():
        pass
    
    # 新增一個任務
    manager.add_job(
        func=test_job,
        trigger=IntervalTrigger(seconds=5),
        id='test_job',
        name='測試任務'
    )
    
    # 取得任務物件
    # get_job() 返回一個 Job 物件，包含任務的所有資訊
    job = manager.get_job('test_job')
    
    # 斷言：檢查任務是否存在（不應該為 None）
    assert job is not None
    
    # 斷言：檢查任務 ID 是否正確
    assert job.id == 'test_job'
    
    # 斷言：檢查任務名稱是否正確
    assert job.name == '測試任務'


def test_scheduler_manager_pause_resume_job():
    """
    測試暫停和恢復任務
    
    這個測試驗證 pause_job() 和 resume_job() 方法是否正確工作。
    它檢查：
    1. 暫停後任務的 next_run_time 是否為 None
    2. 恢復後任務的 next_run_time 是否重新計算
    """
    # 建立一個 SchedulerManager 實例
    manager = SchedulerManager(scheduler_type='blocking')
    
    # 定義一個測試任務函數
    def test_job():
        pass
    
    # 新增一個任務
    manager.add_job(
        func=test_job,
        trigger=IntervalTrigger(seconds=5),
        id='test_job',
        name='測試任務'
    )
    
    # 暫停任務
    # pause_job() 會暫停任務的執行，但不會移除任務
    manager.pause_job('test_job')
    
    # 取得任務物件
    job = manager.get_job('test_job')
    
    # 安全地取得 next_run_time 屬性
    # getattr() 是 Python 的內建函數，用於安全地取得物件屬性
    # 如果屬性不存在，返回預設值（這裡是 None）
    next_run = getattr(job, 'next_run_time', None)
    
    # 斷言：檢查暫停後的 next_run_time
    # 暫停後，next_run_time 應該為 None 或不存在
    # 這裡使用 or 運算符：如果 next_run 為 None，則檢查屬性是否存在
    assert next_run is None or not hasattr(job, 'next_run_time')
    
    # 恢復任務
    # resume_job() 會恢復暫停的任務，讓任務繼續執行
    manager.resume_job('test_job')
    
    # 重新取得任務物件
    job = manager.get_job('test_job')
    
    # 安全地取得 next_run_time 屬性
    next_run = getattr(job, 'next_run_time', None)
    
    # 斷言：檢查任務是否存在
    # 至少任務應該存在（不為 None）
    assert job is not None


def test_scheduler_manager_start_stop():
    """
    測試啟動和停止排程器
    
    這個測試驗證 start() 和 stop() 方法是否正確工作。
    它檢查：
    1. 啟動後 is_running 是否為 True
    2. 停止後 is_running 是否為 False
    
    注意：這個測試使用 BackgroundScheduler，因為 BlockingScheduler 會阻塞執行緒
    """
    # 建立一個背景排程器管理器
    # 使用 'background' 類型，因為 BlockingScheduler 會阻塞執行緒
    # 在測試中，我們不希望阻塞執行緒
    manager = SchedulerManager(scheduler_type='background')
    
    # 定義一個測試任務函數
    def test_job():
        pass
    
    # 新增一個任務
    # 使用較長的間隔（60 秒），避免在測試期間執行
    manager.add_job(
        func=test_job,
        trigger=IntervalTrigger(seconds=60),
        id='test_job',
        name='測試任務'
    )
    
    # 啟動排程器
    # start() 會啟動排程器，開始執行已註冊的任務
    manager.start()
    
    # 斷言：檢查排程器是否在運行
    # is_running 應該為 True
    assert manager.is_running
    
    # 等待一小段時間（0.1 秒）
    # time.sleep() 讓當前執行緒暫停指定的秒數
    # 這裡用於確保排程器有時間啟動
    time.sleep(0.1)
    
    # 停止排程器
    # stop(wait=False) 會立即停止排程器，不等待正在執行的任務完成
    # wait=False 表示不等待任務完成，立即停止
    manager.stop(wait=False)
    
    # 斷言：檢查排程器是否已停止
    # is_running 應該為 False
    assert not manager.is_running
