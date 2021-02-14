#!/usr/bin/python3

from os import system
from sys import argv

args = len(argv)
if args > 0:
    cmd = ''
    for i in range(1, args):
        if i < args-1:
            cmd += "{} ".format(argv[i])
        else:
            cmd += argv[i]
    system(cmd)
