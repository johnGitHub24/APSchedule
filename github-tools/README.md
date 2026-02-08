# GitHub 上傳工具

## 📋 說明

這是用於將專案上傳到 GitHub 的簡化工具集。

## 🚀 快速使用

### 方法一：從工具目錄執行（推薦）

```powershell
cd "D:\MCP\APSchedule\github-tools"
.\upload-to-github.ps1 -ProjectPath "D:\MCP\專案名稱" -RepoName "專案名稱" -Description "專案描述"
```

### 方法二：複製到專案目錄

```powershell
# 複製腳本到專案
Copy-Item "D:\MCP\APSchedule\github-tools\upload-to-github.ps1" -Destination "D:\MCP\專案名稱\upload-to-github.ps1"

# 執行
cd "D:\MCP\專案名稱"
.\upload-to-github.ps1
```

## 📝 參數

- `-ProjectPath`: 專案路徑（預設：腳本所在目錄）
- `-RepoName`: GitHub 倉庫名稱（預設：專案目錄名稱）
- `-Description`: 專案描述（可選）

## ⚠️ 注意事項

1. **上傳前請先在 GitHub 創建倉庫**：https://github.com/new
2. **倉庫名稱要與 -RepoName 參數一致**
3. **腳本會自動檢查敏感文件（.env, *.key 等）**

## 🔧 功能

- ✅ 自動初始化 Git 倉庫
- ✅ 自動創建 .gitignore
- ✅ 簡單安全檢查（檢測敏感文件）
- ✅ 自動添加文件並創建提交
- ✅ 自動設置遠程倉庫
- ✅ 推送到 GitHub

---

**版本**: 1.0 (Final)  
**維護者**: johnGitHub24

