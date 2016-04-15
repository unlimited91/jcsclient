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

import base64
import binascii
import requests
from jcsclient import exception
from jcsclient import utils
from jcsclient import requestify

def describe_instances(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--instance-ids', nargs='+', required=False)
    # Right now filters functionality is broken, it works only
    # for cases like --filters "Name=abc,Values=def"
    parser.add_argument('--filters', nargs='+', required=False)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def start_instances(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--instance-ids', nargs='+', required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def stop_instances(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--instance-ids', nargs='+', required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def reboot_instances(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--instance-ids', nargs='+', required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def terminate_instances(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--instance-ids', nargs='+', required=True)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def describe_instance_types(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--instance-type-ids', nargs='+', required=False)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def run_instances(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--instance-type-id', required=True)
    parser.add_argument('--image-id', required=True)
    parser.add_argument('--subnet-id', required=False)
    parser.add_argument('--security-group-ids', nargs='+', required=False)
    parser.add_argument('--key-name', required=False)
    parser.add_argument('--instance-count', type=int, required=False)
    parser.add_argument('--private-ip-address', required=False)
    parser.add_argument('--block-device-mappings', nargs='+', required=False)
    args = parser.parse_args(args)
    utils.populate_params_from_cli_args(params, args)
    return requestify.make_request(url, verb, headers, params)

def decrypt_instance_password(password, private_key_file, passphrase):
    key = utils.import_ssh_key(private_key_file, passphrase)
    encrypted_data = base64.b64decode(base64.b64decode(password))
    ciphertext = int(binascii.hexlify(encrypted_data), 16)
    plaintext = key.decrypt(ciphertext)
    decrypted_data = utils.long_to_bytes(plaintext)
    unpadded_data = utils.pkcs1_unpad(decrypted_data)
    return unpadded_data 

def get_password_data(url, verb, headers, version, args):
    params = {}
    params['Action'] = utils.dash_to_camelcase(args[0])
    params['Version'] = version
    args = args[1:]
    parser = utils.get_argument_parser()
    parser.add_argument('--instance-id', required=True)
    processed, remaining = parser.parse_known_args(args)
    utils.populate_params_from_cli_args(params, processed)
    response = requestify.make_request(url, verb, headers, params)
    parser = utils.get_argument_parser()
    parser.add_argument('--private-key-file', required=False, default=None)
    parser.add_argument('--key-passphrase', required=False, default=None)
    processed = parser.parse_args(remaining)
    processed = vars(processed)
    private_key_file = processed.get('private_key_file')
    passphrase = processed.get('key_passphrase')
    response_json = utils.web_response_to_json(response)
    try:
        response_body = response_json['GetPasswordDataResponse']
        encrypted_password = response_body['passwordData']
        if not private_key_file or not encrypted_password:
            return response
        decrypted_password = decrypt_instance_password(encrypted_password,
                                                       private_key_file,
                                                       passphrase)
        response_json['GetPasswordDataResponse']['passwordData'] = \
                                                  decrypted_password
        return response_json
    except KeyError as ke:
        raise exception.UnknownOutputFormat()
    
