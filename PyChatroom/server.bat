%以管理员身份运行%
%开启telnet客户端功能%
REM when run as admin, into the current directory.
cd /d %~dp0
dism /online /Enable-Feature /FeatureName:TelnetClient

py -2 Server.py
pause
