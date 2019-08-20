#!/bin/bash
set -e
# Zabbix-agent install 
#This gives Linux use any string to identify host on Zabbix server
MACHINE=`uname -s`

# We can put here any string we want - metadata for Zabbix server to identify server type
# maybe strings like these: webserver,databaseserver,backupserver ...
MACHINE_TYPE='21df83bf21bf0be663090bb8d4128558ab9b95fba66a6dbf834f8b91ae5e08ae'

#IP of Zabbix server (could be comma separtated IP list)
SERVER_NAME='monitoring.bo'
SERVER_IP=`hostname -I ${SERVERNAME}`

#IP of current machine 
ETH='eth0'
MY_IP=`ip addr show $ETH |grep -i inet | grep -v inet6 | awk {'print $2'} | cut -d"/" -f1 | grep -oE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"`

#Add condition to check if there is an IP and it's not from special range (127.x.x.x 169.x.x.x ...)

# Install client
wget http://repo.zabbix.com/zabbix/2.2/debian/pool/main/z/zabbix-release/zabbix-release_2.2-1+wheezy_all.deb
dpkg -i zabbix-release_2.2-1+wheezy_all.deb
apt-get update
apt-get install zabbix-agent -y --force-yes

#Update some configuration variables
sed -i "s|Server=127.0.0.1|Server=$SERVER_IP|" /etc/zabbix/zabbix_agentd.conf
sed -i "s|ServerActive=127.0.0.1|ServerActive=$SERVER_IP|" /etc/zabbix/zabbix_agentd.conf
sed -i "s|Hostname=Zabbix server|Hostname=$SERVER_NAME|" /etc/zabbix/zabbix_agentd.conf

#Extra variables for auto-registration - at least above must be redefined
echo "HostMetadata=$MACHINE $MACHINE_TYPE" >> /etc/zabbix/zabbix_agentd.conf
echo "EnableRemoteCommands=1" >> /etc/zabbix/zabbix_agentd.conf

service zabbix-agent restart
