#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import getopt

from subprocess  import *



try:
    opts, args = getopt.getopt(sys.argv[1:], "prd", [ "runversion=", "cfile="])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    sys.exit(2)

g_run_version = "1"

for o,p in opts:
  if o in ['-r','--runversion']:
     g_run_version = str(p)
  elif o in ['-c','--cfile']:
     g_config_file = p

############################################################################################
g_file_config=g_config_file
############################################################################################

print "Config file is : " + g_file_config

g_RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks = IPv6Address('0::0')
g_RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks = " "
g_LmaAddress                                      = IPv6Address('0::0')
g_LmaPmipNetworkDevice                            = ""
g_LmaCoreNetworkAddress                           = IPv6Address('0::0')
g_LmaCoreNetworkDevice                            = ""
g_MagAddressIngress                               = []
g_MagAddressEgress                                = []
g_num_mags                                        = 0

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
    if line.startswith("#"):
        continue
    if 'RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks' in line:
        print line
        g_RFC5213FixedMAGLinkLocalAddressOnAllAccessLinks = IPv6Address(element)

    elif 'RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks' in line:
        print line
        g_RFC5213FixedMAGLinkLayerAddressOnAllAccessLinks = element
    elif 'LmaPmipNetworkAddress' in line:
        print line
        g_LmaAddress = IPv6Address(element)
    elif 'LmaPmipNetworkDevice' in line:
        print line
        g_LmaPmipNetworkDevice = element
    elif 'LmaCoreNetworkAddress' in line:
        print line
        g_LmaCoreNetworkAddress = IPv6Address(element)
    elif 'LmaCoreNetworkDevice' in line:
        print line
        g_LmaCoreNetworkDevice = element
    elif 'MagAddressIngress' in line:
        print line
        g_MagAddressIngress.append(IPv6Address(element))
    elif 'MagAddressEgress' in line:
        print line
        g_MagAddressEgress.append(IPv6Address(element))

for ip in g_MagAddressIngress:
    if ip.format() != IPv6Address('0::0').format():
        command = "ip -6 route del " + ip.format() + "/64"
        print command
        os.system(command)
        g_num_mags = g_num_mags + 1


for i in range (1 , 255):
    command = "ip -6 tunnel del ip6tnl" + str(i) + " >/dev/null 2>&1"
    os.system(command)

command = "ip -6 addr del " + g_LmaAddress.format() + "/64 dev " + g_LmaPmipNetworkDevice
print command
os.system(command)

command = "rmmod ip6_tunnel"
print command
os.system(command)
command = "rmmod tunnel6"
print command
os.system(command)



command = "echo \"0\" > /proc/sys/net/ipv6/conf/all/accept_ra"
print command
os.system(command)
command = "echo \"0\" > /proc/sys/net/ipv6/conf/" + g_LmaPmipNetworkDevice + "/accept_ra"
print command
os.system(command)
command = "echo \"0\" > /proc/sys/net/ipv6/conf/" + g_LmaCoreNetworkDevice + "/accept_ra"
print command
os.system(command)
command = "echo \"1\" > /proc/sys/net/ipv6/conf/all/forwarding"
print command
os.system(command)



command = "ip -6 addr add " + g_LmaAddress.format() + "/64 dev " + g_LmaPmipNetworkDevice
print command
os.system(command)
command = "ip -6 addr add " + g_LmaCoreNetworkAddress.format()+"/64 dev "+ g_LmaCoreNetworkDevice
print command
os.system(command)

index = 0
for ip_ingress in g_MagAddressIngress:
    ip_egress = g_MagAddressEgress[index]
    if ip_ingress.format() != IPv6Address('0::0').format() and ip_egress.format() != IPv6Address('0::0').format():
        command = "ip -6 route add " + ip_ingress.format() + "/64 via " + ip_egress.format() + " dev " + g_LmaPmipNetworkDevice
        print command
        os.system(command)
    index += 1


command = "insmod ip6_tunnel"
print command
os.system(command)
command = "insmod tunnel6"
print command
os.system(command)

command = "pkill -9 mip6d"
print command
os.system(command)

# LD_LIBRARY_PATH for freeradius libs
command = 'export LD_LIBRARY_PATH=/usr/local/lib; mip6d -c ' + g_file_config
print command
subprocess.call(command, shell=True)

