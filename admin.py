#!/usr/bin/env python
# encoding=utf-8

from django.contrib import admin

from nosmsd.models import Inbox, SentItems


class InboxAdmin(admin.ModelAdmin):
    model = Inbox
    list_display = ('identity', 'date', \
                    'get_status_display', 'content')
    list_filter = ['coding', 'status', 'processed']
    search_fields = ['sendernumber', 'textdecoded']
    date_hierarchy = 'receivingdatetime'


class SentItemsAdmin(admin.ModelAdmin):
    model = SentItems
    list_display = ('identity', 'date', \
                    'get_status_display', 'sequence', 'id', 'content')
    list_filter = ['coding', 'status']
    search_fields = ['destinationnumber', 'textdecoded']
    date_hierarchy = 'sendingdatetime'

admin.site.register(Inbox, InboxAdmin)
admin.site.register(SentItems, SentItemsAdmin)
