#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import re
import urllib
import time
import logging
import logging.handlers
import random

from nosmsd.settings import settings as nosettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)


def import_path(name):
    """ import a callable from full module.callable name """
    modname, _, attr = name.rpartition('.')
    if not modname:
        # single module name
        return __import__(attr)
    m = __import__(modname, fromlist=[attr])
    return getattr(m, attr)


def send_sms(to, text):
    """ create arbitrary message for sending """
    m = {'identity': to, 'text': text}
    process(m)


def random_udh(length):
    """ random alnum string """
    return '050003' + hex(random.randint(0, 255))[2:].upper()


def msg_is_unicode(text):
    """ does this message needs to be sent as unicode ? """
    try:
        text.encode('ascii')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return True
    else:
        return False


def message_to_parts(message):
    """ converts text/identity dict to list of dict repr gammu parts """
    CODING_UNICODE = 'Unicode_No_Compression'
    CODING_DEFAULT = 'Default_No_Compression'
    MAX_LEN = 160
    UMAX_LEN = 70
    CREATOR = 'nosmsd'

    text = message['text']
    udh = random_udh(8)
    is_unicode = msg_is_unicode(text)
    length = text.__len__()
    first_part = {'DestinationNumber': message['identity'],
                  'Coding': '',
                  'TextDecoded': '',
                  'MultiPart': '',
                  'UDH': None,
                  'CreatorID': CREATOR}
    if not is_unicode and length <= MAX_LEN:
        # msg is short ascii text. create single
        first_part['Coding'] = CODING_DEFAULT
        first_part['TextDecoded'] = text
        first_part['MultiPart'] = 'false'
        return [first_part, ]
    elif is_unicode and length <= UMAX_LEN:
        # msg is short unicode. create single
        first_part['Coding'] = CODING_UNICODE
        first_part['TextDecoded'] = text
        first_part['MultiPart'] = 'false'
        return [first_part, ]
    else:
        # msg have to be multipart
        MAX_LEN = 153
        UMAX_LEN = 63
        first_part['MultiPart'] = 'true'

        # while it's possible to send parts of an SMS
        # with different encoding, most phone won't like it
        # and display according to first part encoding (and garbage the rest)
        if not nosettings.NOSMSD_MIX_ENCODING_PARTS:
            if msg_is_unicode(text):
                single_coding = CODING_UNICODE
                MAX_LEN = UMAX_LEN
            else:
                single_coding = CODING_DEFAULT
                UMAX_LEN = MAX_LEN

        # find out first part
        stub = text[:MAX_LEN]
        if not msg_is_unicode(stub):
            first_part['Coding'] = CODING_DEFAULT
            first_part['TextDecoded'] = stub
            parts_text = text[MAX_LEN:]
        else:
            first_part['Coding'] = CODING_UNICODE
            first_part['TextDecoded'] = text[:UMAX_LEN]
            parts_text = text[UMAX_LEN:]

        parts = []
        seq = 1
        while parts_text:
            # create part for each chunk
            seq += 1
            part = {'Coding': '', 'TextDecoded': '',
                    'SequencePosition': seq, 'UDH': udh}
            stub = parts_text[:MAX_LEN]
            if not msg_is_unicode(stub):
                part['Coding'] = CODING_DEFAULT
                part['TextDecoded'] = stub
                parts_text = parts_text[MAX_LEN:]
            else:
                part['Coding'] = CODING_UNICODE
                part['TextDecoded'] = parts_text[:UMAX_LEN]
                parts_text = parts_text[UMAX_LEN:]
            parts.append(part)

    all_parts = [first_part] + parts
    parts_num = all_parts.__len__()

    # adjust UDH for multipart
    for i in range(0, parts_num):
        all_parts[i]['UDH'] = '%s%s%s' \
                              % (udh,
                                 str(parts_num).zfill(2),
                                 str(i + 1).zfill(2))
        # harmonize Coding for all parts if required
        if not nosettings.NOSMSD_MIX_ENCODING_PARTS:
            all_parts[i]['Coding'] = single_coding

    return all_parts


def process_smsd(message):
    """ record message to gammu DB for sending.

    Will be sent as soon as gammu loops on it """

    from nosmsd.database import dbh, Outbox
    cursor = dbh.get_cursor()

    parts = message_to_parts(message)
    import pprint
    logger.debug(pprint.pformat(parts))

    # create message (first part)
    part = parts[0]
    cursor.execute("INSERT INTO outbox (DestinationNumber, Coding, " \
                   "TextDecoded, MultiPart, CreatorID, UDH) " \
                   "VALUES (%s, %s, %s, %s, %s, %s)",
                   [part['DestinationNumber'], part['Coding'],
                   part['TextDecoded'], part['MultiPart'],
                   part['CreatorID'], part['UDH']])
    dbh.commit()

    if parts.__len__() > 1:
        msg_id = dbh.last_insert_id(cursor, Outbox)
        logger.debug(u"MULTIPART with ID %d" % msg_id)

        for i in range(1, parts.__len__()):
            part = parts[i]
            cursor.execute("INSERT INTO outbox_multipart " \
                           "(ID, Coding, TextDecoded, " \
                           "SequencePosition, UDH) " \
                           "VALUES (%s, %s, %s, %s, %s)", [msg_id,
                           part['Coding'], part['TextDecoded'],
                           part['SequencePosition'], part['UDH']])
            dbh.commit()


def process(message):
    return process_smsd(message)
