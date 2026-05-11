@echo off
cd /d "%~dp0"
echo Verificando arquivos...
if not exist "Manual-Ferias-SIGRH.pdf" echo AVISO: PDF NAO ENCONTRADO NA PASTA!
python seu_script.py
echo.
echo Processo concluido! Verifique a pasta 'Chunks_Manuais'.
pause