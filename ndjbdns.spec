Name:       ndjbdns
Version:    1.05.5
Release:    1%{?dist}
Summary:    New djbdns: usable djbdns

Group:      Applications/System
License:    GPLv2+
URL:        http://pjp.dgplug.org/djbdns/
Source0:    http://pjp.dgplug.org/djbdns/%{name}-%{version}.tar.gz

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  systemd-units
%endif

%if 0%{?fedora} == 16 || 0%{?fedora} == 17
Requires(post):     systemd-units
Requires(preun):    systemd-units
Requires(postun):   systemd-units
%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
Requires(post):     systemd-sysv
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%endif

%if 0%{?rhel} == 5 || 0%{?rhel} == 6
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service
%endif

%description
New djbdns: is a usable fork of djbdns. `djbdns' is a Domain Name System
originally written by the eminent author of Qmail, Dr D. J. Bernstein.
This *new* version of djbdns is a complete makeover to the original
source(djbdns-1.05) and is meant to make life a lot more pleasant. The
notable changes so far are in the set-up & configuration steps and
integration with the systemd(1) framework. This new release is free from
the clutches of `daemon-tools'. The original source is in public-domain
since late Dec 2007(see: http://cr.yp.to/distributors.html);


%prep
%setup -q %{name}


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%if 0%{?fedora} || 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
install -p -m 644 axfrdns.service $RPM_BUILD_ROOT/%{_unitdir}/
install -p -m 644 dnscache.service $RPM_BUILD_ROOT/%{_unitdir}/
install -p -m 644 tinydns.service $RPM_BUILD_ROOT/%{_unitdir}/
rm -r $RPM_BUILD_ROOT/%{_initrddir}/
%else
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
mv ndjbdns.logrotate $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/ndjbdns
%endif

%if 0%{?fedora} == 16 || 0%{?fedora} == 17

%post
if [ $1 -eq 1 ]; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
    /sbin/systemctl --no-reload disable axfrdns.service > /dev/null 2>&1 || :
    /sbin/systemctl stop axfrdns.service > /dev/null 2>&1 || :

    /sbin/systemctl --no-reload disable dnscache.service > /dev/null 2>&1 || :
    /sbin/systemctl stop dnscache.service > /dev/null 2>&1 || :

    /sbin/systemctl --no-reload disable tinydns.service > /dev/null 2>&1 || :
    /sbin/systemctl stop tinydns.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload > /dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart axfrdns.service > /dev/null 2>&1 || :
    /bin/systemctl try-restart dnscache.service > /dev/null 2>&1 || :
    /bin/systemctl try-restart tinydns.service > /dev/null 2>&1 || :
fi

%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7

%post
%systemd_post axfrdns.service
%systemd_post dnscache.service
%systemd_post tinydns.service

%preun
%systemd_preun axfrdns.service
%systemd_preun dnscache.service
%systemd_preun tinydns.service

%postun
%systemd_postun_with_restart axfrdns.service
%systemd_postun_with_restart dnscache.service
%systemd_postun_with_restart tinydns.service

%endif

%if 0%{?rhel} == 6 || 0%{?rhel} == 5

%post
#/sbin/chkconfig --add axfrdnsd
/sbin/chkconfig --add dnscached
#/sbin/chkconfig --add tinydnsd

%preun
if [ "$1" = 0 ]; then
    /sbin/service axfrdnsd stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del axfrdnsd

    /sbin/service dnscached stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del dnscached

    /sbin/service tinydnsd stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del tinydnsd
fi

%postun
if [ "$1" -ge "1" ]; then
    /sbin/service axfrdnsd restart > /dev/null 2>&1 || :
    /sbin/service dnscached restart > /dev/null 2>&1 || :
    /sbin/service tinydnsd restart > /dev/null 2>&1 || :
fi

%endif

%files
%doc README COPYING ChangeLog

%{_bindir}/axfrdns
%{_bindir}/axfr-get
%{_bindir}/dnscache
%{_bindir}/dnsfilter
%{_bindir}/dnsip
%{_bindir}/dnsipq
%{_bindir}/dnsname
%{_bindir}/dnsq
%{_bindir}/dnsqr
%{_bindir}/dnstrace
%{_bindir}/dnstracesort
%{_bindir}/dnstxt
%{_bindir}/randomip
%{_bindir}/tcprules
%{_bindir}/tinydns
%{_bindir}/tinydns-data
%{_bindir}/tinydns-edit
%{_bindir}/tinydns-get

%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/axfrdns.service
%{_unitdir}/dnscache.service
%{_unitdir}/tinydns.service
%else
%{_initrddir}/axfrdnsd
%{_initrddir}/dnscached
%{_initrddir}/tinydnsd
%config(noreplace) %{_sysconfdir}/logrotate.d/ndjbdns
%endif

%config(noreplace) %{_sysconfdir}/%{name}/ip/127.0.0.1
%config(noreplace) %{_sysconfdir}/%{name}/tinydns.conf
%config(noreplace) %{_sysconfdir}/%{name}/axfrdns.conf
%config(noreplace) %{_sysconfdir}/%{name}/servers/roots
%config(noreplace) %{_sysconfdir}/%{name}/dnscache.conf

%{_mandir}/man1/axfrdns.1.gz
%{_mandir}/man1/axfr-get.1.gz
%{_mandir}/man1/djbdns.1.gz
%{_mandir}/man1/dnscache.1.gz
%{_mandir}/man1/dnsfilter.1.gz
%{_mandir}/man1/dnsip.1.gz
%{_mandir}/man1/dnsipq.1.gz
%{_mandir}/man1/dnsname.1.gz
%{_mandir}/man1/dnsq.1.gz
%{_mandir}/man1/dnsqr.1.gz
%{_mandir}/man1/dnstrace.1.gz
%{_mandir}/man1/dnstxt.1.gz
%{_mandir}/man1/randomip.1.gz
%{_mandir}/man1/tcprules.1.gz
%{_mandir}/man1/tinydns.1.gz
%{_mandir}/man1/tinydns-data.1.gz
%{_mandir}/man1/tinydns-edit.1.gz
%{_mandir}/man1/tinydns-get.1.gz


%changelog
* Wed Dec 23 2012 pjp <pj.pandit@yahoo.co.in> - 1.05.5-1
- Applied patch to make SOA responses cache-able.
- Applied patch to merge identical outgoing requests.
- Applied patch to install Sys-V init scripts for RHEL and systemd
  unit files for latest fedora and RHEL-7 distributions.
  patch from: Simone Caronni <negativo17@gmail.com>

* Tue Mar 13 2012 pjp <pj.pandit@yahoo.co.in> - 1.05.4-9
- added logrotate configuration file /etc/logrotate.d/ndjbdns and a
  systemd service unit file: axfrdns.service.

* Mon Mar 12 2012 pjp <pj.pandit@yahoo.co.in> - 1.05.4-8
- listed individual files under _bindir and _mandir. Removed wild card: *.

* Sun Mar 11 2012 pjp <pj.pandit@yahoo.co.in> - 1.05.4-7
- added user manual for commands. Removed couple of commands.

* Fri Mar  2 2012 pjp <pj.pandit@yahoo.co.in> - 1.05.4-6
- renamed /etc/djbdns to /etc/ndjbdns; removed the clean section above.

* Tue Feb 28 2012 pjp <pj.pandit@yahoo.co.in> - 1.05.4-5
- removed SysV init scripts, replaced ./configure with the configure macro.

* Fri Feb 24 2012 pjp <pj.pandit@yahoo.co.in> - 1.05.4-4
- added systemd service unit files. Patch from Jose - jmalv04.

* Tue Jul 26 2011 pjp <pj.pandit@yahoo.co.in> - 1.05.4-3
- name changed to ndjbdns: New djbdns.

* Thu Apr  7 2011 pjp <pj.pandit@yahoo.co.in> - 1.05.4-2
- renamed default root server list from servers/@ to servers/roots.

* Thu Jan  6 2011 pjp <pj.pandit@yahoo.co.in> - 1.05.4-1
- init service script djbdns renamed to dnscached. and added a new service
  tinydnsd for DNS server.

* Wed Aug 19 2009 pjp <pj.pandit@yahoo.co.in> - 1.05.3-2
- Changes made to the build, install & files sections above, as indicated in
  the package review: https://bugzilla.redhat.com/show_bug.cgi?id=480724

* Sun Aug 16 2009 pjp <pj.pandit@yahoo.co.in> - 1.05.3-1
- A new release djbdns-1.05.3 of djbdns, includes tinydns and few more tools.

* Tue Mar 17 2009 pjp <pj.pandit@yahoo.co.in> - 1.05.2-1
- It's release 1 of new version 1.05.2 of djbdns.

* Fri Mar  6 2009 pjp <pj.pandit@yahoo.co.in> - 1.05.1-2
- changed README and the spec file to include reference to DJBs public-domain
  announcement at: http://cr.yp.to/distributors.html

* Thu Mar  5 2009 pjp <pj.pandit@yahoo.co.in> - 1.05.1-1
- Initial RPM release of djbdns-1.05.1
