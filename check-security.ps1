# 安全檢查腳本 - 檢測敏感資訊
# 用途：在上傳到 GitHub 前檢查專案中是否包含敏感資訊
# 作者：johnGitHub24
# 日期：2026-02-08

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = $PSScriptRoot,
    
    [Parameter(Mandatory=$false)]
    [switch]$Strict = $false
)

# 設置錯誤處理
$ErrorActionPreference = "Continue"

# 顏色輸出
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

Write-Info "========================================="
Write-Info "安全檢查 - 敏感資訊檢測"
Write-Info "========================================="
Write-Info "專案路徑: $ProjectPath"
Write-Info ""

# 切換到專案目錄
Push-Location $ProjectPath

try {
    $issues = @()
    $warnings = @()
    
    # 定義敏感資訊模式
    $sensitivePatterns = @{
        "API Key" = @(
            "api[_-]?key\s*[=:]\s*['""]?[A-Za-z0-9_-]{20,}['""]?",
            "apikey\s*[=:]\s*['""]?[A-Za-z0-9_-]{20,}['""]?",
            "API_KEY\s*[=:]\s*['""]?[A-Za-z0-9_-]{20,}['""]?"
        )
        "Secret Key" = @(
            "secret[_-]?key\s*[=:]\s*['""]?[A-Za-z0-9_-]{20,}['""]?",
            "SECRET_KEY\s*[=:]\s*['""]?[A-Za-z0-9_-]{20,}['""]?"
        )
        "Password" = @(
            "password\s*[=:]\s*['""]?[^'""\s]{6,}['""]?",
            "PASSWORD\s*[=:]\s*['""]?[^'""\s]{6,}['""]?",
            "pwd\s*[=:]\s*['""]?[^'""\s]{6,}['""]?"
        )
        "Access Token" = @(
            "access[_-]?token\s*[=:]\s*['""]?[A-Za-z0-9_-]{20,}['""]?",
            "ACCESS_TOKEN\s*[=:]\s*['""]?[A-Za-z0-9_-]{20,}['""]?"
        )
        "Private Key" = @(
            "-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
            "-----BEGIN\s+EC\s+PRIVATE\s+KEY-----"
        )
        "AWS Credentials" = @(
            "aws_access_key_id\s*[=:]\s*['""]?[A-Z0-9]{20}['""]?",
            "aws_secret_access_key\s*[=:]\s*['""]?[A-Za-z0-9/+=]{40}['""]?"
        )
        "Database Connection" = @(
            "mongodb://[^'\s""]+:[^'\s""]+@",
            "postgresql://[^'\s""]+:[^'\s""]+@",
            "mysql://[^'\s""]+:[^'\s""]+@",
            "DATABASE_URL\s*[=:]\s*['""]?[^'""\s]+://[^'""\s]+:[^'""\s]+@"
        )
        "Email Credentials" = @(
            "smtp[_-]?password\s*[=:]\s*['""]?[^'""\s]{6,}['""]?",
            "email[_-]?password\s*[=:]\s*['""]?[^'""\s]{6,}['""]?"
        )
    }
    
    # 需要檢查的文件類型
    $fileExtensions = @("*.py", "*.js", "*.ts", "*.json", "*.yml", "*.yaml", "*.env", "*.config", "*.conf", "*.txt", "*.md")
    
    # 排除的目錄
    $excludeDirs = @(".git", ".venv", "venv", "env", "__pycache__", "node_modules", ".idea", ".vscode", "dist", "build")
    
    Write-Info "開始掃描文件..."
    
    # 掃描所有相關文件
    foreach ($ext in $fileExtensions) {
        $files = Get-ChildItem -Path $ProjectPath -Filter $ext -Recurse -File | 
            Where-Object { 
                $dirName = $_.DirectoryName
                $shouldExclude = $false
                foreach ($excludeDir in $excludeDirs) {
                    if ($dirName -like "*\$excludeDir\*" -or $dirName -like "*\$excludeDir") {
                        $shouldExclude = $true
                        break
                    }
                }
                -not $shouldExclude
            }
        
        foreach ($file in $files) {
            try {
                $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
                if ($null -eq $content) { continue }
                
                $lineNumber = 0
                $lines = $content -split "`n"
                
                foreach ($category in $sensitivePatterns.Keys) {
                    foreach ($pattern in $sensitivePatterns[$category]) {
                        $lineNumber = 0
                        foreach ($line in $lines) {
                            $lineNumber++
                            if ($line -match $pattern) {
                                $relativePath = $file.FullName.Replace($ProjectPath, "").TrimStart('\')
                                $issue = @{
                                    File = $relativePath
                                    Line = $lineNumber
                                    Category = $category
                                    Pattern = $pattern
                                    Content = $line.Trim()
                                }
                                
                                if ($category -in @("API Key", "Secret Key", "Access Token", "Private Key", "AWS Credentials")) {
                                    $issues += $issue
                                } else {
                                    $warnings += $issue
                                }
                            }
                        }
                    }
                }
            } catch {
                # 跳過無法讀取的文件
                continue
            }
        }
    }
    
    # 檢查常見的敏感文件名
    Write-Info "檢查敏感文件名..."
    $sensitiveFileNames = @("*.key", "*.pem", "*.p12", "*.pfx", "*.env", "secrets.json", "credentials.json", "config.json")
    foreach ($pattern in $sensitiveFileNames) {
        $files = Get-ChildItem -Path $ProjectPath -Filter $pattern -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object {
                $dirName = $_.DirectoryName
                $shouldExclude = $false
                foreach ($excludeDir in $excludeDirs) {
                    if ($dirName -like "*\$excludeDir\*" -or $dirName -like "*\$excludeDir") {
                        $shouldExclude = $true
                        break
                    }
                }
                -not $shouldExclude
            }
        
        foreach ($file in $files) {
            $relativePath = $file.FullName.Replace($ProjectPath, "").TrimStart('\')
            $warnings += @{
                File = $relativePath
                Line = 0
                Category = "敏感文件名"
                Pattern = $pattern
                Content = "文件名可能包含敏感資訊"
            }
        }
    }
    
    # 顯示結果
    Write-Info ""
    Write-Info "========================================="
    Write-Info "檢查結果"
    Write-Info "========================================="
    
    if ($issues.Count -eq 0 -and $warnings.Count -eq 0) {
        Write-Success "未發現敏感資訊！可以安全上傳。"
        exit 0
    }
    
    if ($issues.Count -gt 0) {
        Write-Error "發現 $($issues.Count) 個嚴重安全問題："
        Write-Info ""
        
        $grouped = $issues | Group-Object -Property File
        foreach ($group in $grouped) {
            Write-Error "文件: $($group.Name)"
            foreach ($issue in $group.Group) {
                Write-Info "  行 $($issue.Line): [$($issue.Category)] $($issue.Content.Substring(0, [Math]::Min(80, $issue.Content.Length)))"
            }
            Write-Info ""
        }
    }
    
    if ($warnings.Count -gt 0) {
        Write-Warning "發現 $($warnings.Count) 個警告："
        Write-Info ""
        
        $grouped = $warnings | Group-Object -Property File
        foreach ($group in $grouped) {
            Write-Warning "文件: $($group.Name)"
            foreach ($warning in $group.Group) {
                if ($warning.Line -gt 0) {
                    Write-Info "  行 $($warning.Line): [$($warning.Category)] $($warning.Content.Substring(0, [Math]::Min(80, $warning.Content.Length)))"
                } else {
                    Write-Info "  [$($warning.Category)] $($warning.Content)"
                }
            }
            Write-Info ""
        }
    }
    
    Write-Info "========================================="
    Write-Error "建議：在上傳前移除所有敏感資訊！"
    Write-Info ""
    Write-Info "處理方式："
    Write-Info "1. 將敏感資訊移到環境變數或配置文件中"
    Write-Info "2. 將配置文件添加到 .gitignore"
    Write-Info "3. 如果已經提交，使用 'git rm --cached' 移除"
    Write-Info "4. 如果已經推送到 GitHub，需要："
    Write-Info "   - 立即更改所有暴露的密鑰"
    Write-Info "   - 使用 git filter-branch 或 BFG Repo-Cleaner 清理歷史"
    Write-Info ""
    
    if ($Strict) {
        Write-Error "嚴格模式：發現安全問題，建議先處理後再上傳"
        exit 1
    } else {
        Write-Warning "非嚴格模式：請手動確認是否繼續上傳"
        exit 0
    }
    
} catch {
    Write-Error "檢查過程中發生錯誤: $_"
    exit 1
} finally {
    Pop-Location
}

