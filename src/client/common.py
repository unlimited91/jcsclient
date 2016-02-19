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

class HTTPRequest(object):

    def __init__(self, method, protocol, host, port, path, auth_path,
                 params, headers, body):
        self.method = method
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path = path
        if auth_path is None:
            auth_path = path
        self.auth_path = auth_path
        self.params = params
        # chunked Transfer-Encoding should act only on PUT request.
        self.headers = headers
        self.body = body

    def __str__(self):
        return (('method:(%s) protocol:(%s) host(%s) port(%s) path(%s) auth_path(%s)'
                 ' params(%s) headers(%s) body(%s)') % (self.method,
                 self.protocol, self.host, self.port, self.path, self.auth_path, self.params,
                 self.headers, self.body))


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

    def string_to_sign(self, req):
        ss = req.method + '\n' + req.host
	if req.port != 443:
        	ss += ":" + str(req.port)
	ss += "\n" + req.path + '\n'
        self.add_params(req)
        qs = self.sort_params(req.params)
        ss += qs
        return ss

    def add_auth(self, req):
        hmac_256 = hmac.new(self.secret_key, digestmod=hashlib.sha256)
        canonical_string = self.string_to_sign(req)
        hmac_256.update(canonical_string.encode('utf-8'))
        b64 = base64.b64encode(hmac_256.digest()).decode('utf-8')
        req.params['Signature'] = ul.quote(b64)
        return req



method = 'GET'

params = {}

def add_params(string):
    length = len(string)
    parts = string.split('&')
    for p in parts:
        (key, val) = p.split('=')
        params[key] = val

def requestify(request):
    """
    Primary method which generates final request to be sent to JCS servers.

    Example of param 'request':
        'https://10.140.214.71/?Action=DescribeInstances&Version=2016-03-01'
    """
    [initial, rest] = request.split('?')
    parts = initial.split('/')
    protocol, host_port = parts[0][ : -1], parts[2]
    path = '/'
    if (':' not in host_port):
        host = host_port
        port = 443
    else:
       [host, port] = host_port.split(':')
    auth_path = path
    add_params(rest)
    headers = {}
    headers['User-Agent'] = 'curl/7.35.0'
    headers['Content-Type'] = 'application/json'
    headers['Accept-Encoding'] = 'identity'
    print headers

    reqObj = HTTPRequest(method, protocol, host, port, path, auth_path,
                         params, headers, '')
    authHandlerObj = V2Handler(host)
    reqObj = authHandlerObj.add_auth(reqObj)
    request_string = reqObj.method
    request_string += ' \"' + initial + '?'
    for keys in reqObj.params:
        request_string += keys + '=' + reqObj.params[keys] + '&'
    request_string = request_string[ : -1]
    request_string += '\"'
    return request_string

def main():
    req = sys.argv[1]
    chngd_req = requestify(req)
    print chngd_req

if __name__ == '__main__':
    main()
