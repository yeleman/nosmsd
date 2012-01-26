#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

DATABASE = 'smsd'


class NoSMSdRouter(object):

    def allow_syncdb(self, db, model):
        if model._meta.app_label == 'nosmsd':
            return False
        return None

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'nosmsd':
            return DATABASE
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'nosmsd':
            return DATABASE
        return None