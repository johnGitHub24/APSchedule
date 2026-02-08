# GitHub 上傳快速指南（最終公版）

> **這是經過測試和優化的最終版本，可在所有專案中使用，無編碼問題。**

## 使用方式

### 方式一：在專案目錄中執行
```powershell
cd "D:\MCP\您的專案名稱"
.\upload-to-github.ps1
```

### 方式二：從 APSchedule 目錄執行（推薦）
```powershell
cd "D:\MCP\APSchedule"
.\upload-to-github.ps1 -ProjectPath "D:\MCP\專案名稱" -RepoName "專案名稱" -Description "專案描述"
```

## 範例

```powershell
# 上傳 DataFrame_NumPy 專案
.\upload-to-github.ps1 -ProjectPath "D:\MCP\DataFrame_NumPy" -RepoName "DataFrame_NumPy" -Description "DataFrame and NumPy examples"
```

## 腳本功能

- ✅ 自動初始化 Git 倉庫
- ✅ 自動創建 .gitignore
- ✅ 簡單安全檢查（檢測敏感文件）
- ✅ 自動添加文件並創建提交
- ✅ 自動設置遠程倉庫
- ✅ 推送到 GitHub
- ✅ 無編碼問題（使用英文輸出，避免 PowerShell 編碼問題）
- ✅ 增強錯誤處理，更穩定可靠

## 複製腳本到其他專案

**方式一：手動複製**
```powershell
Copy-Item "D:\MCP\APSchedule\upload-to-github.ps1" -Destination "D:\MCP\您的專案\upload-to-github.ps1"
```

**方式二：直接使用（推薦）**
不需要複製，直接從 APSchedule 目錄執行即可：
```powershell
cd "D:\MCP\APSchedule"
.\upload-to-github.ps1 -ProjectPath "D:\MCP\您的專案" -RepoName "專案名稱"
```

## 注意事項

1. **上傳前請先在 GitHub 創建倉庫**：https://github.com/new
2. **倉庫名稱要與 -RepoName 參數一致**
3. **如果發現敏感文件，請先處理後再上傳**

## 保留的文件

- `upload-to-github.ps1` - 最終版本的上傳腳本（簡化版）
- `check-security.ps1` - 獨立的安全檢查工具（可選）
- `GITHUB_UPLOAD_SOP.md` - 詳細的 SOP 文檔

