#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from nosmsd.nosmsd_sendout import handle as nohandle


class Command(BaseCommand):

    def handle(self, *args, **options):

        translation.activate(settings.DEFAULT_LOCALE)

        args = (u"%s %s" % (sys.argv[0], u"nosmsd_sendout"),) + args
        nohandle(*args, DJANGO=True)

        translation.deactivate()
