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

import config
from client import help
from client.dss_api.dss_main import DSS

class Controller(object):
    """DSS Controller class

    This class acts as a thin wrapper to support the common cli 
    interface and all the calls are handled inside client.dss_api.
    Also checks for the currently supported and valid action names 

    In the controller methods, first argument passed
    in list of args is the Action name
    """

    def __init__(self):
        # list of valid and supported actions
        self.valid_actions = [
                              'create_bucket', 
                              'copy_object', 
                              'delete_bucket', 
                              'delete_object',
                              'get_object',
                              'head_bucket',
                              'head_object',
                              'list_buckets',
                              'list_objects',
                              'put_object',
                              'get_presigned_url',
                              'create_multipart_upload',
                              'upload_part',
                              'list_parts',
                              'complete_multipart_upload',
                              'abort_multipart_upload',
                              'list_multipart_uploads',
                             ]

    def __getattr__(self, name):
        """ check for valid and supported action names and give
        the control to main method of DSS class in 
        client.dss_api.dss_main to process the request
        """
        if(name in self.valid_actions):
            return getattr(DSS(), 'main')
        else:
          """ in case of invalid action name, raise AttributeError
          to be consistent with the common cli interface
          """
          raise AttributeError
