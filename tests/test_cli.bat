@echo off
SETLOCAL

cd %~dp0

SET "plateaukit=python ..\plateaukit"

REM TODO: Test remote install
CALL %plateaukit% install plateau-30422-taiji-cho-2021 --force --local .\fixtures\30422_taiji-cho_2021_citygml_2_op.zip
CALL %plateaukit% generate-cityjson --dataset plateau-30422-taiji-cho-2021 %USERPROFILE%\AppData\Local\Temp\output.city.json

ENDLOCAL
