@echo off
setlocal enabledelayedexpansion

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
REM Note: Using call to run the activation script and then execute pip install
call venv\Scripts\activate

REM Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM Check if the .env file exists; if not, create it.
if not exist ".env" (
    echo Creating .env file with default values...
    (
        echo BASE_URL=http://10.69.4.6:8080/api/v2
        echo USERNAME=username
        echo PASSWORD=password
        echo AGE_THRESHOLD_DAYS=16
        echo LAST_ACTIVITY_THRESHOLD_DAYS=10
    ) > .env
) else (
    echo .env file already exists. Skipping creation.
)

echo Setup complete. You can now run your main application.

REM Remove the setup folder
echo Cleaning up setup files...
rmdir /S /Q setup

echo Setup complete and cleanup finished.
pause