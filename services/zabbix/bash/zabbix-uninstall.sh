#!/bin/bash
aptitude purge -y `dpkg -l | grep -i zabbix | awk {'print $2'}`
#apt-get purge --force-yes `dpkg -l | grep -i zabbix | awk {'print $2'}`
dpkg --purge `dpkg -l | grep -i zabbix|awk {'print $2'}`

aptitude purge -y `dpkg -l | grep -i postgresql | awk {'print $2'}`
#apt-get purge --force-yes `dpkg -l | grep -i zabbix | awk {'print $2'}`

aptitude purge -y `dpkg -l | grep -i apache2 | awk {'print $2'}`
dpkg --purge `dpkg -l | grep -i apache2|awk {'print $2'}`
rm -rf /etc/zabbix /usr/share/zabbix
rm -rf /etc/dbconfig-common/zabbix-server*.conf
rm -rf /var/lib/postgresql/
rm -rf /etc/apache2/
