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

from client import utils
from client import requestify
from client import exception
import vpcutils

def create_sec_group_rule(params,args) :


    parser = utils.get_argument_parser()
    parser.add_argument('--group-id',required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--ip-permissions', nargs='*')
    group.add_argument('--protocol', dest = 'ip_Permissions.1._ip_protocol')

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--cidr', dest = 'ip_Permissions.1._ip_ranges.1._cidr_ip')
    group2.add_argument('--source-group', dest='ip_Permissions.1._groups.1._group_id')

    parser.add_argument('--port')


    args = parser.parse_args(args)
    vpcutils.populate_params_from_cli_args(params, args)


def create_vpc(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--cidr-block',required=True)
    args = parser.parse_args(args)
    vpcutils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


    

def delete_vpc(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)



def describe_vpcs(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-ids', nargs='*', required=False)
    args = parser.parse_args(args)
    vpcutils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def create_subnet(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    parser.add_argument('--cidr-block',required=True) 
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def delete_subnet(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--subnet-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def describe_subnets(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--subnet-ids', nargs='*', required=False)
    args = parser.parse_args(args)
    vpcutils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def create_security_group(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    parser.add_argument('--group-name',required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--description', dest='group_description')
    group.add_argument('--group-description', dest='group_description')
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def authorize_security_group_ingress(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    create_sec_group_rule(params,args)
    return requestify.make_request(url, verb, headers, params)



def authorize_security_group_egress(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    create_sec_group_rule(params,args)
    return requestify.make_request(url, verb, headers, params)


def revoke_security_group_ingress(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    create_sec_group_rule(params,args)
    return requestify.make_request(url, verb, headers, params)


def revoke_security_group_egress(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    create_sec_group_rule(params,args)
    return requestify.make_request(url, verb, headers, params)


def describe_security_groups(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--group-ids', nargs='*', required=False)
    args = parser.parse_args(args)
    vpcutils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def delete_security_group(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--group-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def create_route(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--route-table-id',required=True)
    parser.add_argument('--destination-cidr-block',required=True)
    parser.add_argument('--instance-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def delete_route(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser.add_argument('--router-table-id',required=True)
    parser.add_argument('--destination-cidr-block',required=True)
    parser = utils.get_argument_parser()
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def create_route_table(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def delete_route_table(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--route-table-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def associate_route_table(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--route-table-id',required=True)
    parser.add_argument('--subnet-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def disassociate_route_table(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--association-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def describe_route_tables(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--route-table-ids', nargs='*', required=False)
    args = parser.parse_args(args)
    vpcutils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def allocate_address(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--domain',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def associate_address(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--allocation-id',required=True)
    parser.add_argument('--instance-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def disassociate_address(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--association-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def release_address(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--allocation-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def describe_addresses(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--allocation-ids', nargs='*', required=False)
    args = parser.parse_args(args)
    vpcutils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)
