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
import json
from jcsclient import output

class ObjectOp(DSSOp):

    def __init__(self):
        DSSOp.__init__(self)

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))


    def validate_args(self):
        pass

    def execute(self):
        resp = self.make_request()
        return resp

    def process_result(self, result):
        # nonop currently
        return result



class DeleteObjectOp(ObjectOp):

    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'DELETE'


class HeadObjectOp(ObjectOp):

    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'HEAD'

    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        if(result is not None and result.status_code == 200):
            response_json = ('{'
                      '"AcceptRanges": "'+ result.headers['accept-ranges'] + '",'
                      '"ContentType": "' + result.headers['content-type'] + '",'
                      '"LastModified": "' + result.headers['date'] + '",'
                      '"ContentLength": ' + result.headers['content-length'] + ','
                      '"ETag": "' + result.headers['etag'].replace('"', '\\"') + '",'
                      '"Metadata": {}'
                      '}')
            self.pretty_print_json_str(response_json)

        return result



class PutObjectOp(ObjectOp):
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'PUT'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--body', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.local_file_name = args_dict['body'] 


    def validate_args(self):
        pass

    def execute(self):
        result = None
        # check if the local_file_name is a directory or not
        if(os.path.isdir(self.local_file_name)):
            # recursivley upload all the files and subfolders

            self.local_file_name = os.path.normpath(self.local_file_name)
            dir_name = self.object_name
            # create top level folder
            print ("\nCreating folder " + self.object_name)
            result = self.put_single_object(os.path.normpath(self.object_name) + "/", None, is_folder = True)
            self.process_result(result)
            output.format_result(result)
            for root, dirs, files in os.walk(self.local_file_name):
                # iterate over files 
                for name in files:
                    input_file_path = os.path.join(root, name)
                    object_name = dir_name + "/" + os.path.normpath(input_file_path[len(self.local_file_name) + 1:])
                    print ("\nUploading file " + input_file_path + " as " + object_name)
                    result = self.put_single_object(object_name, input_file_path)
                    self.process_result(result)
                    output.format_result(result)
                # iterate over sub directories
                for name in dirs:
                    input_file_path = os.path.join(root, name)
                    object_name = dir_name + "/" + os.path.normpath(input_file_path[len(self.local_file_name) + 1:]) + "/"
                    print ("\nCreating folder " + object_name)
                    result = self.put_single_object(object_name, input_file_path, True)
                    self.process_result(result)
                    output.format_result(result)
                  

            return None
        else:
            return self.put_single_object(self.object_name, self.local_file_name)

    def put_single_object(self, object_name, input_file_path, is_folder = False):
        self.dss_op_path = '/' + self.bucket_name + '/' + object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, content_type = 'application/octet-stream')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        statinfo = os.stat(self.local_file_name)
        self.http_headers['Content-Length'] = statinfo.st_size
        self.http_headers['Content-Type'] = 'application/octet-stream'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        data = None
        if(not is_folder):
          data = open(input_file_path, 'rb')
        # make request
        resp = requests.put(request_url, headers = self.http_headers, data=data, verify = self.is_secure_request)
        return resp


    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        if(result is not None and result.status_code == 200):
            response_json = ('{'
                      '"AcceptRanges": "'+ result.headers['accept-ranges'] + '",'
                      '"LastModified": "' + result.headers['date'] + '",'
                      '"ETag": "' + result.headers['etag'].replace('"', '\\"') + '"'
                      '}')
            self.pretty_print_json_str(response_json)

        return result



class GetObjectOp(ObjectOp):
    
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'GET'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--outfile')
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        if(args_dict['outfile'] is not None):
            self.local_file_name = args_dict['outfile'] 
        else:
            self.local_file_name = self.object_name
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))


    def validate_args(self):
        pass

    def execute(self):
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path)
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str

        # construct request
        request_url = self.dss_url + self.dss_op_path
        # make request
        resp = ''
        with open(self.local_file_name, 'wb') as handle:
            resp = requests.get(request_url, headers = self.http_headers, stream = True, verify = self.is_secure_request)
            if resp.ok:
                for block in resp.iter_content(1024):
                    handle.write(block)
            else:
                resp.raise_for_status()

        return resp

    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        if(result is not None and result.status_code == 200):
            response_json = ('{'
                      '"AcceptRanges": "'+ result.headers['accept-ranges'] + '",'
                      '"ContentType": "' + result.headers['content-type'] + '",'
                      '"LastModified": "' + result.headers['last-modified'] + '",'
                      '"ContentLength": ' + result.headers['content-length'] + ','
                      '"ETag": "' + result.headers['etag'].replace('"', '\\"') + '"'
                      '}')

            self.pretty_print_json_str(response_json)
        
        return result


class GetPresignedURLOp(ObjectOp):
    
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'GET'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--expiry', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.validity = args_dict['expiry'] 
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))


    def validate_args(self):
        pass

    def execute(self):
        # get signature
        date_str = formatdate(usegmt=True)
        expiry_time  = int(time.time()) + int(self.validity)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, use_time_in_seconds = True, expiry_time = expiry_time)
        signature = auth.get_signature()
        # url encode the signature 

        # construct url
        request_url = self.dss_url + self.dss_op_path
        request_url = request_url + '?JCSAccessKeyId=' + self.access_key + '&Expires=' + str(expiry_time) + '&Signature=' + urllib2.quote(signature.encode("utf8"))
        response_json = '{"DownloadUrl": "' + request_url + '"}'
        self.pretty_print_json_str(response_json)
        resp = None
        return resp


    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        return result


class CopyObjectOp(ObjectOp):
    
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'PUT'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--copy-source', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.copy_source = args_dict['copy_source'] 
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))


    def validate_args(self):
        # check for valid copy source should be <bucket>/<object>
        pos = self.copy_source.find('/')
        if(pos == -1 or pos == 0 or pos == len(self.copy_source) - 1):
            raise ValueError('copy-source should be of format <bucket-name>/<object-name>')

    def execute(self):
        self.http_headers['x-jcs-metadata-directive'] = 'COPY'
        self.http_headers['x-jcs-copy-source'] = self.copy_source

        resp = self.make_request()

        return resp

    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        return result


class InitMPUploadOp(ObjectOp):
    
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'POST'
        self.dss_query_str = 'uploads'
        self.dss_query_str_for_signature = 'uploads'


class CancelMPUploadOp(ObjectOp):
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'DELETE'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--upload-id', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.upload_id = args_dict['upload_id']
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        self.dss_query_str = 'uploadId=' + self.upload_id
        self.dss_query_str_for_signature = 'uploadId=' + self.upload_id



class ListPartsOp(ObjectOp):
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'GET'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--upload-id', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.upload_id = args_dict['upload_id']
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        self.dss_query_str = 'uploadId=' + self.upload_id
        self.dss_query_str_for_signature = 'uploadId=' + self.upload_id


    def execute(self):
        resp = self.make_request()
        return resp


class UploadPartOp(ObjectOp):
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'PUT'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--upload-id', required=True)
        parser.add_argument('--part-number', required=True)
        parser.add_argument('--body', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.upload_id = args_dict['upload_id']
        self.part_number = args_dict['part_number']
        self.local_file_name = args_dict['body']
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        self.dss_query_str = 'partNumber=' + self.part_number + '&uploadId=' + self.upload_id
        self.dss_query_str_for_signature = 'partNumber=' + self.part_number + '&uploadId=' + self.upload_id


    def execute(self):
        # get signature
        date_str = formatdate(usegmt=True)
        query_str = 'partNumber=' + self.part_number + '&uploadId=' + self.upload_id
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, query_str = self.dss_query_str_for_signature, content_type = 'application/octet-stream')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        statinfo = os.stat(self.local_file_name)
        self.http_headers['Content-Length'] = statinfo.st_size
        self.http_headers['Content-Type'] = 'application/octet-stream'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        if(self.dss_query_str is not None):
            request_url += '?' + self.dss_query_str  
        data = open(self.local_file_name, 'rb')
        # make request
        resp = requests.put(request_url, headers = self.http_headers, data=data, verify = self.is_secure_request)
      
        return resp


    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        if(result is not None and result.status_code == 200):
            response_json = ('{'
                      '"ETag": "' + result.headers['etag'].replace('"', '\\"') + '"'
                      '}')
            self.pretty_print_json_str(response_json)
            resp_json = resp_json.replace("\\", "")
            print(resp_json)

        return result


class CompleteMPUploadOp(ObjectOp):
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'POST'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--upload-id', required=True)
        parser.add_argument('--multipart-upload', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.upload_id = args_dict['upload_id']
        self.local_file_name = args_dict['multipart_upload']
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        self.dss_query_str = 'uploadId=' + self.upload_id
        self.dss_query_str_for_signature = 'uploadId=' + self.upload_id


    def execute(self):
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, query_str = self.dss_query_str_for_signature, content_type = 'text/xml')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        statinfo = os.stat(self.local_file_name)
        self.http_headers['Content-Length'] = statinfo.st_size
        self.http_headers['Content-Type'] = 'text/xml'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        if(self.dss_query_str is not None):
            request_url += '?' + self.dss_query_str  
        data = open(self.local_file_name, 'rb')
        # make request
        resp = requests.post(request_url, headers = self.http_headers, data=data, verify = self.is_secure_request)
      
        # process response
        processed_resp = self.process_result(resp)
        return processed_resp


