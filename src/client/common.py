import base64
import time
import hmac
import os
import hashlib
import six
import sys

import json
import requests
from six.moves import urllib
import urllib as ul
import xmltodict

import config

common_params_v2 = {
    'AWSAccessKeyId': config.access_key,
    'SignatureVersion': '2',
    'SignatureMethod': 'HmacSHA256',
    'Version': '2016-03-01',
    'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}

common_headers = {
    # 'User-Agent': 'curl/7.35.0', # not required I guess
    'Content-Type': 'application/json',
    'Accept-Encoding': 'identity',
}

def _get_utf8_value(value):
    """Get the UTF8-encoded version of a value."""
    if not isinstance(value, (six.binary_type, six.text_type)):
        value = str(value)
    if isinstance(value, six.text_type):
        return value.encode('utf-8')
    else:
        return value

def get_query_string_from_params(params):
    keys = params.keys()
    keys.sort()
    pairs = []
    for key in keys:
        val = _get_utf8_value(params[key])
        val = urllib.parse.quote(val, safe='-_~')
        pairs.append(urllib.parse.quote(key, safe='') + '=' + val)
    qs = '&'.join(pairs)
    return qs

def string_to_sign(method, host, params):
    ss = method + '\n' + host + '\n' + '/' + '\n'
    params.update(common_params_v2)
    qs = get_query_string_from_params(params)
    ss += qs
    return ss

def get_signature(method, host, params):
    hmac_256 = hmac.new(config.secret_key, digestmod=hashlib.sha256)
    canonical_string = string_to_sign(method, host, params)
    hmac_256.update(canonical_string.encode('utf-8'))
    b64 = base64.b64encode(hmac_256.digest()).decode('utf-8')
    return ul.quote(b64)

def create_param_dict(string):
    params = {}
    length = len(string)
    parts = string.split('&')
    for p in parts:
        (key, val) = p.split('=')
        params[key] = val
    return params

def requestify(host_or_ip, request):
    """
    Method which generates final request URL to be sent to JCS servers.

    Input:
        host_or_ip: e.g. 'http://12.34.56.78'
        request: e.g. 'Action=DescribeInstances&key1=val1&key2=val2'

    Response: Request URL. e.g.  'https://<ip>/?<query-params>'
    """

    if not host_or_ip.endswith('/'):
        host_or_ip += '/'
    host_or_ip += '?'

    params = create_param_dict(request)

    params['Signature'] = get_signature('GET', host_or_ip, params)
    request_string = host_or_ip
    for key, value in params.items():
        request_string += key + '=' + value + '&'
    request_string = request_string[:-1]  # remove last '&'
    return request_string

def do_request(method, url, headers=None):
    """
    Performs HTTP request, and returns response as an ordered dict.

    Method can be 'GET' (string).
    url is also a string.
    headers is a dictionary.
    """
    current_headers = common_headers.copy()

    if headers is not None:
        current_headers.update(headers)

    if method == 'GET':
        resp = requests.get(url, headers=current_headers)
        if resp.status_code >= 400:
            print 'Exception %s thrown!!!' % resp.status_code
            print 'Error: ', resp.content
            raise Exception
        xml = resp.content()
        resp_ordereddict = xmltodict.parse(xml)
        # Ordered dict is difficult to read when printed, and we don't need an
        # order anyway, so just convert it to a normal dictionary
        # NOTE(rushiagr): the dictionary still contains 'items' keys, so either
        # document that, or remove them
        resp_dict = json.loads(json.dumps(resp_ordereddict))
        return resp_dict
    else:
        raise NotImplementedError

def main():
    print requestify(config.compute_url, sys.argv[1])

if __name__ == '__main__':
    main()
