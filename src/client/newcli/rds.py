import argparse
import sys
import pprint

from client import cloud

pp = pprint.PrettyPrinter(indent=2)

# TODO(rushiagr): underscores, camelcase and dash-separated arguments can all
# be put in one place and referenced from that place, instead of doing a 'for'
# loop multiple times

def _camel_case(string):
    """ CLI arg to camel case.

    If input is one_two_three, output is OneTwoThree.
    If input is final_db_snapshot, output is FinalDBSnapshot.
    """
    parts = string.strip('_').split('_')

    return_str = ''

    for part in parts:
        if part == 'db':
            return_str += 'DB'
            continue
        return_str += part.capitalize()
    return return_str

def _dash_separated(string):
    """ CLI arg to camel case.

    If input is one_two_three, output is --one-two-three.
    """
    # TODO(rushiagr): this function can be written in one line
    parts = string.strip('_').split('_')

    return_str = '--'

    for part in parts:
        return_str += part.lower() + '-'
    return return_str[:-1]

def _generate_optional_args(valid_optional_args_list, args_object):
    input_dict = {}
    for option in valid_optional_args_list:
        if getattr(args_object, option):
            input_dict[_camel_case(option)] = str(getattr(args_object, option))
    print input_dict
    return input_dict

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
        cloud.describe_db_instances(DBInstanceIdentifier=args.instance_identifier)
    else:
        cloud.describe_db_instances()

def delete_db_instance(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-instance-identifier', required=True)
    # TODO(rushiagr): If one doesn't specify skip-final-snapshot, then he/she
    # has to specify final-db-snapshot-identifier compulsarily. Add this check
    parser.add_argument('--skip-final-snapshot', dest='skip_final_snapshot',
            action='store_true')
    parser.set_defaults(skip_final_snapshot=False)
    parser.add_argument('--final-db-snapshot-identifier', required=False)
    args = parser.parse_args(*args)

    valid_optional_args = [
        'skip_final_snapshot',
        'final_db_snapshot_identifier']

    input_dict = _generate_optional_args(valid_optional_args, args)

    cloud.delete_db_instance(args.db_instance_identifier, **input_dict)

def modify_db_instance(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-instance-identifier', required=True)
    optional_args = ['preferred_maintenance_window', 'preferred_backup_window',
            'backup_retention_period', 'new_db_instance_identifier']
    for arg in optional_args:
        parser.add_argument(_dash_separated(arg), required=False)
    args = parser.parse_args(*args)

    input_dict = _generate_optional_args(optional_args, args)
    cloud.modify_db_instance(args.db_instance_identifier, **input_dict)

def describe_db_snapshots(*args):
    parser = argparse.ArgumentParser()
    optional_args = ['db_snapshot_identifier', 'db_instance_identifier', 'snapshot_type']
    for arg in optional_args:
        parser.add_argument(_dash_separated(arg), required=False)
    args = parser.parse_args(*args)
    input_dict = _generate_optional_args(optional_args, args)
    cloud.describe_db_snapshots(**input_dict)

def create_db_snapshot(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-instance-identifier', required=True)
    parser.add_argument('--db-snapshot-identifier', required=True)
    args = parser.parse_args(*args)
    cloud.create_db_snapshot(args.db_instance_identifier,
            args.db_snapshot_identifier)

def delete_db_snapshot(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-snapshot-identifier', required=True)
    args = parser.parse_args(*args)
    cloud.delete_db_snapshot(args.db_snapshot_identifier)

def restore_db_instance_from_db_snapshot(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-instance-identifier', required=True)
    parser.add_argument('--db-snapshot-identifier', required=True)
    optional_args = ['db_instance_class', 'preferred_maintenance_window',
        'preferred_backup_window', 'backup_retention_period']
    for arg in optional_args:
        parser.add_argument(_dash_separated(arg), required=False)
    args = parser.parse_args(*args)
    input_dict = _generate_optional_args(optional_args, args)
    cloud.restore_db_instance_from_db_snapshot(args.db_instance_identifier,
            args.db_snapshot_identifier)


actions = [
    'describe-db-instances',
    'create-db-instance',
    'modify-db-instance',
    'delete-db-instance',
    'describe-db-snapshots',
    'create-db-snapshot',
    'delete-db-snapshot',
    'restore-db-instance-from-db-snapshot',
]

# TODO(rushiagr): start using temp dict, and don't use if..elif..elif....
temp_dict = {
    'describe-db-instances': describe_db_instances,
}

def parse_service_related_args(args):
    action = args[0]
    print action
    if action not in actions:
        print 'Invalid RDS action: %s' % action
        print 'Valid actions: %s' % ' '.join(actions)

    if action == 'describe-db-instances':
        describe_db_instances(args[1:])
    elif action == 'create-db-instance':
        create_db_instance(args[1:])
    elif action == 'delete-db-instance':
        delete_db_instance(args[1:])
    elif action == 'modify-db-instance':
        modify_db_instance(args[1:])
    elif action == 'restore-db-instance-from-db-snapshot':
        restore_db_instance_from_db_snapshot(args[1:])
    elif action == 'describe-db-snapshots':
        describe_db_snapshots(args[1:])
    elif action == 'create-db-snapshot':
        create_db_snapshot(args[1:])
    elif action == 'delete-db-snapshot':
        delete_db_snapshot(args[1:])
