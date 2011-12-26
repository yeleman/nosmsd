#!/usr/bin/env python
# encoding=utf-8

NOSMSD_HANDLER = 'nosmsd.handlers.printout'
NOSMSD_GETTEXT = True
NOSMSD_GETTEXT_LOCALE = 'fr_FR.UTF-8'

# whether a multipart SMS can have
# parts with different encoding.
# Numerous phones does not support this.
NOSMSD_MIX_ENCODING_PARTS = False

try:
    from .local_settings import *
except:
    pass

# create and fill dict with
# variables from settings and local_settings module.
dicko = {}
for var in dir():
    if var.startswith('__') or var == 'dicko':
        continue
    dicko[var] = eval(var)


class Options(dict, object):
    """ dumb dict store giving inst.var access to var property """

    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def __getattribute__(self, name):
        try:
            return self[name]
        except:
            return None

# instanciate and fill-up settings dict.
settings = Options(**dicko)
