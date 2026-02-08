# 程式碼註解風格指南

## 概述

本專案的所有程式碼都包含詳細的註解，旨在幫助初學者理解：
1. 每一行程式碼的作用
2. 使用的 library 如何運作
3. Python 語法和特性的說明
4. 最佳實踐和注意事項

## 註解結構

### 1. 模組級別註解

每個 Python 檔案開頭都應該有模組級別的文檔字串（docstring），說明：
- 模組的用途
- 主要功能
- 使用的關鍵 library 和其作用

```python
"""
模組名稱 - 簡短描述

這個模組提供了 XXX 功能。

Library 說明：
- Library1: 用於 XXX
- Library2: 用於 YYY
"""
```

### 2. 類別和函數註解

每個類別和函數都應該有詳細的 docstring，包括：
- 功能描述
- 參數說明（Args）
- 返回值說明（Returns）
- 異常說明（Raises）
- 使用範例（如果適用）

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    函數功能描述
    
    詳細說明這個函數做了什麼，為什麼這樣做。
    
    Args:
        param1: 參數1的說明
        param2: 參數2的說明
    
    Returns:
        返回值的說明
    
    Raises:
        ExceptionType: 何時會拋出這個異常
    """
```

### 3. 行內註解

對於複雜的程式碼，應該添加行內註解說明：
- 為什麼這樣寫
- 這個語法的作用
- 可能的陷阱或注意事項

```python
# 這是一個重要的操作
# 使用 XXX 的原因是因為 YYY
result = complex_operation()
```

## Library 說明

### APScheduler

APScheduler 是一個 Python 的排程任務庫，主要組件：

1. **Scheduler（排程器）**
   - `BlockingScheduler`: 阻塞式排程器，會阻塞主執行緒
   - `BackgroundScheduler`: 背景排程器，在背景執行

2. **Trigger（觸發器）**
   - `IntervalTrigger`: 固定間隔觸發（例如：每 5 秒）
   - `CronTrigger`: Cron 表達式觸發（例如：每天 9 點）
   - `DateTrigger`: 指定日期時間觸發（只執行一次）

3. **JobStore（任務儲存區）**
   - `MemoryJobStore`: 記憶體儲存（重啟後遺失）
   - `SQLAlchemyJobStore`: 資料庫儲存（持久化）

4. **Executor（執行器）**
   - `ThreadPoolExecutor`: 執行緒池執行器
   - `ProcessPoolExecutor`: 進程池執行器

### PyYAML

PyYAML 是 Python 的 YAML 解析庫：
- `yaml.safe_load()`: 安全地載入 YAML 檔案（只載入基本物件）
- `yaml.load()`: 載入 YAML 檔案（可能執行任意程式碼，不安全）

### pytest

pytest 是 Python 的測試框架：
- 測試函數必須以 `test_` 開頭
- 使用 `assert` 語句進行斷言
- 支援 fixture 和參數化測試

## Python 語法說明

### 1. 型別提示（Type Hints）

```python
def function(param: str) -> int:
    """
    param: str 表示參數 param 應該是字串類型
    -> int 表示函數返回整數類型
    """
    return len(param)
```

### 2. 裝飾器（Decorator）

```python
@decorator
def function():
    """
    @decorator 是裝飾器語法
    相當於：function = decorator(function)
    """
    pass
```

### 3. 字典解包（Dictionary Unpacking）

```python
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, **dict1}
# **dict1 會將 dict1 的鍵值對解包
# 結果：{'c': 3, 'a': 1, 'b': 2}
```

### 4. 列表推導式（List Comprehension）

```python
# 傳統寫法
result = []
for x in range(10):
    result.append(x * 2)

# 列表推導式
result = [x * 2 for x in range(10)]
```

### 5. f-string（格式化字串）

```python
name = "張三"
age = 25
# f-string 可以在字串中嵌入表達式
message = f"姓名：{name}，年齡：{age}"
```

## 註解範例

### 好的註解

```python
# 建立排程器實例
# BlockingScheduler 會阻塞主執行緒，適合單執行緒應用
scheduler = BlockingScheduler()

# 新增任務到排程器
# IntervalTrigger(seconds=5) 表示每 5 秒執行一次
scheduler.add_job(
    func=my_function,
    trigger=IntervalTrigger(seconds=5),
    id='my_job'
)
```

### 不好的註解

```python
# 建立排程器
scheduler = BlockingScheduler()

# 新增任務
scheduler.add_job(my_function, IntervalTrigger(seconds=5), 'my_job')
```

## 注意事項

1. **不要過度註解**：對於明顯的程式碼，不需要註解
2. **解釋「為什麼」而不是「是什麼」**：註解應該解釋原因，而不是重複程式碼
3. **保持註解更新**：當程式碼改變時，記得更新註解
4. **使用中文註解**：本專案使用中文註解，方便中文使用者理解

## 檢查清單

在提交程式碼前，請確認：
- [ ] 所有模組都有模組級別 docstring
- [ ] 所有類別和函數都有 docstring
- [ ] 複雜的程式碼有行內註解
- [ ] Library 的使用有說明
- [ ] Python 語法特性有解釋
- [ ] 註解與程式碼同步更新


















