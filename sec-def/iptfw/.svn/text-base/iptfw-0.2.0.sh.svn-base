#!/bin/sh
# iptfw.sh v.0.2.0
# (C)opyright 2003, C.J. Steele, all rights reserved.
# 
# author: C.J. Steele <csteele@forwardsteptech.com>
# homepage: 
# desc: 
#	Netfilter rules for securing servers and configuring PAT boxes; 
#	Users who don't know wtf they're doing shouldn't edit anything
#	except the "VARIABLE DECLARATIONS" section... 
# 
# TODO: 
#	- add egress filtering (v.0.3.0)
# 

#########################################################################
# VARIABLE DECLARATIONS
#########################################################################
# binaries we'll be using
IPTABLES="/sbin/iptables"
INSMOD="/sbin/insmod"
SYSCTL="/sbin/sysctl"
# module library
MODLIB="/lib/iptables"

# packet forwarding policy; 0=no, 1=yes  Only enable this (i.e. 1) if you 
# 	want to forward traffic for some network, and make sure that you 
#	configure the FORWARDNET variable
PACKET_FORWARDING="0"

# network interfaces
# EXTINT is the interface plugged in to the outside world
EXTINT="eth0"
# INTINT is the interface plugged in to the private network
INTINT=""

# network addresses
LO_IP="127.0.0.1"
INT_IP=""
EXT_IP="192.168.2.100"

# these are the nameservers we'll communicate with.  make sure you use
# 	fully qualified host names including CIDR notation.
NAMESERVERS="216.16.0.2/32 216.16.0.4/32"

# icmp types to allow
# RFC7921 ICMP Types
# 0  : echo reply
# 3  : destination unreachable
# 4  : source quench
# 5  : redirect
# 8  : echo
# 11 : time exceeded
# 13 : timestamp
# 14 : timestamp reply
ALLOWEDICMP="0 3 11"

# general services you want to make available:
SERVICES="80 25"

# trusted services
TRUSTEDSERVICES="22"

# these are CIDR blocks you trust, note that a /32 network is a single 
#	host, 24 is a "class C" network, 16 is a "class B" network, and 
#	8 is a "class A" network.
TRUSTED="192.168.2.0/24 172.16.102.11/32"

# the CIDR network you want to forward traffic for, 
# 	use "0.0.0.0/32" if you don't want to forward
FORWARDNET="0.0.0.0/32"	



#########################################################################
# PRELIMINARY ACTIONS
#########################################################################
# turn packet forwarding on/off, depending on site policy
echo "$PACKET_FORWARDING" > /proc/sys/net/ipv4/ip_forward 
# load modules
#$INSMOD $MODLIB/libipt_state.so
#$INSMOD $MODLIB/libipt_LOG.so
# flush existing firewall rules
$IPTABLES -F INPUT
$IPTABLES -F OUTPUT
$IPTABLES -F FORWARD
# set default policies
$IPTABLES -P INPUT DROP
$IPTABLES -P OUTPUT DROP
$IPTABLES -P FORWARD DROP



#########################################################################
# INCOMING RULES
#########################################################################
# allow localhost traffic in coming
$IPTABLES -A INPUT -i lo -s 127.0.0.0/8 -d 127.0.0.0/8 -j ACCEPT
# allow pre-established traffic in.
$IPTABLES -A INPUT -p TCP -m state --state ESTABLISHED,RELATED -j ACCEPT
# setting up allowed services for the general public.
for SERVICE in $SERVICES; do
	$IPTABLES -A INPUT -p TCP -s 0/0 --dport $SERVICE -j ACCEPT
done
# setting up access for trusted services on trusted hosts...
for HOST in $TRUSTED; do
	for TRUSTEDSERVICE in $TRUSTEDSERVICES; do
		$IPTABLES -A INPUT -p TCP -s $HOST --dport $TRUSTEDSERVICE -j ACCEPT
	done
done
# setting up access for the allowed ICMP types
for ICMPTYPE in $ALLOWEDICMP; do
	$IPTABLES -A INPUT -p ICMP -s 0/0 --icmp-type $ICMPTYPE -j ACCEPT
done
# allow our DNS queries to come back in
for NS in $NAMESERVERS; do
	$IPTABLES -A INPUT -p UDP -d $EXT_IP -s $NS --sport 53 -j ACCEPT
done



#########################################################################
# OUTGOING RULES
#########################################################################
$IPTABLES -A OUTPUT -p ALL -s 127.0.0.0/8 -j ACCEPT
$IPTABLES -A OUTPUT -p ALL -s $EXT_IP -j ACCEPT
$IPTABLES -A OUTPUT -p ALL -s $FORWARDNET -j ACCEPT



#########################################################################
# LOG ALL DROPPED PACKETS
#########################################################################
$IPTABLES -A INPUT -p tcp -j LOG --log-prefix="firewall "
$IPTABLES -A INPUT -p udp -j LOG --log-prefix="firewall "
$IPTABLES -A INPUT -p icmp -j LOG --log-prefix="firewall "
$IPTABLES -A INPUT -p ip -j LOG --log-prefix="firewall "
