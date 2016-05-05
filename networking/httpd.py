#!/usr/bin/env python2

from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer
from sys import argv


def start_server(port, handler=SimpleHTTPRequestHandler):
    http = TCPServer(("", port), handler)
    http.serve_forever()


def main():
    try:
        port = 8000
        if argv[1:]:
            port = int(argv[1])
        start_server(port)
    except ValueError:
        print "Invalid parameter. Usage: ./%s.py [port_number]" % argv[1]
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
