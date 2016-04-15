# Copyright (c) 2016 Jiocloud.com, Inc. or its affiliates.  All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import base64
import copy
import datetime
import time
import hmac
import os
import posixpath
import hashlib
import six
import utils
import urllib as ul
from six.moves import urllib

class Authorization(object):
    """This class handles inserting required authorization
       parameters. It needs the access/secret key for performing
       the requisite insertion. That requirement has been taken
       care of while Controller creation initially.
    """

    # Need to add path
    def __init__(self, url, verb, access_key, secret_key, headers,
                 path = '/'):
        self.verb = verb
        self.access_key = access_key
        self.secret_key = secret_key
        self.headers = headers
        self.path = path
        protocol, host = utils.get_protocol_and_host(url)
        if protocol not in ['http', 'https']:
            msg = 'Unsupported protocl present in given url ' + url
            raise ValueError(msg)
        self.protocol = protocol
        self.host = host
        self.port = None # Defaulting to the https port
        if ':' in host:
            parts = host.split(':')
            self.host = parts[0]
            self.port = parts[1]

    def add_params(self, params):
        """Add generic key-value pairs in the params dictionary"""
        params['JCSAccessKeyId'] = self.access_key
        params['SignatureVersion'] = '2'
        params['SignatureMethod'] = 'HmacSHA256'
        params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

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
        """Sort the params and join using & as the delimiter"""
        keys = params.keys()
        keys.sort()
        pairs = []
        for key in keys:
            val = Authorization._get_utf8_value(params[key])
            val = urllib.parse.quote(val, safe='-_~')
            pairs.append(urllib.parse.quote(key, safe='') + '=' + val)
        qs = '&'.join(pairs)
        return qs

    def string_to_sign(self, params):
        """Calculate the canonical string for the request"""
        ss = self.verb + '\n' + self.host
        if self.port:
            ss += ":" + str(self.port)
        ss += "\n" + self.path + '\n'
        self.add_params(params)
        qs = self.sort_params(params)
        ss += qs
        return ss

    def add_authorization(self, params):
        """
        Populate the params dictionary with timestamp and signature
        specific infomation, like signature method and algorithm.

        Then calculate the canonical string based on above params.

        Using secret key, finally calculate the signature and store
        in the params.
        """
        hmac_256 = hmac.new(self.secret_key, digestmod=hashlib.sha256)
        canonical_string = self.string_to_sign(params)
        hmac_256.update(canonical_string.encode('utf-8'))
        b64 = base64.b64encode(hmac_256.digest()).decode('utf-8')
        params['Signature'] = ul.quote(b64) 
