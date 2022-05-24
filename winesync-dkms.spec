%global debug_package %{nil}
%global dkms_name winesync
%global winesync_commit 9ac10c6e711ec096274ecc676ae83a7cf2a1213f

Name:       %{dkms_name}-dkms
Version:    {{{ git_dir_version }}}
Release:    1%{?dist}
Summary:    DKMS module to add Winesync/Fastsync
License:    GPLv2+
URL:        https://github.com/KyleGospo/winesync-dkms

Source0:    https://repo.or.cz/linux/zf.git/blob_plain/%{winesync_commit}:/drivers/misc/winesync.c
Source1:    https://repo.or.cz/linux/zf.git/blob_plain/%{winesync_commit}:/include/uapi/linux/winesync.h
Source2:    Makefile
Source3:    dkms.conf

# Include patch:
Patch0:     winesync.patch

Provides:   %{dkms_name}-dkms = %{version}
Requires:   dkms

%description
Implements Winesync/Fastsync, a reimplementation of the NT syncrhonization primitives used by Wine.

%prep
%setup -q -T -c -n %{name}-%{version}
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} .
%patch0 -p0

%build

%install
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

install -d %{buildroot}%{_sysconfdir}/modules-load.d
cat > %{buildroot}%{_sysconfdir}/modules-load.d/winesync.conf << EOF
winesync
EOF

install -d %{buildroot}%{_sysconfdir}/udev/rules.d
cat > %{buildroot}%{_sysconfdir}/udev/rules.d/99-winesync.rules << EOF
KERNEL=="winesync", MODE="0644"
EOF

%post -n %{name}
if [ -S /run/udev/control ]; then
    udevadm control --reload
    udevadm trigger
fi
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%{_sysconfdir}/modules-load.d/winesync.conf
%{_sysconfdir}/udev/rules.d/99-winesync.rules
