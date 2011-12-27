#!/usr/bin/env python
# encoding=utf-8

# dummy examples of handlers.
# message is a database.Inbox message with the following (notable) fields:
#   - date
#   - content
#   - identity (the sender number
#   - status
#   - respond(text) method to reply directly.


def printout(message):
    import pprint
    pprint.pprint(message)
    return True


def write_to_tmp(message):
    f = open('/tmp/sms.txt', 'w')
    f.write(u"From: %s\nContent: %s\n" % (message.identity.encode('utf-8'),
                                          message.content.encode('utf-8')))
    f.close()
    return True


def echo(message):
    message.respond(message.content)
    return True
