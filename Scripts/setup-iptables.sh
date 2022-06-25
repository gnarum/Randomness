#!/bin/bash

echo "1" > /proc/sys/net/ipv4/ip_forward
modprobe ip_tables
modprobe ip_conntrack
modprobe ip_conntrack_ftp

iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i tun0 -d 192.168.119.211 -j ACCEPT
iptables -A INPUT -i tun0 -d 192.168.49.111 -j ACCEPT
iptables -A INPUT -i eth0 -j ACCEPT

iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i eth0 -o tun0 -j ACCEPT

iptables -A OUTPUT -j ACCEPT
iptables -A OUTPUT -j ACCEPT

