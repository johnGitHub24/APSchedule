"""
排程器管理器 - OOP 設計

這個模組提供了 SchedulerManager 類別，用於管理 APScheduler 排程器。
它封裝了排程器的建立、啟動、停止和任務管理功能。

APScheduler 說明：
- BlockingScheduler: 阻塞式排程器，會阻塞主執行緒直到排程器停止
- BackgroundScheduler: 背景排程器，在背景執行，不會阻塞主執行緒
- MemoryJobStore: 將任務儲存在記憶體中（重啟後會遺失）
- ThreadPoolExecutor: 使用執行緒池來執行任務
"""
# 從 APScheduler 匯入阻塞式排程器
# BlockingScheduler 會阻塞主執行緒，適合單執行緒應用
from apscheduler.schedulers.blocking import BlockingScheduler

# 從 APScheduler 匯入背景排程器
# BackgroundScheduler 在背景執行，不會阻塞主執行緒，適合多執行緒應用
from apscheduler.schedulers.background import BackgroundScheduler

# 從 APScheduler 匯入記憶體任務儲存區
# MemoryJobStore 將任務資訊儲存在記憶體中，應用程式重啟後會遺失
from apscheduler.jobstores.memory import MemoryJobStore

# 從 APScheduler 匯入執行緒池執行器
# ThreadPoolExecutor 使用執行緒池來並行執行多個任務
from apscheduler.executors.pool import ThreadPoolExecutor

# 從 typing 模組匯入型別提示
# Optional: 表示值可以是某個型別或 None
# Dict: 字典型別
# Any: 任意型別
# List: 列表型別
from typing import Optional, Dict, Any, List

# 從 datetime 模組匯入 datetime 類別（雖然這裡沒用到，但保留以備未來使用）
from datetime import datetime

# 匯入 logging 模組用於記錄日誌
# logging 是 Python 標準庫，用於記錄程式執行過程中的資訊、警告和錯誤
import logging

# 建立一個 logger 物件，用於記錄這個模組的日誌
# __name__ 是當前模組的名稱，這樣可以追蹤日誌來自哪個模組
logger = logging.getLogger(__name__)


class SchedulerManager:
    """
    排程器管理器類別
    
    這個類別封裝了 APScheduler 的功能，提供更簡潔的 API 來管理排程任務。
    它負責：
    1. 建立和管理排程器實例
    2. 新增、移除、暫停、恢復任務
    3. 啟動和停止排程器
    """
    
    def __init__(self, 
                 scheduler_type: str = 'blocking',
                 jobstore: Optional[Any] = None,
                 executor: Optional[Any] = None,
                 timezone: Optional[Any] = None):
        """
        初始化排程器管理器
        
        這個方法會建立排程器管理器的實例，並設定相關的配置。
        
        Args:
            scheduler_type: 排程器類型
                - 'blocking': 使用 BlockingScheduler（阻塞式，會阻塞主執行緒）
                - 'background': 使用 BackgroundScheduler（背景執行，不阻塞主執行緒）
            jobstore: 任務儲存區實例
                - 如果為 None，則使用預設的 MemoryJobStore（記憶體儲存）
                - 其他選項：SQLAlchemyJobStore（資料庫儲存）、RedisJobStore（Redis 儲存）等
            executor: 任務執行器實例
                - 如果為 None，則使用預設的 ThreadPoolExecutor（執行緒池）
                - max_workers=10 表示最多同時執行 10 個任務
            timezone: 時區設定
                - 如果為 None，則使用系統預設時區
                - 例如：'Asia/Taipei'、'UTC' 等
        """
        # 儲存排程器類型（'blocking' 或 'background'）
        self.scheduler_type = scheduler_type
        
        # 排程器實例，初始為 None，會在需要時才建立（延遲初始化）
        # Optional[BlockingScheduler] 表示這個變數可以是 BlockingScheduler 或 None
        self._scheduler: Optional[BlockingScheduler] = None
        
        # 任務儲存區：如果沒有提供，則使用預設的 MemoryJobStore
        # MemoryJobStore() 建立一個新的記憶體儲存區實例
        # 這個儲存區會在應用程式重啟後清空所有任務
        self._jobstore = jobstore or MemoryJobStore()
        
        # 任務執行器：如果沒有提供，則使用預設的 ThreadPoolExecutor
        # ThreadPoolExecutor(max_workers=10) 建立一個最多 10 個執行緒的執行緒池
        # 這個執行器會並行執行多個任務
        self._executor = executor or ThreadPoolExecutor(max_workers=10)
        
        # 時區設定：如果沒有提供，則為 None（使用系統預設時區）
        self._timezone = timezone
        
        # 標記排程器是否正在運行
        # False 表示排程器尚未啟動
        self._is_running = False
        
    def _create_scheduler(self) -> BlockingScheduler:
        """
        建立排程器實例
        
        這個私有方法（以 _ 開頭）用於建立 APScheduler 排程器實例。
        它會根據設定的類型建立 BlockingScheduler 或 BackgroundScheduler。
        
        Returns:
            BlockingScheduler 或 BackgroundScheduler 實例
        """
        # 建立排程器配置字典
        # 這個字典包含排程器需要的所有配置
        config = {
            # jobstores: 定義任務儲存區
            # 'default' 是預設儲存區的名稱，所有任務預設會儲存在這裡
            'jobstores': {
                'default': self._jobstore  # 使用設定的任務儲存區
            },
            # executors: 定義任務執行器
            # 'default' 是預設執行器的名稱，所有任務預設會使用這個執行器
            'executors': {
                'default': self._executor  # 使用設定的任務執行器
            },
            # job_defaults: 定義任務的預設設定
            'job_defaults': {
                # coalesce: 是否合併錯過的執行
                # False 表示如果任務錯過了執行時間，不會合併執行
                # 例如：如果任務應該每 5 秒執行一次，但系統忙碌了 20 秒
                # coalesce=False 時，會執行 4 次；coalesce=True 時，只執行 1 次
                'coalesce': False,
                # max_instances: 同一個任務最多可以同時執行的實例數
                # 3 表示如果任務執行時間很長，最多可以同時執行 3 個實例
                # 這可以防止任務堆積
                'max_instances': 3
            }
        }
        
        # 如果有設定時區，則加入時區配置
        if self._timezone:
            # 設定排程器使用的時區
            # 這會影響所有任務的執行時間計算
            config['timezone'] = self._timezone
        
        # 根據排程器類型建立對應的排程器實例
        if self.scheduler_type == 'blocking':
            # 建立阻塞式排程器
            # BlockingScheduler 會阻塞主執行緒，直到排程器停止
            # **config 是 Python 的字典解包語法，將字典的鍵值對作為關鍵字參數傳入
            return BlockingScheduler(**config)
        else:
            # 建立背景排程器
            # BackgroundScheduler 在背景執行，不會阻塞主執行緒
            # 適合在 Web 應用程式或其他需要主執行緒繼續運行的場景使用
            return BackgroundScheduler(**config)
    
    def start(self):
        """
        啟動排程器
        
        這個方法會啟動排程器，開始執行已註冊的任務。
        如果排程器已經在運行，則不會重複啟動。
        """
        # 檢查排程器是否已經在運行
        if self._is_running:
            # 如果已經在運行，記錄警告訊息並返回
            # logger.warning() 用於記錄警告級別的日誌
            logger.warning("排程器已在運行中")
            return
        
        # 如果排程器尚未建立，則建立一個新的排程器實例
        if self._scheduler is None:
            # 呼叫私有方法建立排程器
            self._scheduler = self._create_scheduler()
        
        # 啟動排程器
        # scheduler.start() 是 APScheduler 的方法，會開始執行已註冊的任務
        # 對於 BlockingScheduler，這會阻塞主執行緒
        # 對於 BackgroundScheduler，這會在背景執行
        self._scheduler.start()
        
        # 標記排程器為運行狀態
        self._is_running = True
        
        # 記錄資訊日誌，表示排程器已成功啟動
        logger.info("排程器已啟動")
    
    def stop(self, wait: bool = True):
        """
        停止排程器
        
        這個方法會停止排程器，並可選擇是否等待正在執行的任務完成。
        
        Args:
            wait: 是否等待正在執行的任務完成
                - True: 等待所有任務完成後才停止（預設）
                - False: 立即停止，不等待任務完成
        """
        # 檢查排程器是否在運行或是否存在
        if not self._is_running or self._scheduler is None:
            # 如果排程器未在運行，記錄警告訊息並返回
            logger.warning("排程器未在運行")
            return
        
        # 關閉排程器
        # scheduler.shutdown() 是 APScheduler 的方法，會停止排程器
        # wait 參數決定是否等待正在執行的任務完成
        self._scheduler.shutdown(wait=wait)
        
        # 標記排程器為停止狀態
        self._is_running = False
        
        # 記錄資訊日誌，表示排程器已成功停止
        logger.info("排程器已停止")
    
    def add_job(self, 
                func, 
                trigger=None,
                id: Optional[str] = None,
                name: Optional[str] = None,
                **kwargs) -> str:
        """
        新增任務到排程器
        
        這個方法會將一個函數註冊為排程任務，並設定觸發條件。
        
        Args:
            func: 要執行的函數
                - 可以是任何可呼叫的 Python 物件（函數、方法等）
            trigger: 觸發器物件
                - IntervalTrigger: 間隔觸發（例如：每 5 秒執行一次）
                - CronTrigger: Cron 表達式觸發（例如：每天 9 點執行）
                - DateTrigger: 指定日期時間觸發（只執行一次）
            id: 任務的唯一識別碼
                - 如果為 None，APScheduler 會自動產生一個 ID
                - 建議手動指定，方便後續管理
            name: 任務的名稱（可選，用於顯示）
            **kwargs: 其他參數
                - args: 傳遞給函數的位置參數（元組）
                - kwargs: 傳遞給函數的關鍵字參數（字典）
                - replace_existing: 如果任務已存在，是否替換（預設 False）
                - max_instances: 最多同時執行的實例數
                - coalesce: 是否合併錯過的執行
        
        Returns:
            str: 任務的 ID（如果沒有提供 id，則返回自動產生的 ID）
        """
        # 如果排程器尚未建立，則建立一個新的排程器實例
        if self._scheduler is None:
            # 延遲初始化：只有在需要時才建立排程器
            self._scheduler = self._create_scheduler()
        
        # 呼叫 APScheduler 的 add_job 方法新增任務
        # scheduler.add_job() 會將任務註冊到排程器中
        # 它會返回一個 Job 物件，但我們只需要 ID
        job_id = self._scheduler.add_job(
            func=func,          # 要執行的函數
            trigger=trigger,    # 觸發器（決定何時執行）
            id=id,              # 任務 ID
            name=name,          # 任務名稱
            **kwargs            # 其他參數（args, kwargs 等）
        )
        
        # 記錄資訊日誌，表示任務已成功新增
        # name or '未命名' 是 Python 的簡寫，如果 name 為 None 或空字串，則使用 '未命名'
        logger.info(f"任務已新增: {job_id} ({name or '未命名'})")
        
        # 返回任務 ID
        return job_id
    
    def remove_job(self, job_id: str):
        """
        從排程器中移除任務
        
        這個方法會移除指定的任務，任務將不再執行。
        
        Args:
            job_id: 要移除的任務 ID
        """
        # 檢查排程器是否已初始化
        if self._scheduler is None:
            # 如果排程器尚未初始化，記錄警告並返回
            logger.warning("排程器尚未初始化")
            return
        
        # 使用 try-except 來處理可能的錯誤
        try:
            # 呼叫 APScheduler 的 remove_job 方法移除任務
            # 如果任務不存在，會拋出 JobLookupError 異常
            self._scheduler.remove_job(job_id)
            
            # 記錄資訊日誌，表示任務已成功移除
            logger.info(f"任務已移除: {job_id}")
        except Exception as e:
            # 如果發生任何錯誤（例如任務不存在），記錄錯誤日誌
            # Exception 是所有異常的基類，可以捕獲任何異常
            logger.error(f"移除任務失敗: {job_id}, 錯誤: {e}")
    
    def get_job(self, job_id: str):
        """
        取得指定的任務物件
        
        這個方法會返回指定 ID 的任務物件，可以用來查詢任務的狀態。
        
        Args:
            job_id: 任務 ID
        
        Returns:
            Job 物件或 None（如果任務不存在）
        """
        # 檢查排程器是否已初始化
        if self._scheduler is None:
            # 如果排程器尚未初始化，返回 None
            return None
        
        # 呼叫 APScheduler 的 get_job 方法取得任務
        # 如果任務不存在，會返回 None
        return self._scheduler.get_job(job_id)
    
    def get_jobs(self) -> List:
        """
        取得所有已註冊的任務
        
        這個方法會返回所有已註冊的任務列表。
        
        Returns:
            List: 包含所有 Job 物件的列表
        """
        # 檢查排程器是否已初始化
        if self._scheduler is None:
            # 如果排程器尚未初始化，返回空列表
            return []
        
        # 呼叫 APScheduler 的 get_jobs 方法取得所有任務
        # 返回一個包含所有 Job 物件的列表
        return self._scheduler.get_jobs()
    
    def pause_job(self, job_id: str):
        """
        暫停指定的任務
        
        這個方法會暫停任務的執行，任務不會被移除，只是暫時停止執行。
        可以使用 resume_job() 方法恢復執行。
        
        Args:
            job_id: 要暫停的任務 ID
        """
        # 檢查排程器是否已初始化
        if self._scheduler is None:
            # 如果排程器尚未初始化，記錄警告並返回
            logger.warning("排程器尚未初始化")
            return
        
        # 使用 try-except 來處理可能的錯誤
        try:
            # 呼叫 APScheduler 的 pause_job 方法暫停任務
            # 暫停後，任務的 next_run_time 會變為 None
            self._scheduler.pause_job(job_id)
            
            # 記錄資訊日誌，表示任務已成功暫停
            logger.info(f"任務已暫停: {job_id}")
        except Exception as e:
            # 如果發生任何錯誤（例如任務不存在），記錄錯誤日誌
            logger.error(f"暫停任務失敗: {job_id}, 錯誤: {e}")
    
    def resume_job(self, job_id: str):
        """
        恢復指定的任務
        
        這個方法會恢復之前暫停的任務，讓任務繼續執行。
        
        Args:
            job_id: 要恢復的任務 ID
        """
        # 檢查排程器是否已初始化
        if self._scheduler is None:
            # 如果排程器尚未初始化，記錄警告並返回
            logger.warning("排程器尚未初始化")
            return
        
        # 使用 try-except 來處理可能的錯誤
        try:
            # 呼叫 APScheduler 的 resume_job 方法恢復任務
            # 恢復後，任務會重新計算 next_run_time 並繼續執行
            self._scheduler.resume_job(job_id)
            
            # 記錄資訊日誌，表示任務已成功恢復
            logger.info(f"任務已恢復: {job_id}")
        except Exception as e:
            # 如果發生任何錯誤（例如任務不存在），記錄錯誤日誌
            logger.error(f"恢復任務失敗: {job_id}, 錯誤: {e}")
    
    @property
    def is_running(self) -> bool:
        """
        檢查排程器是否正在運行
        
        這是一個屬性（property），可以像屬性一樣訪問，但實際上是方法。
        使用 @property 裝飾器可以讓方法像屬性一樣使用，不需要加括號。
        
        Returns:
            bool: True 表示排程器正在運行，False 表示已停止
        """
        # 返回排程器的運行狀態
        return self._is_running
    
    @property
    def scheduler(self) -> Optional[BlockingScheduler]:
        """
        取得排程器實例
        
        這個屬性允許外部訪問內部的排程器實例。
        通常用於需要直接操作 APScheduler 的情況。
        
        Returns:
            BlockingScheduler 或 BackgroundScheduler 實例，如果尚未建立則返回 None
        """
        # 返回排程器實例
        return self._scheduler
