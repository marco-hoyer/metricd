# some useful vars
%define bin_dir         /opt/metricd
%define conf_dir        /etc/metricd
%define init_dir	/etc/init.d
%define log_dir         /data/logs/metricd
%define run_dir         /var/run

Name: metricd
Summary: A simple python daemon parsing icinga perfdata and redirecting them to graphite
Version: 1.1
Release: 8
License: GPL 
Group: is24
BuildArch: noarch
Buildroot: %{_tmppath}/%{name}-%{version}-root
Source0: target/dist/dist/metricd-%{version}-SNAPSHOT.tar.gz
Source1: metricd.init
Source2: logrotate
Vendor: Immobilien Scout GmbH
Packager:  $Id: %(date)

Requires: daemonize
Requires: python-argparse

%description
A simple python daemon parsing icinga perfdata and redirecting them to graphite

%prep
%setup -q

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/etc/logrotate.d
%{__mkdir} -p %{buildroot}%{bin_dir}
%{__mkdir} -p %{buildroot}%{conf_dir}
%{__mkdir} -p %{buildroot}%{init_dir}
%{__mkdir} -p %{buildroot}%{log_dir}
%{__mkdir} -p %{buildroot}%{run_dir}

# put binaries in there
%{__install} -m 0755 CarbonFormatter.py -D %{buildroot}%{bin_dir}
%{__install} -m 0755 IcingaParser.py -D %{buildroot}%{bin_dir}
%{__install} -m 0755 Metric.py -D %{buildroot}%{bin_dir}
%{__install} -m 0644 %SOURCE2 %{buildroot}/etc/logrotate.d/%{name}

# sample config
%{__install} -m 0775 metricd.conf.sample -D %{buildroot}%{conf_dir}

# init script
%{__install} -m 0775 %SOURCE1 -D %{buildroot}%{init_dir}/metricd

%files
%defattr(-,metricd,admins,0775)
%{bin_dir}
%{conf_dir}
%{init_dir}/metricd
%{log_dir}
/etc/logrotate.d/%{name}

%clean
%{__rm} -rf %{buildroot}

%pre
%{_sbindir}/groupadd metricd 2> /dev/null || :
%{_sbindir}/useradd -c "metricd" -s /sbin/nologin -r -d %{bin_dir} -g metricd metricd 2> /dev/null || :

%post
# create fifo named pipe for icinga perfdata
mkfifo /data/spool/icinga-perfdata || :
chown metricd:admins /data/spool/icinga-perfdata || :
chmod 777 /data/spool/icinga-perfdata || :
/sbin/chkconfig --add metricd

%changelog
* Wed Jun 19 2013 Thomas Lehmann <thomas.lehmann@immobilienscout24.de>
- added metricd to default runlevel
* Tue Jun 11 2013 Marco Hoyer <marco.hoyer@immobilienscout24.de>
- modified spec to let metricd run as user metricd
* Mon Jun 10 2013 Claudia Vogt <claudia.vogt@immobilienscout24.de>
- delete fucking shit
- useradd for icinga
* Fri Jun 07 2013 Claudia Vogt <claudia.vogt@immobilienscout24.de>
- add icinga user
* Fri Jun 07 2013 Claudia Vogt <claudia.vogt@immobilienscout24.de>
- add requirement icinga
* Mon Jun 03 2013 Marco Hoyer <marco.hoyer@immobilienscout24.de>
- added function-group to top of graphite target
- added lowercasing of graphite targets
* Fri May 31 2013 Marco Hoyer <marco.hoyer@immobilienscout24.de>
- initial release
