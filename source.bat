@echo off

rem The sole purpose of this script is to make the command
rem
rem     source .venv/bin/activate
rem
rem work on Windows.
rem On Windows, this command just runs this batch file.
rem
rem Now we don't need to document a Windows command for activating a virtualenv.

echo Executing .venv\Scripts\activate.bat for you
.venv\Scripts\activate.bat
