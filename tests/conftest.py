"""
Pytest 配置檔案

這個檔案是 pytest 的配置檔案，用於設定測試環境和共享的測試資源。

conftest.py 說明：
- conftest.py 是 pytest 的特殊檔案，會被自動載入
- 在這個檔案中定義的 fixture 可以在所有測試文件中使用
- 不需要明確匯入，pytest 會自動發現並載入

Fixture 說明：
- fixture 是 pytest 提供的測試資源管理機制
- 使用 @pytest.fixture 裝飾器定義
- fixture 可以在測試函數中作為參數使用
- yield 語句之前的程式碼是設定（setup）
- yield 語句之後的程式碼是清理（teardown）
"""
# 匯入 pytest 測試框架
# pytest 是 Python 的測試框架，提供了 fixture 功能
import pytest

# 匯入 sys 模組
# sys 模組提供了與 Python 直譯器互動的功能
# sys.path 是 Python 的模組搜尋路徑列表
import sys

# 從 pathlib 模組匯入 Path 類別
# Path 提供了跨平台的檔案路徑操作功能
from pathlib import Path

# 添加專案根目錄到 Python 模組搜尋路徑
# 這樣測試文件就可以匯入專案中的模組了
# __file__ 是當前檔案的路徑
# Path(__file__) 將字串路徑轉換為 Path 物件
# .parent 取得父目錄（tests 目錄）
# .parent 再次取得父目錄（專案根目錄）
project_root = Path(__file__).parent.parent

# sys.path.insert(0, ...) 將路徑插入到搜尋路徑的最前面
# 0 表示插入到列表的最前面（優先搜尋）
# str(project_root) 將 Path 物件轉換為字串
sys.path.insert(0, str(project_root))


@pytest.fixture
def scheduler_manager():
    """
    提供排程器管理器 fixture
    
    這個 fixture 會建立一個 SchedulerManager 實例，並在測試結束後自動清理。
    使用這個 fixture 可以避免在每個測試函數中重複建立和清理排程器。
    
    Fixture 生命週期：
    1. 測試開始前：執行 yield 之前的程式碼（建立排程器）
    2. 測試執行中：返回排程器實例給測試函數使用
    3. 測試結束後：執行 yield 之後的程式碼（清理排程器）
    
    使用方式：
        def test_something(scheduler_manager):
            # scheduler_manager 是自動注入的 SchedulerManager 實例
            scheduler_manager.add_job(...)
    
    Yields:
        SchedulerManager: 排程器管理器實例
    """
    # 從 apschedule 模組匯入 SchedulerManager
    # 這裡在函數內部匯入，避免循環匯入問題
    from apschedule import SchedulerManager
    
    # 建立一個背景排程器管理器實例
    # 使用 'background' 類型，因為它不會阻塞執行緒
    # 在測試中使用背景排程器可以避免阻塞測試執行
    manager = SchedulerManager(scheduler_type='background')
    
    # yield 語句會暫停函數執行，返回 manager 給測試函數使用
    # 測試函數執行完畢後，會繼續執行 yield 之後的程式碼
    yield manager
    
    # 測試結束後的清理程式碼
    # 檢查排程器是否正在運行
    if manager.is_running:
        # 如果正在運行，則停止排程器
        # 這確保測試結束後資源被正確釋放
        manager.stop()


@pytest.fixture
def job_registry():
    """
    提供任務註冊表 fixture
    
    這個 fixture 會建立一個 JobRegistry 實例。
    JobRegistry 不需要特殊的清理，因為它只是儲存任務處理器的字典。
    
    使用方式：
        def test_something(job_registry):
            # job_registry 是自動注入的 JobRegistry 實例
            handler = JobHandler(...)
            job_registry.register(handler)
    
    Returns:
        JobRegistry: 任務註冊表實例
    """
    # 從 apschedule 模組匯入 JobRegistry
    # 這裡在函數內部匯入，避免循環匯入問題
    from apschedule import JobRegistry
    
    # 建立並返回一個新的 JobRegistry 實例
    # 不需要 yield，因為 JobRegistry 不需要清理
    # 直接返回即可
    return JobRegistry()
