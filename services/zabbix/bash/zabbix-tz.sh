#!/bin/bash
set -e
# Setup timezone for zabbix
#cp /etc/zabbix/apache.conf `pwd`/

REPLACE=`grep 'php_value date.timezone' /etc/zabbix/apache.conf | sed -r 's/^\s*//'`
if [ -z "$REPLACE" ]; then
	#echo "REPLACE is empty setting default"
        REPLACE="php value date.timezone Europe/Prague"
else
        #Some timezone is setup i.e. Europe/Riga - just uncomment it
	#echo "REPLACE is not empty preparing RWITH - ${REPLACE}"
        RWITH=`echo $REPLACE | sed -r -e "s/^\s*#//"`
fi

#echo "Replace ${REPLACE}"
#echo "Rwith ${RWITH}"

sed -i "s|$REPLACE|$RWITH|g" /etc/zabbix/apache.conf
service apache2 reload
