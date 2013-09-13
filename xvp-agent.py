#!/usr/bin/env python2

import sys
import getopt
import syslog
import ConfigParser
from subprocess import *
from supay import Daemon
from socket import getfqdn
from pyres.worker import Worker

queue_name = getfqdn()
syslog.openlog(sys.argv[0].split('/')[-1], syslog.LOG_PID, syslog.LOG_DAEMON)
config = ConfigParser.ConfigParser()
config.read('/etc/xvp-agent.cfg')

class XvpConsumer(object):
    queue = queue_name

    @staticmethod
    def perform(xvp_content):
        try:
            syslog.syslog('Writing XVP file')
            with open('/etc/xvp.conf', 'w') as file:
                file.write(xvp_content)
            syslog.syslog('Restarting XVP')
            cmd = Popen(['/etc/init.d/xvp', 'restart'], stdout=PIPE, stderr=PIPE)
            response = cmd.communicate()[0]
            syslog.syslog(response)
        except Exception as e:
            syslog.syslog('Error running XVP Consumer: %s' % e)

def main():
    Worker.run([queue_name], server=config.get('nephelae', 'resque_server'))

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:', ['action='])
    except getopt.GetoptError, err:
        print str(err)

    action = 'start'
    for o, a in opts:
        if o in ('-a', '--action'):
            action = a

    daemon = Daemon(name='xvp-agent', catch_all_log='/var/log/xvp-agent.log')
    if action == 'start':
        daemon.start()
        main()
    elif action == 'status':
        daemon.status()
    elif action == 'stop':
        daemon.stop()
    elif action == 'foreground':
        main()
