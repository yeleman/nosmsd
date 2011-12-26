#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

""" Injects an arbitrary message to Gammu Inbox Database and process it. """

import sys
import logging

from nosmsd.settings import settings as nosettings
from nosmsd.database import Inbox
from nosmsd.nosmsd_incoming import handle as nohandle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)


def add_to_database(*args, **options):
    """ args format: (sender, text) """

    if len(args) != 2:
        logger.error(u"Incorrect input. Usage is FROM TEXT")
        return False

    sender, text = args
    sender = sender.strip()
    text = text.strip()

    return Inbox.add(sender, text)

if __name__ == '__main__':
    # create message object in DB
    try:
        msg = add_to_database(*sys.argv[1:])
        logger.info("Added message as ID #%d" % msg.id)
        # launch message handler
        nohandle(msg.id)
    except Exception as e:
        logger.error(u"Unable to record message:\n%r" % e)
