@echo off
if not exist "venv" (
    echo Creating Python 3.12 virtual environment...
    py -3.12 -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Running the bot...
python bot.py

pause 