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


from abc import ABCMeta, abstractmethod
from jcsclient import config
import json
import requests
from email.utils import formatdate
from dss_auth import *

class DSSOp(object):
    """Abstract class defining a common api for each DSS opertaion
    """
    __metaclass__ = ABCMeta


    def __init__(self):
        self.http_method = None
        # mandatory headers for each request
        self.http_headers = {
                              'Authorization': None,
                              'Date': None,
                            }
        self.dss_url = config.get_service_url('dss')
        if(self.dss_url.endswith('/')):
            self.dss_url = self.dss_url[:-1]
        self.access_key = config.get_access_key()
        self.secret_key = config.get_secret_key()
        self.is_secure_request = config.check_secure()
        self.dss_op_path = None
        self.dss_query_str = None
        self.dss_query_str_for_signature = None


    @abstractmethod
    def parse_args(self, args):
        pass

    @abstractmethod
    def validate_args(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    """ Each operation should override this method if it needs to 
    reprocess the output from DSS to make it compatible with the
    the cli

    param result : the string result which needs to be processed
    """
    def process_result(self, result):
        return result

    def make_request(self):
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, query_str = self.dss_query_str_for_signature)
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str

        # construct request
        request_url = self.dss_url + self.dss_op_path

        if(self.dss_query_str is not None):
            request_url += '?' + self.dss_query_str  
        # make request
        resp = requests.request(self.http_method, request_url, headers = self.http_headers, verify = self.is_secure_request)
        return resp

    def pretty_print_json_str(self, json_str):
        resp_dict = json.loads(json_str)
        resp_json = json.dumps(resp_dict, indent=4, sort_keys=True)
        resp_json = resp_json.replace("\\n", "\n")
        resp_json = resp_json.replace("\\", "")
        print(resp_json)


