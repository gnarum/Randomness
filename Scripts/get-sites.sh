#!/bin/bash

date=`date +%F_%T`
webFile='web-results.html'

nmap -A -p80 --open $1 -oG nmap-scan_$1_$date.grep

for ip in `grep 'Ports: ' nmap-scan_$1_$date.grep | awk '{print $2}'`; do 
	cutycapt --url=$ip --out=$ip.png
done

echo "<HTML><BODY><BR>" > $webFile
ls -l *.png | awk -F : '{print $1":\n<BR><IMG SRC=\""$1""$2"\" width=600><BR>"}' >> $webFile
echo "</BODY></HTML>" >> $webFile
firefox $webFile
