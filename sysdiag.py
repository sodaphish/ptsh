#!/usr/bin/python
"""
@name: sysdiag.py
@author: sodaphish@protonmail.py
@copyright: 2016/07/25, Forward Step Tech, Inc., all rights reserved
@changed: __updated__

This is a system diagnostic script 
"""

import psutil
import socket


af_map = {
    socket.AF_INET: 'IPv4',
    socket.AF_INET6: 'IPv6',
    psutil.AF_LINK: 'MAC',
}


# get CPU info
print "cpu info"
cputimes = psutil.cpu_times(percpu=True)
cpu = 0
for cpus in cputimes:
    print cpu, ": user:", cpus.user, " system:", cpus.system, " idle:", cpus.idle
    cpu += 1
print ""

# get memory info
print "memory information"
vram = psutil.virtual_memory()
print "total: ", vram.total
print "avail: ", vram.available
print "percent: ", vram.percent, "%"
swap = psutil.swap_memory()
print "total swap: ", getattr(swap, 'total')
print "used swap: ", getattr(swap, 'used')
print "free swap: ", getattr(swap, 'free')
print ""

# get filesystem info

# get disk I/O stats

# get network info
print "network interfaces"
stats = psutil.net_if_stats()
for nics, addrs in psutil.net_if_addrs().items():
    for addr in addrs:
        if af_map.get(addr.family) == 'IPv4':
            print nics, ":", addr.address, " mask:", addr.netmask

# get open sockets

# gather logs

# get open files

# get processes
