@echo off
call .\venv\Scripts\activate
python cli.py %*
call .\venv\Scripts\deactivate
@echo on