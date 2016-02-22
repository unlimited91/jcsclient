import base64
import time
import hmac
import os
import hashlib
import six
import sys

import urllib as ul
import requests
from six.moves import urllib
import xmltodict

import config

common_params_v2 = {
    'AWSAccessKeyId': config.access_key,
    'SignatureVersion': '2',
    'SignatureMethod': 'HmacSHA256',
    'Version': '2016-03-01',
    'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}

headers = {
    'User-Agent': 'curl/7.35.0',
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
    Primary method which generates final request URL to be sent to JCS servers.

    Input:
        host_or_ip: e.g. 'http://12.34.56.78'
        request: e.g. 'Action=DescribeInstances&key1=val1&key2=val2'

    Return value is a 3-tuple.
        First index: request type as a string: 'GET' or 'POST'
        Second index: Request URL. e.g.  'https://<ip>/?<other-details>'
        Third index: headers, as a dictionary
    """
    request_type = 'GET'

    if not host_or_ip.endswith('/'):
        host_or_ip += '/'
    host_or_ip += '?'

    params = create_param_dict(request)

    params['Signature'] = get_signature('GET', host_or_ip, params)
    request_string = host_or_ip
    for key, value in params.items():
        request_string += key + '=' + value + '&'
    request_string = request_string[:-1]  # remove last '&'
    return request_type, request_string, headers

def do_request(method, url, headers=None):
    """Performs HTTP request, and returns response as an ordered dict."""
    if method == 'GET':
        resp = requests.get(url)
        xml = resp.content()
        return xmltodict.parse(xml)
    else:
        raise NotImplementedError

def main():
    print requestify(config.compute_url, sys.argv[1])

if __name__ == '__main__':
    main()
