
Eurecom PMIPV6 integration in OpenWrt


Overview
--------


Supported Devices
-----------------

Being tested on a TpLink wdr 4300

  
What you need
------------------

To install opmip capabilities in your router you need to:

* Get an appropriate image for it.
* Compile the image with the OAI package
* Load this image to your device.
* Verify that everything works. 

 Build the OpenWrt Image
---------------

#### Building a vanilla image

It is strongly recommended that you build
and load a vanilla OpenWrt tree before adding any ODTONE-related functionality.

This release is based on the Attitude Adjustment OpenWrt release.

Install packages required by the OpenWrt buildsystem. (Instructions for Debian)

    apt-get install build-essential binutils flex bison autoconf gettext texinfo sharutils \
                subversion libncurses5-dev ncurses-term zlib1g-dev gawk git-core indent

Checkout and prepare Attitude Adjustment. For the rest of
this section we assume that `~/projects` is your working directory. 

    cd ~/projects
    git clone git://git.openwrt.org/12.09/openwrt.git
    cd openwrt
   
Configure Attitude Adjustment (select target system) and the packages

    make menuconfig

Compile a vanilla version of OpenWrt. The first compilation can take much time. The first compilation must download and configure the toolchain and the crosscompile environment.

	make

#### Change kernel settings
Now we need to make some changes to the kernel configurations.
	
	make kernel_menuconfig

And activate the following options:

	General setup 
		--> Prompt for development and/or incomplete code/drivers [CONFIG_EXPERIMENTAL]
		--> System V IPC [CONFIG_SYSVIPC]

		Networking support [CONFIG_NET]
		--> Networking options
		    --> Transformation user configuration interface [CONFIG_XFRM_USER]
		    --> Transformation sub policy support [CONFIG_XFRM_SUB_POLICY]
		    --> Transformation migrate database [CONFIG_XFRM_MIGRATE]
		    --> PF_KEY sockets [CONFIG_NET_KEY]
		    --> PF_KEY MIGRATE [CONFIG_NET_KEY_MIGRATE]
		    --> TCP/IP networking [CONFIG_INET]
		    --> The IPv6 protocol [CONFIG_IPV6]
			--> IPv6: AH transformation [CONFIG_INET6_AH]
			--> IPv6: ESP transformation [CONFIG_INET6_ESP]
			--> IPv6: IPComp transformation [CONFIG_INET6_IPCOMP]
			--> IPv6: Mobility [CONFIG_IPV6_MIP6]
			--> IPv6: IPsec transport mode [CONFIG_INET6_XFRM_MODE_TRANSPORT]
			--> IPv6: IPsec tunnel mode [CONFIG_INET6_XFRM_MODE_TUNNEL]
			--> IPv6: MIPv6 route optimization mode [CONFIG_INET6_XFRM_MODE_ROUTEOPTIMIZATION]
			--> IPv6: IP-in-IPv6 tunnel (RFC2473) [CONFIG_IPV6_TUNNEL]
			--> IPv6: Multiple Routing Tables [CONFIG_IPV6_MULTIPLE_TABLES]
			--> IPv6: source address based routing [CONFIG_IPV6_SUBTREES]

		File systems
		--> Pseudo filesystems
		    --> /proc file system support [CONFIG_PROC_FS]

Now compile the image with the changes:
    make


#### Add the OAI and the OAI-freeRadiusClient packages to the image

Add the OAI package to the list of avaialable packages:

    cd ~/projects
    git clone https://github.com/hugo-ma-alves/OAI-PMIPv6-OpenWrt.git
    cd ~/projects/openwrt/package/
    ln -s ~/projects/OAI-PMIPv6-OpenWrt/oai-pmip/

Add the OAI Free radius client to the list of avaialable packages.

    cd ~/projects
    git clone https://github.com/hugo-ma-alves/OAI-PMIPv6-OpenWrt.git
    cd ~/projects/openwrt/package/
    ln -s ~/projects/OAI-PMIPv6-freeRadiusClient/oai-freeradius/


Both packages are now under the network section. Select the oai-pmip
  
    make menuconfig
    

#### Build the final image
Finally build OpenWrt with OPMIP and ODTONE

    make V=s | tee make.log

If the compilation was sucessfull you now have a image with all the software required to use OAI.

Load the image to your device. All images can be found under
`~/projects/openwrt/bin/` After the device has rebooted make
sure that you can login. Typically, this can be done as following:

    Connect to one of the "LAN" ports, not the Internet port (if there is any).
    Give your PC IP address 192.168.1.10, netmask 255.255.255.0
    Try to ping the device at 192.168.1.1
    Login to the device using "telnet 192.168.1.1" 

You should see an OpenWrt welcome message.
Make sure that your pc have an ip in 192.168.1.x range. 
Immediately after logon change the root password:
      
      passwd

After changing the password logout and connect through ssh

      ssh root@192.168.1.1

Check if there is everything ok and exit.


Help 
-------------

Configure the PATH to use the gcc from the toolchain instead off the host gcc:

      http://wiki.openwrt.org/doc/devel/crosscompile
      
Build an individual package:

    make V=s package/oai-pmip/compile


## Loading the Image

There are different ways of loading the binary image to your device.
Please consult the related OpenWrt page and/or the OpenWrt info page
for your specific device for appropriate instructions.
For example the wiki for TpLink wdr4300
	http://wiki.openwrt.org/toh/tp-link/tl-wdr4300

Configuration
-------------

TODO





