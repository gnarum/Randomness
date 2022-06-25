#!/bin/bash
# mkdir (TCP,UDP,"Web Services")
for f in `ls tcp* | cut -d '_' -f 2 | uniq | sort -n`; do
	mkdir -p TCP/$f
	cp tcp_$f* TCP/$f
	if [ $f -eq 445 ]; then
		cp enum4linux.txt TCP/$f
		cp smb* TCP/$f
	fi
done
for f in `grep 'open' _top_20_udp_nmap.txt | cut -d '/' -f 1`; do
	mkdir -p UDP/$f
	echo 'Needs Validation' > UDP/$f/udp_$f.txt
done
