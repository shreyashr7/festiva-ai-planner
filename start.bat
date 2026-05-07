@echo off
REM Festiva Moments - Startup Script for Windows
REM Simplified deployment for local development and testing

setlocal enabledelayedexpansion

REM =========================================================================
REM HEADER
REM =========================================================================
cls
echo.
echo ============================================================================
echo.
echo         CLS  Festiva Moments - Event Planning Platform
echo                   Phase 4: Deployment ^& Production
echo.
echo ============================================================================
echo.

REM =========================================================================
REM CHECK PREREQUISITES
REM =========================================================================
echo [1/4] Checking prerequisites...

where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed
    echo Install from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('docker --version') do set DOCKER_VERSION=%%i
echo [OK] %DOCKER_VERSION%

where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Docker Compose is not installed
    echo Install from: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('docker-compose --version') do set COMPOSE_VERSION=%%i
echo [OK] %COMPOSE_VERSION%

REM =========================================================================
REM VERIFY PROJECT STRUCTURE
REM =========================================================================
echo.
echo [2/4] Verifying project structure...

setlocal enabledelayedexpansion
set required_files=^
    phase_1_data_ml\budget_engine.pkl ^
    phase_2_nlp_rag\faiss_index\index.faiss ^
    phase_3_agents\orchestrator.py ^
    phase_4_deployment\server.py ^
    phase_4_deployment\app.py ^
    docker-compose.yml ^
    Dockerfile

for %%f in (%required_files%) do (
    if not exist "%%f" (
        echo [ERROR] Missing: %%f
        pause
        exit /b 1
    )
    echo [OK] Found: %%f
)

REM =========================================================================
REM BUILD & START SERVICES
REM =========================================================================
echo.
echo [3/4] Building Docker images and starting services...
echo This may take a few minutes on first run...
echo.

docker-compose up --build -d

REM =========================================================================
REM WAIT FOR SERVICES
REM =========================================================================
echo.
echo [4/4] Waiting for services to be healthy...

setlocal enabledelayedexpansion
set /a count=0
echo Waiting for API (port 8000)...

:wait_api
set /a count+=1
if %count% gtr 30 (
    echo Warning: API may still be starting, continuing...
    goto wait_dashboard
)
timeout /t 1 /nobreak >nul
curl -f http://localhost:8000/api/v1/health >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] API is ready
    goto wait_dashboard
)
set /a remainder=%count% %% 5
if %remainder% equ 0 echo Still waiting... (%count% seconds)
goto wait_api

:wait_dashboard
set /a count=0
echo Waiting for Dashboard (port 8501)...

:wait_dashboard_loop
set /a count+=1
if %count% gtr 30 (
    echo Warning: Dashboard may still be starting, continuing...
    goto services_ready
)
timeout /t 1 /nobreak >nul
curl -f http://localhost:8501/healthz >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Dashboard is ready
    goto services_ready
)
set /a remainder=%count% %% 5
if %remainder% equ 0 echo Still waiting... (%count% seconds)
goto wait_dashboard_loop

:services_ready
echo.
echo ============================================================================
echo.
echo              [SUCCESS] Festiva Moments is ready to use!
echo.
echo ============================================================================
echo.

echo Dashboard (Web UI):
echo   - http://localhost:8501
echo.

echo API Server:
echo   - http://localhost:8000
echo.

echo API Documentation:
echo   - http://localhost:8000/docs
echo   - http://localhost:8000/redoc
echo.

echo Health Check:
echo   - http://localhost:8000/api/v1/health
echo.

echo Service Commands:
echo   - Stop:    docker-compose down
echo   - Logs:    docker-compose logs -f
echo   - Status:  docker-compose ps
echo   - Restart: docker-compose restart
echo.

docker-compose ps

echo.
echo Ready to plan events! [SUCCESS]
echo.

endlocal
pause
