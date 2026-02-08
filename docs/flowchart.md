# APSchedule 流程圖說明

## 系統架構流程圖

```mermaid
graph TB
    A[使用者] --> B{選擇配置方式}
    B -->|基本範例| C[basic_example.py]
    B -->|OOP設計| D[oop_example.py]
    B -->|YML配置| E[yml_example.py]
    B -->|Annotation| F[annotation_example.py]
    
    C --> G[SchedulerManager]
    D --> G
    E --> H[ConfigLoader]
    H --> G
    F --> I[Decorators]
    I --> G
    
    G --> J[BlockingScheduler/BackgroundScheduler]
    J --> K[JobStore]
    J --> L[Executor]
    
    G --> M[JobHandler]
    M --> N[JobRegistry]
    
    J --> O[執行任務]
    O --> P[記錄統計]
    P --> N
```

## 任務執行流程圖

```mermaid
sequenceDiagram
    participant U as 使用者
    participant SM as SchedulerManager
    participant S as Scheduler
    participant JH as JobHandler
    participant JR as JobRegistry
    participant F as 任務函數
    
    U->>SM: 建立排程器管理器
    SM->>S: 建立排程器實例
    U->>SM: 新增任務
    SM->>JH: 建立任務處理器
    SM->>JR: 註冊任務
    SM->>S: 添加任務到排程器
    U->>SM: 啟動排程器
    SM->>S: 啟動
    
    loop 排程執行
        S->>JH: 觸發任務執行
        JH->>F: 執行任務函數
        F-->>JH: 返回結果
        JH->>JH: 更新統計資訊
        JH->>JR: 更新註冊表
    end
    
    U->>SM: 停止排程器
    SM->>S: 停止
```

## YML 配置載入流程圖

```mermaid
flowchart TD
    A[讀取YML檔案] --> B[ConfigLoader.load_from_file]
    B --> C[解析YAML內容]
    C --> D[ConfigLoader.parse_jobs]
    D --> E{遍歷每個任務}
    E --> F[解析觸發器類型]
    F -->|interval| G[建立IntervalTrigger]
    F -->|cron| H[建立CronTrigger]
    G --> I[建立任務配置]
    H --> I
    I --> J[新增到SchedulerManager]
    J --> K[啟動排程器]
```

## Annotation 裝飾器流程圖

```mermaid
flowchart LR
    A[定義函數] --> B[使用裝飾器]
    B --> C{裝飾器類型}
    C -->|interval_job| D[建立IntervalTrigger]
    C -->|cron_job| E[建立CronTrigger]
    C -->|scheduled_job| F[使用自訂Trigger]
    D --> G[scheduled_job裝飾器]
    E --> G
    F --> G
    G --> H{全域排程器已設定?}
    H -->|是| I[自動註冊任務]
    H -->|否| J[僅包裝函數]
    I --> K[任務可執行]
    J --> K
```

說明：展示如何使用裝飾器定義排程任務，支援三種裝飾器類型（@interval_job、@cron_job、@scheduled_job），並自動註冊到全域排程器。

## 任務生命週期流程圖

```mermaid
stateDiagram-v2
    [*] --> 已建立: 新增任務
    已建立 --> 已註冊: 註冊到排程器
    已註冊 --> 等待執行: 排程器啟動
    等待執行 --> 執行中: 觸發時間到達
    執行中 --> 執行成功: 任務完成
    執行中 --> 執行失敗: 發生錯誤
    執行成功 --> 更新統計: 記錄執行資訊
    執行失敗 --> 更新統計: 記錄錯誤資訊
    更新統計 --> 等待執行: 等待下次觸發
    等待執行 --> 已暫停: 暫停任務
    已暫停 --> 等待執行: 恢復任務
    等待執行 --> 已移除: 移除任務
    已暫停 --> 已移除: 移除任務
    已移除 --> [*]
```

## 錯誤處理流程圖

```mermaid
flowchart TD
    A[任務執行] --> B{執行成功?}
    B -->|是| C[更新執行次數]
    B -->|否| D[捕獲異常]
    D --> E[更新錯誤次數]
    E --> F[記錄錯誤訊息]
    F --> G[記錄最後執行時間]
    C --> G
    G --> H[更新JobHandler統計]
    H --> I[更新JobRegistry]
    I --> J{繼續執行?}
    J -->|是| K[等待下次觸發]
    J -->|否| L[停止排程器]
```

## 測試流程圖

```mermaid
graph TB
    A[執行pytest] --> B[載入測試配置]
    B --> C[執行單元測試]
    C --> D[test_scheduler_manager]
    C --> E[test_job_handler]
    C --> F[test_config_loader]
    C --> G[test_decorators]
    
    D --> H[測試排程器管理]
    E --> I[測試任務處理]
    F --> J[測試配置載入]
    G --> K[測試裝飾器]
    
    H --> L[生成測試報告]
    I --> L
    J --> L
    K --> L
    
    L --> M{所有測試通過?}
    M -->|是| N[測試成功]
    M -->|否| O[測試失敗]
```

