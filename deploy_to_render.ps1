# ======================================================
# LinkedIn Automation - Render.com Deployment Script
# ======================================================
# This script automates the deployment process to Render.com
# ======================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "LinkedIn Automation - Render Deployment" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your credentials first." -ForegroundColor Yellow
    exit 1
}

# Check if Git is installed
Write-Host "[1/6] Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    Write-Host "  Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host "  Install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Initialize Git repository if not already initialized
Write-Host "`n[2/6] Setting up Git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "  Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "  Git repository already exists" -ForegroundColor Green
}

# Create .gitignore if it doesn't exist
Write-Host "`n[3/6] Checking .gitignore..." -ForegroundColor Yellow
if (-not (Test-Path ".gitignore")) {
    Write-Host "  Creating .gitignore..." -ForegroundColor Yellow
    @"
# Environment variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite3

# Logs
data/logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Local scripts (not needed on Render)
*.ps1
setup_task_scheduler.ps1
start_automation.ps1
stop_automation.ps1

# Documentation (optional, can keep)
docs/
FREE_DEPLOYMENT_OPTIONS.md
QUICKSTART.md
SETUP_COMPLETE.md
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "  .gitignore created" -ForegroundColor Green
} else {
    Write-Host "  .gitignore already exists" -ForegroundColor Green
}

# Add and commit files
Write-Host "`n[4/6] Committing changes..." -ForegroundColor Yellow
git add .
$commitMessage = "Deploy to Render.com - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git commit -m "$commitMessage" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  Changes committed successfully" -ForegroundColor Green
} else {
    Write-Host "  No new changes to commit (already up to date)" -ForegroundColor Yellow
}

# Display deployment instructions
Write-Host "`n[5/6] Render.com Deployment Instructions" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Your code is ready for deployment! Follow these steps:`n" -ForegroundColor Green

Write-Host "STEP 1: Create GitHub Repository" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "  2. Repository name: linkedin-automation" -ForegroundColor White
Write-Host "  3. Keep it Private" -ForegroundColor White
Write-Host "  4. Click 'Create repository'`n" -ForegroundColor White

Write-Host "STEP 2: Push Code to GitHub" -ForegroundColor Yellow
Write-Host "  Run these commands:" -ForegroundColor White
Write-Host "  git remote add origin https://github.com/YOUR_USERNAME/linkedin-automation.git" -ForegroundColor Cyan
Write-Host "  git branch -M main" -ForegroundColor Cyan
Write-Host "  git push -u origin main`n" -ForegroundColor Cyan

Write-Host "STEP 3: Deploy to Render.com" -ForegroundColor Yellow
Write-Host "  1. Sign up at: https://render.com" -ForegroundColor White
Write-Host "  2. Click 'New +' → 'Background Worker'" -ForegroundColor White
Write-Host "  3. Connect your GitHub repository" -ForegroundColor White
Write-Host "  4. Configure:" -ForegroundColor White
Write-Host "     - Name: linkedin-automation" -ForegroundColor Cyan
Write-Host "     - Environment: Python 3" -ForegroundColor Cyan
Write-Host "     - Build Command: pip install -r requirements-minimal.txt" -ForegroundColor Cyan
Write-Host "     - Start Command: python main.py --mode auto" -ForegroundColor Cyan
Write-Host "  5. Add Environment Variables (from your .env file):" -ForegroundColor White
Write-Host "     - LINKEDIN_CLIENT_ID" -ForegroundColor Cyan
Write-Host "     - LINKEDIN_CLIENT_SECRET" -ForegroundColor Cyan
Write-Host "     - LINKEDIN_ACCESS_TOKEN" -ForegroundColor Cyan
Write-Host "     - LINKEDIN_USER_ID" -ForegroundColor Cyan
Write-Host "     - GEMINI_API_KEY" -ForegroundColor Cyan
Write-Host "     - AI_PROVIDER = gemini" -ForegroundColor Cyan
Write-Host "     - AI_MODEL = gemini-2.5-flash" -ForegroundColor Cyan
Write-Host "  6. Click 'Create Background Worker'`n" -ForegroundColor White

Write-Host "[6/6] Environment Variables from .env" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
Write-Host "Copy these values to Render.com:" -ForegroundColor Green

# Read .env file and display (without showing sensitive values)
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    foreach ($line in $envContent) {
        if ($line -match "^([^=]+)=(.*)$") {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            
            # Mask sensitive values
            if ($value.Length -gt 10) {
                $maskedValue = $value.Substring(0, 5) + "..." + $value.Substring($value.Length - 5)
            } else {
                $maskedValue = "***"
            }
            
            Write-Host "  $key = $maskedValue" -ForegroundColor Cyan
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Deployment Preparation Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Push to GitHub (see commands above)" -ForegroundColor White
Write-Host "  2. Deploy on Render.com (see instructions above)" -ForegroundColor White
Write-Host "  3. Monitor logs at: https://dashboard.render.com`n" -ForegroundColor White

Write-Host "Need help? Read RENDER_DEPLOY.md`n" -ForegroundColor Yellow
