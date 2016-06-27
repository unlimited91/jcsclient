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

import sys
from jcsclient import utils
from jcsclient.utils import SUCCESS
from jcsclient.utils import FAILURE
from jcsclient import help
from jcsclient import exception
from jcsclient import config
from jcsclient.constants import ERROR_STRING
from jcsclient import output

def main(args = sys.argv):
    """
    Entry point for the cli

    params args: Command line arguments passed to the function

    Format for any api : jcs command subcommand
    """

    try:
        # As stated above, the first argument would be the 
        # cli binary path. Pop the first argument.
        args = args[1:]
        config.setup_config_handler(args)
        if 'help' in args:
            help.Helper().show(args)
            return SUCCESS

        service_name = args[0]
        service = utils.load_service(service_name)
        controller = utils.create_controller(service, service_name)
        command = utils.dash_to_underscore(args[1])
        method = utils.get_module_method(controller, command,
                                         service_name)
        result = method(args[1:])
        return output.format_result(result)
    except IndexError as ie:
        msg = 'Incorrect number/order of arguments received'
        sys.stderr.write('usage: %s\n' % ERROR_STRING)
        sys.stderr.write(msg)
        sys.stderr.write("\n")
        return FAILURE
    except exception.UnknownCredentials as ue:
        sys.stderr.write(str(ue))
        sys.stderr.write("\n")
        return FAILURE
    except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.write("\n")
        if config.check_debug():
            raise
        return FAILURE
        
