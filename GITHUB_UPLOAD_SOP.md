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

### ⚠️ 重要提醒：安全檢查
**在上傳前，務必確認專案中沒有包含：**
- API Keys
- 密碼
- Access Tokens
- 私鑰文件
- 資料庫連接字串（含密碼）
- 其他敏感資訊

**自動化腳本會自動執行安全檢查，發現問題會阻止上傳。**

### 最快速方式
使用自動化腳本，只需執行一個命令即可完成所有步驟（包含安全檢查）。

---

## 方法一：使用自動化腳本（推薦）

### 步驟 1：準備腳本
將以下腳本複製到您的專案目錄：
- `upload-to-github.ps1` - 上傳腳本
- `check-security.ps1` - 安全檢查腳本（重要！）

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
- ✅ **執行安全檢查**（檢測 API Key、密碼等敏感資訊）🔒
- ✅ 檢查是否為 Git 倉庫
- ✅ 初始化 Git（如需要）
- ✅ 檢查並創建 .gitignore
- ✅ 添加所有文件
- ✅ 創建提交（使用正確的中文編碼）
- ✅ 添加遠程倉庫
- ✅ 推送到 GitHub

**重要：** 如果安全檢查發現敏感資訊，腳本會**停止執行**，要求您先處理敏感資訊後再上傳。

**跳過安全檢查（不建議）：**
```powershell
.\upload-to-github.ps1 -SkipSecurityCheck
```

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

### 問題 6：已提交敏感資訊（API Key、密碼等）⚠️ 嚴重

**這是最嚴重的安全問題！如果已經推送到 GitHub，需要立即處理：**

#### 步驟 1：立即更改所有暴露的密鑰
- 登入相關服務（AWS、GitHub、資料庫等）
- **立即撤銷或更改所有暴露的 API Key、Token、密碼**
- 這比清理 Git 歷史更重要！

#### 步驟 2：從 Git 歷史中移除敏感資訊

**方法 A：使用 git filter-branch（Git 內建）**
```powershell
# 移除包含敏感資訊的文件
git filter-branch --force --index-filter `
    "git rm --cached --ignore-unmatch path/to/sensitive-file" `
    --prune-empty --tag-name-filter cat -- --all

# 強制推送（會重寫歷史，需要協調團隊）
git push origin --force --all
git push origin --force --tags
```

**方法 B：使用 BFG Repo-Cleaner（推薦，更快）**
```powershell
# 1. 下載 BFG: https://rtyley.github.io/bfg-repo-cleaner/
# 2. 創建敏感資訊列表文件 passwords.txt
# 3. 執行清理
java -jar bfg.jar --replace-text passwords.txt

# 4. 清理並推送
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

**方法 C：如果只是最後一次提交（最簡單）**
```powershell
# 1. 從暫存區移除敏感文件
git rm --cached path/to/sensitive-file

# 2. 添加到 .gitignore
echo "path/to/sensitive-file" >> .gitignore

# 3. 修改最後一次提交
git commit --amend

# 4. 強制推送（如果已經推送過）
git push -f origin main
```

#### 步驟 3：預防措施
```powershell
# 創建 .env.example 範例文件（不包含真實值）
# 將真實的 .env 添加到 .gitignore
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "secrets.json" >> .gitignore
```

**重要提醒：**
- ⚠️ 一旦敏感資訊推送到 GitHub，即使刪除，Git 歷史中仍然存在
- ⚠️ 必須使用上述方法清理歷史，或考慮刪除倉庫重新創建
- ⚠️ 更改所有暴露的密鑰是最優先事項

---

## 🔒 安全檢查（必做！）

### 使用自動化安全檢查腳本

**在上傳前，務必執行安全檢查：**

```powershell
cd "D:\MCP\[您的專案名稱]"
.\check-security.ps1
```

或使用嚴格模式（發現問題會阻止上傳）：
```powershell
.\check-security.ps1 -Strict
```

### 手動檢查要點

1. **檢查常見敏感資訊位置：**
   - `.env` 文件
   - `config.json`、`settings.json`
   - `credentials.json`、`secrets.json`
   - 任何包含 `key`、`password`、`token` 的文件

2. **檢查程式碼中的硬編碼：**
   ```python
   # ❌ 錯誤示範
   API_KEY = "sk-1234567890abcdef"
   password = "mypassword123"
   
   # ✅ 正確做法
   import os
   API_KEY = os.getenv("API_KEY")
   password = os.getenv("PASSWORD")
   ```

3. **確認 .gitignore 包含：**
   ```
   .env
   *.key
   *.pem
   secrets.json
   credentials.json
   config.local.json
   ```

### 如果發現敏感資訊

**在推送前：**
1. 移除敏感資訊
2. 使用環境變數或配置文件（並加入 .gitignore）
3. 重新執行安全檢查確認

**如果已經推送：**
1. **立即更改所有暴露的密鑰**（最優先！）
2. 參考 [問題 6](#問題-6已提交敏感資訊api-key密碼等-嚴重) 清理 Git 歷史

---

## 檢查清單

在上傳前，請確認：

### 🔒 安全檢查（最重要！）
- [ ] **已執行安全檢查腳本** `check-security.ps1`
- [ ] **未發現 API Key、密碼等敏感資訊**
- [ ] 已將敏感資訊移到環境變數或配置文件
- [ ] 配置文件已添加到 .gitignore
- [ ] 已檢查所有 `.env`、`config.json` 等文件

### 專案準備
- [ ] 專案有 README.md 文件
- [ ] 有適當的 .gitignore 文件
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

