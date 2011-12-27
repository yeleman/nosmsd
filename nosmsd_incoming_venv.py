#!/usr/bin/env python
# encoding=utf-8

import sys
import site
import os

# import the settings.py file to be able to retrieve VENV path
import imp
try:
    imp.find_module('settings')  # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in " \
                     "the directory containing %r.\n" % __file__)
    sys.exit(1)
from settings import settings as nosettings

# exit if VENV path is not set or does not exist.
vepath = nosettings.NOSMSD_VENV_PATH
if not os.path.exists(unicode(vepath)):
    sys.stderr.write("Virtual Env not found: %r\n" % vepath)
    sys.exit(1)

prev_sys_path = list(sys.path)

# add the site-packages of our virtualenv as a site dir
site.addsitedir(vepath)

# reorder sys.path so new directories from the addsitedir show up first
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path

from nosmsd.nosmsd_incoming import handle

if __name__ == '__main__':
    handle(*sys.argv[1:])
