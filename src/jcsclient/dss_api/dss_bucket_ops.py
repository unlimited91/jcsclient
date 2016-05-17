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

from dss_op import *
from dss_auth import *
from jcsclient import utils
import os
import sys
import time
import hmac
import json
import base64
import requests
import exceptions
from email.utils import formatdate
import xml.sax

class BucketOp(DSSOp):

    def __init__(self):
        DSSOp.__init__(self)
        self.bucket_name = None

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.dss_op_path = '/' + self.bucket_name


    def validate_args(self):
        pass

    def execute(self):
        resp = self.make_request()
        return resp

    def process_result(self, result):
        # nonop currently
        return result



class ListBucketsOp(BucketOp):

    def __init__(self):
        BucketOp.__init__(self)
        self.dss_op_path = '/'
        self.http_method = 'GET'

    def parse_args(self, args):
        # no arguments in list-buckets for now
        pass

class CreateBucketOp(BucketOp):

    def __init__(self):
        BucketOp.__init__(self)
        self.http_method = 'PUT'


    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        if(result.status_code == 200):
            respone_json = '{ "Location": "' + self.dss_url + '/' + self.bucket_name + '" }'
            self.pretty_print_json_str(respone_json)
        return result


class DeleteBucketOp(BucketOp):

    def __init__(self):
        BucketOp.__init__(self)
        self.http_method = 'DELETE'


class HeadBucketOp(BucketOp):

    def __init__(self):
        DSSOp.__init__(self)
        self.http_method = 'HEAD'

class ListObjectsOp(BucketOp):

    def __init__(self):
        DSSOp.__init__(self)
        self.http_method = 'GET'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--prefix')
        parser.add_argument('--max-items')
        parser.add_argument('--starting-token')
        parser.add_argument('--delimiter')
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.dss_op_path = '/' + self.bucket_name
        is_query_params_set = False
        self.dss_query_str = ''
        if(args_dict['prefix'] is not None):
            self.dss_query_str = 'prefix=' + args_dict['prefix']
            is_query_params_set = True
        if(args_dict['starting_token'] is not None):
            if(not is_query_params_set):
                self.dss_query_str += 'marker=' + args_dict['starting_token']
                is_query_params_set = True
            else:
                self.dss_query_str += '&marker=' + args_dict['starting_token']
        if(args_dict['max_items'] is not None):
            if(not is_query_params_set):
                self.dss_query_str += 'max-keys=' + args_dict['max_items']
                is_query_params_set = True
            else:
                self.dss_query_str += '&max-keys=' + args_dict['max_items']
        if(args_dict['delimiter'] is not None):
            if(not is_query_params_set):
                self.dss_query_str += 'delimiter=' + args_dict['delimiter']
                is_query_params_set = True
            else:
                self.dss_query_str += '&delimiter=' + args_dict['delimiter']
        if(self.dss_query_str == ''):
            self.dss_query_str = None

class ListMPUploadsOp(BucketOp):
    
    def __init__(self):
        BucketOp.__init__(self)
        self.http_method = 'GET'
        self.dss_query_str_for_signature = 'uploads'
        self.dss_query_str = 'uploads'

