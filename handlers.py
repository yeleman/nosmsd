#!/usr/bin/env python
# encoding=utf-8


def printout(message):
    import pprint
    pprint.pprint(message)
    return True


def write_to_tmp(msg):
    f = open('/tmp/sms.txt', 'w')
    f.write(msg.content.encode('utf-8'))
    f.close()
    return True
