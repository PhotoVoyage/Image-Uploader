@echo off
setlocal

rem Get the path of the VBS script
set "vbsScriptPath=%~dp0run.vbs"

rem Execute the VBS script
start /B "" wscript "%vbsScriptPath%"

endlocal
