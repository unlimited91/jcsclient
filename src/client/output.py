# Copyright (c) 2016 Jiocloud.com, Inc. or its affiliates.  All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import json
import pprint
import xmltodict
import requests
from client.utils import SUCCESS

class OutputFormat(object):
    """
    Class to handle how the response from the APIs would be processed
    and displayed to the user.

    Currently there is no command line option to configure how the
    output would be displayed. Thus, there is no __init__() function.
    As the cli is enhanced, this section would be made configurable.
    """
    def display(self, response):
        resp_json = ""
        try:
            resp_dict = dict()
            if response is not '':
                resp_dict = json.loads(response.content)
                resp_json = json.dumps(resp_dict, indent=4, sort_keys=True)
        except:
            try:
                resp_dict = dict()
                resp_ordereddict = xmltodict.parse(response.content)
                resp_json = json.dumps(resp_ordereddict, indent=4,
                                       sort_keys=True)
                resp_dict = json.loads(resp_json)
                resp_json = resp_json.replace("\\n", "\n")
                resp_json = resp_json.replace("\\", "")
                print(resp_json)
            except:
                msg = ("Issue with displaying the output. Please raise a"
                      " request for customer support.")
                raise IOError(msg)

def format_result(response):
    output_formatter = OutputFormat()
    output_formatter.display(response)
    if response.status_code != 200:
        response.raise_for_status()
    else:
        return SUCCESS
