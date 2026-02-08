# GitHub Upload Script (Final Version)
# Universal script for uploading any project to GitHub
# 
# Usage:
#   1. Copy this script to your project directory, then run:
#      .\upload-to-github.ps1
#   
#   2. Or run from APSchedule directory for any project:
#      .\upload-to-github.ps1 -ProjectPath "D:\MCP\ProjectName" -RepoName "ProjectName" -Description "Description"
#
# Author: johnGitHub24
# Version: 1.0 (Final)

param(
    [string]$ProjectPath = $PSScriptRoot,
    [string]$RepoName = (Split-Path -Leaf $ProjectPath),
    [string]$Description = ""
)

$ErrorActionPreference = "Stop"

function Write-Success($msg) { Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Info($msg) { Write-Host "[*] $msg" -ForegroundColor Cyan }
function Write-Warning($msg) { Write-Host "[!] $msg" -ForegroundColor Yellow }
function Write-Error($msg) { Write-Host "[X] $msg" -ForegroundColor Red }

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Project Upload" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Info "Project: $RepoName"
Write-Info "Path: $ProjectPath"
Write-Host ""

Push-Location $ProjectPath

try {
    # 1. Init Git
    if (-not (Test-Path ".git")) {
        Write-Info "Initializing Git repository..."
        git init | Out-Null
        Write-Success "Git initialized"
    }
    
    # 2. Check .gitignore
    if (-not (Test-Path ".gitignore")) {
        Write-Info "Creating .gitignore..."
        $gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
.venv/
venv/

# IDE
.idea/
.vscode/

# Sensitive files
.env
*.key
*.pem
secrets.json
credentials.json

# OS
.DS_Store
Thumbs.db
"@
        $gitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8
        Write-Success ".gitignore created"
    }
    
    # 3. Simple security check
    Write-Info "Checking for sensitive files..."
    $sensitivePatterns = @(".env", "*.key", "*.pem", "secrets.json", "credentials.json")
    $foundSensitive = $false
    $sensitiveFilesList = @()
    
    foreach ($pattern in $sensitivePatterns) {
        try {
            $files = Get-ChildItem -Path $ProjectPath -Filter $pattern -Recurse -ErrorAction SilentlyContinue |
                Where-Object { 
                    $fullPath = $_.FullName
                    $fullPath -notlike "*\.git\*" -and 
                    $fullPath -notlike "*\.venv\*" -and 
                    $fullPath -notlike "*\venv\*" -and
                    $fullPath -notlike "*\node_modules\*" -and
                    $fullPath -notlike "*\__pycache__\*"
                }
            
            if ($files) {
                foreach ($file in $files) {
                    $relativePath = $file.FullName.Replace($ProjectPath, "").TrimStart('\')
                    $sensitiveFilesList += $relativePath
                }
                $foundSensitive = $true
            }
        } catch {
            # 忽略檢查錯誤，繼續執行
        }
    }
    
    if ($foundSensitive) {
        Write-Warning "Found potentially sensitive files:"
        foreach ($file in $sensitiveFilesList) {
            Write-Warning "  - $file"
        }
        Write-Error "Please handle sensitive files before uploading."
        Write-Info "Suggestion: Add these files to .gitignore or remove them"
        Write-Info "Press Enter to continue (not recommended), or Ctrl+C to cancel..."
        Read-Host | Out-Null
    } else {
        Write-Success "No obvious sensitive files found"
    }
    
    # 4. Add files
    Write-Info "Adding files..."
    git add . | Out-Null
    Write-Success "Files added"
    
    # 5. Create commit (only if no commits exist)
    $hasCommits = $false
    try {
        $commitCheck = git log -1 --oneline 2>$null
        if ($LASTEXITCODE -eq 0 -and $commitCheck) {
            $hasCommits = $true
        }
    } catch {
        $hasCommits = $false
    }
    
    if (-not $hasCommits) {
        Write-Info "Creating initial commit..."
        if ($Description) {
            $msg = "Initial commit: $RepoName - $Description"
        } else {
            $msg = "Initial commit: $RepoName"
        }
        $commitMsgFile = Join-Path $ProjectPath "commit_msg.txt"
        $msg | Out-File -FilePath $commitMsgFile -Encoding UTF8 -NoNewline
        git commit -F $commitMsgFile 2>&1 | Out-Null
        Remove-Item $commitMsgFile -ErrorAction SilentlyContinue
        Write-Success "Commit created"
    } else {
        Write-Info "Repository already has commits, skipping initial commit"
    }
    
    # 6. Set main branch
    git branch -M main 2>$null | Out-Null
    
    # 7. Add remote
    $remoteUrl = "https://github.com/johnGitHub24/$RepoName.git"
    $existingRemote = git remote get-url origin 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Info "Adding remote repository..."
        git remote add origin $remoteUrl | Out-Null
        Write-Success "Remote added"
    } elseif ($existingRemote -ne $remoteUrl) {
        Write-Info "Updating remote URL..."
        git remote set-url origin $remoteUrl | Out-Null
        Write-Success "Remote updated"
    }
    
    # 8. Push
    Write-Host ""
    Write-Info "Ready to push to GitHub..."
    Write-Warning "Please confirm repository created at: https://github.com/new"
    Write-Info "Repository name: $RepoName"
    Write-Info "Press Enter to continue push, or Ctrl+C to cancel..."
    Read-Host | Out-Null
    
    Write-Info "Pushing..."
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success ""
        Write-Success "Upload successful!"
        Write-Info "Repository: https://github.com/johnGitHub24/$RepoName"
    } else {
        Write-Error "Push failed!"
        Write-Info "Please check:"
        Write-Info "1. Repository created on GitHub"
        Write-Info "2. You have push permissions"
        exit 1
    }
    
} catch {
    Write-Error "Error: $_"
    exit 1
} finally {
    Pop-Location
}

Write-Host ""
Write-Success "Done!"
Write-Host ""

