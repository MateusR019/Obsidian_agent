@echo off
REM Segundo Cérebro — Start All (Windows)
echo === Segundo Cérebro ===

REM 1. Sobe Evolution API via Docker Compose
echo [1/3] Subindo Evolution API...
docker compose up -d
if errorlevel 1 (
    echo ERRO: Docker Compose falhou. Verifique se o Docker está rodando.
    exit /b 1
)

REM 2. Aguarda Evolution ficar saudável
echo [2/3] Aguardando Evolution API...
:WAIT_LOOP
curl -s http://localhost:8080 >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto WAIT_LOOP
)
echo Evolution API pronta.

REM 3. Inicia FastAPI
echo [3/3] Iniciando Segundo Cérebro...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
