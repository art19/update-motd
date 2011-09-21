Name:       update-motd
Version:    1.0
Release:    1%{?dist}
License:    ASL 2.0
Summary:    Framework for dynamically generating MOTD
Group:      System Environment/Base
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
Requires:   bash coreutils
Requires:   upstart

Source0:    sbin_update-motd
Source1:    cron_update-motd
Source2:    upstart_update-motd.conf
Source3:    yum_update-motd.py
Source4:    yum_update-motd.conf

%description
Framework and scripts for producing a dynamically generated Message Of The Day. 
Based on and compatible with the framework implemented Ubuntu.

%install
rm -rf %{buildroot}
install -d %{buildroot}/etc/update-motd.d
install -D -m 0755 %{SOURCE0} %{buildroot}/usr/sbin/update-motd
install -D -m 0755 %{SOURCE1} %{buildroot}/etc/cron.daily/update-motd
install -D -m 0444 %{SOURCE2} %{buildroot}/etc/init/update-motd.conf
install -D -m 0444 %{SOURCE3} %{buildroot}/usr/lib/yum-plugins/update-motd.py
install -D -m 0444 %{SOURCE4} %{buildroot}/etc/yum/pluginconf.d/update-motd.conf
# for %ghost
install -d %{buildroot}/var/lib/update-motd
touch %{buildroot}/var/lib/update-motd/motd

%clean
rm -rf %{buildroot}

%post
# Only run this on initial install
if [ "$1" = "1" ]; then
    # Backup the current MOTD
    if [ -e /etc/motd ] && [ "$(readlink /etc/motd)" != "/var/lib/update-motd/motd" ]; then
        mv /etc/motd /etc/motd.rpmsave
        # And let it be the MOTD until update-motd gets run
        cp -L /etc/motd.rpmsave /var/lib/update-motd/motd
    fi
    ln -snf /var/lib/update-motd/motd /etc/motd
elif [ "$1" = "2" ]; then
    if [ -e /etc/motd ] && [ "$(readlink /etc/motd)" = "/var/run/motd" ]; then
        ln -snf /var/lib/update-motd/motd /etc/motd
    fi
fi
# We don't run update-motd on install because the various update-motd.d scripts
# are not installed yet (since their packages will depend on this one).
# This could also be the case in an upgrade situation, so we leave it to cron.

%files
%defattr(-,root,root,-)
%dir /etc/update-motd.d
%dir /var/lib/update-motd
%config /etc/cron.daily/update-motd
%config /etc/init/update-motd.conf
%config /etc/yum/pluginconf.d/update-motd.conf
/usr/sbin/update-motd
/usr/lib/yum-plugins/update-motd.py*
%ghost /var/lib/update-motd/motd

%changelog
