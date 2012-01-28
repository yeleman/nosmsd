#!/usr/bin/env python
# encoding=utf-8

# example user config file

NOSMSD_HANDLER = 'myapp.mymodule.my_function'
NOSMSD_GETTEXT = False
NOSMSD_GETTEXT_LOCALE = 'en_US.UTF-8'

NOSMSD_DATABASE = {'type': 'MySQL', 'name': 'gammu'}
NOSMSD_DATABASE_OPTIONS = {'user': 'gammu', 'passwd': 'gammu',
                           'host': 'localhost',
                           'use_unicode': True, 'charset': 'utf8'}

NOSMSD_USE_INJECT = False
NOSMSD_INJECT_PATH = '/usr/bin/gammu-smsd-inject'
