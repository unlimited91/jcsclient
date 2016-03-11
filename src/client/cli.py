"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mclient` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``client.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``client.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys

from client import common
from client import dss

def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """

    if len(argv) < 3 or argv[1] in ['-h', '--help', 'help']:
        print "Example usage: jcs [--curl|--prettyprint] compute Action=DescribeInstances\n"
        print "               jcs [--curl|--prettyprint] compute 'Action=CreateVolume&Size=1'\n"
        print "               jcs [--curl|--prettyprint] dss     'Action=GetObject' 'Target=bucketname/obj'\n"
        print "Service argument can be 'compute', 'vpc' or 'dss'"
        print "If '--curl' is specified, only curl request input will be"
        print "produced. No request will be made"
        print "If --prettyprint is specified, response of request made will be"
        print "printed using a pretty printer"
        print "DSS Target is the path of the entity you want to address"
        print "It can be just the bucket name, or bucket name followed by object name"
        sys.exit(1)

    ## Separate out DSS workflow
    if argv[2].lower() == "dss" or argv[1].lower() == "dss":
        if argv[2].lower() == "dss":
            if len(argv) >= 5:
                dss.initiate(argv[1], argv[3], argv[4])
            elif len(argv) == 4:
                dss.initiate(argv[1], argv[3], None)
            else:
                print "Not enough args for DSS service!"
                return 0

        elif argv[1].lower() == "dss":
            #dss.initiate("--prettyprint", argv[2], argv[3])
            if len(argv) >= 4:
                dss.initiate("--prettyprint", argv[2], argv[3])
            elif len(argv) == 3:
                dss.initiate("--prettyprint", argv[2], None)
            else:
                #Control will never reach here as help menu gets printed for less than 3 args
                print "Not enough args for DSS service!"
                return 0

    if argv[1] == '--curl' and len(argv) == 4:
        common.curlify(argv[2], argv[3])
    elif argv[1] == '--prettyprint' and len(argv) == 4:
        common.curlify(argv[2], argv[3], False, True, True)
    elif len(argv) == 3 and '=' in argv[2]:
        common.curlify(argv[1], argv[2], False, True)
    elif len(argv) >= 3:
        common.curlify(argv[1], argv[2:], True, True)
    else:
        print "Invalid client request"
    return 0
