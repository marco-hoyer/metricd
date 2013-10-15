#!/bin/bash
# create fifo named pipe for icinga perfdata
mkfifo /var/spool/icinga-perfdata || :
chown metricd:admins /var/spool/icinga-perfdata || :
chmod 777 /var/spool/icinga-perfdata || :
# set autostart
/sbin/chkconfig --add metricd