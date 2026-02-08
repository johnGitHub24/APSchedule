"""
測試 ConfigLoader

這個模組包含 ConfigLoader 類別的所有單元測試。

測試內容：
1. 從檔案載入配置
2. 載入不存在的檔案（錯誤處理）
3. 解析任務配置
4. 建立間隔觸發器
5. 建立 Cron 觸發器
6. 建立無效的觸發器（錯誤處理）

測試技巧：
- 使用 tempfile 模組建立臨時檔案，避免污染檔案系統
- 使用 pytest.raises() 測試異常情況
- 使用 isinstance() 檢查物件類型
"""
# 匯入 pytest 測試框架
import pytest

# 匯入 PyYAML 庫
# yaml 模組用於讀寫 YAML 檔案
# yaml.dump() 用於將 Python 物件轉換為 YAML 格式
import yaml

# 從 pathlib 模組匯入 Path 類別
# Path 用於處理檔案路徑
from pathlib import Path

# 匯入 tempfile 模組
# tempfile 用於建立臨時檔案和目錄
# NamedTemporaryFile 用於建立臨時檔案，測試結束後自動刪除
import tempfile

# 從 apschedule.config_loader 匯入 ConfigLoader
# 這是我們要測試的類別
from apschedule.config_loader import ConfigLoader

# 從 APScheduler 匯入觸發器
# 用於驗證 ConfigLoader.create_trigger() 建立的觸發器類型
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger


def test_load_from_file():
    """
    測試從檔案載入配置
    
    這個測試驗證 ConfigLoader.load_from_file() 是否正確載入 YAML 檔案。
    它使用臨時檔案來避免污染檔案系統。
    
    測試步驟：
    1. 建立一個臨時 YAML 檔案
    2. 將測試資料寫入檔案
    3. 使用 ConfigLoader.load_from_file() 載入檔案
    4. 驗證載入的配置是否正確
    
    臨時檔案說明：
    - NamedTemporaryFile 會建立一個臨時檔案
    - delete=False 表示檔案不會自動刪除（我們需要手動刪除）
    - suffix='.yml' 指定檔案副檔名
    """
    # 建立臨時配置檔案的資料
    # 這是一個字典，模擬真實的 YAML 配置檔案內容
    config_data = {
        # scheduler 區塊：排程器的配置
        'scheduler': {
            'type': 'blocking'  # 排程器類型
        },
        # jobs 區塊：任務列表
        'jobs': [
            {
                'id': 'test_job',           # 任務 ID
                'name': '測試任務',          # 任務名稱
                'func': 'test_func',        # 任務函數名稱（字串）
                'trigger': {                # 觸發器配置
                    'type': 'interval',     # 觸發器類型：間隔觸發
                    'params': {             # 觸發器參數
                        'seconds': 5        # 每 5 秒執行一次
                    }
                }
            }
        ]
    }
    
    # 使用 with 語句建立臨時檔案
    # NamedTemporaryFile 會建立一個臨時檔案
    # mode='w' 表示以寫入模式開啟
    # suffix='.yml' 指定檔案副檔名為 .yml
    # delete=False 表示檔案不會自動刪除（我們需要手動刪除）
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        # 使用 yaml.dump() 將 Python 字典轉換為 YAML 格式並寫入檔案
        # yaml.dump() 會將字典序列化為 YAML 字串
        yaml.dump(config_data, f)
        
        # 取得臨時檔案的路徑
        # f.name 是臨時檔案的完整路徑
        temp_path = f.name
    
    # 使用 try-finally 確保臨時檔案被刪除
    # 即使測試失敗，也要清理臨時檔案
    try:
        # 使用 ConfigLoader.load_from_file() 載入配置檔案
        # 這個方法會讀取 YAML 檔案並解析為 Python 字典
        config = ConfigLoader.load_from_file(temp_path)
        
        # 斷言：檢查配置字典是否包含 'scheduler' 鍵
        # 'scheduler' in config 檢查鍵是否存在於字典中
        assert 'scheduler' in config
        
        # 斷言：檢查配置字典是否包含 'jobs' 鍵
        assert 'jobs' in config
        
        # 斷言：檢查任務列表的長度是否為 1
        # len(config['jobs']) 取得任務列表的長度
        assert len(config['jobs']) == 1
    finally:
        # 清理臨時檔案
        # Path(temp_path).unlink() 刪除臨時檔案
        # unlink() 是刪除檔案的方法
        Path(temp_path).unlink()


def test_load_from_file_not_found():
    """
    測試載入不存在的檔案
    
    這個測試驗證當檔案不存在時，ConfigLoader.load_from_file() 是否正確拋出異常。
    
    異常測試說明：
    - 使用 pytest.raises() 來測試是否拋出預期的異常
    - pytest.raises() 是一個上下文管理器，會捕獲異常
    - 如果沒有拋出異常，測試會失敗
    - 如果拋出錯誤的異常類型，測試也會失敗
    """
    # 使用 pytest.raises() 測試異常
    # pytest.raises(FileNotFoundError) 表示我們期望拋出 FileNotFoundError 異常
    # 如果沒有拋出異常，或拋出其他異常，測試會失敗
    with pytest.raises(FileNotFoundError):
        # 嘗試載入一個不存在的檔案
        # 這應該會拋出 FileNotFoundError 異常
        ConfigLoader.load_from_file('nonexistent.yml')


def test_parse_jobs():
    """
    測試解析任務配置
    
    這個測試驗證 ConfigLoader.parse_jobs() 是否正確解析任務配置。
    它測試了多種情況：
    1. 有名稱的任務
    2. 沒有名稱的任務（應該使用 ID 作為名稱）
    3. 啟用的任務
    4. 停用的任務
    """
    # 建立測試用的配置字典
    config = {
        'jobs': [
            {
                'id': 'job1',                    # 任務 ID
                'name': '任務1',                  # 任務名稱（有提供）
                'func': 'func1',                 # 任務函數名稱
                'trigger': {
                    'type': 'interval',          # 觸發器類型：間隔觸發
                    'params': {'seconds': 5}     # 觸發器參數
                },
                'enabled': True                  # 任務已啟用
            },
            {
                'id': 'job2',                    # 任務 ID
                # 注意：這個任務沒有提供 'name'，應該使用 'id' 作為名稱
                'func': 'func2',                 # 任務函數名稱
                'trigger': {
                    'type': 'cron',              # 觸發器類型：Cron 觸發
                    'params': {'hour': 9}         # 觸發器參數：每天 9 點
                },
                'enabled': False                 # 任務已停用
            }
        ]
    }
    
    # 呼叫 parse_jobs() 解析任務配置
    # 這個方法會將 YAML 格式的任務配置轉換為標準化的字典格式
    jobs = ConfigLoader.parse_jobs(config)
    
    # 斷言：檢查解析後的任務數量是否為 2
    assert len(jobs) == 2
    
    # 檢查第一個任務的配置
    # jobs[0] 是第一個任務的字典
    assert jobs[0]['id'] == 'job1'                    # 任務 ID
    assert jobs[0]['name'] == '任務1'                  # 任務名稱
    assert jobs[0]['trigger_type'] == 'interval'      # 觸發器類型
    assert jobs[0]['enabled'] is True                 # 是否啟用
    
    # 檢查第二個任務的配置
    assert jobs[1]['id'] == 'job2'
    # 注意：第二個任務沒有提供 'name'，所以應該使用 'id' 作為名稱
    assert jobs[1]['name'] == 'job2'                   # 預設使用 id 作為 name
    assert jobs[1]['trigger_type'] == 'cron'          # 觸發器類型
    assert jobs[1]['enabled'] is False                # 是否啟用


def test_create_trigger_interval():
    """
    測試建立間隔觸發器
    
    這個測試驗證 ConfigLoader.create_trigger() 是否正確建立 IntervalTrigger。
    它檢查返回的物件是否是 IntervalTrigger 的實例。
    
    isinstance() 說明：
    - isinstance(obj, class) 檢查物件是否是某個類別的實例
    - 也可以用於檢查是否是子類別的實例
    - 比使用 type() 更靈活
    """
    # 呼叫 create_trigger() 建立間隔觸發器
    # 'interval' 是觸發器類型
    # {'seconds': 5, 'minutes': 1} 是觸發器參數
    # 這會建立一個每 1 分 5 秒執行一次的觸發器
    trigger = ConfigLoader.create_trigger(
        'interval',                        # 觸發器類型
        {'seconds': 5, 'minutes': 1}       # 觸發器參數
    )
    
    # 斷言：檢查返回的物件是否是 IntervalTrigger 的實例
    # isinstance() 用於檢查物件的類型
    # 這確保 create_trigger() 正確建立了 IntervalTrigger 物件
    assert isinstance(trigger, IntervalTrigger)


def test_create_trigger_cron():
    """
    測試建立 Cron 觸發器
    
    這個測試驗證 ConfigLoader.create_trigger() 是否正確建立 CronTrigger。
    它檢查返回的物件是否是 CronTrigger 的實例。
    """
    # 呼叫 create_trigger() 建立 Cron 觸發器
    # 'cron' 是觸發器類型
    # {'hour': 9, 'minute': 0} 是觸發器參數
    # 這會建立一個每天 9 點執行的觸發器
    trigger = ConfigLoader.create_trigger(
        'cron',                            # 觸發器類型
        {'hour': 9, 'minute': 0}          # 觸發器參數
    )
    
    # 斷言：檢查返回的物件是否是 CronTrigger 的實例
    assert isinstance(trigger, CronTrigger)


def test_create_trigger_invalid():
    """
    測試建立無效的觸發器
    
    這個測試驗證當觸發器類型無效時，ConfigLoader.create_trigger() 是否正確拋出異常。
    
    錯誤處理測試：
    - 測試程式碼應該覆蓋正常情況和異常情況
    - 使用 pytest.raises() 測試異常情況
    - 確保錯誤訊息有意義，方便除錯
    """
    # 使用 pytest.raises() 測試異常
    # pytest.raises(ValueError) 表示我們期望拋出 ValueError 異常
    with pytest.raises(ValueError):
        # 嘗試建立一個無效的觸發器類型
        # 'invalid' 不是支援的觸發器類型，應該拋出 ValueError
        ConfigLoader.create_trigger('invalid', {})
