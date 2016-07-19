#!/usr/bin/python -u

import sys, SocketServer
from getopt import getopt, GetoptError

from socket import SOL_SOCKET, SO_KEEPALIVE
from socket import SOL_TCP, TCP_KEEPIDLE, TCP_KEEPCNT, TCP_KEEPINTVL

CONN_TIMEOUT = 10
RECV_BUFFER = 4096


def usage():
    print("Usage:")
    print("    ./socket_server.py [options]")
    print("Options:")
    print(" -a   --address=    bind address, default is 0.0.0.0")
    print(" -p   --port=       server port to listen on, default is 13668")
    print(" -u   --udp         use UDP rather than TCP")
    print(" -h   --help        view this message")
    exit(1)


class TCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(CONN_TIMEOUT)
        print ("Client connected - {}".format(self.client_address))
        while True:
            try:
                data = self.request.recv(RECV_BUFFER)
                if not data:
                    break
                self.request.sendall('HELLO')
            except Exception, e:
                print(e)
        return


class UDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(CONN_TIMEOUT)
        print ("Client connected - ip: {}".format(self.client_address[0]))
        while True:
            try:
                data = self.request[0].strip()
                if not data:
                    break
                socket = self.request[1]
                socket.sendto('HELLO', self.client_address)
            except Exception, e:
                print(e)
        return


class TCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.socket.settimeout(CONN_TIMEOUT)
        if 0 == self.socket.getsockopt(SOL_SOCKET, SO_KEEPALIVE):
            self.socket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
            self.socket.setsockopt(SOL_TCP, TCP_KEEPIDLE, 15)
            self.socket.setsockopt(SOL_TCP, TCP_KEEPCNT, 2)
            self.socket.setsockopt(SOL_TCP, TCP_KEEPINTVL, 10)


class UDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass)
        self.socket.settimeout(CONN_TIMEOUT)


def main(argv):
    try:
        shortopts = "a:p:uh"
        longopts = ["address=", "port=", "udp", "help"]
        opts, args = getopt(argv, shortopts, longopts)
    except GetoptError:
        usage()

    # default options
    use_udp = False
    address = "0.0.0.0"
    port = 13666

    for opt, arg in opts:
        if opt in ("-a", "--address"):
            address = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-u", "--udp"):
            use_udp = True
        else:
            usage()

    if use_udp:
        server = UDPServer((address, port), UDPRequestHandler)
    else:
        server = TCPServer((address, port), TCPRequestHandler)

    try:
        print ("Started on port {}, ^C to stop".format(port))
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        print("")
        print("Stopping...")
        sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])