# GitHub 專案上傳標準作業程序 (SOP)

## 📋 目錄
- [快速開始](#快速開始)
- [方法一：使用自動化腳本（推薦）](#方法一使用自動化腳本推薦)
- [方法二：手動上傳流程](#方法二手動上傳流程)
- [批次上傳多個專案](#批次上傳多個專案)
- [常見問題處理](#常見問題處理)
- [檢查清單](#檢查清單)

---

## 🚀 快速開始

### 前置需求
1. 已安裝 Git
2. 已配置 GitHub 帳號（johnGitHub24）
3. 專案目錄路徑：`D:\MCP\[專案名稱]`

### 最快速方式
使用自動化腳本，只需執行一個命令即可完成所有步驟。

---

## 方法一：使用自動化腳本（推薦）

### 步驟 1：準備腳本
將 `upload-to-github.ps1` 腳本複製到您的專案目錄，或放在 `D:\MCP\` 目錄下。

### 步驟 2：執行腳本
在 PowerShell 中執行：

```powershell
cd "D:\MCP\APSchedule"
.\upload-to-github.ps1
```

或使用完整路徑：

```powershell
D:\MCP\upload-to-github.ps1 -ProjectPath "D:\MCP\APSchedule" -RepoName "APSchedule"
```

### 步驟 3：確認
腳本會自動完成：
- ✅ 檢查是否為 Git 倉庫
- ✅ 初始化 Git（如需要）
- ✅ 添加所有文件
- ✅ 創建提交（使用正確的中文編碼）
- ✅ 添加遠程倉庫
- ✅ 推送到 GitHub

---

## 方法二：手動上傳流程

### 步驟 1：進入專案目錄
```powershell
cd "D:\MCP\[您的專案名稱]"
```

### 步驟 2：檢查 Git 狀態
```powershell
git status
```

如果顯示 "not a git repository"，需要初始化：
```powershell
git init
```

### 步驟 3：檢查 .gitignore
確保 `.gitignore` 文件存在且包含：
- `__pycache__/`
- `.venv/` 或 `venv/`
- `.idea/`
- `.vscode/`
- `*.pyc`
- 其他不需要上傳的文件

### 步驟 4：添加文件
```powershell
git add .
```

### 步驟 5：創建提交（避免中文亂碼）
**重要：使用文件方式創建提交訊息，避免 PowerShell 編碼問題**

創建臨時提交訊息文件：
```powershell
@"
Initial commit: [專案名稱] - [專案描述]
"@ | Out-File -FilePath commit_msg.txt -Encoding UTF8
```

然後使用文件創建提交：
```powershell
git commit -F commit_msg.txt
```

刪除臨時文件：
```powershell
Remove-Item commit_msg.txt
```

### 步驟 6：設置主分支
```powershell
git branch -M main
```

### 步驟 7：添加遠程倉庫
```powershell
git remote add origin https://github.com/johnGitHub24/[倉庫名稱].git
```

如果遠程倉庫已存在，先移除再添加：
```powershell
git remote remove origin
git remote add origin https://github.com/johnGitHub24/[倉庫名稱].git
```

### 步驟 8：在 GitHub 上創建倉庫
1. 前往：https://github.com/new
2. Repository name: `[您的倉庫名稱]`
3. Description: `[專案描述]`
4. 選擇 Public 或 Private
5. **不要**勾選 "Initialize this repository with a README"
6. 點擊 "Create repository"

### 步驟 9：推送代碼
```powershell
git push -u origin main
```

---

## 批次上傳多個專案

### 使用批次腳本

執行批次上傳腳本：

```powershell
cd "D:\MCP"
.\batch-upload-to-github.ps1
```

腳本會：
1. 掃描 `D:\MCP\` 目錄下的所有專案
2. 檢查哪些專案還沒有推送到 GitHub
3. 逐一處理每個專案
4. 生成處理報告

### 手動批次處理

創建專案清單文件 `projects.txt`：

```
APSchedule
AI Stock Insight
AI_Backtrader
calorie-tracker
FastAPIDemo
```

然後執行：

```powershell
$projects = Get-Content "D:\MCP\projects.txt"
foreach ($project in $projects) {
    Write-Host "處理專案: $project" -ForegroundColor Green
    cd "D:\MCP\$project"
    .\upload-to-github.ps1 -RepoName $project
}
```

---

## 常見問題處理

### 問題 1：提交訊息中文亂碼

**解決方案：**
使用文件方式創建提交訊息：

```powershell
# 創建 UTF-8 編碼的提交訊息文件
@"
Initial commit: [專案名稱] - [描述]
"@ | Out-File -FilePath commit_msg.txt -Encoding UTF8

# 使用文件創建提交
git commit -F commit_msg.txt

# 刪除臨時文件
Remove-Item commit_msg.txt
```

### 問題 2：遠程倉庫已存在

**解決方案：**
```powershell
# 檢查現有遠程倉庫
git remote -v

# 如果存在，先移除
git remote remove origin

# 重新添加
git remote add origin https://github.com/johnGitHub24/[倉庫名稱].git
```

### 問題 3：推送被拒絕（已存在提交）

**解決方案：**
```powershell
# 強制推送（謹慎使用）
git push -f origin main
```

### 問題 4：需要更新已推送的提交訊息

**解決方案：**
```powershell
# 創建修正後的提交訊息
@"
修正後的提交訊息
"@ | Out-File -FilePath commit_msg.txt -Encoding UTF8

# 修改最後一次提交
git commit --amend -F commit_msg.txt

# 強制推送
git push -f origin main

# 清理
Remove-Item commit_msg.txt
```

### 問題 5：忘記添加 .gitignore

**解決方案：**
```powershell
# 如果已經提交了不該提交的文件，需要：
# 1. 更新 .gitignore
# 2. 從 Git 中移除這些文件（但保留本地文件）
git rm -r --cached .venv
git rm -r --cached __pycache__
# 3. 重新提交
git add .gitignore
git commit -m "Update .gitignore and remove tracked files"
git push
```

---

## 檢查清單

在上傳前，請確認：

### 專案準備
- [ ] 專案有 README.md 文件
- [ ] 有適當的 .gitignore 文件
- [ ] 已移除敏感資訊（API keys、密碼等）
- [ ] 已移除大型二進制文件（如需要，使用 Git LFS）
- [ ] 已移除虛擬環境目錄（.venv, venv）
- [ ] 已移除 IDE 配置目錄（.idea, .vscode）

### Git 配置
- [ ] Git 用戶名和郵箱已配置
- [ ] 專案已初始化為 Git 倉庫
- [ ] 所有文件已添加到暫存區
- [ ] 提交訊息正確且無亂碼

### GitHub 準備
- [ ] 已在 GitHub 上創建倉庫（或確認倉庫名稱）
- [ ] 遠程倉庫 URL 正確
- [ ] 有推送權限

### 推送後
- [ ] 在 GitHub 上確認文件已上傳
- [ ] 確認提交訊息顯示正確
- [ ] 確認 README.md 顯示正常

---

## 📝 提交訊息範例

### 初始提交
```
Initial commit: APSchedule - 簡易排程系統
```

### 功能更新
```
feat: 新增 YAML 配置支援
```

### 修復問題
```
fix: 修正排程任務執行時間錯誤
```

### 文檔更新
```
docs: 更新 README 和快速開始指南
```

---

## 🔗 相關資源

- [Git 官方文檔](https://git-scm.com/doc)
- [GitHub 文檔](https://docs.github.com/)
- [Git 中文教程](https://git-scm.com/book/zh-tw/v2)

---

## 📞 支援

如有問題，請檢查：
1. Git 版本：`git --version`
2. GitHub 連接：`git ls-remote https://github.com/johnGitHub24/[倉庫名稱].git`
3. 遠程倉庫配置：`git remote -v`

---

**最後更新：** 2026-02-08
**維護者：** johnGitHub24

