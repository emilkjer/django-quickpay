from hashlib import md5, sha256

import hmac


def request_md5check(data, secret):
    """
    Computes the MD5 signature for a quickpay request.
    """

    md5pieces = (
        data['protocol'],
        data['msgtype'],
        data['merchant'],
        data['language'],
        data['ordernumber'],
        data['amount'],
        data['currency'],
        data['continueurl'],
        data['cancelurl'],

        data.get('callbackurl', ''),
        data.get('autocapture', ''),
        data.get('autofee', ''),
        data.get('cardtypelock', ''),
        data.get('description', ''),
        data.get('group', ''),
        data.get('testmode', ''),
        data.get('splitpayment', ''),
        data.get('forcemobile', ''),
        data.get('deadline', ''),
        data.get('cardhash', ''),

        secret
    )

    md5string = ''.join([str(val) for val
        in md5pieces if val is not None])
    return md5(md5string).hexdigest()



def sign(params, api_key):
    '''Compute the checkum on ordered keys'''
    items = sorted(params.items(), key=lambda x: x[0])
    base = ' '.join([ str(pair[1]) for pair in items])

    return hmac.new(api_key, base, sha256).hexdigest()
