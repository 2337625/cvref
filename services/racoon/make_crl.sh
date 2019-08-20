#!/bin/sh
openssl ca -gencrl -config ./openssl.cnf -out ca/crl.pem
cd ca ; ln -sf crl.pem `openssl x509 -hash -noout -in ipsec_ca.pem`.r0 ;
cd ..
