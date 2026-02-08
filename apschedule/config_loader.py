"""
YML 配置檔案載入器

這個模組提供了 ConfigLoader 類別，用於從 YAML 配置檔案載入任務配置。

YAML 說明：
- YAML (YAML Ain't Markup Language) 是一種人類可讀的資料序列化標準
- 常用於配置檔案，因為它比 JSON 更易讀，比 XML 更簡潔
- PyYAML 是 Python 的 YAML 解析庫，可以將 YAML 檔案解析為 Python 字典

配置檔案格式範例：
    scheduler:
      type: blocking
    jobs:
      - id: job1
        name: 任務1
        func: my_function
        trigger:
          type: interval
          params:
            seconds: 5
"""
# 匯入 PyYAML 庫
# yaml 模組提供了 YAML 檔案的讀寫功能
# safe_load() 用於安全地載入 YAML 檔案（只載入基本的 Python 物件）
import yaml

# 從 typing 模組匯入型別提示
# Dict: 字典型別
# Any: 任意型別
# List: 列表型別
# Optional: 可選型別（可以是某個型別或 None）
from typing import Dict, Any, List, Optional

# 從 pathlib 模組匯入 Path 類別
# Path 提供了跨平台的檔案路徑操作功能
# 比使用字串操作路徑更安全和方便
from pathlib import Path

# 匯入 logging 模組用於記錄日誌
import logging

# 建立一個 logger 物件，用於記錄這個模組的日誌
logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    配置檔案載入器類別
    
    這個類別提供了靜態方法來載入和解析 YAML 配置檔案。
    所有方法都是靜態方法（@staticmethod），可以直接透過類別呼叫，不需要建立實例。
    """
    
    @staticmethod
    def load_from_file(file_path: str) -> Dict[str, Any]:
        """
        從 YML 檔案載入配置
        
        這個方法會讀取 YAML 配置檔案，並將其解析為 Python 字典。
        
        Args:
            file_path: YML 檔案的路徑
                - 可以是相對路徑或絕對路徑
                - 例如：'config/jobs.yml' 或 '/path/to/jobs.yml'
        
        Returns:
            Dict[str, Any]: 解析後的配置字典
                - 通常包含 'scheduler' 和 'jobs' 兩個鍵
                - 'scheduler' 包含排程器的配置
                - 'jobs' 包含任務列表
        
        Raises:
            FileNotFoundError: 如果配置檔案不存在
        
        使用範例：
            config = ConfigLoader.load_from_file('config/jobs.yml')
            print(config['jobs'])  # 輸出任務列表
        """
        # 將字串路徑轉換為 Path 物件
        # Path 物件提供了更好的路徑操作方法
        path = Path(file_path)
        
        # 檢查檔案是否存在
        # path.exists() 返回 True 如果檔案存在，否則返回 False
        if not path.exists():
            # 如果檔案不存在，拋出 FileNotFoundError 異常
            # 這是一個內建的異常類別，用於表示檔案找不到
            raise FileNotFoundError(f"配置檔案不存在: {file_path}")
        
        # 使用 with 語句開啟檔案
        # with 語句會自動處理檔案的開啟和關閉，即使發生異常也會正確關閉
        # 'r' 表示以讀取模式開啟
        # encoding='utf-8' 指定使用 UTF-8 編碼（支援中文）
        with open(path, 'r', encoding='utf-8') as f:
            # 使用 yaml.safe_load() 解析 YAML 檔案
            # safe_load() 只會載入基本的 Python 物件（字典、列表、字串、數字等）
            # 這比 load() 更安全，因為它不會執行任意的 Python 程式碼
            # f.read() 讀取檔案的整個內容
            config = yaml.safe_load(f)
        
        # 記錄資訊日誌，表示配置檔案已成功載入
        logger.info(f"配置檔案已載入: {file_path}")
        
        # 返回解析後的配置字典
        return config
    
    @staticmethod
    def parse_jobs(config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        解析配置中的任務定義
        
        這個方法會從配置字典中提取任務列表，並解析每個任務的配置。
        它會將 YAML 中的任務配置轉換為標準化的字典格式。
        
        Args:
            config: 配置字典（通常由 load_from_file() 返回）
                - 應該包含 'jobs' 鍵，值是一個任務列表
        
        Returns:
            List[Dict[str, Any]]: 解析後的任務列表
                每個任務字典包含以下鍵：
                - id: 任務 ID
                - name: 任務名稱
                - func: 任務函數名稱（字串）
                - trigger_type: 觸發器類型（'interval' 或 'cron'）
                - trigger_params: 觸發器參數（字典）
                - args: 傳遞給函數的位置參數（列表）
                - kwargs: 傳遞給函數的關鍵字參數（字典）
                - enabled: 是否啟用（布林值）
        
        使用範例：
            config = ConfigLoader.load_from_file('config/jobs.yml')
            jobs = ConfigLoader.parse_jobs(config)
            for job in jobs:
                print(job['id'], job['name'])
        """
        # 從配置字典中取得任務列表
        # config.get('jobs', []) 表示如果 'jobs' 鍵存在則返回其值，否則返回空列表 []
        # 這樣可以避免 KeyError 異常
        jobs = config.get('jobs', [])
        
        # 建立一個空列表來儲存解析後的任務
        parsed_jobs = []
        
        # 遍歷配置中的每個任務
        # for 迴圈會依次處理列表中的每個元素
        for job in jobs:
            # 建立解析後的任務字典
            # 這個字典包含標準化的任務配置
            parsed_job = {
                # 任務 ID
                # job.get('id') 如果 'id' 鍵存在則返回其值，否則返回 None
                'id': job.get('id'),
                
                # 任務名稱
                # 如果 'name' 鍵存在則使用其值，否則使用 'id' 作為名稱
                # job.get('name', job.get('id')) 表示如果 'name' 不存在，則使用 'id'
                'name': job.get('name', job.get('id')),
                
                # 任務函數名稱（字串）
                # 這個字串需要對應到實際的 Python 函數
                'func': job.get('func'),
                
                # 觸發器類型
                # job.get('trigger', {}) 取得 'trigger' 鍵的值，如果不存在則返回空字典 {}
                # .get('type') 從觸發器字典中取得 'type' 鍵的值
                # 應該是 'interval' 或 'cron'
                'trigger_type': job.get('trigger', {}).get('type'),
                
                # 觸發器參數
                # 從觸發器字典中取得 'params' 鍵的值，如果不存在則返回空字典 {}
                # 這些參數會用於建立觸發器物件
                'trigger_params': job.get('trigger', {}).get('params', {}),
                
                # 傳遞給函數的位置參數
                # 如果 'args' 鍵不存在，則返回空列表 []
                'args': job.get('args', []),
                
                # 傳遞給函數的關鍵字參數
                # 如果 'kwargs' 鍵不存在，則返回空字典 {}
                'kwargs': job.get('kwargs', {}),
                
                # 是否啟用任務
                # 如果 'enabled' 鍵不存在，則預設為 True（啟用）
                'enabled': job.get('enabled', True)
            }
            
            # 將解析後的任務字典添加到列表中
            parsed_jobs.append(parsed_job)
        
        # 返回解析後的任務列表
        return parsed_jobs
    
    @staticmethod
    def create_trigger(trigger_type: str, trigger_params: Dict[str, Any]):
        """
        根據配置建立觸發器
        
        這個方法會根據觸發器類型和參數建立對應的 APScheduler 觸發器物件。
        
        Args:
            trigger_type: 觸發器類型
                - 'interval': 間隔觸發（例如：每 5 秒執行一次）
                - 'cron': Cron 表達式觸發（例如：每天 9 點執行）
            trigger_params: 觸發器參數（字典）
                - 對於 'interval' 類型：包含 'seconds', 'minutes', 'hours' 等
                - 對於 'cron' 類型：包含 'hour', 'minute', 'day_of_week' 等
        
        Returns:
            IntervalTrigger 或 CronTrigger 物件
        
        Raises:
            ValueError: 如果觸發器類型不支援
        
        使用範例：
            # 建立間隔觸發器
            trigger = ConfigLoader.create_trigger(
                'interval',
                {'seconds': 5}
            )
            
            # 建立 Cron 觸發器
            trigger = ConfigLoader.create_trigger(
                'cron',
                {'hour': 9, 'minute': 0}
            )
        """
        # 在方法內部匯入觸發器類別
        # 這樣可以避免在模組層級匯入，減少不必要的依賴
        from apscheduler.triggers.interval import IntervalTrigger
        from apscheduler.triggers.cron import CronTrigger
        
        # 根據觸發器類型建立對應的觸發器物件
        if trigger_type == 'interval':
            # 建立間隔觸發器
            # IntervalTrigger(**trigger_params) 使用字典解包語法
            # 例如：trigger_params={'seconds': 5} 會變成 IntervalTrigger(seconds=5)
            return IntervalTrigger(**trigger_params)
        elif trigger_type == 'cron':
            # 建立 Cron 觸發器
            # CronTrigger(**trigger_params) 使用字典解包語法
            # 例如：trigger_params={'hour': 9} 會變成 CronTrigger(hour=9)
            return CronTrigger(**trigger_params)
        else:
            # 如果觸發器類型不支援，拋出 ValueError 異常
            # ValueError 是內建的異常類別，用於表示參數值不正確
            raise ValueError(f"不支援的觸發器類型: {trigger_type}")
