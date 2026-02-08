"""
APSchedule - 簡易排程系統

這個模組提供了排程任務管理的核心功能。

主要類別：
- SchedulerManager: 排程器管理器，用於管理 APScheduler 排程器
- JobHandler: 任務處理器，用於封裝任務的執行邏輯和統計資訊
- JobRegistry: 任務註冊表，用於管理多個任務處理器

主要函數：
- scheduled_job: 通用排程任務裝飾器
- interval_job: 間隔時間任務裝飾器
- cron_job: Cron 任務裝飾器
"""
# 從 scheduler_manager 模組匯入 SchedulerManager 類別
# SchedulerManager 是排程器管理器，用於管理 APScheduler 排程器
from .scheduler_manager import SchedulerManager

# 從 job_handler 模組匯入 JobHandler 和 JobRegistry 類別
# JobHandler: 任務處理器，用於封裝任務的執行邏輯和統計資訊
# JobRegistry: 任務註冊表，用於管理多個任務處理器
from .job_handler import JobHandler, JobRegistry

# 從 decorators 模組匯入裝飾器函數
# 這些裝飾器用於以裝飾器語法定義排程任務
from .decorators import scheduled_job, cron_job, interval_job

# 模組版本號
__version__ = '1.0.0'

# 定義模組的公開 API
# __all__ 列表定義了當使用 from module import * 時會導入哪些名稱
# 這是一個良好的實踐，明確指定模組的公開介面
__all__ = [
    'SchedulerManager',    # 排程器管理器類別
    'JobHandler',          # 任務處理器類別
    'JobRegistry',         # 任務註冊表類別
    'scheduled_job',       # 通用排程任務裝飾器
    'cron_job',            # Cron 任務裝飾器
    'interval_job'         # 間隔時間任務裝飾器
]

