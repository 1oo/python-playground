#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE, check_output

try:
    from termcolor import colored
except ImportError:
    print ("termcolor module is required")
    sys.exit(1)


def colorize_whois_info(s):
    tokens = s.split(":", 1)
    tokens[0] = colored(tokens[0] + ":", "magenta", attrs=["bold"])
    return " ".join(tokens)


def colorize_stdout(s):
    if len(s) == 0:  # empty
        return s
    if s[0] in ("%", "#"):  # header
        return colored(s, "cyan")
    if s.find("Last update") >= 0:  # footer
        return colored(s, "yellow")
    # whois info
    return colorize_whois_info(s)


def mkoutput(out):
    try:
        print(out)
    except BrokenPipeError:
        pass


def main():
    cmd = ["whois"]
    if len(sys.argv) > 1:
        cmd += sys.argv[1:]

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    for i in out.decode("utf-8").splitlines():
        mkoutput(colorize_stdout(i))

    err = err.decode("utf-8")
    if len(err) > 0:
        mkoutput(colored(err, "red"))

if __name__ == "__main__":
    main()
