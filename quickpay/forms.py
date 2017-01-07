from django import forms
from django.conf import settings

from .utils import sign


class QuickpayForm(forms.Form):
    version = forms.CharField(widget=forms.HiddenInput, initial='v10')
    merchant_id = forms.CharField(widget=forms.HiddenInput)
    agreement_id = forms.CharField(widget=forms.HiddenInput)
    order_id = forms.CharField(widget=forms.HiddenInput)
    amount = forms.IntegerField(widget=forms.HiddenInput)
    # ISO 4217 - http://www.iso.org/iso/home/standards/currency_codes.htm
    currency = forms.CharField(widget=forms.HiddenInput, initial='DKK')
    continueurl = forms.URLField(widget=forms.HiddenInput)
    cancelurl = forms.URLField(widget=forms.HiddenInput)
    checksum = forms.CharField(widget=forms.HiddenInput)

    # Non required fields for
    callbackurl = forms.URLField(widget=forms.HiddenInput, required=False)
    language = forms.CharField(widget=forms.HiddenInput, initial=settings.LANGUAGE_CODE)
    autocapture = forms.IntegerField(widget=forms.HiddenInput, required=False)
    autofee = forms.IntegerField(widget=forms.HiddenInput, required=False)
    subscription = forms.IntegerField(widget=forms.HiddenInput, required=False)
    description = forms.CharField(widget=forms.HiddenInput, required=False, max_length=20)
    payment_methods = forms.CharField(widget=forms.HiddenInput, required=False)
    acquirer = forms.CharField(widget=forms.HiddenInput, required=False)
    branding_id = forms.CharField(widget=forms.HiddenInput, required=False)
    google_analytics_tracking_id = forms.CharField(widget=forms.HiddenInput, required=False)
    google_analytics_client_id = forms.CharField(widget=forms.HiddenInput, required=False)
    variables = forms.CharField(widget=forms.HiddenInput, required=False)
    deadline = forms.IntegerField(widget=forms.HiddenInput, required=False)
    text_on_statement = forms.CharField(widget=forms.HiddenInput, required=False)
    vat_amount = forms.IntegerField(widget=forms.HiddenInput, required=False)
    category = forms.CharField(widget=forms.HiddenInput, required=False)
    reference_title = forms.CharField(widget=forms.HiddenInput, required=False)
    product_id = forms.CharField(widget=forms.HiddenInput, required=False)
    customer_email = forms.EmailField(widget=forms.HiddenInput, required=False)

    # protocol = forms.IntegerField(widget=forms.HiddenInput, initial=6)
    # msgtype = forms.IntegerField(widget=forms.HiddenInput, initial='authorize')
    # cardtypelock = forms.CharField(widget=forms.HiddenInput, required=False)
    # group = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # testmode = forms.IntegerField(widget=forms.HiddenInput, initial=int(settings.DEBUG), required=False)
    # splitpayment = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # forcemobile = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # deadline = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # cardhash = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # md5check = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        secret = kwargs.pop('secret', None)
        super(QuickpayForm, self).__init__(*args, **kwargs)

        if secret:
            self.set_checksum(secret)


    def set_checksum(self, secret):
        # Compute HMAC with SHA256
        data = {x.name: x.value() if x.value() else '' for x in self}
        data.pop('checksum')
        self.fields['checksum'].initial = sign(data, secret)
