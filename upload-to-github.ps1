# GitHub 專案上傳自動化腳本
# 用途：自動化將本地專案上傳到 GitHub 的流程
# 作者：johnGitHub24
# 日期：2026-02-08

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = $PSScriptRoot,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = (Split-Path -Leaf $ProjectPath),
    
    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Description = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$Force = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipSecurityCheck = $false
)

# 設置錯誤處理
$ErrorActionPreference = "Stop"

# 顏色輸出函數
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Success($message) {
    Write-ColorOutput Green "✅ $message"
}

function Write-Info($message) {
    Write-ColorOutput Cyan "ℹ️  $message"
}

function Write-Warning($message) {
    Write-ColorOutput Yellow "⚠️  $message"
}

function Write-Error($message) {
    Write-ColorOutput Red "❌ $message"
}

# 檢查專案路徑
if (-not (Test-Path $ProjectPath)) {
    Write-Error "專案路徑不存在: $ProjectPath"
    exit 1
}

Write-Info "========================================="
Write-Info "GitHub 專案上傳自動化腳本"
Write-Info "========================================="
Write-Info "專案路徑: $ProjectPath"
Write-Info "倉庫名稱: $RepoName"
Write-Info ""

# 切換到專案目錄
Push-Location $ProjectPath

try {
    # 步驟 1: 檢查是否為 Git 倉庫
    Write-Info "步驟 1: 檢查 Git 倉庫狀態..."
    $isGitRepo = Test-Path ".git"
    
    if (-not $isGitRepo) {
        Write-Info "初始化 Git 倉庫..."
        git init
        if ($LASTEXITCODE -ne 0) {
            throw "Git 初始化失敗"
        }
        Write-Success "Git 倉庫已初始化"
    } else {
        Write-Success "已是 Git 倉庫"
    }
    
    # 步驟 2: 檢查 .gitignore
    Write-Info "步驟 2: 檢查 .gitignore 文件..."
    if (-not (Test-Path ".gitignore")) {
        Write-Warning ".gitignore 文件不存在，創建基本版本..."
        @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual Environment
venv/
env/
ENV/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Security - 敏感資訊
.env
*.key
*.pem
secrets.json
credentials.json
config.local.json

# OS
.DS_Store
Thumbs.db
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
        Write-Success ".gitignore 文件已創建"
    } else {
        Write-Success ".gitignore 文件存在"
    }
    
    # 步驟 2.5: 安全檢查（重要！）
    if (-not $SkipSecurityCheck) {
        Write-Info ""
        Write-Info "步驟 2.5: 🔒 執行安全檢查..."
        $securityScript = Join-Path $ProjectPath "check-security.ps1"
        
        # 如果安全檢查腳本在同目錄，使用它
        if (Test-Path $securityScript) {
            Write-Info "執行安全檢查腳本..."
            & $securityScript -ProjectPath $ProjectPath -Strict
            if ($LASTEXITCODE -ne 0) {
                Write-Error "安全檢查失敗！發現敏感資訊。"
                Write-Warning "請先移除敏感資訊後再上傳，或使用 -SkipSecurityCheck 參數跳過檢查（不建議）"
                Write-Info ""
                Write-Info "處理方式："
                Write-Info "1. 檢查並移除所有 API Key、密碼等敏感資訊"
                Write-Info "2. 將敏感資訊移到環境變數或配置文件"
                Write-Info "3. 確保配置文件在 .gitignore 中"
                Write-Info "4. 重新執行安全檢查確認"
                exit 1
            }
            Write-Success "安全檢查通過"
        } else {
            Write-Warning "未找到 check-security.ps1，跳過自動安全檢查"
            Write-Warning "建議手動檢查專案中是否包含敏感資訊（API Key、密碼等）"
            Write-Info "按 Enter 繼續，或按 Ctrl+C 取消..."
            Read-Host
        }
        Write-Info ""
    } else {
        Write-Warning "⚠️  已跳過安全檢查（不建議）"
        Write-Info ""
    }
    
    # 步驟 3: 檢查是否有未提交的更改
    Write-Info "步驟 3: 檢查文件狀態..."
    git status --porcelain | Out-Null
    $hasChanges = $LASTEXITCODE -eq 0
    
    # 步驟 4: 添加文件
    Write-Info "步驟 4: 添加文件到暫存區..."
    git add .
    if ($LASTEXITCODE -ne 0) {
        throw "添加文件失敗"
    }
    Write-Success "文件已添加到暫存區"
    
    # 步驟 5: 檢查是否有提交
    $hasCommits = $false
    try {
        git log -1 --oneline | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $hasCommits = $true
        }
    } catch {
        $hasCommits = $false
    }
    
    # 步驟 6: 創建提交
    if (-not $hasCommits -or $Force) {
        Write-Info "步驟 5: 創建提交..."
        
        # 準備提交訊息
        if ([string]::IsNullOrEmpty($CommitMessage)) {
            if ([string]::IsNullOrEmpty($Description)) {
                $CommitMessage = "Initial commit: $RepoName"
            } else {
                $CommitMessage = "Initial commit: $RepoName - $Description"
            }
        }
        
        # 使用文件方式創建提交（避免中文亂碼）
        $commitMsgFile = Join-Path $ProjectPath "commit_msg_temp.txt"
        $CommitMessage | Out-File -FilePath $commitMsgFile -Encoding UTF8 -NoNewline
        
        git commit -F $commitMsgFile
        if ($LASTEXITCODE -ne 0) {
            Remove-Item $commitMsgFile -ErrorAction SilentlyContinue
            throw "創建提交失敗"
        }
        
        Remove-Item $commitMsgFile -ErrorAction SilentlyContinue
        Write-Success "提交已創建: $CommitMessage"
    } else {
        Write-Info "已有提交記錄，跳過創建提交"
    }
    
    # 步驟 7: 設置主分支
    Write-Info "步驟 6: 設置主分支..."
    git branch -M main 2>&1 | Out-Null
    Write-Success "主分支已設置"
    
    # 步驟 8: 檢查遠程倉庫
    Write-Info "步驟 7: 檢查遠程倉庫配置..."
    $remoteUrl = "https://github.com/johnGitHub24/$RepoName.git"
    
    $existingRemote = git remote get-url origin 2>&1
    if ($LASTEXITCODE -eq 0) {
        if ($existingRemote -ne $remoteUrl) {
            Write-Warning "遠程倉庫 URL 不匹配，更新中..."
            git remote set-url origin $remoteUrl
            Write-Success "遠程倉庫 URL 已更新"
        } else {
            Write-Success "遠程倉庫已配置"
        }
    } else {
        Write-Info "添加遠程倉庫..."
        git remote add origin $remoteUrl
        if ($LASTEXITCODE -ne 0) {
            throw "添加遠程倉庫失敗"
        }
        Write-Success "遠程倉庫已添加"
    }
    
    # 步驟 9: 推送代碼
    Write-Info "步驟 8: 推送到 GitHub..."
    Write-Warning "請確保已在 GitHub 上創建倉庫: https://github.com/new"
    Write-Info "倉庫名稱應為: $RepoName"
    Write-Info "按 Enter 繼續推送，或按 Ctrl+C 取消..."
    Read-Host
    
    if ($Force) {
        git push -f -u origin main
    } else {
        git push -u origin main
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "推送失敗！"
        Write-Info "可能的原因："
        Write-Info "1. 倉庫尚未在 GitHub 上創建"
        Write-Info "2. 沒有推送權限"
        Write-Info "3. 需要認證"
        Write-Info ""
        Write-Info "請前往 https://github.com/new 創建倉庫後重試"
        exit 1
    }
    
    Write-Success "代碼已成功推送到 GitHub！"
    Write-Info "倉庫地址: https://github.com/johnGitHub24/$RepoName"
    
} catch {
    Write-Error "發生錯誤: $_"
    exit 1
} finally {
    Pop-Location
}

Write-Info ""
Write-Success "完成！"

