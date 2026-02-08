# APSchedule 快速開始指南

## 安裝

```bash
pip install -r requirements.txt
```

## 使用方式

### 1. 基本範例

最簡單的使用方式：

```python
from apschedule import SchedulerManager
from apscheduler.triggers.interval import IntervalTrigger

def my_task():
    print("執行任務")

manager = SchedulerManager()
manager.add_job(
    func=my_task,
    trigger=IntervalTrigger(seconds=5),
    id='my_job',
    name='我的任務'
)
manager.start()
```

執行範例：
```bash
python examples/basic_example.py
```

### 2. OOP 設計範例

使用物件導向的方式管理任務：

```python
from apschedule import SchedulerManager, JobHandler, JobRegistry

def task():
    print("執行任務")

# 建立管理器
manager = SchedulerManager()
registry = JobRegistry()

# 建立任務處理器
handler = JobHandler('job1', '任務1', task)
registry.register(handler)

# 包裝執行函數
def wrapped_task():
    handler.execute()

# 新增到排程器
manager.add_job(
    func=wrapped_task,
    trigger=IntervalTrigger(seconds=5),
    id='job1'
)

manager.start()
```

執行範例：
```bash
python examples/oop_example.py
```

### 3. YML 配置範例

使用 YAML 配置檔案定義任務：

```yaml
jobs:
  - id: my_job
    name: 我的任務
    func: my_task
    trigger:
      type: interval
      params:
        seconds: 5
    enabled: true
```

```python
from apschedule import SchedulerManager
from apschedule.config_loader import ConfigLoader

config = ConfigLoader.load_from_file('config/jobs.yml')
jobs = ConfigLoader.parse_jobs(config)

manager = SchedulerManager()
for job_config in jobs:
    if job_config['enabled']:
        trigger = ConfigLoader.create_trigger(
            job_config['trigger_type'],
            job_config['trigger_params']
        )
        manager.add_job(
            func=get_function(job_config['func']),
            trigger=trigger,
            id=job_config['id'],
            name=job_config['name']
        )

manager.start()
```

執行範例：
```bash
python examples/yml_example.py
```

### 4. Annotation 裝飾器範例

使用裝飾器定義任務：

```python
from apschedule import SchedulerManager
from apschedule.decorators import set_global_scheduler, interval_job

manager = SchedulerManager()
manager._scheduler = manager._create_scheduler()
set_global_scheduler(manager)

@interval_job(seconds=5, id='job1', name='任務1')
def my_task():
    print("執行任務")

manager.start()
```

執行範例：
```bash
python examples/annotation_example.py
```

## 執行測試

```bash
# 執行所有測試
pytest

# 執行測試並顯示覆蓋率
pytest --cov=apschedule --cov-report=html

# 執行特定測試檔案
pytest tests/test_scheduler_manager.py
```

## 查看文件

開啟 `docs/flowchart.html` 查看流程圖說明文件。

## 專案結構

```
APSchedule/
├── apschedule/          # 核心模組
│   ├── __init__.py
│   ├── scheduler_manager.py  # 排程器管理器
│   ├── job_handler.py        # 任務處理器
│   ├── decorators.py        # 裝飾器
│   └── config_loader.py     # 配置載入器
├── examples/            # 範例程式
│   ├── basic_example.py
│   ├── oop_example.py
│   ├── yml_example.py
│   └── annotation_example.py
├── tests/              # 測試檔案
│   ├── test_scheduler_manager.py
│   ├── test_job_handler.py
│   ├── test_config_loader.py
│   └── test_decorators.py
├── config/            # 配置檔案
│   └── jobs.yml
├── docs/              # 文件
│   ├── flowchart.md
│   └── flowchart.html
├── requirements.txt   # 依賴套件
├── setup.py          # 安裝設定
└── README.md         # 說明文件
```

## 常見問題

### Q: 如何停止排程器？

A: 使用 `Ctrl+C` 或呼叫 `manager.stop()`

### Q: 如何暫停特定任務？

A: 使用 `manager.pause_job('job_id')`

### Q: 如何查看任務統計？

A: 使用 `JobHandler.get_stats()` 或 `JobRegistry.get_stats()`

### Q: 支援哪些觸發器類型？

A: 支援 `IntervalTrigger` (間隔觸發) 和 `CronTrigger` (Cron 表達式)


















