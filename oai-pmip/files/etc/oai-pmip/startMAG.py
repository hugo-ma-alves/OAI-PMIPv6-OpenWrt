#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import getopt

from subprocess  import *

class IPv6Address:

        def __init__ (self, ipv6):
                self.ipv6 = ipv6

        def __str__ (self):
                return self.format()

        def format(self):
                splited = self.ipv6.split("::")
                toReturn =[]
                if len(splited) == 0:
                        toReturn = self.ipv6
                else:
                        toReturn.append(splited[0])
                        octetsMiss = 8 - ( len(splited[0].split(":")) + len(splited[1].split(":")))
                        toReturn.append(":0000" * octetsMiss)
                        toReturn.append(":")
                        toReturn.append(splited[1])

                return ''.join(toReturn)


try:
    opts, args = getopt.getopt(sys.argv[1:], "prdc", [ "runversion=", "cfile="])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    sys.exit(2)

g_run_version = "1"
g_config_file = ""

for o,p in opts:
  if o in ['-r','--runversion']:
     g_run_version = str(p)
  elif o in ['-c','--cfile']:
     g_config_file = str(p)

############################################################################################
g_file_config=g_config_file
############################################################################################

print "Config file is : " + g_file_config


g_RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks = IPv6Address('0::0')
g_RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks = " "
g_LmaAddress                                      = IPv6Address('0::0')
g_MagAddressIngress                               = IPv6Address('0::0')
g_MagAddressEgress                                = IPv6Address('0::0')
g_MagDeviceIngress                                = " "
g_MagDeviceEgress                                 = " "


g_fhandle = open(g_file_config, 'r')
g_fcontent = g_fhandle.read()
g_fhandle.close()

lines = g_fcontent.splitlines()
for line in lines:
    line = line.rstrip().lstrip()
    line = line.rstrip(';')
    split = line.split(' ')
    element = split[-1]
    element = element.strip('"')
    if 'RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks' in line:
        print line
        g_RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks = IPv6Address(element)

    elif 'RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks' in line:
        print line
        g_RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks = element
    elif 'LmaPmipNetworkAddress' in line:
        print line
        g_LmaAddress = IPv6Address(element)
    elif 'MagAddressIngress' in line:
        print line
        g_MagAddressIngress = IPv6Address(element)
    elif 'MagAddressEgress' in line:
        print line
        g_MagAddressEgress = IPv6Address(element)
    elif 'MagDeviceIngress' in line:
        print line
        g_MagDeviceIngress = element
    elif 'MagDeviceEgress' in line:
        print line
        g_MagDeviceEgress = element

command = "ifconfig " + g_MagDeviceIngress + " down"
print command
os.system(command)

command = "macchanger -m " +  g_RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks + " " + g_MagDeviceIngress
print command
os.system(command)

command = "ifconfig " + g_MagDeviceIngress + " up"
print command
os.system(command)

command = "ip -6 addr del " + g_MagAddressEgress.format() + "/64 dev " + g_MagDeviceEgress + " > /dev/null 2>&1"
print command
os.system(command)

command = "ip -6 addr del " + g_MagAddressIngress.format() + "/64 dev " + g_MagDeviceIngress + " > /dev/null 2>&1"
print command
os.system(command)


for i in range (1 , 255):
    command = "ip -6 tunnel del ip6tnl" + str(i) + " >/dev/null 2>&1"
    os.system(command)

command = "rmmod ip6_tunnel > /dev/null 2>&1"
print command
os.system(command)
command = "rmmod tunnel6 > /dev/null 2>&1"
print command
os.system(command)

command = "ip -6 addr add " + g_MagAddressEgress.format() + "/64 dev " + g_MagDeviceEgress
print command
os.system(command)

command = "ip -6 addr add " + g_MagAddressIngress.format() + "/64 dev " + g_MagDeviceIngress
print command
os.system(command)

command = "echo \"0\" > /proc/sys/net/ipv6/conf/all/accept_ra"
print command
os.system(command)
command = "echo \"0\" > /proc/sys/net/ipv6/conf/"+g_MagDeviceIngress+"/accept_ra"
print command
os.system(command)
command = "echo \"0\" > /proc/sys/net/ipv6/conf/"+g_MagDeviceEgress+"/accept_ra"
print command
os.system(command)
command = "echo \"1\" > /proc/sys/net/ipv6/conf/all/forwarding"
print command
os.system(command)

command = "ip -6 route add to default via " + g_LmaAddress.format() + " dev " + g_MagDeviceEgress
print command
os.system(command)

command = "modprobe ip6_tunnel"
print command
os.system(command)
command = "modprobe tunnel6"
print command
os.system(command)

command = "pkill -9 mip6d > /dev/null 2>&1"
print command
os.system(command)


# LD_LIBRARY_PATH for freeradius libs
command = 'export LD_LIBRARY_PATH=/usr/local/lib;/usr/local/sbin/mip6d -c ' + g_file_config
subprocess.call(command, shell=True)

