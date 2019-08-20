#!/bin/bash
#pg_dump -U zabbix -W -E en_us.UTF-8 -F c -b -v -f zabbix-clean.dump zabbix
su - postgres -c 'dropdb -U postgres zabbix'
su - postgres -c "createdb -U postgres -E UTF-8 zabbix zabbix"
pg_restore -i -U zabbix -W -d zabbix -v zabbix-test.dump
