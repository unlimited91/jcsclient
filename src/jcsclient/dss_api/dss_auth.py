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

import hmac
import base64
from hashlib import sha1
import urllib2


class DSSAuth(object):
    """Class for handling authorization in DSS requests
    """

    def __init__(self, http_method, access_key, secret_key, date_str, path = '/', query_str = None, content_type = None, use_time_in_seconds=False, expiry_time=0):
        self.http_method = http_method
        self.access_key = access_key
        self.secret_key = secret_key
        self.path = path
        self.date_str = date_str
        self.query_str = query_str
        self.content_type = content_type
        self.use_time_in_seconds = use_time_in_seconds
        self.expiry_time = expiry_time

    def get_cannonical_str(self):
        cannonical_str = ''
        md5_checksum   = ''
        if(self.use_time_in_seconds):
            self.date_str = str(self.expiry_time)
        path           = self.get_path_for_cannonical_str()

        cannonical_str += self.http_method
        cannonical_str += "\n" + md5_checksum
        if(self.content_type is not None):
            cannonical_str += "\n" + self.content_type
        else:
          cannonical_str += "\n"
        cannonical_str += "\n" + self.date_str
        cannonical_str += "\n" + path
        return cannonical_str


    def get_signature(self):
        secret = self.secret_key
        secret_encoded = (str(secret)).encode('utf-8')
        cannonical_str_encoded = (self.get_cannonical_str()).encode('utf-8')

        dss_hmac = hmac.new(secret_encoded, digestmod=sha1)
        dss_hmac.update(cannonical_str_encoded)
        b64_hmac = ((base64.encodestring(dss_hmac.digest()))).decode('utf-8').strip()
        auth = ''
        if(self.use_time_in_seconds):
            auth = b64_hmac
        else:
            auth = ("%s %s:%s" % ("JCS", self.access_key, b64_hmac))
        return auth

    def get_path_for_cannonical_str(self):
        path = self.path
        if(self.query_str is not None):
            path += '?' + self.query_str
        return str(path)
