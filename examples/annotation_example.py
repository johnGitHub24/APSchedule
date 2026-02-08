"""
Annotation 裝飾器範例
展示如何使用裝飾器定義排程任務
"""
import sys
from pathlib import Path

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apschedule import SchedulerManager
from apschedule.decorators import (
    set_global_scheduler,
    interval_job,
    cron_job,
    scheduled_job
)
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# 建立排程器管理器 (模組層級，用於裝飾器)
scheduler_manager = SchedulerManager(scheduler_type='blocking')

# 初始化排程器 (必須在設定全域排程器之前)
scheduler_manager._scheduler = scheduler_manager._create_scheduler()

# 設定全域排程器 (讓裝飾器可以自動註冊任務)
set_global_scheduler(scheduler_manager)


# 使用 interval_job 裝飾器
@interval_job(seconds=5, id='decorated_job_1', name='裝飾器任務1')
def job_1():
    """每5秒執行一次的任務"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行裝飾器任務1")


# 使用 interval_job 裝飾器 (每10秒)
@interval_job(seconds=10, id='decorated_job_2', name='裝飾器任務2')
def job_2():
    """每10秒執行一次的任務"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行裝飾器任務2")


# 使用 cron_job 裝飾器
@cron_job(second=30, id='decorated_job_3', name='裝飾器任務3')
def job_3():
    """每分鐘的第30秒執行"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行裝飾器任務3")


# 使用通用 scheduled_job 裝飾器
@scheduled_job(
    trigger=IntervalTrigger(seconds=15),
    id='decorated_job_4',
    name='裝飾器任務4'
)
def job_4():
    """每15秒執行一次的任務"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行裝飾器任務4")


def main():
    # 建立排程器管理器
    scheduler_manager = SchedulerManager(scheduler_type='blocking')
    
    # 初始化排程器 (必須在設定全域排程器之前)
    scheduler_manager._scheduler = scheduler_manager._create_scheduler()
    
    # 設定全域排程器 (讓裝飾器可以自動註冊任務)
    set_global_scheduler(scheduler_manager)
    
    print("排程器已啟動，按 Ctrl+C 停止...")
    print("\n任務列表 (透過裝飾器註冊):")
    for job in scheduler_manager.get_jobs():
        print(f"  - {job.id}: {job.name}")
        # 安全地獲取下次執行時間
        next_run = getattr(job, 'next_run_time', None)
        if next_run:
            print(f"    下次執行: {next_run}")
        else:
            print(f"    下次執行: 尚未計算")
    
    try:
        scheduler_manager.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n排程器已停止")
        scheduler_manager.stop()


if __name__ == '__main__':
    main()

