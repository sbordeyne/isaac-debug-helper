@echo off
echo Build started, please wait...
Python setupWin32.py build > build.log
echo Build finished, check build.log
PAUSE