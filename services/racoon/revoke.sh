#!/bin/sh
openssl ca -revoke /etc/racoon/certs/ca/newcerts/$1.pem
