#!/bin/bash
# create fifo named pipe for icinga perfdata
mkfifo /var/spool/icinga-perfdata || :
chown metricd:admins /var/spool/icinga-perfdata || :
chmod 777 /var/spool/icinga-perfdata || :
# set autostart
/sbin/chkconfig --add metricd

# always restart metricd if it was running
if service metricd status > /dev/null 2>&1; then
        echo "Restarting metricd service because it was running."
        if ! service metricd restart ; then
                logger -p user.err -s -t metricd -- "ERROR: Could not restart metricd service." 
                exit 0
        fi
fi