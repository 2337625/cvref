#!/bin/sh
# Default FW
SERVER_IP=$(ifconfig eth0|grep -i 'inet addr' | awk {'print $2'} | grep -oE '(\w+)\.(\w+)\.(\w+)\.(\w+)')
echo 'ServerIP:'$SERVER_IP

#Flush tables
iptables -F
iptables -X
# Setting default filter policy
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
# Allow unlimited traffic on loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
 
# Allow incoming ssh only
iptables -A INPUT -p tcp -s 0/0 -d $SERVER_IP --sport 513:65535 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -s $SERVER_IP -d 0/0 --sport 22 --dport 513:65535 -m state --state ESTABLISHED -j ACCEPT

# Allow incomming HTTP:80
iptables -A INPUT -p tcp -s 0/0 --sport 1024:65535 -d $SERVER_IP --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -s $SERVER_IP --sport 80 -d 0/0 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT

# Allow incomming HTTPS:443
iptables -A INPUT -p tcp -s 0/0 --sport 1024:65535 -d $SERVER_IP --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -s $SERVER_IP --sport 443 -d 0/0 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT

# Allow forward
#iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT

# Allow input
#iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

# make sure nothing comes or goes out of this box
iptables -A FORWARD -j DROP
iptables -A INPUT -j DROP
iptables -A OUTPUT -j DROP
