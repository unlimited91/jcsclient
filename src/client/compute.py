from client import common

from client import config

print common.requestify(config.compute_url, 'Action=DescribeInstances')
