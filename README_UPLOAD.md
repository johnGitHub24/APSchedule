# GitHub 上傳腳本 - 最終公版

## 📋 說明

這是經過測試和優化的最終版本上傳腳本，適用於所有專案。

### ✅ 特點

- **無編碼問題**：使用英文輸出，避免 PowerShell 中文編碼問題
- **穩定可靠**：增強錯誤處理，適用於各種情況
- **簡單易用**：一鍵完成所有上傳步驟
- **安全檢查**：自動檢測敏感文件

## 🚀 快速使用

### 方法一：從 APSchedule 目錄執行（推薦）

```powershell
cd "D:\MCP\APSchedule"
.\upload-to-github.ps1 -ProjectPath "D:\MCP\專案名稱" -RepoName "專案名稱" -Description "專案描述"
```

### 方法二：複製到專案目錄

```powershell
# 1. 複製腳本
Copy-Item "D:\MCP\APSchedule\upload-to-github.ps1" -Destination "D:\MCP\專案名稱\upload-to-github.ps1"

# 2. 執行
cd "D:\MCP\專案名稱"
.\upload-to-github.ps1
```

## 📝 參數說明

- `-ProjectPath`: 專案路徑（預設：腳本所在目錄）
- `-RepoName`: GitHub 倉庫名稱（預設：專案目錄名稱）
- `-Description`: 專案描述（可選）

## ⚠️ 注意事項

1. **上傳前請先在 GitHub 創建倉庫**：https://github.com/new
2. **倉庫名稱要與 -RepoName 參數一致**
3. **如果發現敏感文件，請先處理後再上傳**

## 🔄 更新腳本

如果需要更新到最新版本：

```powershell
# 從 GitHub 拉取最新版本
cd "D:\MCP\APSchedule"
git pull origin main

# 然後複製到其他專案（如需要）
Copy-Item "D:\MCP\APSchedule\upload-to-github.ps1" -Destination "D:\MCP\其他專案\upload-to-github.ps1"
```

## 📚 相關文檔

- `UPLOAD_GUIDE.md` - 快速上傳指南
- `GITHUB_UPLOAD_SOP.md` - 詳細 SOP 文檔

---

**版本**: 1.0 (Final)  
**最後更新**: 2026-02-08  
**維護者**: johnGitHub24

