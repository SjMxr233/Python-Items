%�Թ���Ա�������%
%����telnet�ͻ��˹���%
REM when run as admin, into the current directory.
cd /d %~dp0
dism /online /Enable-Feature /FeatureName:TelnetClient

py -2 Server.py
pause
