#!/usr/bin/python

import sys
from time import sleep

def calc(iface):
    tx_pkts = tx_bytes = rx_pkts = rx_bytes = 0
    base_path = '/sys/class/net/%s/statistics/' % iface
    for i in range(2):
        for file in ['rx_packets', 'tx_packets', 'rx_bytes', 'tx_bytes']:
            if 'tx_packets' in file:
                tx_pkts = int(open('%s/%s' % (base_path, file)).read().strip()) - tx_pkts
            elif 'tx_bytes' in file:
                tx_bytes = int(open('%s/%s' % (base_path, file)).read().strip()) - tx_bytes
            elif 'rx_packets' in file:
                rx_pkts = int(open('%s/%s' % (base_path, file)).read().strip()) - rx_pkts
            else:
                rx_bytes = int(open('%s/%s' % (base_path, file)).read().strip()) - rx_bytes
        sleep(1)
    return rx_pkts, tx_pkts, rx_bytes, tx_bytes

def main(argv):
    if len(argv) == 0:
            print 'Usage: netwatch interfaces'
            exit()
    else:
            while True:
            for iface in argv:
                rx_pkts, tx_pkts, rx_bytes, tx_bytes = calc(iface)
                print '%s rx: %d pkts/s, %d MB/s, tx: %d pkts/s, %d MB/s' % (iface, rx_pkts, ((rx_bytes/1024)/1024), tx_pkts, ((tx_bytes/1024)/1024))

if __name__ == '__main__':
    main(sys.argv[1:])
