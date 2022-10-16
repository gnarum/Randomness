#!/bin/bash
IPADD=`ip add show dev tun0 | grep 'inet ' | sed 's|^[ \t]+||' | cut -d ' ' -f 6 | cut -d '/' -f 1`

echo "1" > /proc/sys/net/ipv4/ip_forward
modprobe ip_tables
modprobe ip_conntrack
modprobe ip_conntrack_ftp

iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

iptables-restore /opt/.Scripts/fwd-firewall.ipt

iptables -A INPUT -i tun0 -d $IPADD -j ACCEPT
