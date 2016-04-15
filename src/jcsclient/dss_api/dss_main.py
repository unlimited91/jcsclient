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

from dss_bucket_ops import *
from dss_object_ops import *

class DSS(object):
    """DSS main class, each cli command is processed here
    Object is created from inside the dss Controller
    """

    def __init__(self):
        pass

    def main(self, args):
        """ main function to process all cli commands
        This function gets called from the cli driver
        Here, the first argument passed in list of args is the api
        Steps to process a cli command
        1. create an object of type DSSOp based on the api
        2. parse the args
        3. validate the args
        4. execute the operation
        5. process the result to make it compatible with the cli driver
        6. return the result
        """
        
        op_factory = DSSOpFactory()
        op = op_factory.get_op(args[0])
        if(op is None):
          raise MethodNotFound('dss', args[0])
        op.parse_args(args)
        op.validate_args()
        result = op.execute()
        processed_result = op.process_result(result)
        return processed_result


class DSSOpFactory(object):
    """Factory to create objects of types DSSOp based on the 
    cli arguments
    """

    def __init__(self):
        pass

    def get_op(self, cli_action):
        if(cli_action == 'create-bucket'):
			return CreateBucketOp()
        if(cli_action == 'delete-bucket'):
			return DeleteBucketOp()
        if(cli_action == 'head-bucket'):
			return HeadBucketOp()
        if(cli_action == 'list-buckets'):
			return ListBucketsOp()
        if(cli_action == 'copy-object'):
			return CopyObjectOp()
        if(cli_action == 'delete-object'):
			return DeleteObjectOp()
        if(cli_action == 'get-object'):
			return GetObjectOp()
        if(cli_action == 'head-object'):
			return HeadObjectOp()
        if(cli_action == 'list-objects'):
			return ListObjectsOp()
        if(cli_action == 'put-object'):
			return PutObjectOp()
        if(cli_action == 'get-presigned-url'):
			return GetPresignedURLOp()
        if(cli_action == 'create-multipart-upload'):
			return InitMPUploadOp()
        if(cli_action == 'abort-multipart-upload'):
			return CancelMPUploadOp()
        if(cli_action == 'complete-multipart-upload'):
			return CompleteMPUploadOp()
        if(cli_action == 'list-multipart-uploads'):
			return ListMPUploadsOp()
        if(cli_action == 'list-parts'):
			return ListPartsOp()
        if(cli_action == 'upload-part'):
			return UploadPartOp()
        
        return None
