

include $(TOPDIR)/rules.mk

PKG_NAME_SHORT:=oai-pmip
PKG_NAME:=$(PKG_NAME_SHORT)
PKG_VERSION:=0.4.1

PKG_SOURCE:=umip-428974c.tar.gz
PKG_SOURCE_URL:= https://dl.dropboxusercontent.com/u/4108237
PKG_BUILD_DIR:=$(BUILD_DIR)/umip-428974c

include $(INCLUDE_DIR)/package.mk

define Package/oai-pmip
  SECTION:=net
  CATEGORY:=Network
  URL:=https://github.com/hugo-ma-alves/OAI-PMIPv6-OpenWrt && http://umip.org/contrib/umip-oai-pmipv6.html
  DEPENDS:= +libpcap +oai-freeradius-client +libpthread +libopenssl +macchanger +python-mini +syslogd +libpcap
  PKG_BUILD_DEPENDS:= +oai-freeradius-client +libpcap
  TITLE:=oai-pmip 
endef

define Package/oai-pmip/description
 This package contains the Eurecom implementation of Proxy Mobile IPV6
endef

define Package/Prepare
	$(call Build/Prepare/Default)
endef

define Build/Compile
	
	
	+( cd $(PKG_BUILD_DIR); \
		AR=$(GNU_TARGET_NAME)-ar \
		LD=$(GNU_TARGET_NAME)-ld \
		NM=$(GNU_TARGET_NAME)-nm \
		CC=$(GNU_TARGET_NAME)-gcc \
		GCC=$(GNU_TARGET_NAME)-gcc \
		CXX=$(GNU_TARGET_NAME)-g++ \
		RANLIB=$(GNU_TARGET_NAME)-ranlib \
		STRIP=$(GNU_TARGET_NAME)-strip \
		OBJCOPY=$(GNU_TARGET_NAME)-objcopy \
		autoreconf -i ;\
		./configure $(CONFIGURE_ARGS) --enable-vt --with-pmip-use-radius; \
		make ;\
	)
endef

define Package/oai-pmip/install
	
	$(INSTALL_DIR) $(1)/sbin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/src/mip6d $(1)/sbin/

	$(INSTALL_DIR) $(1)/etc/oai-pmip
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/extras/example-cn.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/extras/example-ha.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/extras/example-ha-lma.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/extras/example-mag1.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/extras/example-mag2.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/extras/example-mn.conf $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/extras/UMIP0.4_LMA_UBUNTU.10.04.py $(1)/etc/oai-pmip/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/extras/UMIP0.4_MAG_UBUNTU.10.04.py $(1)/etc/oai-pmip/

endef

$(eval $(call BuildPackage,oai-pmip))
