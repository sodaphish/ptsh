#!/usr/bin/python

import urllib2
import sys

host = "remote"
zone = "intertrusion.com"
pswd = "en0m1234"

enom = "http://dynamic.name-services.com/interface.asp"
args = "Command=SetDNSHost&HostName=%s&Zone=%s&DomainPassword=%s" % (
    host, zone, pswd)

URL = "%s?%s" % (enom, args)

req = urllib2.Request(url=URL)

sys.exit(0)

try:
    response = urllib2.urlopen(
        "http://dynamic.name-services.com/interface.asp?Command=SetDNSHost&HostName=remote&Zone=intertrusion.com&DomainPassword=en0m1234")
except Exception as E:
    pass
