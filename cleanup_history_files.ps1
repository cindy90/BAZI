# 清理项目中的重复历史文件
Write-Host "开始清理重复的历史文件..." -ForegroundColor Green

# 定义要删除的文件类型和模式
$filesToDelete = @(
    # 各种报告和文档文件
    "*_REPORT.md",
    "*_COMPLETION_REPORT.md", 
    "*_INTEGRATION_REPORT.md",
    "*_SUMMARY.md",
    "*_GUIDE.md",
    "*_FIX_REPORT.md",
    "*_SUCCESS_REPORT.md",
    "*_IMPLEMENTATION_REPORT.md",
    "*_OPTIMIZATION_REPORT.md",
    "*_CONFIG_GUIDE.md",
    
    # 测试文件
    "test_*.py",
    "debug_*.py",
    "diagnose_*.py",
    "explore_*.py",
    "verify_*.py",
    "check_*.py",
    "final_*.py",
    
    # 演示和临时文件
    "demo_*.py",
    "demo_*.html",
    "quick_*.py",
    "simple_*.py",
    "direct_*.py",
    
    # 特定的测试HTML文件
    "*.html",
    
    # JSON测试结果文件
    "*.json",
    
    # 数据库相关测试脚本
    "create_tables.py",
    "reset_database.py",
    
    # 其他临时脚本
    "save_full_response.py",
    "FINAL_STATUS_REPORT.py"
)

# 需要保留的重要文件
$keepFiles = @(
    "cleanup_project.ps1",
    "pyrightconfig.json"
)

$deletedCount = 0
$totalSize = 0

foreach ($pattern in $filesToDelete) {
    $files = Get-ChildItem -Path "." -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if ($keepFiles -notcontains $file) {
            try {
                $fileInfo = Get-Item $file -ErrorAction SilentlyContinue
                if ($fileInfo) {
                    $totalSize += $fileInfo.Length
                    Remove-Item $file -Force
                    Write-Host "已删除: $file" -ForegroundColor Yellow
                    $deletedCount++
                }
            }
            catch {
                Write-Host "无法删除: $file - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
}

Write-Host "`n清理完成!" -ForegroundColor Green
Write-Host "删除了 $deletedCount 个文件" -ForegroundColor Cyan
Write-Host "释放了 $([math]::Round($totalSize/1KB, 2)) KB 空间" -ForegroundColor Cyan

# 显示剩余的重要文件
Write-Host "`n剩余的重要文件:" -ForegroundColor Green
Get-ChildItem -Path "." -Name "*.md" | Sort-Object | ForEach-Object {
    if ($_ -notmatch "_REPORT\.md$" -and $_ -notmatch "_GUIDE\.md$" -and $_ -notmatch "_SUMMARY\.md$") {
        Write-Host "  - $_" -ForegroundColor White
    }
}

Write-Host "`n项目目录:" -ForegroundColor Green
Get-ChildItem -Path "." -Directory | ForEach-Object {
    Write-Host "  - $($_.Name)/" -ForegroundColor Cyan
}
