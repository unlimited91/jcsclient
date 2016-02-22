from client import common
from client import config


def describe_instances():
    """DescribeInstances API wrapper."""
    # TODO(rushiagr): add filters etc in params.
    request_string = common.requestify(config.compute_url,
                                       'Action=DescribeInstances')
    resp_dict = common.do_request('GET', request_string)
    print resp_dict

describe_instances()
