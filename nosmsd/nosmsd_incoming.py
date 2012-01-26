#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
import locale
import time
import logging
from datetime import datetime, timedelta

from nosmsd.utils import import_path
from nosmsd.database import Inbox
from nosmsd.settings import settings as nosettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

if nosettings.NOSMSD_GETTEXT:
    locale.setlocale(locale.LC_ALL, nosettings.NOSMSD_GETTEXT_LOCALE)


def handle(*args, **options):

    # Message ID in DB is provided as first argument
    if len(args) != 2:
        logger.error(u"No message ID provided")
        sys.exit(1)
    try:
        sql_id = int(args[1])
    except:
        sql_id = None

    if not isinstance(sql_id, int):
        logger.error(u"Provided ID (%s) is not an int." % sql_id)
        sys.exit(1)

    # open up smsd DB
    try:
        message = Inbox.select().get(ID=sql_id, Processed=Inbox.PROC_FALSE)
    except Inbox.DoesNotExist:
        logger.warning(u"No unprocessed row in DB for ID %d" % sql_id)
        return False

    # process handler
    try:
        handler_func = import_path(nosettings.NOSMSD_HANDLER)
    except AttributeError:
        message.status = Inbox.STATUS_ERROR
        message.save()
        logger.error(u"NO SMS_HANDLER defined while receiving SMS")
    except Exception as e:
        message.status = Inbox.STATUS_ERROR
        message.save()
        logger.error(u"Unbale to call SMS_HANDLER with %r" % e)
    else:
        try:
            handler_func(message)
        except Exception as e:
            message.status = Inbox.STATUS_ERROR
            message.save()
            logger.error(u"SMS handler failed on %s with %r" \
                          % (message, e))

    message.status = Inbox.STATUS_PROCESSED
    message.Processed = Inbox.PROC_TRUE
    message.save()

if __name__ == '__main__':
    handle(*sys.argv)
