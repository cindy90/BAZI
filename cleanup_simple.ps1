# 清理项目中的重复历史文件
Write-Host "开始清理重复的历史文件..." -ForegroundColor Green

# 定义要删除的文件
$filesToDelete = @(
    # 报告文件
    "ADVANCED_DAYUN_INTEGRATION_FINAL_SUMMARY.md",
    "ADVANCED_DAYUN_INTEGRATION_REPORT.md",
    "AI_ANALYSIS_BUTTON_GUIDE.md",
    "AI_ANALYSIS_DISPLAY_FIX_REPORT.md",
    "AI_ANALYSIS_FIX_COMPLETION_REPORT.md",
    "API_KEY_SETUP.md",
    "BACKEND_RESTART_SUCCESS_REPORT.md",
    "BAZI_CALCULATOR_FINAL_COMPLETION_REPORT.md",
    "BAZI_FIELDS_FIX_COMPLETION_REPORT.md",
    "CURRENT_YEAR_AI_ANALYSIS_FIX_REPORT.md",
    "DAYUN_DISPLAY_FIX_REPORT.md",
    "DAYUN_REFERENCE_INTEGRATION_FINAL_REPORT.md",
    "DAY_MASTER_STRENGTH_FIELD_FIX_REPORT.md",
    "DAY_MASTER_STRENGTH_INTEGRATION_REPORT.md",
    "DEEPSEEK_AI_SERVICE_COMPLETION_REPORT.md",
    "DEEPSEEK_API_CONFIG_GUIDE.md",
    "DEEPSEEK_DAYUN_INTEGRATION_REPORT.md",
    "DEEPSEEK_PROFESSIONAL_FRAMEWORK_OPTIMIZATION_REPORT.md",
    "DEEPSEEK_SERVICE_DEBUG_REPORT.md",
    "DETAILED_ANALYSIS_IMPLEMENTATION_REPORT.md",
    "FIVE_ELEMENTS_PERCENTAGE_AND_PRECISION_FINAL_REPORT.md",
    "FRONTEND_AXIOS_RADIO_FIX_REPORT.md",
    "FRONTEND_IMPORT_PATH_FIX_REPORT.md",
    "FRONTEND_OPTIMIZATION_COMPLETION_REPORT.md",
    "FRONTEND_TIMEOUT_FIX_GUIDE.md",
    "ICHING_500_ERROR_FIX_REPORT.md",
    "ICHING_API_IMPLEMENTATION_REPORT.md",
    "INTEGRATION_SUCCESS_SUMMARY.md",
    "MAJOR_CYCLES_OPTIMIZATION_REPORT.md",
    "NEW_FRAMEWORK_FINAL_COMPLETION_REPORT.md",
    "NEW_FRAMEWORK_INTEGRATION_COMPLETION_REPORT.md",
    "OPTIMIZATION_COMPLETION_REPORT.md",
    "PALACE_INFO_FIX_COMPLETION_REPORT.md",
    "PALACE_INFO_FIX_REPORT.md",
    "PRECISE_DAYUN_IMPLEMENTATION_REPORT.md",
    "PROJECT_COMPLETION_REPORT.md",
    "SOLUTION_SUMMARY.md",
    "SPECIFIC_CASE_END_TO_END_VERIFICATION_REPORT.md",
    "STEPWISE_FRONTEND_GUIDE.md",
    "TWELVE_PALACES_IMPLEMENTATION_REPORT.md"
)

# 删除所有 test_*.py 文件
$testFiles = Get-ChildItem -Name "test_*.py"
$filesToDelete += $testFiles

# 删除所有 debug_*.py 文件  
$debugFiles = Get-ChildItem -Name "debug_*.py"
$filesToDelete += $debugFiles

# 删除其他临时文件
$otherFiles = @(
    "check_database.py",
    "check_eightchar_methods.py",
    "cors_test.html",
    "create_tables.py",
    "demo_ai_analysis_frontend.html",
    "demo_stepwise_frontend.py",
    "diagnose_dayun_analysis.py",
    "diagnose_deepseek_issues.py",
    "direct_api_call.py",
    "explore_ichingshifa.py",
    "explore_iching_library.py",
    "explore_palace_info.py",
    "explore_twelve_palaces.py",
    "final_comprehensive_test.py",
    "final_integration_test.py",
    "FINAL_STATUS_REPORT.py",
    "final_verification.py",
    "final_verification_1990_case.py",
    "quick_api_test.py",
    "quick_backend_test.py",
    "quick_test.py",
    "reset_database.py",
    "save_full_response.py",
    "simple_api_test.py",
    "simple_connection_test.py",
    "simple_iching_test.py",
    "simple_test.py",
    "specific_case_1990_0429_result_20250626_160912.json",
    "verify_dayun_fields.py",
    "verify_deepseek_config.py",
    "verify_precise_dayun.py"
)

$filesToDelete += $otherFiles

$deletedCount = 0

foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        try {
            Remove-Item $file -Force
            Write-Host "已删除: $file" -ForegroundColor Yellow
            $deletedCount++
        }
        catch {
            Write-Host "无法删除: $file" -ForegroundColor Red
        }
    }
}

Write-Host "`n清理完成! 删除了 $deletedCount 个文件" -ForegroundColor Green

# 显示剩余文件
Write-Host "`n剩余的重要文件:" -ForegroundColor Green
Get-ChildItem -Name "*.md" | Sort-Object
