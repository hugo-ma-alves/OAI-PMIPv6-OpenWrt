

include $(TOPDIR)/rules.mk

PKG_NAME_SHORT:=oai-pmip
PKG_NAME:=$(PKG_NAME_SHORT)
PKG_VERSION:=0.4.1

PKG_SOURCE:=PMIPv6_v0.4.1.tar.bz2
PKG_SOURCE_URL:= http://www.openairinterface.org/openairfiles/documents//PMIPv6/PMIPv6_V0.4.1/
PKG_BUILD_DIR:=$(BUILD_DIR)/PMIPv6_v0.4.1

include $(INCLUDE_DIR)/package.mk

define Package/oai-pmip
  SECTION:=net
  CATEGORY:=Network
  URL:=https://github.com/hugo-ma-alves/OAI-PMIPv6-OpenWrt && http://www.openairinterface.org/openairinterface-proxy-mobile-ipv6-oai-pmipv6
  DEPENDS:= +libpcap +libpthread 
  TITLE:=oai-pmip 
endef

define Package/oai-pmip/description
 This package contains the Eurecom implementation of Proxy Mobile IPV6
endef

define Package/Prepare
	$(call Build/Prepare/Default)
endef

define Build/Compile
	+( cd $(PKG_BUILD_DIR)/freeradius-client-1.1.6; \
		AR=$(GNU_TARGET_NAME)-ar \
		LD=$(GNU_TARGET_NAME)-ld \
		NM=$(GNU_TARGET_NAME)-nm \
		CC=$(GNU_TARGET_NAME)-gcc \
		GCC=$(GNU_TARGET_NAME)-gcc \
		CXX=$(GNU_TARGET_NAME)-g++ \
		RANLIB=$(GNU_TARGET_NAME)-ranlib \
		STRIP=$(GNU_TARGET_NAME)-strip \
		OBJCOPY=$(GNU_TARGET_NAME)-objcopy \
		autoreconf -i  ; \
		./configure $(CONFIGURE_ARGS); \
		make; \
	)
	$(CP) $(PKG_BUILD_DIR)/freeradius-client-1.1.6/lib/.libs/libfreeradius-client.a $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/libmissing
	$(CP) $(PKG_BUILD_DIR)/freeradius-client-1.1.6/include/freeradius-client.h $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/include

	+( cd $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4; \
		AR=$(GNU_TARGET_NAME)-ar \
		LD=$(GNU_TARGET_NAME)-ld \
		NM=$(GNU_TARGET_NAME)-nm \
		CC=$(GNU_TARGET_NAME)-gcc \
		GCC=$(GNU_TARGET_NAME)-gcc \
		CXX=$(GNU_TARGET_NAME)-g++ \
		RANLIB=$(GNU_TARGET_NAME)-ranlib \
		STRIP=$(GNU_TARGET_NAME)-strip \
		OBJCOPY=$(GNU_TARGET_NAME)-objcopy \
		autoreconf -i  ; \
		./configure $(CONFIGURE_ARGS); \
		make; \
	)
endef

define Package/oai-pmip/install
	
	$(INSTALL_DIR) $(1)/sbin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/src/pmip6d $(1)/sbin/

	$(INSTALL_DIR) $(1)/etc/oai-pmip
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/example-cn.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/example-ha.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/example-lma.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/example-mag1.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/example-mag2.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/example-mn.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/UMIP0.4_LMA_UBUNTU.10.04.py $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/UMIP0.4_MAG1_UBUNTU.10.04.py $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/pmipv6-daemon-umip-0.4/extras/UMIP0.4_MAG2_UBUNTU.10.04.py $(1)/etc/oai-pmip/





endef

$(eval $(call BuildPackage,oai-pmip))
