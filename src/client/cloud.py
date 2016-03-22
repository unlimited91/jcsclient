from client import common

import pprint

# TODO(rushiagr): also check the 'type' of parameter supplied. E.g. don't
# accept 'blah' as a value for InstanceCount, which expects an integer

# =============== Instances =================

def describe_instances(**optional_params):
    """DescribeInstances API wrapper."""
    valid_optional_params = ['InstanceId.1']
    mandatory_params = {'Action': 'DescribeInstances'}
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def run_instances(ImageId, InstanceTypeId, **optional_params):
    """
    Run one or more instances.

    Supported params:
        image_id, instance_type_id, key_name, instance_count, subnet_id,
        private_ip_address
    Unsupported params:
        block_device_mapping, security_group_id. Blocked on '.N' feature
        ambiguity.
    """
    # TODO(rushiagr): support for BlockDeviceMapping.N, SecurityGroupId.N
    valid_optional_params = ['KeyName', 'InstanceCount', 'SubnetId', 'PrivateIPAddress']

    mandatory_params = {
        'Action': 'RunInstances',
        'ImageId': ImageId,
        'InstanceTypeId': InstanceTypeId,
    }

    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)


def delete_instance():
    pass

def stop_instances():
    """StopInstances API wrapper"""
    pass


def run_instances(image_id,
                  flavor_id,
                  keypair_name,
                  subnet_id,
                  security_group_id,
                  instance_count):
    """RunInstances API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params= {
        'Action': 'RunInstances',
        'ImageId': image_id,
        'InstanceTypeId': flavor_id,
        'KeyName': keypair_name,
        'InstanceCount': instance_count,
        'SubnetId': subnet_id,
        'SecurityGroupId.1': security_group_id
    }
    return common.do_compute_request(valid_optional_params,
                                     optional_params,
                                     mandatory_params)

def reboot_instances():
    """RebootInstances API wrapper."""
    pass

def terminate_instances(instance_id):
    """TerminateInstances API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params= {
        'Action': 'TerminateInstances',
        'InstanceId.1': instance_id
    }
    return  common.do_compute_request(valid_optional_params,
                                     optional_params,
                                     mandatory_params)

# =============== Images =================

def describe_images():
    """DescribeImages API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {'Action': 'DescribeImages'}
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

# =============== Key pairs =================

def create_key_pair(KeyName):
    """CreateKeyPair."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'CreateKeyPair',
        'KeyName': KeyName,
    }
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def delete_key_pair(KeyName):
    """DeleteKeyPair."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'DeleteKeyPair',
        'KeyName': KeyName,
    }
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def import_key_pair():
    """ImportKeyPair."""
    pass

def describe_key_pairs():
    """DescribeKeyPairs."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params= {'Action': 'DescribeKeyPairs'}
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

# =============== Volumes =================

def describe_volumes(**optional_params):
    """DescribeVolumes API wrapper."""
    valid_optional_params = ['VolumeId', 'Detail']
    mandatory_params = {'Action': 'DescribeVolumes'}
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def create_volume(**optional_params):
    """
    CreateVolume API wrapper.

    Either Size or SnapshotId is mandatory.
    """
    if not optional_params.get('Size') and not optional_params.get('SnapshotId'):
        print 'size or snap id is required'
        raise Exception
    valid_optional_params = ['Size', 'SnapshotId', 'Description']
    mandatory_params = {'Action': 'CreateVolume'}
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def attach_volume(volume_id, instance_id, device):
    """AttachVolume."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'AttachVolume',
        'VolumeId': volume_id,
        'InstanceId': instance_id,
        'device': device
    }
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def detach_volume(volume_id, instance_id):
    """DetachVolume."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'DetachVolume',
        'VolumeId': volume_id,
        'InstanceId': instance_id
    }
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def delete_volume(VolumeId):
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'DeleteVolume',
        'VolumeId': VolumeId
    }
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

# =============== Snapshots =================

def describe_snapshots(**optional_params):
    """DescribeSnapshots API wrapper."""
    valid_optional_params = ['SnapshotId']
    mandatory_params = {'Action': 'DescribeSnapshots'}
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def create_snapshot(volume_id):
    """DescribeSnapshots API wrapper."""
    valid_optional_params = ['Name', 'Description']
    optional_params = {}
    mandatory_params = {
        'Action': 'CreateSnapshot',
        'VolumeId': volume_id,
    }
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def delete_snapshot(SnapshotId):
    """DescribeSnapshots API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'DeleteSnapshot',
        'SnapshotId': SnapshotId,
    }
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

# =============== VPC =================

def describe_vpcs():
    """DescribeVpcs API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {'Action': 'DescribeVpcs'}
    return common.do_vpc_request(valid_optional_params, optional_params, mandatory_params)

def create_vpc(CidrBlock):
    """CreateVpc API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'CreateVpc',
        'CidrBlock': CidrBlock,
    }
    return common.do_vpc_request(valid_optional_params, optional_params, mandatory_params)

def allocate_address(Domain, **optional_params):
    """AllocateAddress API wrapper."""
    # TODO(rushiagr): seems like specifying Domain (with value = 'vpc') is
    # required to get a proper 'allocationId'.
    valid_optional_params = ['Domain']
    mandatory_params = {
        'Action': 'AllocateAddress',
        'Domain': Domain,
    }
    return common.do_vpc_request(valid_optional_params, optional_params, mandatory_params)

def release_address(allocation_id):
    """ReleaseAddress API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'ReleaseAddress',
        'AllocationId': allocation_id,
    }
    return common.do_vpc_request(valid_optional_params, optional_params, mandatory_params)

def associate_address(allocation_id, instance_id):
    """AssociateAddress API wrapper."""

    optional_params = {}

    valid_optional_params = ['NetworkInterfaceId']
    mandatory_params = {
        'Action': 'AssociateAddress',
        'AllocationId': allocation_id,
        'InstanceId': instance_id,
    }
    return common.do_vpc_request(valid_optional_params, optional_params, mandatory_params)

# =============== RDS =================

def describe_db_instances(**optional_params):
    valid_optional_params = ['DBInstanceIdentifier']
    mandatory_params = {'Action': 'DescribeDBInstances'}
    return common.do_rds_request(valid_optional_params, optional_params, mandatory_params)

def create_db_instance(DBInstanceIdentifier, DBInstanceClass, Engine,
        AllocatedStorage, MasterUsername, MasterUserPassword, **optional_params):
    valid_optional_params = ['Port', 'EngineVersion',
        'PreferredMaintenanceWindow', 'PreferredBackupWindow',
        'BackupRetentionPeriod']
    mandatory_params = {
        'Action': 'CreateDBInstance',
        'DBInstanceIdentifier': DBInstanceIdentifier,
        'DBInstanceClass': DBInstanceClass,
        'Engine': Engine,
        'AllocatedStorage': AllocatedStorage,
        'MasterUsername': MasterUsername,
        'MasterUserPassword': MasterUserPassword,
    }
    return common.do_rds_request(valid_optional_params, optional_params, mandatory_params)

def modify_db_instance(DBInstanceIdentifier, **optional_params):
    valid_optional_params = [
        'PreferredMaintenanceWindow',
        'PreferredBackupWindow',
        'BackupRetentionPeriod',
        'NewDBInstanceIdentifier'
    ]
    mandatory_params = {
        'Action': 'ModifyDBInstance',
        'DBInstanceIdentifier': DBInstanceIdentifier,
    }
    return common.do_rds_request(valid_optional_params, optional_params, mandatory_params)

def delete_db_instance(DBInstanceIdentifier, **optional_params):
    valid_optional_params = ['FinalDBSnapshotIdentifier', 'SkipFinalSnapshot']
    mandatory_params = {
        'Action': 'DeleteDBInstance',
        'DBInstanceIdentifier': DBInstanceIdentifier,
    }
    return common.do_rds_request(valid_optional_params, optional_params, mandatory_params)

def create_db_snapshot(DBInstanceIdentifier, DBSnapshotIdentifier, **optional_params):
    valid_optional_params = []
    mandatory_params = {
        'Action': 'CreateDBSnapshot',
        'DBInstanceIdentifier': DBInstanceIdentifier,
        'DBSnapshotIdentifier': DBSnapshotIdentifier,
    }
    return common.do_rds_request(valid_optional_params, optional_params, mandatory_params)

def delete_db_snapshot(DBSnapshotIdentifier, **optional_params):
    valid_optional_params = []
    mandatory_params = {
        'Action': 'DeleteDBSnapshot',
        'DBSnapshotIdentifier': DBSnapshotIdentifier,
    }
    return common.do_rds_request(valid_optional_params, optional_params, mandatory_params)

def describe_db_snapshots(**optional_params):
    valid_optional_params = ['DBSnapshotIdentifier', 'DBInstanceIdentifier', 'SnapshotType']
    mandatory_params = {'Action': 'DescribeDBSnapshots'}
    return common.do_rds_request(valid_optional_params, optional_params, mandatory_params)

def restore_db_instance_from_db_snapshot(DBInstanceIdentifier, DBSnapshotIdentifier, **optional_params):
    valid_optional_params = [
        'DBInstanceClass',
        'PreferredMaintenanceWindow',
        'PreferredBackupWindow',
        'BackupRetentionPeriod']
    mandatory_params = {
        'Action': 'RestoreDBInstanceFromDBSnapshot',
        'DBInstanceIdentifier': DBInstanceIdentifier,
        'DBSnapshotIdentifier': DBSnapshotIdentifier,
    }
    return common.do_rds_request(valid_optional_params, optional_params, mandatory_params)

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(describe_instances())
    pp.pprint(describe_volumes())
    pp.pprint(describe_images())
    pp.pprint(describe_vpcs())
    #pp.pprint(describe_snapshots())
    #pp.pprint(delete_volume('9e501705-6721-4880-abcd-cd4d8bdbf005'))
    #print create_volume(Size=2)
