#!/bin/bash --debug
aptitude remove zabbix-agent --purge -y
dpkg --purge zabbix-agent
