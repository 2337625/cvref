#!/bin/sh
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
CERTPATH="/etc/racoon/certs"
openssl req -newkey rsa:2048 -nodes -config $CERTPATH/openssl.cnf
-keyout $CERTPATH/ca/certs/$1.key -out $CERTPATH/ca/certs/$1.req
openssl ca -in $CERTPATH/ca/certs/$1.req -out $CERTPATH/ca/certs/$1.pem
-config $CERTPATH/openssl.cnf
