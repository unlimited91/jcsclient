import argparse
import sys
import pprint

from client import cloud
from client import common

from client.newcli import rds

common.setup_client_from_env_vars()

pp = pprint.PrettyPrinter(indent=2)


# TODO(rushiagr): if no env var present, don't throw exception but a human
# readable message
# TODO(rushiagr): better help texts

# parser = argparse.ArgumentParser(description='Example with long option names')
#
# parser.add_argument('service', nargs='?')

services = {
    'rds': rds,
    'dummy': None
}

def generate_cli_output(input_args):
    #args = parser.parse_args(input_args[0])
    service = input_args[0]

    if service not in services.keys():
        print 'Invalid service "%s"' % args.service
        print 'Valid services: %s' % ' '.join(services.keys())
        sys.exit(1)

    services[service].parse_service_related_args(input_args[1:])
