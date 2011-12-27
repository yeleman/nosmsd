#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import translation

from nosmsd.nosmsd_incoming import handle as nohandle


class Command(BaseCommand):

    def handle(self, *args, **options):

        translation.activate(settings.DEFAULT_LOCALE)

        nohandle(*args, DJANGO=True)

        translation.deactivate()
