#!/usr/bin/env python
# encoding=utf-8

import sys
import site
import os
import imp

# try to find local settings to retrieve VENV path
for fpath in ['/etc/nosmsd.conf.py',
              os.path.expanduser('~/.nosmsd.conf.py'),
              os.path.expanduser('~/nosmsd.conf.py'),
              'nosmsd.conf.py']:
    try:
        imp.load_source('settings', fpath)
        break
    except (IOError, ImportError):
        continue
try:
    local_settings = __import__('settings')
    vepath = local_settings.NOSMSD_VENV_PATH
except ImportError:
    vepath = None

# exit if VENV path is not set or does not exist.
#vepath = nosettings.NOSMSD_VENV_PATH
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
