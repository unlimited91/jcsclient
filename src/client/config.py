# File to contain all the configuration values. Note that this is a python
# file, so make sure you follow Python syntax throughout this file

is_secure=False
keystone_token_url='https://iam.ind-west-1.staging.jiocloudservices.com:5000/v3/auth/tokens'
compute_url = 'http://10.140.214.69'
compute_url = 'https://compute.ind-west-1.staging.jiocloudservices.com/services/Cloud/'
vpc_url = 'https://vpc.ind-west-1.staging.jiocloudservices.com'

access_key = '67e4d6080c884d3382cc43aa5c52d963' # random dummy value
secret_key = '71dc96bc558944b9824d30f4ca7aea42' # random dummy value

# TODO(rushiagr): take username, account id and password as config values, and
# write api call to generate access and secret for the same account

# You can add same configs below so that you can override the above values with
# new ones
