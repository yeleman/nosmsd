#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

""" Injects an arbitrary message to Gammu Inbox Database and process it. """

import sys
import logging

from nosmsd.database import Inbox
from nosmsd.nosmsd_incoming import handle as nohandle
from nosmsd.settings import settings as nosettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)


def handle(*args, **options):

    # args format: (sender, text)
    if len(args) != 3:
        logger.error(u"Incorrect input.\nUsage: %s FROM TEXT" % args[0])
        sys.exit(1)

    # create message object in DB
    try:
        sender, text = args[1:]
        sender = sender.strip()
        text = text.strip()
        msg = Inbox.add(sender, text)

        logger.info("Added message as ID #%d" % msg.id)

        # launch message handler
        nohandle(args[0], msg.id)

    except Exception as e:
        logger.error(u"Unable to record message:\n%r" % e)
        sys.exit(1)

if __name__ == '__main__':
    handle(*sys.argv)
