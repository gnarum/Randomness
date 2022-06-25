#!/bin/bash

if [ $# -le 2 ]; then
	echo 'Usage:  do-pingsweep <Subnet> <First IP> <Last IP>'
	echo 'Example:  do-pingsweep 127.0.0 1 254'
	exit
fi

for i in `seq $2 $3`; do 
	ping -n -c 2 -w 1 $1.$i | grep 'icmp_seq=1' &>/dev/null && echo $1.$i | tee -a pingable.txt
done
