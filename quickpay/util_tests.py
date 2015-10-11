from datetime import datetime, date, timedelta
from nose.tools import assert_equal, assert_raises

from django import test
from django.test.client import Client

from utils import sign


class TestUtils(object):
    def test_checksum(self):
        params = dict(
            version      = "v10",
            merchant_id  = 1,
            agreement_id = 1,
            order_id     = "0001",
            amount       = 100,
            currency     = "DKK",
            continueurl = "http://shop.domain.tld/continue",
            cancelurl   = "http://shop.domain.tld/cancel",
            callbackurl = "http://shop.domain.tld/callback"
        )
        params['checksum'] = sign(params, "your_secret_agreement_api_key")

        assert_equal(
            '8f5122b7912dd76ac6e25395451a2fa682e0c9b0304126463466933f21ab6733',
            params['checksum']
        )
