@echo off
REM run_analysis.bat
REM This script activates the virtual environment, generates financial data, and runs the analysis.

REM Check if virtual environment exists
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo Virtual environment not found. creating venv virtual environment now:
    call python -m venv venv
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Generate financial data
echo Generating financial data...
python data\generate_financial_data.py

REM Run the analysis
echo Running data analysis...
python analysis.py


echo.
echo All tasks completed successfully.



REM After running analysis.py

echo Running unit tests...
pytest || (
    echo Tests failed.
    deactivate
    exit /b 1
)

echo All unit tests passed
REM Deactivate the virtual environment
echo Deactivating virtual environment...
deactivate
pause

