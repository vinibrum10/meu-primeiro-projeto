@echo off
cd /d "%~dp0"
echo Iniciando Gestao Vinicius...
call .venv\Scripts\activate
streamlit run app.py
pause
