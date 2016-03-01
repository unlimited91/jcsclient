from client import common
from client import config

import pprint

# TODO(rushiagr): also check the 'type' of parameter supplied. E.g. don't
# accept 'blah' as a value for InstanceCount, which expects an integer

# =============== Instances =================

def describe_instances():
    """DescribeInstances API wrapper."""
    valid_optional_params = []
    optional_params = {}
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

def start_instances():
    """StartInstances API wrapper."""
    pass

def reboot_instances():
    """RebootInstances API wrapper."""
    pass

def terminate_instances():
    """TerminateInstances API wrapper."""
    pass

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

def attach_volume():
    """AttachVolume."""
    pass

def delete_volume(VolumeId):
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'DeleteVolume',
        'VolumeId': VolumeId,
    }
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

# =============== Snapshots =================

def describe_snapshots():
    """DescribeSnapshots API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {'Action': 'DescribeSnapshots'}
    return common.do_compute_request(valid_optional_params, optional_params, mandatory_params)

def create_snapshot(VolumeId, **optional_params):
    """DescribeSnapshots API wrapper."""
    valid_optional_params = ['Name', 'Description']
    mandatory_params = {
        'Action': 'CreateSnapshot',
        'VolumeId': VolumeId,
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

def release_address(AllocationId):
    """ReleaseAddress API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'ReleaseAddress',
        'AllocationId': AllocationId,
    }
    return common.do_vpc_request(valid_optional_params, optional_params, mandatory_params)

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(describe_instances())
    pp.pprint(describe_volumes())
    pp.pprint(describe_images())
    pp.pprint(describe_vpcs())
    #pp.pprint(describe_snapshots())
    #pp.pprint(delete_volume('9e501705-6721-4880-abcd-cd4d8bdbf005'))
    #print create_volume(Size=2)
