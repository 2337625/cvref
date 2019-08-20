#!/bin/bash
# Unattended Zabbix 2.2 Server installation script for Debian Wheezy
# using PostgreSQL Server
#
# This will also install all dependencies:
#
# 	postgres
# 	zabbix-server-pgsql
# 	zabbix-frontend (apache, php5, php5-pgsql)
# 	zabbix-agent
set -e
TIMEZONE='Etc/UTC'
DBNAME='zabbix'
DBUSER='zabbix'
DBPWD='zabbix'
SERVER_NAME='monitoring.bo'	#name of the server script will handle IP

# Setup timezone for server
echo $TIMEZONE > /etc/timezone
dpkg-reconfigure --frontend noninteractive tzdata


# Download Zabbix release from official repo (it will add sources list)
wget http://repo.zabbix.com/zabbix/2.2/debian/pool/main/z/zabbix-release/zabbix-release_2.2-1+wheezy_all.deb
dpkg -i zabbix-release_2.2-1+wheezy_all.deb
apt-get update

# No let's make quite noninteractive installation with force-yes
# Change database if you have to.
# For postgres change /etc/postgres/9.1/main/pg_hba.conf
# local		all	all			trust (peer originaly)
# if you want login from console to database.
# Possibly you can make backup/restore from console or
# run as root su - postgres -c 'pg_dump -U postgres ...'
# than you don't have to change conf settings.

DEBIAN_FRONTEND=noninteractive apt-get install postgresql -y --force-yes
DEBIAN_FRONTEND=noninteractive apt-get install -y -q --force-yes zabbix-server-pgsql zabbix-frontend-php php5-pgsql

#su - postgres -c 'psql -c "CREATE USER zabbix WITH PASSWORD '\'zabbix\''"'
#su - postgres -c 'psql -c "CREATE DATABASE zabbix OWNER zabbix"'
su - postgres -c 'psql -c "ALTER USER zabbix WITH PASSWORD '\'zabbix\''"'
su - postgres -c 'psql -c "GRANT ALL PRIVILEGES ON DATABASE zabbix TO zabbix"'


# Setup timezone for server
REPLACE=''
RWITH=''

# Setup timezone for zabbix, depends what TZ we want
REPLACE=`grep 'php_value date.timezone' /etc/zabbix/apache.conf | sed -r 's/^\s*//'`
if [ -e $REPLACE ]
then
        echo "REPLACE is empty - set default"
        REPLACE="php value date.timezone $TIMEZONE"
else
        #Some timezone is setup i.e. Europe/Riga - just uncomment it
        RWITH=$(echo $REPLACE | sed -r "s|^\s*#||")
fi

echo "REPLACE what $REPLACE"
echo "REPLACE with $RWITH"

# Optionaly maybe we would like to change timezone
sed -i "s|$REPLACE|$RWITH|g" /etc/zabbix/apache.conf

# We will use values setup at the begining
tee /etc/zabbix/web/zabbix.conf.php <<EOF
<?php
// Zabbix GUI configuration file
global \$DB;

\$DB['TYPE']     = 'POSTGRESQL';
\$DB['SERVER']   = 'localhost';
\$DB['PORT']     = '0';
\$DB['DATABASE'] = 'zabbix';
\$DB['USER']     = 'zabbix';
\$DB['PASSWORD'] = 'zabbix';

// SCHEMA is relevant only for IBM_DB2 database
##\$DB['SCHEMA'] = '';

\$ZBX_SERVER      = '10.33.0.133';
\$ZBX_SERVER_PORT = '10051';
\$ZBX_SERVER_NAME = '`hostname`';

\$IMAGE_FORMAT_DEFAULT = IMAGE_FORMAT_PNG;
?>
EOF

chown -R www-data:root /etc/zabbix/web/

service apache2 reload

# Zabbix-agent install 
#This gives Linux use any string to identify host on Zabbix server
MACHINE=`uname -s`

# We can put here any string we want - metadata for Zabbix server to identify server type
# maybe strings like these: webserver,databaseserver,backupserver ...
MACHINE_TYPE='linuxdesktop'
#MACHINE_TYPE='debianserver apache2 postgresql'

#IP of Zabbix server (could be comma separtated IP list)
SERVER_IP=`hostname -I ${SERVERNAME}`

#IP of current machine 
ETH='eth0'
MY_IP=`ip addr show $ETH |grep -i inet | grep -v inet6 | awk {'print $2'} | cut -d"/" -f1 | grep -oE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"`
#Add condition to check if there is an IP and it's not from special range (127.x.x.x 169.x.x.x ...)

# Install client
apt-get install zabbix-agent -y --force-yes

#Update some configuration variables
sed -i "s|Server=127.0.0.1|Server=$SERVER_IP|" /etc/zabbix/zabbix_agentd.conf
sed -i "s|ServerActive=127.0.0.1|ServerActive=$SERVER_IP|" /etc/zabbix/zabbix_agentd.conf
sed -i "s|Hostname=Zabbix server|Hostname=$SERVER_NAME|" /etc/zabbix/zabbix_agentd.conf

#Extra variables for auto-registration - at least above must be redefined
echo "HostMetadata=$MACHINE $MACHINE_TYPE" >> /etc/zabbix/zabbix_agentd.conf

service zabbix-agent restart
