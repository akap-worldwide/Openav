@echo off

rem ----------------------------------------------------------------------
rem Sanesecurity downloader v0.8 beta for ClamWin/ClamAV (c) Steve Basford
rem Please see readme.txt
rem -----------------------------------------------------------------------

echo.
echo Sanesecurity downloader for ClamAV/ClamWin
echo.

rem ### Manually Set the default sigupdate.bat log location
rem ### For ClamWin 64bit:  set logloc=%ProgramFiles(x86)%\ClamWin
rem ### For ClamWin 32bit:  set logloc=%ProgramFiles%\ClamWin
rem ### For MailEnable   :  set logloc=%ProgramFiles(x86)%\Mailen~1\Antivi~1\ClamAV
rem ### Change the line below to match the pathname you need (see above examples)



echo Checking for common config errors...
echo.

IF NOT EXIST winrsync\rsync.exe echo Warning: Cannot find rsync.exe (winsync\rsync.exe)
IF NOT EXIST signames.txt echo "Warning: signames.txt not found


IF NOT EXIST winrsync\rsync.exe goto fin
IF NOT EXIST signames.txt goto fin


echo.
echo Config check passed...
echo.

rem ### Manually set ClamWin/ClamAV database path
rem ### Example: ClamWin    : Set db=%ALLUSERSPROFILE%\.clamwin\db\
rem ### Example: ClamAV     : set db=C:\clamav\database
rem ### Example: MailEnable : set db=%ProgramFiles(x86)%\Mailen~1\Antivi~1\ClamAV\db\
rem ### Change the line below to match the database pathname you need (see above examples



rem ### Automatically obtain the DB directory from the Clamwin.conf file
rem ### This will override the above manual setting


echo Standby for action...
echo.

echo Current batch path:
echo %~f0
echo Started: %date%-%time%
echo Started: %date%-%time% > sigupdate.log
echo Downloading files from mirror... 
echo Downloading files from mirror...  >> sigupdate.log
echo.

rem ### Normal *public* rsync address is: rsync.sanesecurity.net
rem ### If you have been given a private donators rsync address, replace rsync.sanesecurity.net
rem ### with your private donators rsync address

"winrsync\rsync.exe" >> sigupdate.log --timeout 120 -i  -vv -p -z -t rsync://rsync.sanesecurity.net/sanesecurity/* dbtemp


rem ### uncomment thees lines to reload/restart clamd
rem echo Reloading ClamD....
rem echo Reloading ClamD....  >> "%logloc%"\sigupdate.log
rem reload clamd databases
rem net stop clamd
rem net start clamd

echo Deleting extra files
cd dbtemp
del *.md5
del *.sha*
del *.txt
del TIMESTAMP
cd ..
echo copying Files from detemp to databse folder....
ROBOCOPY dbtemp ../clamEngine/database /mov

echo Finished: %date%-%time% >> sigupdate.log
echo Finished: %date%-%time%
echo.

:fin

