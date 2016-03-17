import argparse
import sys
import pprint

from client import cloud

pp = pprint.PrettyPrinter(indent=2)


def create_db_instance(*args):
    parser = argparse.ArgumentParser(description='create db')
    parser.add_argument('--instance-identifier', required=True, help='server name')
    parser.add_argument('--instance-class', required=True)
    parser.add_argument('--engine', required=True)
    parser.add_argument('--allocated-storage', required=True)
    parser.add_argument('--master-user-name', required=True)
    parser.add_argument('--master-user-password', required=True)
    # parser.add_argument('--port', required=False)
    args = parser.parse_args(*args)
    cloud.create_db_instance(args.instance_identifier, args.instance_class,
        args.engine, args.allocated_storage, args.master_user_name,
        args.master_user_password)

def describe_db_instances(*args):
    parser = argparse.ArgumentParser(description='list db')
    parser.add_argument('--instance-identifier', required=False, help='server name')
    args = parser.parse_args(*args)
    if args.instance_identifier:
        pp.pprint(cloud.describe_db_instances(DBInstanceIdentifier=args.instance_identifier))
    else:
        pp.pprint(cloud.describe_db_instances())

actions = [
    'describe-db-instances',
    'create-db-instance',
]

def parse_service_related_args(args):
    action = args[0]
    print action
    if action not in actions:
        print 'Invalid RDS action: %s' % action
        print 'Valid actions: %s' % ' '.join(actions)

    if action == 'describe-db-instances':
        describe_db_instances(args[1:])
