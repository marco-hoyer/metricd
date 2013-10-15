%pre
# add service user and group
groupadd metricd 2> /dev/null || :
useradd -c "metricd" -s /sbin/nologin -r -d /etc/metricd -g metricd metricd 2> /dev/null || :