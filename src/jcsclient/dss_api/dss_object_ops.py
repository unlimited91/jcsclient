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
from dss_bucket_ops import *
from dss_auth import *
from jcsclient import utils
import os
import math
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
import xmltodict
from filechunkio import *



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

class MultipartUpload(object):

    def __init__(self, bucketName, objectName, chunkSize = 5*1024*1024*1024):
        self.bucketName = bucketName
        self.objectName = objectName
        self.chunkSize = chunkSize

    def initiate(self):
        print("\nInitiating multipart upload")
        op = InitMPUploadOp()
        op.parse_args(["", "--bucket", self.bucketName, "--key", self.objectName])
        resp = op.execute()
        op.raise_for_failure(resp)
        self.uploadId = xmltodict.parse(resp.content)["InitiateMultipartUploadResult"]["UploadId"]
        self.numParts = 0
        self.parts = []
        op.process_result(resp)
        output.format_result(resp)
    
    def cancel(self):
        pass

    def listParts(self):
        pass

    def partsToXML(self):
        s = '<CompleteMultipartUpload>\n'
        for (partNum, partEtag) in self.parts:
            s += '  <Part>\n'
            s += '    <PartNumber>%d</PartNumber>\n' % partNum
            s += '    <ETag>%s</ETag>\n' % partEtag
            s += '  </Part>\n'
        s += '</CompleteMultipartUpload>'
        return s

    def uploadPart(self, partNum, fp, size):
        print("\nUploading part number " + str(partNum))
        op = UploadPartOp()
        op.parse_args(["","--bucket", self.bucketName, "--key", self.objectName, "--upload-id", self.uploadId, "--part-number", str(partNum), "--body", ""])

        resp = op.execute(fp, size)
        op.raise_for_failure(resp)
        partEtag = resp.headers["etag"]
        self.numParts += 1
        self.parts.append((partNum, partEtag))
        output.format_result(resp)

    def complete(self):
        print("\nCompleting multipart upload")
        op = CompleteMPUploadOp()
        op.parse_args(["","--bucket", self.bucketName, "--key", self.objectName, "--upload-id", self.uploadId, "--multipart-upload", ""])
        xmlStr = self.partsToXML()
        resp = op.execute(xmlStr)
        op.process_result(resp)
        output.format_result(resp)
        return None



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

    def get_object_name_from_path(self, path):
        normalized_path = os.path.normpath(path)
        path_without_drive = os.path.splitdrive(normalized_path)[1]
        return path_without_drive.replace(os.sep, "/")
    
    
    def execute(self):
        result = None
        # check if the local_file_name is a directory or not
        if(os.path.isdir(self.local_file_name)):
            # recursivley upload all the files and subfolders

            self.local_file_name = os.path.normpath(self.local_file_name)
            object_style_local_file_name = self.get_object_name_from_path(self.local_file_name)
            dir_name = self.object_name
            # create top level folder
            print ("\nCreating folder " + self.object_name)
            (result, processResult) = self.put_single_object(os.path.normpath(self.object_name) + "/", self.local_file_name, is_folder = True)
            self.process_result(result)
            output.format_result(result)
            for root, dirs, files in os.walk(self.local_file_name):
                # iterate over files 
                for name in files:
                    input_file_path = os.path.join(root, name)
                    object_name = dir_name + "/" + self.get_object_name_from_path(input_file_path)[len(object_style_local_file_name) + 1:]
                    print ("\nUploading file " + input_file_path + " as " + object_name)
                    result, processResult = self.put_single_object(object_name, input_file_path)
                    if(processResult):
                        self.process_result(result)
                    output.format_result(result)
                # iterate over sub directories
                for name in dirs:
                    input_file_path = os.path.join(root, name)
                    object_name = dir_name + "/" + self.get_object_name_from_path(input_file_path)[len(object_style_local_file_name) + 1:] + "/"
                    print ("\nCreating folder " + object_name)
                    result, processResult = self.put_single_object(object_name, input_file_path, True)
                    if(processResult):
                        self.process_result(result)
                    output.format_result(result)
                  

            return None
        else:
            result, processResult = self.put_single_object(self.object_name, self.local_file_name)
            if(processResult):
                return result
            else:
                return None

    def put_single_object(self, object_name, input_file_path, is_folder = False):
        statinfo = os.stat(input_file_path)
        if(not is_folder and statinfo.st_size > 5*1024*1024*1024):
            return (self.put_single_object_multipart(object_name, input_file_path), False)
          
        self.dss_op_path = '/' + self.bucket_name + '/' + object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, content_type = 'application/octet-stream')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        if(is_folder):
          self.http_headers['Content-Length'] = 0
        else:
          self.http_headers['Content-Length'] = statinfo.st_size
        self.http_headers['Content-Type'] = 'application/octet-stream'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        data = None
        if(not is_folder):
          data = open(input_file_path, 'rb')
        # make request
        resp = requests.put(request_url, headers = self.http_headers, data=data, verify = self.is_secure_request)
        return (resp, True)

    def put_single_object_multipart(self, object_name, input_file_path):
        part_size = 5*1024*1024*1024
        statinfo = os.stat(input_file_path)
        total_size = statinfo.st_size
        print("\nPerforming multipart upload as the size of file " + input_file_path + " is greater that 5GB : " + str(total_size))
        part_count = int(math.ceil(total_size / float(part_size)))
        mp = MultipartUpload(self.bucket_name, object_name)
        mp.initiate()
        for i in range(part_count):
            offset = part_size * i
            bytes = min(part_size, total_size - offset)
            with FileChunkIO(input_file_path, 'r', offset=offset, bytes=bytes) as fp:
                mp.uploadPart(i + 1, fp, bytes)
        return mp.complete()
        
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
                for block in resp.iter_content(10240):
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


class DownloadFolderOp(ObjectOp):
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'GET'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--outdir', required=True)
        parser.add_argument('--complete-bucket', action='store_true')
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.local_dir_name = args_dict['outdir'] 
        if(args_dict['complete_bucket'] is not None):
            self.download_complete_bucket = True
        else:
            self.download_complete_bucket = False
            


    def validate_args(self):
        pass

    def check_and_raise_for_zero_size(self, key):
        #check if the given folder object is of size 0
        op = HeadObjectOp()
        op.parse_args(["", "--bucket", self.bucket_name, "--key", key])
        res = op.execute()
        self.raise_for_failure(res)
        size = res.headers.get('content-length')
        if(size != "0"):
            print ("\nGiven folder " + key + " is not a zero size object in DSS, size is " + size)
            exit()
        
    def create_folder_for_object(self, key):
        os_style_key_name = key.replace("/", os.sep)
        joined_path = self.local_dir_name + os.sep + os_style_key_name
        path = os.path.normpath(joined_path)
        dirname = os.path.dirname(path)
        if(not os.path.exists(dirname)):
            print ("\nCreating folder " + dirname)
            os.makedirs(dirname)
        return path


    def execute(self):
        if(not self.download_complete_bucket):
            self.check_and_raise_for_zero_size(self.object_name)
        nextMarker = None
        while(True):
            op = ListObjectsOp()
            if(not self.download_complete_bucket):
                if(nextMarker is None):
                    op.parse_args(["", "--bucket", self.bucket_name, "--prefix", self.object_name])
                else:
                    op.parse_args(["", "--bucket", self.bucket_name, "--prefix", self.object_name, "--starting-token", nextMarker])
            else:
                if(nextMarker is None):
                    op.parse_args(["", "--bucket", self.bucket_name])
                else:
                    op.parse_args(["", "--bucket", self.bucket_name, "--starting-token", nextMarker])

            res = op.execute()
            self.raise_for_failure(res)
            responseDict = xmltodict.parse(res.content)
            isTruncated = responseDict.get("ListBucketResult").get("IsTruncated")
            contents = responseDict.get("ListBucketResult").get("Contents")
            if(len(contents) == 0):
                nextMarker = None
            else:
                nextMarker = contents[-1].get("Key")
  
            for content in contents:
                key = content.get("Key")
                if(key.endswith("/")):
                    #this is a folder
                    self.check_and_raise_for_zero_size(key)
                else:
                    download_path = self.create_folder_for_object(key)
                    print ("\nDownloading " + key + " to " + download_path)
                    op = GetObjectOp()
                    op.parse_args(["", "--bucket", self.bucket_name, "--key", key, "--outfile", download_path])
                    resp = op.execute()
                    op.process_result(resp)
                    output.format_result(resp)
                    
            
            if(isTruncated == "false"):
                break
                
        return None


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
        parser.add_argument('--outfile')
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.upload_id = args_dict['upload_id']
        self.outfile = args_dict['outfile']
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        self.dss_query_str = 'uploadId=' + self.upload_id + "&max-parts=2048"
        self.dss_query_str_for_signature = 'uploadId=' + self.upload_id


    def execute(self):
        resp = self.make_request()
        if(self.outfile is not None):
            self.raise_for_failure(resp)
            parts = xmltodict.parse(resp.content)["ListPartsResult"]["Part"]
            s = '<CompleteMultipartUpload>\n'
            for part in parts:
                s += '  <Part>\n'
                s += '    <PartNumber>%s</PartNumber>\n' % part["PartNumber"]
                s += '    <ETag>%s</ETag>\n' % part["ETag"]
                s += '  </Part>\n'
            s += '</CompleteMultipartUpload>'
            fp = open(self.outfile, "w")
            fp.write(s)
            fp.close()
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


    def execute(self, fp = None, size = None):
        # get signature
        date_str = formatdate(usegmt=True)
        query_str = 'partNumber=' + self.part_number + '&uploadId=' + self.upload_id
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, query_str = self.dss_query_str_for_signature, content_type = 'application/octet-stream')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        if(fp is None and size is None):
            statinfo = os.stat(self.local_file_name)
            self.http_headers['Content-Length'] = statinfo.st_size
        else:
            self.http_headers['Content-Length'] = size
            
        self.http_headers['Content-Type'] = 'application/octet-stream'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        if(self.dss_query_str is not None):
            request_url += '?' + self.dss_query_str  
        if(fp is None):
            data = open(self.local_file_name, 'rb')
        else:
            data = fp
        # make request
        resp = None
        if(fp is None and size is None):
            resp = requests.put(request_url, headers = self.http_headers, data=data, verify = self.is_secure_request)
        else:
            s = requests.Session()
            req = requests.Request('PUT', request_url, headers = self.http_headers, data=data)
            prepped = req.prepare()
            prepped.headers['Content-Length'] = size
            resp = s.send(prepped, verify = self.is_secure_request)
            self.process_result(resp)
        return resp


    def process_result(self, result):
        # nonop currently, just dump a json in case of success
        if(result is not None and result.status_code == 200):
            response_json = ('{'
                      '"ETag": "' + result.headers['etag'].replace('"', '\\"') + '"'
                      '}')
            self.pretty_print_json_str(response_json)

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


    def execute(self, xmlStr = None):
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, query_str = self.dss_query_str_for_signature, content_type = 'text/xml')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        if(xmlStr is None):
            statinfo = os.stat(self.local_file_name)
            self.http_headers['Content-Length'] = statinfo.st_size
        else:
            self.http_headers['Content-Length'] = len(xmlStr)
        self.http_headers['Content-Type'] = 'text/xml'

        # construct request
        request_url = self.dss_url + self.dss_op_path
        if(self.dss_query_str is not None):
            request_url += '?' + self.dss_query_str  
        if(xmlStr is None):
            data = open(self.local_file_name, 'rb')
        else:
            data = xmlStr
        # make request
        resp = requests.post(request_url, headers = self.http_headers, data=data, verify = self.is_secure_request)
      
        # process response
        processed_resp = self.process_result(resp)
        return processed_resp



class RenameObjectOp(ObjectOp):
    
    def __init__(self):
        ObjectOp.__init__(self)
        self.http_method = 'PUT'

    def parse_args(self, args):
        params = {}
        args = args[1:]
        parser = utils.get_argument_parser()
        parser.add_argument('--bucket', required=True)
        parser.add_argument('--key', required=True)
        parser.add_argument('--new-name', required=True)
        args = parser.parse_args(args)
        args_dict = vars(args)
        self.bucket_name = args_dict['bucket']
        self.object_name = args_dict['key']
        self.new_name = args_dict['new_name'] 

    def execute(self):
        self.dss_op_path = '/' + self.bucket_name + '/' + self.object_name 
        self.dss_op_path = urllib2.quote(self.dss_op_path.encode("utf8"))
        # get signature
        date_str = formatdate(usegmt=True)
        auth = DSSAuth(self.http_method, self.access_key, self.secret_key, date_str, self.dss_op_path, content_type = 'application/octet-stream')
        signature = auth.get_signature()
        self.http_headers['Authorization'] = signature
        self.http_headers['Date'] = date_str
        self.http_headers['Content-Type'] = 'application/octet-stream'

        # construct request
        query_params = "?newname=" + urllib2.quote(self.new_name.encode("utf8"))
        request_url = self.dss_url + urllib2.quote(self.dss_op_path.encode("utf8")) + query_params
        # make request
        resp = requests.put(request_url, headers = self.http_headers, data=None, verify = self.is_secure_request)
        return resp


