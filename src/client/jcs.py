
import json

import requests


# Example curl request:
# curl --insecure -i -H "Content-Type: application/json" -d '{"auth": {"identity": {"methods": ["password"], "password": {"user": {"name": "rds", "account": {"id": "0bc437d91ce3401fa0fc97366a11ba3b" }, "password": "Reliance111@"}}}}}' https://iam.ind-west-1.staging.jiocloudservices.com:5000/v3/auth/tokens

def get_token():
    """
    Returns token as a dictionary.

    Keys are
        'token': the actual token string
        'expires_at': time at which the token expires, as a string for now
        'user_id': user or owner id as specified in the original HTTP request
    """
    # TODO(rushiagr): make expires_at a datetime.datetime object
    # TODO(rushiagr): add logic for reusing token if token is not expired
    data_dict = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": rds_user_name,
                        "account": {
                            "id": rds_account_id,
                            },
                        "password": rds_user_password,
                    }
                }
            }
        }
    }

    header_dict = {'Content-Type': 'application/json'}

    response = requests.post(keystone_token_url,
        data=json.dumps(data_dict),
        headers=header_dict,
        verify=is_secure,
    )

    response_dict = {
        'token': response.headers['X-Subject-Token'],
        'expires_at': response.json()['expires_at'],
        'user_id': response.json()['user_id'],
    }
    return response_dict

if __name__=='__main__':
    print get_token()
