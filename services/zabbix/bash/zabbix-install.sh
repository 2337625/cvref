#!/bin/bash
# Download Zabbix release from official repo (it will add sources list)
wget -O /tmp/zabbix-release.deb http://repo.zabbix.com/zabbix/2.2/debian/pool/main/z/zabbix-release/zabbix-release_2.2-1+wheezy_all.deb
dpkg -i /tmp/zabbix-relase.deb
apt-get update

# Setup timezone for server
echo 'Etc/UTC' > /etc/timezone
dpkg-reconfigure --frontend noninteractive tzdata

# No let's make quite noninteractive installation with force-yes
# Change database if you have to
DEBIAN_FRONTEND=noninteractive apt-get install postgresql -y --force-yes
DEBIAN_FRONTEND=noninteractive apt-get install -y -q --force-yes zabbix-server-pgsql zabbix-frontend-php php5-pgsql

su - postgres -c 'psql -c "ALTER USER zabbix WITH PASSWORD '\'zabbix\''"'
su - postgres -c 'psql -c "GRANT ALL PRIVILEGES ON DATABASE zabbix TO zabbix"'
