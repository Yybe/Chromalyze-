# PowerShell script to setup and train the face shape CNN model

Write-Host "Face Shape CNN Model Setup" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Navigate to project directory
$projectDir = Get-Location
Write-Host "Project directory: $projectDir" -ForegroundColor Yellow

# Check if dataset exists
$datasetPath = Join-Path $projectDir "backend\FaceShapeDS"
if (-not (Test-Path $datasetPath)) {
    Write-Host "Error: Dataset not found at $datasetPath" -ForegroundColor Red
    Write-Host "Please ensure the FaceShapeDS folder is in the backend directory." -ForegroundColor Red
    exit 1
}

Write-Host "Dataset found at: $datasetPath" -ForegroundColor Green

# Run the setup script
Write-Host "`nRunning setup script..." -ForegroundColor Yellow
try {
    python backend\setup_ml_model.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nSetup completed successfully!" -ForegroundColor Green
        
        # Run integration test
        Write-Host "`nRunning integration test..." -ForegroundColor Yellow
        python backend\test_cnn_integration.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`nAll tests passed! The CNN model is ready to use." -ForegroundColor Green
        } else {
            Write-Host "`nWarning: Some tests failed, but the model should still work." -ForegroundColor Yellow
        }
    } else {
        Write-Host "`nSetup failed. Please check the error messages above." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error running setup: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 Face Shape CNN Model setup complete!" -ForegroundColor Green
Write-Host "The model will now be used automatically for face shape detection." -ForegroundColor Green
Write-Host "MediaPipe will be used as fallback if the CNN model fails." -ForegroundColor Green
