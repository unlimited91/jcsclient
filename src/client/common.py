import base64
import time
import hmac
import os
import hashlib
import six
import sys

import urllib as ul
from six.moves import urllib

import config

# TODO(rushiagr): remove this HTTPRequest class, it's unnecessary bloat

class HTTPRequest(object):

    def __init__(self, method, host, params, headers):
        self.method = method
        self.host = host
        self.params = params
        # chunked Transfer-Encoding should act only on PUT request.
        self.headers = headers

    def __str__(self):
        return (('method:(%s) host(%s)' ' params(%s) headers(%s)') % (
                     self.method, self.host, self.params, self.headers))


class V2Handler(object):

    def __init__(self, host, service_name=None, region_name=None):
        # You can set the service_name and region_name to override the
        # values which would otherwise come from the endpoint, e.g.
        # <service>.<region>.amazonaws.com.
        self.host = host
        self.service_name = service_name
        self.region_name = region_name
        self.access_key = config.access_key
        self.secret_key = config.secret_key

    def add_params(self, req):
        req.params['AWSAccessKeyId'] = self.access_key
        req.params['SignatureVersion'] = '2'
        req.params['SignatureMethod'] = 'HmacSHA256'
        req.params['Version'] = '2016-03-01'
        req.params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @staticmethod
    def _get_utf8_value(value):
        """Get the UTF8-encoded version of a value."""
        if not isinstance(value, (six.binary_type, six.text_type)):
            value = str(value)
        if isinstance(value, six.text_type):
            return value.encode('utf-8')
        else:
            return value

    def sort_params(self, params):
        keys = params.keys()
        keys.sort()
        pairs = []
        for key in keys:
            val = V2Handler._get_utf8_value(params[key])
            val = urllib.parse.quote(val, safe='-_~')
            pairs.append(urllib.parse.quote(key, safe='') + '=' + val)
        qs = '&'.join(pairs)
        return qs

    def string_to_sign(self, req, method, host):
        ss = req.method + '\n' + req.host
	ss += "\n" + '/' + '\n'
        self.add_params(req)
        qs = self.sort_params(req.params)
        ss += qs
        return ss

    def add_auth(self, req, secret_key, method, host):
        hmac_256 = hmac.new(secret_key, digestmod=hashlib.sha256)
        canonical_string = self.string_to_sign(req, method, host)
        hmac_256.update(canonical_string.encode('utf-8'))
        b64 = base64.b64encode(hmac_256.digest()).decode('utf-8')
        req.params['Signature'] = ul.quote(b64)
        return req


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

    headers = {
        'User-Agent': 'curl/7.35.0',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'identity',
    }

    params = create_param_dict(request)

    reqObj = HTTPRequest('GET', host_or_ip, params, headers)
    authHandlerObj = V2Handler(host_or_ip)
    reqObj = authHandlerObj.add_auth(reqObj, config.secret_key, 'GET',
            host_or_ip)
    request_string = host_or_ip
    for keys in reqObj.params:
        request_string += keys + '=' + reqObj.params[keys] + '&'
    request_string = request_string[:-1]
    return request_type, request_string, headers

def main():
    print requestify(sys.argv[1])

if __name__ == '__main__':
    main()
