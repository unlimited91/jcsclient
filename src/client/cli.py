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

def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """
    if len(argv) < 3:
        print "Example usage: jcs compute Action=DescribeInstances\n"
        print "First argument can be 'compute' or 'vpc'"
        sys.exit(1)
    common.curlify(argv[1], argv[2])
    return 0
