@echo off
REM ============================================================
REM  DevTools - One-click deploy to AWS Lambda (FREE TIER)
REM  Prerequisites: AWS CLI + AWS SAM CLI installed & configured
REM ============================================================

set "AWS_EXE=C:\Program Files\Amazon\AWSCLIV2\aws.exe"
set "SAM_CMD=C:\Program Files\Amazon\AWSSAMCLI\bin\sam.cmd"

if not exist "%AWS_EXE%" (
	echo AWS CLI not found at "%AWS_EXE%"
	echo Install it with: winget install --id Amazon.AWSCLI -e
	pause
	exit /b 1
)

if not exist "%SAM_CMD%" (
	echo AWS SAM CLI not found at "%SAM_CMD%"
	echo Install it with: winget install --id Amazon.SAM-CLI -e
	pause
	exit /b 1
)

echo.
echo === DevTools AWS Lambda Deploy ===
echo.

echo [0/3] Checking AWS credentials...
"%AWS_EXE%" sts get-caller-identity >nul 2>&1
if errorlevel 1 (
	echo AWS credentials not configured.
	echo Run this first, then run deploy.bat again:
	echo   "%AWS_EXE%" configure
	pause
	exit /b 1
)

REM 1. Build the SAM project (lightweight, no Docker required)
echo [1/3] Building SAM project...
"%SAM_CMD%" build --cached
if errorlevel 1 (
	echo Build failed.
	echo If dependency compilation is required, start Docker Desktop and use:
	echo   "%SAM_CMD%" build --use-container --cached
	pause
	exit /b 1
)

REM 2. Deploy non-interactively
echo [2/3] Deploying to AWS...
"%SAM_CMD%" deploy --template-file .aws-sam\build\template.yaml --stack-name devtools-app --capabilities CAPABILITY_IAM --resolve-s3 --region us-east-1 --no-confirm-changeset --no-fail-on-empty-changeset
if errorlevel 1 (
	echo Deploy failed. Check IAM permissions and AWS region.
	pause
	exit /b 1
)

echo.
echo [3/3] Done! Your app URL is shown above in the Outputs section.
echo        It only runs when someone visits (zero cost when idle).
echo.
pause
