#!/usr/bin/env python

import sys
import grp
from daemon import runner
from pwd import getpwnam
from Metric import (
	init
    )

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/metricd.pid'
        self.pidfile_timeout = 5

    def run(self):
	while True:
		print 'hello'
		

app = App()
daemon_runner = runner.DaemonRunner(app)

# set user and group to run as
daemon_runner.daemon_context.uid = getpwnam('icinga').pw_uid
daemon_runner.daemon_context.gid = grp.getgrnam('icinga').gr_gid

# start the action
daemon_runner.do_action()
