#!/bin/sh

# Allow traffic that has been established 
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Block all new traffic to the port 3306
iptables -I INPUT -p tcp --dport 3306 -j DROP

# Start knockd
knockd -c /knockd.conf -d

# Listen on 3306
while true; do
    nc -l -p 3306
done
