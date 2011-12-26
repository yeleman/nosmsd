#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

""" Injects an arbitrary message to Gammu Outbox Database and process it. """

import sys
import logging

from nosmsd.settings import settings as nosettings
from nosmsd.utils import send_sms

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)


def add_to_database(*args, **options):
    """ args format: (sender, text) """

    if len(args) != 2:
        logger.error(u"Incorrect input. Usage is TO TEXT")
        return False

    dest, text = args
    dest = dest.strip()
    text = text.strip()

    return send_sms(dest, text)

if __name__ == '__main__':
    # create message object in DB
    try:
        add_to_database(*sys.argv[1:])
        logger.info("Added message to DB for Gammu processing")
    except Exception as e:
        logger.error(u"Unable to record message:\n%r" % e)
