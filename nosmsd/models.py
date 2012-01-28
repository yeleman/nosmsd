#!/usr/bin/env python
# encoding=utf-8

from django.db import models
from nosmsd.utils import send_sms

class Inbox(models.Model):

    class Meta:
        db_table = u'inbox'
        verbose_name = "Received Message"
        verbose_name_plural = "Received Messages"
        ordering = ['-receivingdatetime']

    STATUS_CREATED = 'created'
    STATUS_PROCESSED = 'processed'
    STATUS_ERROR = 'error'
    STATUSES = ((STATUS_CREATED, u"Created"),
                (STATUS_PROCESSED, u"Processed"),
                (STATUS_ERROR, u"Error"))

    PROC_TRUE = 'true'
    PROC_FALSE = 'false'
    PROCS = ((PROC_FALSE, False),
             (PROC_TRUE, True))

    NO_COMP = 'Default_No_Compression'
    NO_COMP_UNI = 'Unicode_No_Compression'
    HEIGHTB = '8bit'
    COMP = 'Default_Compression'
    COMP_UNI = 'Unicode_Compression'
    CODINGS = ((NO_COMP, u"Default No Compression"),
               (NO_COMP_UNI, u"Unicode No Compression"),
               (HEIGHTB, u"8bit"),
               (COMP, u"Default Compression"),
               (COMP_UNI, u"Unicode Compression"))
    DEFAULT_CODING = NO_COMP

    updatedindb = models.DateTimeField(db_column='UpdatedInDB')
    receivingdatetime = models.DateTimeField(db_column='ReceivingDateTime')
    text = models.TextField(db_column='Text')
    sendernumber = models.CharField(max_length=60, db_column='SenderNumber')
    coding = models.CharField(max_length=66, db_column='Coding',
                              choices=CODINGS, default=DEFAULT_CODING)
    udh = models.TextField(db_column='UDH')
    smscnumber = models.CharField(max_length=60, db_column='SMSCNumber')
    class_field = models.IntegerField(db_column='Class')
    textdecoded = models.TextField(db_column='TextDecoded')
    id = models.IntegerField(primary_key=True, db_column='ID')
    recipientid = models.TextField(db_column='RecipientID')
    processed = models.CharField(max_length=15,
                                 db_column='Processed', choices=PROCS)
    status = models.CharField(max_length=27, choices=STATUSES)

    def __unicode__(self):
        return self.textdecoded

    @property
    def identity(self):
        return self.sendernumber

    @property
    def date(self):
        return self.receivingdatetime

    def get_status_display(self):
        return self.status

    @property
    def content(self):
        return Inbox.multipart_text(self)

    @property
    def udh_root(self):
        if not self.udh:
            return ''
        return self.udh[:-2]

    @property
    def SequencePosition(self):
        try:
            return int(self.udh[-2:])
        except:
            return 0

    def is_multipart(self):
        return bool(len(self.udh))

    def parts(self):
        return Inbox.parts_from(self)

    @classmethod
    def parts_from(cls, message):
        parts = {}
        peers = Inbox.objects.filter(sendernumber=message.sendernumber,
                                     udh__contains=message.udh_root)
        for peer in peers:
            # UDH colision?
            if not peer.udh.startswith(message.udh_root):
                continue
            parts[peer.SequencePosition] = peer

        return parts

    @classmethod
    def multipart_text(cls, message):
        if message.is_multipart():
            return u''.join([p.textdecoded
                             for p in cls.parts_from(message).values()])
        return message.textdecoded

    def change_status(self, new_status, cascade=True):
        if not new_status in (self.STATUS_CREATED,
                              self.STATUS_PROCESSED,
                              self.STATUS_ERROR):
            return False
        if new_status == self.STATUS_CREATED:
            self.processed = self.PROC_FALSE
        else:
            self.processed = self.PROC_TRUE
        self.status = new_status
        self.save()
        if cascade and self.is_multipart():
            for part in self.parts():
                part.change_status(new_status, cascade=False)
        return True

    def mark_processed(self, cascade=True):
        self.change_status(self.STATUS_PROCESSED)

    def mark_error(self, cascade=True):
        self.change_status(self.STATUS_ERROR)

    def unmark_processed(self, cascade=True):
        self.change_status(self.STATUS_CREATED)

    @property
    def is_hw_processed(self):
        return self.processed == self.PROC_TRUE

    @property
    def is_processed(self):
        return self.status == self.STATUS_PROCESSED

    @property
    def is_error(self):
        return self.status == self.STATUS_ERROR

    def respond(self, text):
        return send_sms(self.sendernumber, text)

    @classmethod
    def from_id(cls, id_):
        return cls.objects.get(id=id_)

    @classmethod
    def from_identity(cls, ident):
        return cls.objects.filter(sendernumber=ident)


class SentItems(models.Model):

    class Meta:
        db_table = u'sentitems'
        verbose_name = "Sent Message"
        verbose_name_plural = "Sent Messages"
        ordering = ['-sendingdatetime']

    NO_COMP = 'Default_No_Compression'
    NO_COMP_UNI = 'Unicode_No_Compression'
    HEIGHTB = '8bit'
    COMP = 'Default_Compression'
    COMP_UNI = 'Unicode_Compression'
    CODINGS = ((NO_COMP, u"Default No Compression"),
               (NO_COMP_UNI, u"Unicode No Compression"),
               (HEIGHTB, u"8bit"),
               (COMP, u"Default Compression"),
               (COMP_UNI, u"Unicode Compression"))
    DEFAULT_CODING = NO_COMP

    STATUS_SENDING_OK = 'SendingOK'
    STATUS_SENDING_OK_NOREPORT = 'SendingOKNoReport'
    STATUS_SENDING_ERROR = 'SendingError'
    STATUS_DELIVERY_OK = 'DeliveryOK'
    STATUS_DELIVERY_FAILED = 'DeliveryFailed'
    STATUS_DELIVERY_PENDING = 'DeliveryPending'
    STATUS_DELIVERY_UNKNOWN = 'DeliveryUnknown'
    STATUS_ERROR = 'Error'
    STATUSES = ((STATUS_SENDING_OK, u"SendingOK"),
                (STATUS_SENDING_OK_NOREPORT, u"Sending OK NoReport"),
                (STATUS_SENDING_ERROR, u"Sending Error"),
                (STATUS_DELIVERY_OK, u"Delivery OK"),
                (STATUS_DELIVERY_FAILED, u"Delivery Failed"),
                (STATUS_DELIVERY_PENDING, u"Delivery Pending"),
                (STATUS_DELIVERY_UNKNOWN, u"Delivery Unknown"),
                (STATUS_ERROR, u"Error"))

    updatedindb = models.DateTimeField(db_column='UpdatedInDB')
    insertintodb = models.DateTimeField(db_column='InsertIntoDB')
    sendingdatetime = models.DateTimeField(db_column='SendingDateTime')
    deliverydatetime = models.DateTimeField(null=True,
                                            db_column='DeliveryDateTime',
                                            blank=True)
    text = models.TextField(db_column='Text')
    destinationnumber = models.CharField(max_length=60,
                                        db_column='DestinationNumber')
    coding = models.CharField(max_length=66, db_column='Coding',
                              choices=CODINGS, default=DEFAULT_CODING)
    udh = models.TextField(db_column='UDH')
    smscnumber = models.CharField(max_length=60, db_column='SMSCNumber')
    class_field = models.IntegerField(db_column='Class')
    textdecoded = models.TextField(db_column='TextDecoded')
    id = models.IntegerField(primary_key=True, db_column='ID')
    senderid = models.CharField(max_length=765, db_column='SenderID')
    sequenceposition = models.IntegerField(primary_key=True,
                                           db_column='SequencePosition')
    status = models.CharField(max_length=51,
                              db_column='Status', choices=STATUSES)
    statuserror = models.IntegerField(db_column='StatusError')
    tpmr = models.IntegerField(db_column='TPMR')
    relativevalidity = models.IntegerField(db_column='RelativeValidity')
    creatorid = models.TextField(db_column='CreatorID')

    def __unicode__(self):
        return self.textdecoded

    @property
    def identity(self):
        return self.destinationnumber

    @property
    def date(self):
        return self.sendingdatetime

    @property
    def content(self):
        return self.textdecoded

    def get_status_display(self):
        return self.status

    def total_parts(self):
        return SentItems.objects.filter(id=self.id).count()

    @property
    def sequence(self):
        return u"%d/%d" % (self.sequenceposition, self.total_parts())
