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
        
            ip_str=self.ipv6
            if ip_str.find("::") >0:
                new_ip = []
                hextet = ip_str.split('::')
                sep = len(hextet[0].split(':')) + len(hextet[1].split(':'))
                new_ip = hextet[0].split(':')
    
                for _ in range(8 - sep):
                    new_ip.append('0000')
                new_ip += hextet[1].split(':')
    
                # Now need to make sure every hextet is 4 lower case characters.
                # If a hextet is < 4 characters, we've got missing leading 0's.
                ret_ip = []
                for hextet in new_ip:
                    ret_ip.append(('0' * (4 - len(hextet)) + hextet).lower())
                return ':'.join(ret_ip)
            # We've already got a longhand ip_str.
            return ip_str


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

command = "insmod ip6_tunnel"
print command
os.system(command)
command = "insmod tunnel6"
print command
os.system(command)

command = "pkill -9 mip6d > /dev/null 2>&1"
print command
os.system(command)


# LD_LIBRARY_PATH for freeradius libs
command = 'export LD_LIBRARY_PATH=/usr/local/lib; mip6d -c ' + g_file_config
subprocess.call(command, shell=True)

