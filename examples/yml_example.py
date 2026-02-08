"""
YML 配置範例
展示如何使用 YML 配置檔案定義排程任務
"""
import sys
import os
from pathlib import Path

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apschedule import SchedulerManager
from apschedule.config_loader import ConfigLoader
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# 定義任務函數 (這些函數應該在配置中引用)
def daily_report():
    """每日報告任務"""
    from datetime import datetime
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 生成每日報告")


def hourly_check():
    """每小時檢查任務"""
    from datetime import datetime
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行每小時檢查")


def weekly_backup():
    """每週備份任務"""
    from datetime import datetime
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 執行每週備份")


def task_with_params(name: str, count: int):
    """帶參數的任務"""
    from datetime import datetime
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 任務: {name}, 計數: {count}")


# 任務函數映射表 (用於從字串名稱找到實際函數)
JOB_FUNCTIONS = {
    'daily_report': daily_report,
    'hourly_check': hourly_check,
    'weekly_backup': weekly_backup,
    'task_with_params': task_with_params
}


def main():
    # 載入配置檔案
    config_path = Path(__file__).parent.parent / 'config' / 'jobs.yml'
    config = ConfigLoader.load_from_file(str(config_path))
    
    # 解析任務配置
    jobs = ConfigLoader.parse_jobs(config)
    
    # 建立排程器管理器
    scheduler_manager = SchedulerManager(scheduler_type='blocking')
    
    # 根據配置新增任務
    for job_config in jobs:
        if not job_config.get('enabled', True):
            print(f"跳過已停用的任務: {job_config['name']}")
            continue
        
        # 取得任務函數
        func_name = job_config['func']
        if func_name not in JOB_FUNCTIONS:
            print(f"警告: 找不到任務函數: {func_name}")
            continue
        
        func = JOB_FUNCTIONS[func_name]
        
        # 建立觸發器
        trigger = ConfigLoader.create_trigger(
            job_config['trigger_type'],
            job_config['trigger_params']
        )
        
        # 新增任務
        scheduler_manager.add_job(
            func=func,
            trigger=trigger,
            id=job_config['id'],
            name=job_config['name'],
            args=job_config.get('args', []),
            kwargs=job_config.get('kwargs', {})
        )
    
    print("排程器已啟動，按 Ctrl+C 停止...")
    print("\n任務列表:")
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

