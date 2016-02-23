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
    # TODO(rushiagr): add filters etc in params.
    request_string = common.requestify(config.compute_url, {'Action': 'DescribeInstances'})
    resp_dict = common.do_request('GET', request_string)
    instances = resp_dict['ListInstancesResponse']['instanceSet']['item']
    if type(instances) == dict:
        instances = [instances]  # Only one instance
    print resp_dict
    return instances

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
        'ImageId': image_id,
        'InstanceTypeId': instance_type_id,
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

def attach_volume():
    """AttachVolume."""
    pass

def create_volume():
    pass

def delete_volume():
    pass

def create_volume():
    pass



if __name__ == '__main__':
    describe_instances()
