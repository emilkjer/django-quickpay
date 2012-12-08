from django.db import models
from django.utils.hashcompat import md5_constructor
from django.db.models.signals import post_save
from django.dispatch import receiver
import signals

class QuickpayTransaction(models.Model):
    msgtype = models.CharField(max_length=128)
    ordernumber = models.CharField(max_length=20)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=3)
    time = models.CharField(max_length=12)
    state = models.IntegerField()
    qpstat = models.CharField(max_length=3)
    qpstatmsg = models.CharField(max_length=512, blank=True)
    chstat = models.CharField(max_length=3)
    chstatmsg = models.CharField(max_length=512, blank=True)
    merchant = models.CharField(max_length=100)
    merchantemail = models.EmailField(max_length=256)
    transaction = models.CharField(max_length=32)
    cardtype = models.CharField(max_length=32, blank=True)
    cardnumber = models.CharField(max_length=32, blank=True)
    cardhash = models.CharField(max_length=53)
    cardexpire = models.CharField(max_length=4, blank=True)
    splitpayment = models.IntegerField()
    fraudprobability = models.CharField(max_length=10, blank=True)
    fraudremarks = models.CharField(max_length=512, blank=True)
    fraudreport = models.CharField(max_length=512, blank=True)
    fee = models.CharField(max_length=10, blank=True)
    md5check = models.CharField(max_length=32)

    def __unicode__(self):
        return self.ordernumber

    def is_success(self):
        return self.qpstat == '000'

    def is_fail(self):
        return not self.is_success()

    def is_valid(secret):
        md_input = ''.join((
            self.msgtype,
            self.ordernumber,
            str(self.amount),
            self.currency,
            self.time,
            str(self.state),
            self.qpstat,
            self.qpstatmsg,
            self.chstat,
            self.chstatmsg,
            self.merchant,
            self.merchantemail,
            self.transaction,
            self.cardtype,
            self.cardnumber,
            self.cardhash,
            self.cardexpire,
            self.splitpayment,
            self.fraudprobability,
            self.fraudremarks,
            self.fraudreport,
            self.fee,
            secret,
        ))

        return md5_constructor(md_input).hexdigest() == self.md5check

@receiver(post_save, sender=QuickpayTransaction, dispatch_uid='check_status')
def check_status(sender, instance, created, *a, **k):
    if not created:
        return
    elif instance.is_success():
        signals.payment_successful.send(sender=instance)
    else:
        signals.payment_failed.send(sender=instance)
