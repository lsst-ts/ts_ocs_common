#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
import argparse
import re
import sys


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Functions for getting the SAL constants in the Python OCS components"""
__email__ = "pdaly@lsst.org"
__file__ = "ocs_get_sal_constants.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: ocs_get_sal_constants()
# -
def ocs_get_sal_constants(sal_include='', output_file=''):
    """
        :param sal_include: SAL include file
        :param output_file: SAL output Python file
        :return: returns populated output file
    """

    if not isinstance(sal_include, str) or sal_include == '':
        print('Cannot find or input read file!')

    elif not isinstance(output_file, str) or output_file == '':
        print('Cannot write to null or empty output file!')

    else:

        # declare some variables and initialize them
        contents = []
        patterns = [
            r'#define\sSAL__OK',
            r'#define\sSAL__ERR',
            r'#define\sSAL__EVENT',
            r'#define\sSAL__CMD'
            ]

        # get and parse the input file
        try:
            with open(sal_include, 'rb') as f:
                for line in f:
                    for patt in patterns:
                        if re.search(patt, line):
                            _def, _var, _val = line.split()
                            contents.append(_var + ' = ' + _val)
        except IOError as e:
            print(e.errstr)

        # write the output file
        try:
            with open(output_file, 'wb') as f:

               # write out the header boilerplate
               f.write('#!/usr/bin/env python\n')
               f.write('# -*- coding: utf-8 -*-\n\n')
               f.write('# +\n')
               f.write('# Python 2.x -> 3.x compatability function(s)\n')
               f.write('# -\n')
               f.write('from __future__ import print_function\n\n')
               f.write('# +\n')
               f.write('# dunder string(s)\n')
               f.write('# -\n')
               f.write('__author__ = \"Philip N. Daly\"\n')
               f.write('__copyright__ = u\"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."\n')
               f.write('__date__ = \"31 October 2016\"\n')
               f.write('__doc__ = \"\"\"SAL constatnts for Python in the OCS\"\"\"\n')
               f.write('__email__ = \"pdaly@lsst.org\"\n')
               f.write('__file__ = \"ocs_sal_constants.py\"\n')
               f.write('__history__ = __date__ + \": \" + \"original version (\" + __email__ + \")\"\n')
               f.write('__version__ = \"0.1.0\"\n\n')
               f.write('# +\n')
               f.write('# SAL constant(s)\n')
               f.write('# -\n')

               # write out the contants from the contents list
               if contents:
                   for elem in contents:
                       f.write(elem+'\n')
        except IOError as e:
            print(e.errstr)


# +
# main()
# -
if __name__ == '__main__':

    # add parser
    parser = argparse.ArgumentParser()

    # add argument(s) that require a parameter value
    parser.add_argument("-f", "--salfile", help="input SAL include file")
    parser.add_argument("-o", "--output", help="output SAL Python file")

    # parse the command line arguments
    args = parser.parse_args()

    # continue if all command line arguments are present
    if args.salfile and args.output:

        # get constants from old file and write them to a new file
        ocs_get_sal_constants(args.salfile, args.output)

    else:
        print('No command line arguments specified')
        print('Use: python ' + sys.argv[0] + ' --help for more information')
