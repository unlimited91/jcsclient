from client import common
from client import config

# TODO(rushiagr): also check the 'type' of parameter supplied. E.g. don't
# accept 'blah' as a value for InstanceCount, which expects an integer

def _do_compute_request(valid_params, supplied_optional_params,
        supplied_mandatory_params=None):
    request_dict = _create_valid_request_dictionary(
        valid_params,
        supplied_optional_params,
        supplied_mandatory_params)
    request_string = common.requestify(config.compute_url, request_dict)
    resp_dict = common.do_request('GET', request_string)
    return _remove_items_keys(resp_dict)

def _create_valid_request_dictionary(valid_params, supplied_optional_params,
        supplied_mandatory_params):
    """
    Create a valid request dictionary from user supplied key-values.

    valid_params is a list, e.g. ['InstanceCount', 'KeyName']
    supplied_optional_params is a dictionary, e.g. {'InstanceCount': 3}
    supplied_mandatory_params is a dictionary of mandatory params.

    Returns a dictionary of valid parameters for the given request
    """
    final_dict = {}

    if supplied_mandatory_params:
        final_dict = supplied_mandatory_params.copy()

    for key, value in supplied_optional_params:
        if key in valid_params:
            final_dict[key] = value
        else:
            print 'Unsupported key! Dropping key-value', key, value

    return final_dict

def _remove_items_keys(response):
    """
    Remove all 'items' keys from 'response' dictionary.

    The value for 'items' key can be either a dictionary or a list of
    dictionaries. Replace the dict whose key is 'items' with the value of
    'items' key. And if this value is a dict, then make it a list which
    contains only that dict.

    Examples:
        Input: {'instances': {'items': {'key1': 'value1'}}}
        Output: {'instances': [{'key1': 'value1'}]}

        Input: {'instances': {'items': [{'key1': 'value1'}, {'key2': 'value2'}]}}
        Output: {'instances': [{'key1': 'value1'}, {'key2': 'value2'}]}
    """
    # TODO(rushiagr): implement this :)
    return response



def describe_instances():
    """DescribeInstances API wrapper."""
    valid_params = []

    request_dict = {'Action': 'DescribeInstances'}

    return _do_compute_request(valid_params, {}, request_dict)

def run_instances(ImageId, InstanceTypeId, **kwargs):
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
    valid_params = ['KeyName', 'InstanceCount', 'SubnetId', 'PrivateIPAddress']

    request_dict = {
        'Action': 'RunInstances',
        'ImageId': ImageId,
        'InstanceTypeId': InstanceTypeId,
    }

    return _do_compute_request(valid_params, kwargs, request_dict)


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

def create_key_pair():
    """CreateKeyPair."""
    pass

def delete_key_pair():
    """DelateKeyPair."""
    pass

def import_key_pair():
    """ImportKeyPair."""
    pass

def describe_key_pairs():
    """DescribeKeyPairs."""
    pass

# =============== Volumes =================

def describe_volumes():
    """DescribeVolumes API wrapper."""
    valid_optional_params = []
    mandatory_params = {'Action': 'DescribeVolumes'}
    return _do_compute_request(valid_optional_params, {}, mandatory_params)

def create_volume(**optional_params):
    """
    CreateVolume API wrapper.

    Either Size or SnapshotId is mandatory.
    """
    if not optional_params.get('Size') and not optional_params.get('SnapshotId'):
        print 'size or snap id is required'
        raise Exception
    valid_optional_params = ['Size', 'SnapshotId']
    mandatory_params = {'Action': 'CreateVolume'}
    return _do_compute_request(valid_optional_params, optional_params, mandatory_params)

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
    return _do_compute_request(valid_optional_params, optional_params, mandatory_params)

# =============== Snapshots =================

def describe_snapshots():
    """DescribeSnapshots API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {'Action': 'DescribeSnapshots'}
    return _do_compute_request(valid_optional_params, optional_params, mandatory_params)

def create_snapshot(VolumeId, **optional_params):
    """DescribeSnapshots API wrapper."""
    valid_optional_params = ['Name', 'Description']
    mandatory_params = {
        'Action': 'CreateSnapshot',
        'VolumeId': VolumeId,
    }
    return _do_compute_request(valid_optional_params, optional_params, mandatory_params)

def delete_snapshot(SnapshotId):
    """DescribeSnapshots API wrapper."""
    valid_optional_params = []
    optional_params = {}
    mandatory_params = {
        'Action': 'DeleteSnapshot',
        'SnapshotId': SnapshotId,
    }
    return _do_compute_request(valid_optional_params, optional_params, mandatory_params)


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(describe_instances())
    pp.pprint(describe_volumes())
    #pp.pprint(describe_snapshots())
    #pp.pprint(delete_volume('9e501705-6721-4880-abcd-cd4d8bdbf005'))
    #print create_volume(Size=2)
