"""
測試裝飾器

這個模組包含所有裝飾器相關的單元測試。

測試內容：
1. 設定全域排程器
2. interval_job 裝飾器
3. cron_job 裝飾器
4. scheduled_job 裝飾器

裝飾器測試說明：
- 裝飾器是 Python 的高級特性，用於修改或擴展函數的行為
- 測試裝飾器需要驗證：
  1. 裝飾後的函數仍然可以正常呼叫
  2. 裝飾器正確註冊了任務到排程器
  3. 任務的配置（ID、名稱、觸發器等）正確
"""
# 匯入 pytest 測試框架
import pytest

# 從 unittest.mock 匯入 Mock 和 patch
# Mock 用於建立模擬物件，可以模擬函數或類別的行為
# 在測試中，我們可以使用 Mock 來模擬排程器的行為
from unittest.mock import Mock, patch

# 從 apschedule 模組匯入 SchedulerManager
# 這是我們要測試的類別
from apschedule import SchedulerManager

# 從 apschedule.decorators 匯入裝飾器函數
# 這些是我們要測試的裝飾器
from apschedule.decorators import (
    set_global_scheduler,  # 設定全域排程器的函數
    interval_job,           # 間隔任務裝飾器
    cron_job,               # Cron 任務裝飾器
    scheduled_job            # 通用排程任務裝飾器
)

# 從 APScheduler 匯入觸發器
# 用於建立測試用的觸發器
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger


def test_set_global_scheduler():
    """
    測試設定全域排程器
    
    這個測試驗證 set_global_scheduler() 函數是否正確設定全域排程器。
    全域排程器用於裝飾器自動註冊任務。
    
    測試步驟：
    1. 建立一個 Mock 物件模擬排程器
    2. 呼叫 set_global_scheduler() 設定全域排程器
    3. 驗證全域排程器變數是否正確設定
    """
    # 建立一個 Mock 物件
    # Mock() 會建立一個模擬物件，可以模擬任何屬性和方法
    # 在測試中，我們不需要真實的排程器，只需要模擬物件即可
    scheduler = Mock()
    
    # 呼叫 set_global_scheduler() 設定全域排程器
    # 這個函數會將傳入的排程器儲存到模組的全域變數中
    set_global_scheduler(scheduler)
    
    # 驗證全域排程器已設定
    # 從 decorators 模組匯入 _global_scheduler 全域變數
    # _global_scheduler 是裝飾器模組中的私有全域變數
    from apschedule.decorators import _global_scheduler
    
    # 斷言：檢查全域排程器是否等於我們設定的 Mock 物件
    # is 運算符用於檢查兩個物件是否是同一個物件（身份比較）
    # 這確保全域排程器確實被設定了
    assert _global_scheduler is scheduler


def test_interval_job_decorator():
    """
    測試間隔任務裝飾器
    
    這個測試驗證 @interval_job 裝飾器是否正確工作。
    它檢查：
    1. 裝飾後的函數仍然可以正常呼叫
    2. 任務是否正確註冊到排程器
    3. 任務的配置（ID、名稱）是否正確
    
    裝飾器測試技巧：
    - 裝飾器在函數定義時就會執行（不是呼叫時）
    - 所以我們需要先設定全域排程器，然後定義函數
    - 這樣裝飾器才能正確註冊任務
    """
    # 建立一個排程器管理器實例
    # 使用 'blocking' 類型，但在測試中不會啟動
    scheduler = SchedulerManager(scheduler_type='blocking')
    
    # 設定全域排程器
    # 這必須在定義使用裝飾器的函數之前完成
    # 因為裝飾器在函數定義時就會執行
    set_global_scheduler(scheduler)
    
    # 使用 @interval_job 裝飾器定義一個測試函數
    # @interval_job 是裝飾器語法，相當於：
    # def test_func(): ...
    # test_func = interval_job(seconds=5, id='test_job', name='測試任務')(test_func)
    # 裝飾器會在函數定義時執行，自動註冊任務到全域排程器
    @interval_job(seconds=5, id='test_job', name='測試任務')
    def test_func():
        # 這是一個簡單的測試函數，返回字串 "test"
        return "test"
    
    # 驗證函數仍然可以正常呼叫
    # 裝飾器不應該影響函數的正常功能
    # 裝飾後的函數應該可以像原函數一樣被呼叫
    result = test_func()
    
    # 斷言：檢查函數返回值是否正確
    assert result == "test"
    
    # 驗證任務已註冊
    # scheduler.get_jobs() 返回所有已註冊的任務列表
    # 應該有 1 個任務（我們剛才透過裝飾器註冊的）
    assert len(scheduler.get_jobs()) == 1
    
    # 取得任務物件
    # scheduler.get_job() 根據任務 ID 取得任務物件
    job = scheduler.get_job('test_job')
    
    # 斷言：檢查任務是否存在
    assert job is not None
    
    # 斷言：檢查任務名稱是否正確
    # 這驗證裝飾器正確設定了任務的名稱
    assert job.name == '測試任務'


def test_cron_job_decorator():
    """
    測試 Cron 任務裝飾器
    
    這個測試驗證 @cron_job 裝飾器是否正確工作。
    它檢查：
    1. 裝飾後的函數仍然可以正常呼叫
    2. 任務是否正確註冊到排程器
    3. 任務是否使用 CronTrigger
    
    Cron 裝飾器說明：
    - @cron_job 用於建立基於 Cron 表達式的任務
    - 它內部會建立 CronTrigger，然後呼叫 scheduled_job 裝飾器
    - 使用方式類似 @interval_job，但參數是 Cron 表達式的各個部分
    """
    # 建立一個排程器管理器實例
    scheduler = SchedulerManager(scheduler_type='blocking')
    
    # 設定全域排程器
    set_global_scheduler(scheduler)
    
    # 使用 @cron_job 裝飾器定義一個測試函數
    # @cron_job 接受 Cron 表達式的各個部分作為參數
    # hour=9, minute=0 表示每天 9 點執行
    @cron_job(hour=9, minute=0, id='cron_job', name='Cron任務')
    def test_func():
        # 測試函數，返回字串 "test"
        return "test"
    
    # 驗證函數仍然可以正常呼叫
    result = test_func()
    
    # 斷言：檢查函數返回值是否正確
    assert result == "test"
    
    # 驗證任務已註冊
    # 應該有 1 個任務
    assert len(scheduler.get_jobs()) == 1
    
    # 取得任務物件
    job = scheduler.get_job('cron_job')
    
    # 斷言：檢查任務是否存在
    assert job is not None


def test_scheduled_job_decorator():
    """
    測試通用排程任務裝飾器
    
    這個測試驗證 @scheduled_job 裝飾器是否正確工作。
    @scheduled_job 是最通用的裝飾器，可以接受任何觸發器。
    
    裝飾器層次說明：
    - @scheduled_job: 最底層的裝飾器，接受任何觸發器
    - @interval_job: 基於 @scheduled_job，自動建立 IntervalTrigger
    - @cron_job: 基於 @scheduled_job，自動建立 CronTrigger
    
    使用 @scheduled_job 的場景：
    - 需要使用自訂的觸發器
    - 需要更靈活的配置
    """
    # 建立一個排程器管理器實例
    scheduler = SchedulerManager(scheduler_type='blocking')
    
    # 設定全域排程器
    set_global_scheduler(scheduler)
    
    # 建立一個間隔觸發器
    # IntervalTrigger(seconds=10) 表示每 10 秒執行一次
    # 這裡手動建立觸發器，然後傳給 @scheduled_job 裝飾器
    trigger = IntervalTrigger(seconds=10)
    
    # 使用 @scheduled_job 裝飾器定義一個測試函數
    # @scheduled_job 接受 trigger 參數，可以是任何觸發器類型
    @scheduled_job(trigger=trigger, id='scheduled_job', name='排程任務')
    def test_func():
        # 測試函數，返回字串 "test"
        return "test"
    
    # 驗證函數仍然可以正常呼叫
    result = test_func()
    
    # 斷言：檢查函數返回值是否正確
    assert result == "test"
    
    # 驗證任務已註冊
    # 應該有 1 個任務
    assert len(scheduler.get_jobs()) == 1
