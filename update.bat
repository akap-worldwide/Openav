@ECHO off

rem downloading/updating core clamav db
"clamEngine/freshclam"

rem updating the extra databases....
cd pkg_update
sigupdate.bat

cd ..