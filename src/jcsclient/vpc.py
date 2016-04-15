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
from vpc_api import com

class Controller(object):
    """Vpc Controller class

    This class has all the functions for Vpc

    It acts as a wrapper over how the calls are
    internally handled

    In the controller methods, first argument passed
    in list of args is the Action name
    """

    def __init__(self):
        self.url = config.get_service_url('vpc')
        self.headers = {}
        self.version = '2016-03-01'
        self.verb = 'GET'



    def create_vpc(self, args):

        return com.create_vpc(self.url, self.verb, self.headers,
                self.version, args)

    def delete_vpc(self, args):

        return com.delete_vpc(self.url, self.verb, self.headers,
                self.version, args)

    def describe_vpcs(self, args):

        return com.describe_vpcs(self.url, self.verb, self.headers,
                self.version, args)

    def create_subnet(self, args):

        return com.create_subnet(self.url, self.verb, self.headers,
                self.version, args)

    def delete_subnet(self, args):

        return com.delete_subnet(self.url, self.verb, self.headers,
                self.version, args)

    def describe_subnets(self, args):

        return com.describe_subnets(self.url, self.verb, self.headers,
                self.version, args)

    def create_security_group(self, args):

        return com.create_security_group(self.url, self.verb, self.headers,
                self.version, args)

    def authorize_security_group_ingress(self, args):

        return com.authorize_security_group_ingress(self.url, self.verb, self.headers,
                self.version, args)

    def authorize_security_group_egress(self, args):

        return com.authorize_security_group_egress(self.url, self.verb, self.headers,
                self.version, args)

    def revoke_security_group_ingress(self, args):

        return com.revoke_security_group_ingress(self.url, self.verb, self.headers,
                self.version, args)

    def revoke_security_group_egress(self, args):

        return com.revoke_security_group_egress(self.url, self.verb, self.headers,
                self.version, args)

    def describe_security_groups(self, args):

        return com.describe_security_groups(self.url, self.verb, self.headers,
                self.version, args)

    def delete_security_group(self, args):

        return com.delete_security_group(self.url, self.verb, self.headers,
                self.version, args)

    def create_route(self, args):

        return com.create_route(self.url, self.verb, self.headers,
                self.version, args)

    def delete_route(self, args):

        return com.delete_route(self.url, self.verb, self.headers,
                self.version, args)

    def create_route_table(self, args):

        return com.create_route_table(self.url, self.verb, self.headers,
                self.version, args)

    def delete_route_table(self, args):

        return com.delete_route_table(self.url, self.verb, self.headers,
                self.version, args)

    def associate_route_table(self, args):

        return com.associate_route_table(self.url, self.verb, self.headers,
                self.version, args)

    def disassociate_route_table(self, args):

        return com.disassociate_route_table(self.url, self.verb, self.headers,
                self.version, args)

    def describe_route_tables(self, args):

        return com.describe_route_tables(self.url, self.verb, self.headers,
                self.version, args)

    def allocate_address(self, args):

        return com.allocate_address(self.url, self.verb, self.headers,
                self.version, args)

    def associate_address(self, args):

        return com.associate_address(self.url, self.verb, self.headers,
                self.version, args)

    def disassociate_address(self, args):

        return com.disassociate_address(self.url, self.verb, self.headers,
                self.version, args)

    def release_address(self, args):

        return com.release_address(self.url, self.verb, self.headers,
                self.version, args)

    def describe_addresses(self, args):

        return com.describe_addresses(self.url, self.verb, self.headers,
                self.version, args)

