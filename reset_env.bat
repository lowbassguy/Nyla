@echo off
reg delete HKCU\Environment /v VIRTUAL_ENV /f 2>nul
reg delete HKCU\Environment /v VIRTUAL_ENV_PROMPT /f 2>nul
reg delete HKCU\Environment /v _OLD_VIRTUAL_PROMPT /f 2>nul

setx VIRTUAL_ENV ""
setx VIRTUAL_ENV_PROMPT ""
setx _OLD_VIRTUAL_PROMPT ""

set VIRTUAL_ENV=
set VIRTUAL_ENV_PROMPT=
set _OLD_VIRTUAL_PROMPT=

:: Reset the PATH
set PATH=%PATH:venv\Scripts;=%

:: Reset the prompt
set PROMPT=$P$G

:: Start a clean command prompt
cmd /k "prompt $P$G" 