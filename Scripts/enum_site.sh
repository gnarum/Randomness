#!/bin/bash

PORTS='21-25,80,110,389,443,445'
TS=`date +%F_%H:%m:%S`
TLD=`echo $1 | egrep -o '[^/]*\.\w{2,3}' | rev | cut -d '.' -f 1 | rev`
DN=`echo $1 | egrep -o '[^/]*\.\w{2,3}' | rev | cut -d '.' -f 2 | rev`
SUB=`echo $1 | egrep -o '[^/]*\.\w{2,3}' | rev | cut -d '.' -f 3 | rev`

function Get-Pages( ) {
	# IF only one argument then do first pass
	
	# Need to make this recursive funciton so I can call it, download things, if new downloads call it again
	# once all recursion finishes then run the other scans
	for url in $(grep href $SUB.$DN.$TLD-index* | grep $DN.$TLD | cut -d '"' -f 2 | egrep '^http'); do
		FN=`cut -d '/' -f 3- | sed 's|/|_|g'`
		wget $url -O $FN.DL$1
	done

	# Else this is a recursion so start a second pass with DL$1 files downloaded	

	# IF files of DL$1 exist, call Get-Pages $1+1 
}

touch list-$DN-$TS.txt

wget $1 -O '$SUB.$DN.$TLD-index.html'

Get-Pages "1"

# Extract additional hostnames in the domain and resolve their IP addresses
for url in $(egrep -o "[^/]*\.$DN\.$TLD" $SUB.$DN.$TLD-index* | uniq | sort -u); do 
	host $url >> list-$DN-$TS.txt
done

# Quickly scan identified hosts for the ports we're interested in
for IP in $(cat list-$DN-$TS.txt | grep "has address" | cut -d " " -f 4 | sort -u); do 
	nmap -Pn -sS -p $PORTS $IP -oG nmap-scan_$TS-$IP.nmap.grep -oN nmap-scan_$TS-$IP.nmap
done

# Render all of the hosts that are serving web pages
for IP in $(cat nmap-scan_*.grep | grep "80/open" | awk '{print $2}'); do 
	cutycapt --url=http://$IP --out=$IP-80.png; 
done
for IP In $(cat nmap-scan_*.grep | grep "443/open" | awk '{print $2}'); do
	cutycapt --url=http://$IP --out=$IP-443.png;
done

# Take all of the web page renders and put them into an HTML file for easy viewing
echo "<HTML><HEAD></HEAD><BODY><br>" > pages.html
ls -l *.png | awk -F : '{ print $1":\n<BR><IMG SRC=\""$1""$2"\" width=600><BR>"}' >> pages.html
echo "</BODY></HTML>" >> pages.html
firefox pages.html
