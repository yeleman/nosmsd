#!/usr/bin/env python
# encoding=utf-8

# example user config file

NOSMSD_HANDLER = 'myapp.mymodule.my_function'
NOSMSD_GETTEXT = True
NOSMSD_GETTEXT_LOCALE = 'fr_FR.UTF-8'

NOSMSD_DATABASE = {'type': 'MySQL', 'name': 'gammu'}
NOSMSD_DATABASE_OPTIONS = {'user': 'gammu', 'passwd': 'gammu',
                           'host': 'localhost', 'use_unicode': True}
