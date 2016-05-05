#!/usr/bin/env python
# pylint:disable=C0111

from time import sleep
from datetime import datetime
from getopt import getopt, GetoptError
import sys


def usage():
    print "Usage: {}".format(sys.argv[0])
    print "     -d (--device=) : print device stats"
    print "     -h (--help)    : print help and exit"
    sys.exit(1)


def check_platform():
    if not sys.platform.startswith('linux'):
        sys.exit("-err: {} OS is unsupported".format(sys.platform))


def check_device(device):
    try:
        fname = "/sys/class/net/{0}/flags".format(device)
        f = open(fname, "r")
        f.close
    except IOError:
        sys.exit("-err: {} - no such device".format(device))


def print_header():
    fmt = "{:>15}{:<40}{:<40}"
    spec = ("", "RX:", "TX: ")
    print(fmt.format(*spec))

    fmt = "{:>15}\t{:>14}\t{:>3}\t{:>3}\t{:>14}\t{:>14}\t{:>3}\t{:>3}\t{:>14}"
    spec = ("bytes", "drp", "err", "pkts") * 2
    print(fmt.format("timestamp", *spec))


def get_interface_allstats(intf):
    ret = {}
    for stat in ("rx_bytes", "rx_dropped", "rx_errors", "rx_packets",
                 "tx_bytes", "tx_dropped", "tx_errors", "tx_packets"):
        fname = "/sys/class/net/{0}/statistics/{1}".format(intf, stat)
        ret[stat] = int(open(fname, "r").read().strip())
    return ret


def print_data(ts, stats):
    fmt = "{:>15}"
    fmt += "\t{rx_bytes:>14}\t{rx_dropped:>3}\t{rx_errors:>3}\t{rx_packets:>14}"
    fmt += "\t{tx_bytes:>14}\t{tx_dropped:>3}\t{tx_errors:>3}\t{tx_packets:>14}"
    print(fmt.format(ts, **stats))


def mainloop(device):
    try:
        while True:
            time = datetime.now().strftime("%H:%M:%S.%f")
            print_data(time, get_interface_allstats(intf=device))
            sleep(1)
    except KeyboardInterrupt:
        pass


def get_options():
    if len(sys.argv) == 1:
        usage()

    try:
        opts, args = getopt(sys.argv[1:], "hd:", ["device="])
        opts = opts or [("--help", "")]
    except GetoptError:
        usage()

    return (opts, args)



if __name__ == '__main__':
    check_platform()
    for opt, arg in get_options():
        if opt in ("-d", "--device"):
            check_device(device=arg)
            print_header()
            mainloop(device=arg)
        else:
            usage()
