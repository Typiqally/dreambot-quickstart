@echo off
setlocal EnableDelayedExpansion

color 0B

python quickstart.py

set /p "min_delay=Enter the minimum delay time (in seconds): "
set /p "max_delay=Enter the maximum delay time (in seconds): "

set /a "delay_range=%max_delay% - %min_delay% + 1"

echo Running all quick starts...

cd output
set "total=0"
for /R %%x in (*.bat) do (
    set /a total+=1
)

set "index=0"
for /R %%x in (*.bat) do (
    if not "%%x" == "%~0" (
        set /a index+=1
        set /a "delay=%min_delay% + (!RANDOM! %% delay_range)"
        echo [!index!/!total!] Waiting for !delay! seconds before calling "%%x"...
        timeout /t !delay! >nul
        call "%%x"
    )
)

del /s /q "output\*"
for /d %%a in ("output\*") do rmdir /s /q "%%a"

endlocal