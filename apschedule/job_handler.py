"""
任務處理器 - OOP 設計

這個模組提供了 JobHandler 和 JobRegistry 類別，用於管理任務的執行和統計。

JobHandler: 封裝任務的執行邏輯，記錄執行統計資訊
JobRegistry: 管理多個任務處理器，提供統一的註冊和查詢介面
"""
# 從 typing 模組匯入型別提示
# Callable: 可呼叫物件型別（函數、方法等）
# Dict: 字典型別
# Any: 任意型別
# Optional: 可選型別（可以是某個型別或 None）
from typing import Callable, Dict, Any, Optional

# 從 datetime 模組匯入 datetime 類別
# datetime 用於處理日期和時間
from datetime import datetime

# 匯入 logging 模組用於記錄日誌
# logging 是 Python 標準庫，用於記錄程式執行過程中的資訊、警告和錯誤
import logging

# 建立一個 logger 物件，用於記錄這個模組的日誌
# __name__ 是當前模組的名稱，這樣可以追蹤日誌來自哪個模組
logger = logging.getLogger(__name__)


class JobHandler:
    """
    任務處理器類別
    
    這個類別封裝了任務的執行邏輯，並記錄執行統計資訊。
    它提供了：
    1. 任務執行功能（帶錯誤處理）
    2. 執行統計追蹤（執行次數、錯誤次數等）
    3. 統計資訊查詢和重置功能
    """
    
    def __init__(self, job_id: str, name: str, func: Callable, **kwargs):
        """
        初始化任務處理器
        
        這個方法會建立一個新的任務處理器實例，並初始化所有統計變數。
        
        Args:
            job_id: 任務的唯一識別碼
                - 用於識別不同的任務
                - 建議使用有意義的名稱，例如：'daily_report'、'hourly_check'
            name: 任務的顯示名稱
                - 用於日誌和顯示，可以更友好地描述任務
            func: 要執行的函數
                - 必須是可呼叫的 Python 物件（函數、方法等）
                - 這個函數會在 execute() 方法中被呼叫
            **kwargs: 其他參數
                - 這些參數會在執行任務時傳遞給函數
                - 例如：name='測試', count=100
        """
        # 儲存任務 ID
        self.job_id = job_id
        
        # 儲存任務名稱
        self.name = name
        
        # 儲存要執行的函數
        # func 是一個可呼叫物件，可以是函數、方法或任何實現 __call__ 的物件
        self.func = func
        
        # 儲存額外的關鍵字參數
        # 這些參數會在執行任務時與執行時傳入的參數合併
        self.kwargs = kwargs
        
        # 初始化執行計數器
        # 用於追蹤任務執行了多少次
        self.execution_count = 0
        
        # 初始化最後執行時間
        # Optional[datetime] 表示這個變數可以是 datetime 物件或 None
        # 初始為 None，表示尚未執行過
        self.last_execution_time: Optional[datetime] = None
        
        # 初始化錯誤計數器
        # 用於追蹤任務執行失敗了多少次
        self.error_count = 0
        
        # 初始化最後錯誤訊息
        # Optional[str] 表示這個變數可以是字串或 None
        # 初始為 None，表示尚未發生錯誤
        self.last_error: Optional[str] = None
    
    def execute(self, *args, **kwargs):
        """
        執行任務
        
        這個方法會執行任務函數，並記錄執行結果和統計資訊。
        如果執行失敗，會捕獲異常並記錄錯誤資訊。
        
        Args:
            *args: 位置參數
                - 這些參數會直接傳遞給任務函數
                - *args 是 Python 的可變位置參數語法
            **kwargs: 關鍵字參數
                - 這些參數會與初始化時的 kwargs 合併後傳遞給任務函數
                - **kwargs 是 Python 的可變關鍵字參數語法
                - 執行時傳入的參數會覆蓋初始化時的參數
        
        Returns:
            任務函數的返回值
        
        Raises:
            Exception: 如果任務執行失敗，會重新拋出異常
        """
        # 使用 try-except 來捕獲執行過程中的異常
        try:
            # 記錄資訊日誌，表示開始執行任務
            # f-string 是 Python 3.6+ 的字串格式化語法，可以在字串中嵌入表達式
            logger.info(f"開始執行任務: {self.name} (ID: {self.job_id})")
            
            # 增加執行計數器
            # 每次執行任務時，計數器加 1
            self.execution_count += 1
            
            # 記錄當前時間作為最後執行時間
            # datetime.now() 返回當前的日期和時間
            self.last_execution_time = datetime.now()
            
            # 合併初始化時的 kwargs 和執行時的 kwargs
            # {**self.kwargs, **kwargs} 是字典合併語法
            # 如果兩個字典有相同的鍵，後面的值會覆蓋前面的值
            # 所以執行時傳入的參數會優先於初始化時的參數
            merged_kwargs = {**self.kwargs, **kwargs}
            
            # 執行任務函數
            # *args 解包位置參數，**merged_kwargs 解包關鍵字參數
            # 這相當於 func(arg1, arg2, ..., key1=value1, key2=value2, ...)
            result = self.func(*args, **merged_kwargs)
            
            # 記錄資訊日誌，表示任務執行完成
            logger.info(f"任務執行完成: {self.name} (ID: {self.job_id})")
            
            # 返回任務函數的返回值
            return result
            
        except Exception as e:
            # 如果執行過程中發生任何異常，進入這個區塊
            # Exception 是所有異常的基類，可以捕獲任何異常
            
            # 增加錯誤計數器
            self.error_count += 1
            
            # 記錄錯誤訊息
            # str(e) 將異常物件轉換為字串
            self.last_error = str(e)
            
            # 記錄錯誤日誌
            # logger.error() 用於記錄錯誤級別的日誌
            logger.error(f"任務執行失敗: {self.name} (ID: {self.job_id}), 錯誤: {e}")
            
            # 重新拋出異常，讓呼叫者知道執行失敗了
            # raise 會將異常向上傳遞
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        取得任務統計資訊
        
        這個方法會返回一個字典，包含任務的所有統計資訊。
        可以用於監控和報告任務的執行狀況。
        
        Returns:
            Dict[str, Any]: 包含以下鍵的字典：
                - job_id: 任務 ID
                - name: 任務名稱
                - execution_count: 執行次數
                - last_execution_time: 最後執行時間（ISO 格式字串或 None）
                - error_count: 錯誤次數
                - last_error: 最後錯誤訊息（或 None）
        """
        # 返回統計資訊字典
        return {
            # 任務 ID
            'job_id': self.job_id,
            
            # 任務名稱
            'name': self.name,
            
            # 執行次數
            'execution_count': self.execution_count,
            
            # 最後執行時間
            # 如果 last_execution_time 不是 None，則轉換為 ISO 格式字串
            # ISO 格式：'2024-01-01T12:00:00'
            # 如果為 None，則返回 None
            # 這是一個三元表達式：value if condition else other_value
            'last_execution_time': self.last_execution_time.isoformat() if self.last_execution_time else None,
            
            # 錯誤次數
            'error_count': self.error_count,
            
            # 最後錯誤訊息
            'last_error': self.last_error
        }
    
    def reset_stats(self):
        """
        重置統計資訊
        
        這個方法會將所有統計資訊重置為初始狀態。
        可以用於重新開始統計或清除舊的統計資料。
        """
        # 重置執行計數器為 0
        self.execution_count = 0
        
        # 重置錯誤計數器為 0
        self.error_count = 0
        
        # 清除最後執行時間
        self.last_execution_time = None
        
        # 清除最後錯誤訊息
        self.last_error = None
        
        # 記錄資訊日誌，表示統計資訊已重置
        logger.info(f"任務統計已重置: {self.name} (ID: {self.job_id})")


class JobRegistry:
    """
    任務註冊表類別
    
    這個類別管理多個任務處理器，提供統一的註冊、查詢和統計功能。
    它使用字典來儲存任務處理器，以任務 ID 作為鍵。
    """
    
    def __init__(self):
        """
        初始化任務註冊表
        
        這個方法會建立一個新的任務註冊表實例。
        註冊表使用字典來儲存任務處理器，以任務 ID 作為鍵。
        """
        # 建立一個字典來儲存任務處理器
        # Dict[str, JobHandler] 表示鍵是字串（任務 ID），值是 JobHandler 物件
        # 使用字典可以快速根據 ID 查找任務處理器
        self._handlers: Dict[str, JobHandler] = {}
    
    def register(self, handler: JobHandler):
        """
        註冊任務處理器
        
        這個方法會將一個任務處理器註冊到註冊表中。
        如果任務 ID 已存在，會覆蓋舊的處理器。
        
        Args:
            handler: 要註冊的任務處理器實例
        """
        # 將任務處理器儲存到字典中
        # handler.job_id 是任務 ID，作為字典的鍵
        # handler 是任務處理器物件，作為字典的值
        self._handlers[handler.job_id] = handler
        
        # 記錄資訊日誌，表示任務已註冊
        logger.info(f"任務已註冊: {handler.job_id}")
    
    def unregister(self, job_id: str):
        """
        取消註冊任務處理器
        
        這個方法會從註冊表中移除指定的任務處理器。
        如果任務 ID 不存在，不會發生任何事。
        
        Args:
            job_id: 要取消註冊的任務 ID
        """
        # 檢查任務 ID 是否存在於字典中
        if job_id in self._handlers:
            # 如果存在，則從字典中刪除
            # del 語句用於刪除字典中的鍵值對
            del self._handlers[job_id]
            
            # 記錄資訊日誌，表示任務已取消註冊
            logger.info(f"任務已取消註冊: {job_id}")
    
    def get_handler(self, job_id: str) -> Optional[JobHandler]:
        """
        取得指定的任務處理器
        
        這個方法會根據任務 ID 查找並返回對應的任務處理器。
        
        Args:
            job_id: 任務 ID
        
        Returns:
            JobHandler 物件，如果不存在則返回 None
        """
        # 使用字典的 get 方法查找任務處理器
        # get() 方法如果找不到鍵，會返回 None（而不是拋出 KeyError）
        return self._handlers.get(job_id)
    
    def get_all_handlers(self) -> Dict[str, JobHandler]:
        """
        取得所有任務處理器
        
        這個方法會返回所有已註冊的任務處理器的副本。
        返回副本可以防止外部直接修改內部字典。
        
        Returns:
            Dict[str, JobHandler]: 包含所有任務處理器的字典副本
        """
        # 使用字典的 copy() 方法返回副本
        # 這樣外部修改返回的字典不會影響內部的字典
        return self._handlers.copy()
    
    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        取得所有任務的統計資訊
        
        這個方法會返回所有已註冊任務的統計資訊。
        可以用於生成整體的執行報告。
        
        Returns:
            Dict[str, Dict[str, Any]]: 
                - 外層字典的鍵是任務 ID
                - 內層字典是每個任務的統計資訊（由 JobHandler.get_stats() 返回）
        """
        # 使用字典推導式（dictionary comprehension）建立統計資訊字典
        # 這相當於：
        # stats = {}
        # for job_id, handler in self._handlers.items():
        #     stats[job_id] = handler.get_stats()
        # return stats
        return {
            job_id: handler.get_stats()  # 對每個任務處理器呼叫 get_stats() 方法
            for job_id, handler in self._handlers.items()  # 遍歷所有任務處理器
        }
