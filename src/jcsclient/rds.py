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
from jcsclient import help
from jcsclient.rds_api import rds

class Controller(object):
    """RDS Controller class

    This class has all the functions for rds

    It acts as a wrapper over how the calls are
    internally handled

    In the controller methods, first argument passed
    in list of args is the Action name
    """

    def __init__(self):
        self.url = config.get_service_url('rds')
        self.headers = {}
        self.version = '2016-03-01'
        self.verb = 'POST'

    def create_db_instance(self, args):
        return rds.create_db_instance(
            self.url, self.verb, self.headers, self.version, args)

    def describe_db_instances(self, args):
        return rds.describe_db_instances(
            self.url, 'GET', self.headers, self.version, args)

    def delete_db_instance(self, args):
        return rds.delete_db_instance(
            self.url, self.verb, self.headers, self.version, args)

    def modify_db_instance(self, args):
        return rds.modify_db_instance(
            self.url, self.verb, self.headers, self.version, args)

    def describe_db_snapshots(self, args):
        return rds.describe_db_snapshots(
            self.url, 'GET' , self.headers, self.version, args)

    def create_db_snapshot(self, args):
        return rds.create_db_snapshot(
            self.url, self.verb, self.headers, self.version, args)

    def delete_db_snapshot(self, args):
        return rds.delete_db_snapshot(
            self.url, self.verb, self.headers, self.version, args)

    def restore_db_instance_from_db_snapshot(self, args):
        return rds.restore_db_instance_from_db_snapshot(
            self.url, self.verb, self.headers, self.version, args)
 
    def describe_db_types(self, args):
        return rds.describe_db_types(
            self.url, 'GET', self.headers, self.version, args)

    def upload_db_instance_logs(self, args):
        return rds.upload_db_instance_logs(
            self.url, self.verb, self.headers, self.version, args)
