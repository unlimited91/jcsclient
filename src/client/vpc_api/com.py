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

import argparse
from client import utils
from client import requestify

def createUrl(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    print args


def create_vpc(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--cidr-block',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
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
    parser.add_argument('--vpc-ids',required=False)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    print params
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

def create_security_group(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    parser.add_argument('--group-name',required=True)
    parser.add_argument('--group-descri',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def authorize_security_group_ingress(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]

def authorize_security_group_egress(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]

def revoke_security_group_ingress(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]

def revoke_security_group_egress(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]

def describe_security_groups(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]

def delete_security_group(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def create_route(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def delete_route(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
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
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)


def associate_route_table(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def disassociate_route_table(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def describe_route_tables(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]

def allocate_address(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def associate_address(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def disassociate_address(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def release_address(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def describe_addresses(url, verb, headers, version, args):

    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--vpc-id',required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)
