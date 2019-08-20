#!/bin/sh
IPSEC_CA="./ca/ipsec_ca"

rm -rf ./ca
mkdir -p ca/certs
mkdir -p ca/newcerts
mkdir -p ca/crl
mkdir -p ca/private

touch ./ca/index.txt
echo '01' > ./ca/serial

# Build root CA
openssl req -new -x509 -config ./openssl.cnf -newkey rsa:2048 -days 3650
-nodes -keyout ./ca/private/ipsec_ca.key -out ./ca/ipsec_ca.pem
