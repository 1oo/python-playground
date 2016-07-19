#!/usr/bin/python -u

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from socket import SOL_SOCKET, SO_KEEPALIVE
from socket import SOL_TCP, TCP_KEEPIDLE, TCP_KEEPCNT, TCP_KEEPINTVL

from time import sleep
from getopt import getopt, GetoptError
import sys, threading, traceback


def usage():
    print("Usage:")
    print("    ./socket_client.py [options]")
    print("Options:")
    print(" -a   --address=    server address")
    print(" -p   --port=       server port")
    print(" -u   --udp         use UDP rather than TCP")
    print(" -h   --help        view this message")
    exit(1)


def get_integer_stat(fname):
    fd = open(fname, 'r')
    retval = int(fd.read().strip())
    fd.close()
    return retval


def get_tcp_fin_timeout():
    fd = open('/proc/sys/net/ipv4/tcp_fin_timeout', 'r')
    retval = fd.read().strip()
    fd.close()
    return int(retval)


def prepare_socket(host, port, socket_type):
    s = socket(AF_INET, socket_type)
    if socket_type == SOCK_STREAM:
        s.settimeout(10)
        if 0 == s.getsockopt(SOL_SOCKET, SO_KEEPALIVE):
            # check and turn on TCP Keepalive
            s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
            # net.ipv4.tcp_keepalive_time
            s.setsockopt(SOL_TCP, TCP_KEEPIDLE, 15)
            # net.ipv4.tcp_keepalive_probes
            s.setsockopt(SOL_TCP, TCP_KEEPCNT, 2)
            # net.ipv4.tcp_keepalive_intvl
            s.setsockopt(SOL_TCP, TCP_KEEPINTVL, 10)
    s.connect((host, port))
    return s


def interact(s):
    fin_timeout = get_integer_stat('/proc/sys/net/ipv4/tcp_fin_timeout')
    try:
        while True:
            s.send('CAN_HAS_REPLY?')
            msg = s.recv(4096)
            if not msg:
                break
            sleep(fin_timeout / 2)
            s.send('AWSUM_THX')
    except Exception, e:
        print(traceback.format_exc())
    return


def run_client(address, port, socket_type):
    cln = prepare_socket(address, port, socket_type)
    interact(cln)
    return


def start_new_thread(thread_number, address, port, socket_type):
    try:
        thread = threading.Thread(name='thread-{}'.format(thread_number),
                                  target=run_client, args=(address, port, socket_type))
        thread.setDaemon(True)
        thread.start()
    except Exception, e:
        print(traceback.format_exc())
    return


def main(argv):
    try:
        shortopts = "a:p:t:uh:"
        longopts = ["address=", "port=", "threads=", "udp", "help"]
        opts, args = getopt(argv, shortopts, longopts)
    except GetoptError:
        usage()

    socket_type = SOCK_STREAM
    threads = 1

    for opt, arg in opts:
        if opt in ("-a", "--address"):
            address = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-u", "--udp"):
            socket_type = SOCK_DGRAM
        elif opt in ("-t", "--threads"):
            threads = int(arg)
        else:
            usage()

    try:
        max_threads = get_integer_stat('/proc/sys/kernel/threads-max')
        if threads > max_threads:
            msg = "Number of threads ({0}) is more than OS limit ({1})"
            sys.exit(msg.format(threads, max_threads))
        else:
            msg = "Connecting to {}:{}\n{} thread(s)"
            print (msg.format(address, port, threads))

        for n in xrange(1, threads + 1):
            print("start_new_thread: {} of {}".format(n, threads))
            start_new_thread(n, address, port, socket_type)

        # wait for the last thread to complete
        # using non-blocking calls to respect KeyboardInterrupt
        while threading.active_count() > 0:
            sleep(0.1)

    except KeyboardInterrupt:
        print("")
        print("Stopping...")


if __name__ == '__main__':
    main(sys.argv[1:])