#!/bin/bash --debug
set -e
# Setup timezone for server
TIMEZONE='Etc/UTC'
REPLACE=''
RWITH=''
echo $TIMEZONE > /etc/timezone
dpkg-reconfigure --frontend noninteractive tzdata

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

# Optionaly maybe we would like to change timezone (@TODO: get TZ from server and replace)
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

#delete setup.php
