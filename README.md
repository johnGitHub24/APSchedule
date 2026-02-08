# APSchedule - 簡易排程系統

一個基於 APScheduler 的簡易排程系統，支援多種配置方式和 OOP 設計。

## 功能特色

1. **基本範例** - Schedule/Job/APScheduler 基本用法
2. **OOP 設計** - 完善的物件導向架構
3. **YML 配置** - 支援 YAML 配置檔案
4. **Annotation 裝飾器** - 使用裝飾器定義排程任務
5. **單元測試** - 完整的測試套件
6. **流程圖文件** - Mermaid 和 HTML 流程圖說明
7. **詳細註解** - 每一行程式碼都有詳細註解，適合初學者學習

## 安裝

```bash
pip install -r requirements.txt
```

## 使用方式

### 基本範例
```python
python examples/basic_example.py
```

### OOP 範例
```python
python examples/oop_example.py
```

### YML 配置範例
```python
python examples/yml_example.py
```

### Annotation 範例
```python
python examples/annotation_example.py
```

## 執行測試

```bash
pytest tests/ -v --cov=apschedule
```

## 文件

- **流程圖文件**: 查看 `docs/` 目錄下的流程圖文件
- **程式碼註解**: 所有程式碼都包含詳細的每一行註解，說明：
  - 每一行程式碼的作用
  - 使用的 library 如何運作（APScheduler、PyYAML、pytest 等）
  - Python 語法和特性的說明
  - 最佳實踐和注意事項
- **註解風格指南**: 查看 `CODING_STYLE.md` 了解註解風格和規範

## 學習資源

本專案特別適合初學者學習，因為：

1. **完整的註解**: 每一行程式碼都有詳細註解，解釋：
   - 程式碼的作用
   - 為什麼這樣寫
   - 使用的 library 如何運作
   - Python 語法特性

2. **Library 說明**: 在註解中詳細說明：
   - APScheduler 的組件和用法
   - PyYAML 的 YAML 解析
   - pytest 的測試框架
   - Python 標準庫的使用

3. **從簡單到複雜**: 
   - `examples/basic_example.py`: 最基礎的用法
   - `examples/oop_example.py`: OOP 設計
   - `examples/yml_example.py`: YML 配置
   - `examples/annotation_example.py`: 裝飾器用法

4. **測試範例**: 測試文件也包含詳細註解，說明如何編寫單元測試

