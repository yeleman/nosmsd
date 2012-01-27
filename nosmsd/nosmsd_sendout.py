#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

""" Injects an arbitrary message to Gammu Outbox Database and process it. """

import sys
import logging

from nosmsd.utils import send_sms

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)


def handle(*args, **options):

    # args format: (sender, text)
    if len(args) != 3:
        logger.error(u"Incorrect input.\nUsage: %s TO TEXT" % args[0])
        sys.exit(1)

    try:
        dest, text = args[1:]
        dest = dest.strip()
        text = text.strip()

        # create message object in DB
        send_sms(dest, text)

        logger.info("Added message to DB for Gammu processing")

    except Exception as e:
        logger.error(u"Unable to record message:\n%r" % e)
        sys.exit(1)

if __name__ == '__main__':
    handle(*sys.argv)
