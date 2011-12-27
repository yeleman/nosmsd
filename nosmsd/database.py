#!/usr/bin/env python
# encoding=utf-8

import peewee

from nosmsd.settings import settings as nosettings
from nosmsd.utils import send_sms


def get_db_class(dbtype):
    return eval('peewee.%sDatabase' % dbtype)

db_adapter = get_db_class(nosettings.NOSMSD_DATABASE['type'])
dbh = db_adapter(nosettings.NOSMSD_DATABASE['name'],
                 **nosettings.NOSMSD_DATABASE_OPTIONS)


class BaseModel(peewee.Model):

    class Meta:
        database = dbh


class Inbox(BaseModel):

    class Meta:
        db_table = 'inbox'

    NO_COMP = 'Default_No_Compression'
    NO_COMP_UNI = 'Unicode_No_Compression'
    HEIGHTB = '8bit'
    COMP = 'Default_Compression'
    COMP_UNI = 'Unicode_Compression'
    CODINGS = (NO_COMP, NO_COMP_UNI, HEIGHTB, COMP, COMP_UNI)
    DEFAULT_CODING = NO_COMP

    STATUS_CREATED = 'created'
    STATUS_PROCESSED = 'processed'
    STATUS_ERROR = 'error'

    PROC_TRUE = 'true'
    PROC_FALSE = 'false'

    UpdatedInDB = peewee.DateTimeField()
    ReceivingDateTime = peewee.DateTimeField()
    Text = peewee.TextField()
    SenderNumber = peewee.CharField(max_length=20)
    Coding = peewee.CharField(max_length=50)
    UDH = peewee.TextField()
    SMSCNumber = peewee.CharField(max_length=20)
    Class = peewee.IntegerField()
    TextDecoded = peewee.TextField()
    ID = peewee.PrimaryKeyField()
    RecipientID = peewee.TextField()
    Processed = peewee.CharField(max_length=50)
    status = peewee.CharField(db_index=True, max_length=50)

    @property
    def content(self):
        return self.TextDecoded

    @property
    def identity(self):
        return self.SenderNumber

    @property
    def is_hw_processed(self):
        return self.Processed == PROC_TRUE

    @property
    def is_processed(self):
        return self.status == self.STATUS_PROCESSED

    @property
    def is_error(self):
        return self.status == self.STATUS_ERROR

    @property
    def id(self):
        return self.ID

    @property
    def date(self):
        return self.ReceivingDateTime

    def respond(self, text):
        return send_sms(self.SenderNumber, text)

    @classmethod
    def from_id(cls, id_):
        return cls.select().get(ID=id_)

    @classmethod
    def from_identity(cls, ident):
        return cls.select().Where(SenderNumber=ident)

    @classmethod
    def add(cls, sender, text):

        from nosmsd.utils import msg_is_unicode

        coding = cls.NO_COMP_UNI if msg_is_unicode(text) else cls.NO_COMP
        instance = cls(TextDecoded=text,
                       SenderNumber=sender,
                       status=cls.STATUS_CREATED,
                       Coding=coding,
                       Processed=Inbox.PROC_FALSE)
        instance.save()
        return instance


class Outbox(BaseModel):

    """ Do not use this model as it holds temporary data for gammu """

    class Meta:
        db_table = 'outbox'

    ID = peewee.PrimaryKeyField()


class SentItems(BaseModel):

    class Meta:
        db_table = 'sentitems'

    NO_COMP = 'Default_No_Compression'
    NO_COMP_UNI = 'Unicode_No_Compression'
    HEIGHTB = '8bit'
    COMP = 'Default_Compression'
    COMP_UNI = 'Unicode_Compression'
    CODINGS = (NO_COMP, NO_COMP_UNI, HEIGHTB, COMP, COMP_UNI)
    DEFAULT_CODING = NO_COMP

    STATUS_SENDING_OK = 'SendingOK'
    STATUS_SENDING_OK_NOREPORT = 'SendingOKNoReport'
    STATUS_SENDING_ERROR = 'SendingError'
    STATUS_DELIVERY_OK = 'DeliveryOK'
    STATUS_DELIVERY_FAILED = 'DeliveryFailed'
    STATUS_DELIVERY_PENDING = 'DeliveryPending'
    STATUS_DELIVERY_UNKNOWN = 'DeliveryUnknown'
    STATUS_ERROR = 'Error'

    UpdatedInDB = peewee.DateTimeField()
    InsertIntoDB = peewee.DateTimeField()
    SendingDateTime = peewee.DateTimeField()
    DeliveryDateTime = peewee.DateTimeField()
    Text = peewee.TextField()
    DestinationNumber = peewee.CharField(max_length=20)
    Coding = peewee.CharField()
    UDH = peewee.TextField()
    SMSCNumber = peewee.CharField(max_length=20)
    Class = peewee.IntegerField()
    TextDecoded = peewee.TextField()
    ID = peewee.PrimaryKeyField()
    SenderID = peewee.CharField(max_length=255)
    SequencePosition = peewee.PrimaryKeyField()
    Status = peewee.CharField()
    StatusError = peewee.IntegerField()
    TPMR = peewee.IntegerField()
    RelativeValidity = peewee.IntegerField()
    CreatorID = peewee.TextField()

    @property
    def content(self):
        return self.TextDecoded

    @property
    def identity(self):
        return self.DestinationNumber

    @property
    def is_error(self):
        return self.status == self.STATUS_ERROR

    @property
    def id(self):
        return self.ID

    @property
    def date(self):
        return self.SendingDateTime
