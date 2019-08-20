#!/bin/bash -debug

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

INTERNAL_ADDR="192.168.44.115"
VPN_NETWORK="192.168.44.0/24"

#OUTBOUND_IP="192.168.1.10" # if you're behind a router/gateway, otherwise use WAN IP
OUTBOUND_IP="10.33.0.115" # if you're behind a router/gateway, otherwise use WAN IP
VPN_GATEWAY="10.33.0.115"

setkey -c <<EOF
flush;
spdflush;

spdadd $VPN_NETWORK[any] $INTERNAL_ADDR[any] any -P in ipsec
esp/tunnel/$VPN_GATEWAY-$OUTBOUND_IP/require;
spdadd $INTERNAL_ADDR[any] $VPN_NETWORK[any] any -P out ipsec
esp/tunnel/$OUTBOUND_IP-$VPN_GATEWAY/require;
spddelete $VPN_NETWORK[any] $INTERNAL_ADDR[any] any -P fwd ipsec
esp/tunnel/$VPN_GATEWAY-$OUTBOUND_IP/require;

EOF
