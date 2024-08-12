@echo off
SETLOCAL

cd %~dp0

SET "plateaukit=python ..\plateaukit"

REM TODO: Test remote install
CALL %plateaukit% install plateau-30422-taiji-cho-2021 --force --local .\fixtures\30422_taiji-cho_2021_citygml_2_op.zip
CALL %plateaukit% prebuild plateau-30422-taiji-cho-2021 -t bldg

CALL %plateaukit% export-geojson --dataset plateau-30422-taiji-cho-2021 %USERPROFILE%\AppData\Local\Temp\output.geo.json
CALL %plateaukit% export-cityjson --dataset plateau-30422-taiji-cho-2021 %USERPROFILE%\AppData\Local\Temp\output.city.json

CALL %plateaukit% export-geojson --dataset plateau-30422-taiji-cho-2021 %USERPROFILE%\AppData\Local\Temp\output.city.jsonl --seq
CALL %plateaukit% export-cityjson --dataset plateau-30422-taiji-cho-2021 %USERPROFILE%\AppData\Local\Temp\output.city.jsonl --seq

CALL %plateaukit% info plateau-30422-taiji-cho-2021
CALL %plateaukit% info plateau-28225-asago-shi-2022

ENDLOCAL
