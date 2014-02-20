#!/usr/bin/python
#http://packetlife.net/blog/2008/aug/4/eui-64-ipv6/

import sys

res = sys.argv[1]

if res == "" :
	print ("USE: convertMacToEui XX:XX:XX:XX:XX:XX")

octets= res.split(":")
eui64 = []
counter = 1

for i in octets: 
	if counter == 4:
		eui64.append("FF")
		eui64.append("FE")
		eui64.append(i)
	else:
		eui64.append(i)
	counter = counter + 1	

firstBinary =  int(eui64[0], 16) | 2
eui64[0]= hex(firstBinary)[2:].upper()

counter = 0
str = ""

for i in eui64:
	if counter < 2:
		str += i
		counter = counter + 1
	else:
		counter = 1
		str += ":"
		str += i
print eui64
print str
			 
