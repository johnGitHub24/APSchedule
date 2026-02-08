"""
測試 JobHandler

這個模組包含 JobHandler 和 JobRegistry 類別的所有單元測試。

測試內容：
1. 任務處理器初始化
2. 任務執行（正常情況）
3. 任務執行錯誤處理
4. 取得統計資訊
5. 重置統計資訊
6. 任務註冊表操作
7. 取得所有任務處理器
8. 取得所有任務統計資訊

測試策略：
- 使用簡單的測試函數，避免複雜的依賴
- 使用列表來追蹤函數是否被執行
- 使用 pytest.raises() 測試異常情況
- 驗證統計資訊的正確性
"""
# 匯入 pytest 測試框架
import pytest

# 從 datetime 模組匯入 datetime 類別
# 用於驗證 last_execution_time 是否正確設定
from datetime import datetime

# 從 apschedule 模組匯入要測試的類別
from apschedule import JobHandler, JobRegistry


def test_job_handler_initialization():
    """
    測試任務處理器初始化
    
    這個測試驗證 JobHandler 在建立時是否正確初始化所有屬性。
    它檢查：
    1. job_id 是否正確設定
    2. name 是否正確設定
    3. 統計變數是否初始化為 0 或 None
    """
    # 定義一個測試函數
    # 這是一個簡單的函數，返回字串 "test"
    def test_func():
        return "test"
    
    # 建立一個 JobHandler 實例
    # JobHandler 需要三個必要參數：job_id, name, func
    handler = JobHandler(
        job_id='test_job',      # 任務 ID
        name='測試任務',         # 任務名稱
        func=test_func          # 要執行的函數
    )
    
    # 斷言：檢查任務 ID 是否正確
    assert handler.job_id == 'test_job'
    
    # 斷言：檢查任務名稱是否正確
    assert handler.name == '測試任務'
    
    # 斷言：檢查執行計數器是否初始化為 0
    # 初始狀態下，任務尚未執行，所以計數器應該為 0
    assert handler.execution_count == 0
    
    # 斷言：檢查錯誤計數器是否初始化為 0
    assert handler.error_count == 0
    
    # 斷言：檢查最後執行時間是否初始化為 None
    # 初始狀態下，任務尚未執行，所以時間應該為 None
    assert handler.last_execution_time is None


def test_job_handler_execute():
    """
    測試任務執行
    
    這個測試驗證 JobHandler.execute() 是否正確執行任務並更新統計資訊。
    它檢查：
    1. 函數是否被執行
    2. 返回值是否正確
    3. 執行計數器是否增加
    4. 最後執行時間是否被設定
    """
    # 建立一個列表來追蹤函數是否被執行
    # 這是一個常見的測試技巧，用於驗證函數是否被呼叫
    execution_log = []
    
    # 定義一個測試函數
    # 這個函數會在執行時將 'executed' 添加到 execution_log 中
    def test_func():
        execution_log.append('executed')  # 記錄函數已被執行
        return "success"                   # 返回成功訊息
    
    # 建立一個 JobHandler 實例
    handler = JobHandler(
        job_id='test_job',
        name='測試任務',
        func=test_func
    )
    
    # 執行任務
    # execute() 方法會呼叫任務函數並更新統計資訊
    result = handler.execute()
    
    # 斷言：檢查函數返回值是否正確
    assert result == "success"
    
    # 斷言：檢查執行計數器是否增加為 1
    # 執行一次後，計數器應該從 0 變為 1
    assert handler.execution_count == 1
    
    # 斷言：檢查最後執行時間是否被設定
    # 執行後，last_execution_time 應該是一個 datetime 物件，不應該是 None
    assert handler.last_execution_time is not None
    
    # 斷言：檢查函數是否被執行
    # execution_log 應該包含 'executed'，表示函數確實被執行了
    assert len(execution_log) == 1


def test_job_handler_execute_with_error():
    """
    測試任務執行錯誤處理
    
    這個測試驗證當任務執行失敗時，JobHandler 是否正確處理錯誤。
    它檢查：
    1. 異常是否被重新拋出
    2. 錯誤計數器是否增加
    3. 錯誤訊息是否被記錄
    """
    # 定義一個會拋出異常的測試函數
    def test_func():
        # raise 語句用於拋出異常
        # ValueError 是內建的異常類別，用於表示值錯誤
        raise ValueError("測試錯誤")
    
    # 建立一個 JobHandler 實例
    handler = JobHandler(
        job_id='test_job',
        name='測試任務',
        func=test_func
    )
    
    # 使用 pytest.raises() 測試異常
    # pytest.raises(ValueError) 表示我們期望拋出 ValueError 異常
    # 如果沒有拋出異常，或拋出其他異常，測試會失敗
    with pytest.raises(ValueError):
        # 執行任務，這應該會拋出 ValueError 異常
        handler.execute()
    
    # 斷言：檢查錯誤計數器是否增加為 1
    # 執行失敗後，error_count 應該從 0 變為 1
    assert handler.error_count == 1
    
    # 斷言：檢查錯誤訊息是否被記錄
    # last_error 應該包含異常的訊息字串
    assert handler.last_error == "測試錯誤"


def test_job_handler_get_stats():
    """
    測試取得統計資訊
    
    這個測試驗證 JobHandler.get_stats() 是否正確返回統計資訊。
    它檢查返回的字典是否包含所有必要的鍵和正確的值。
    """
    # 定義一個測試函數
    def test_func():
        return "test"
    
    # 建立一個 JobHandler 實例
    handler = JobHandler(
        job_id='test_job',
        name='測試任務',
        func=test_func
    )
    
    # 執行任務一次，以便產生統計資料
    handler.execute()
    
    # 取得統計資訊
    # get_stats() 返回一個包含所有統計資訊的字典
    stats = handler.get_stats()
    
    # 斷言：檢查統計字典是否包含所有必要的鍵
    assert stats['job_id'] == 'test_job'              # 任務 ID
    assert stats['name'] == '測試任務'                 # 任務名稱
    assert stats['execution_count'] == 1              # 執行次數
    assert stats['error_count'] == 0                  # 錯誤次數
    assert stats['last_execution_time'] is not None   # 最後執行時間


def test_job_handler_reset_stats():
    """
    測試重置統計資訊
    
    這個測試驗證 JobHandler.reset_stats() 是否正確重置所有統計資訊。
    它檢查重置後所有統計變數是否回到初始狀態。
    """
    # 定義一個測試函數
    def test_func():
        return "test"
    
    # 建立一個 JobHandler 實例
    handler = JobHandler(
        job_id='test_job',
        name='測試任務',
        func=test_func
    )
    
    # 執行任務一次，產生一些統計資料
    handler.execute()
    
    # 重置統計資訊
    # reset_stats() 會將所有統計變數重置為初始狀態
    handler.reset_stats()
    
    # 斷言：檢查所有統計變數是否已重置
    assert handler.execution_count == 0              # 執行計數器應該為 0
    assert handler.error_count == 0                    # 錯誤計數器應該為 0
    assert handler.last_execution_time is None         # 最後執行時間應該為 None
    assert handler.last_error is None                  # 最後錯誤應該為 None


def test_job_registry():
    """
    測試任務註冊表
    
    這個測試驗證 JobRegistry 的基本功能：
    1. 註冊任務處理器
    2. 取得任務處理器
    3. 取消註冊任務處理器
    """
    # 建立一個 JobRegistry 實例
    registry = JobRegistry()
    
    # 定義一個測試函數
    def test_func():
        return "test"
    
    # 建立一個 JobHandler 實例
    handler = JobHandler(
        job_id='test_job',
        name='測試任務',
        func=test_func
    )
    
    # 註冊任務處理器
    # register() 會將任務處理器儲存到註冊表中
    registry.register(handler)
    
    # 斷言：檢查任務處理器是否成功註冊
    # get_handler() 應該返回剛才註冊的處理器，不應該是 None
    assert registry.get_handler('test_job') is not None
    
    # 取消註冊任務處理器
    # unregister() 會從註冊表中移除任務處理器
    registry.unregister('test_job')
    
    # 斷言：檢查任務處理器是否成功取消註冊
    # get_handler() 應該返回 None，因為處理器已被移除
    assert registry.get_handler('test_job') is None


def test_job_registry_get_all_handlers():
    """
    測試取得所有任務處理器
    
    這個測試驗證 JobRegistry.get_all_handlers() 是否正確返回所有已註冊的任務處理器。
    """
    # 建立一個 JobRegistry 實例
    registry = JobRegistry()
    
    # 建立兩個任務處理器
    # lambda: None 是一個匿名函數，什麼都不做
    # 在測試中，我們不需要實際的函數邏輯，只需要函數物件即可
    handler1 = JobHandler('job1', '任務1', lambda: None)
    handler2 = JobHandler('job2', '任務2', lambda: None)
    
    # 註冊兩個任務處理器
    registry.register(handler1)
    registry.register(handler2)
    
    # 取得所有任務處理器
    # get_all_handlers() 返回一個包含所有處理器的字典副本
    handlers = registry.get_all_handlers()
    
    # 斷言：檢查處理器數量是否正確
    assert len(handlers) == 2
    
    # 斷言：檢查兩個處理器是否都在字典中
    # 'job1' in handlers 檢查鍵是否存在於字典中
    assert 'job1' in handlers
    assert 'job2' in handlers


def test_job_registry_get_stats():
    """
    測試取得所有任務統計資訊
    
    這個測試驗證 JobRegistry.get_stats() 是否正確返回所有任務的統計資訊。
    """
    # 建立一個 JobRegistry 實例
    registry = JobRegistry()
    
    # 建立一個任務處理器
    handler = JobHandler('test_job', '測試任務', lambda: None)
    
    # 執行任務一次，產生統計資料
    handler.execute()
    
    # 註冊任務處理器
    registry.register(handler)
    
    # 取得所有任務的統計資訊
    # get_stats() 返回一個字典，鍵是任務 ID，值是統計資訊字典
    stats = registry.get_stats()
    
    # 斷言：檢查統計字典是否包含任務 ID
    assert 'test_job' in stats
    
    # 斷言：檢查任務的執行次數是否正確
    # stats['test_job'] 是任務的統計資訊字典
    # ['execution_count'] 是執行次數
    assert stats['test_job']['execution_count'] == 1
