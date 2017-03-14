#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsExceptions import *
import argparse
import re
import sys


# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/ocs_get_sal_constants.py, contains the code to search the ts_sal
include file(s) to extract defined constants within that system as it does not appear to be done
anywhere else. In future, this file may be superceded by an include file provided by ts_sal itself.
This file should not be imported as it is called only once, at installation time, by
$TS_OCS_COMMON_BIN/ocs_sal_get_contants.sh and writes out the file
$TS_OCS_COMMON_SRC/ocs_sal_constants.py which should be imported by other components.

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
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
        raise OcsGeneralException(OCS_GENERAL_ERROR_NOFIL, "sal_include='{0:s}'".format(str(sal_include)))

    elif not isinstance(output_file, str) or output_file == '':
        raise OcsGeneralException(OCS_GENERAL_ERROR_NOFIL, "output_file='{0:s}'".format(str(output_file)))

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
    except IOError as e1:
        print(e1)

    # write the output file
    try:
        with open(output_file, 'wb') as f:

            # write out the header boilerplate
            f.write('#!/usr/bin/env python\n')
            f.write('# -*- coding: utf-8 -*-\n')
            f.write('\n')
            f.write('\n')
            f.write('# +\n')
            f.write('# __doc__ string\n')
            f.write('# -\n')
            f.write('__doc__ = """\n')
            f.write('\n')
            f.write('This file, $TS_OCS_COMMON_SRC/ocs_sal_constants.py, contains contains the ts_sal constants in Python\n')
            f.write('format. It is generated, automatically, by $TS_OCS_COMMON_BIN/ocs_sal_get_constants.sh which, in turn,\n')
            f.write('calls $TS_OCS_COMMON_SRC/ocs_get_sal_constants.py.\n')
            f.write('Import:\n')
            f.write('\n')
            f.write('    from ocs_sal_constants import *\n')
            f.write('\n')
            f.write('"""\n')
            f.write('\n')
            f.write('\n')
            f.write('# +\n')
            f.write('# dunder string(s)\n')
            f.write('# -\n')
            f.write('__author__ = "Philip N. Daly"\n')
            f.write('__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."\n')
            f.write('__date__ = "31 October 2016"\n')
            f.write('__email__ = "pdaly@lsst.org"\n')
            f.write('__file__ = "ocs_sal_constants.py"\n')
            f.write('__history__ = __date__ + ": " + "original version (" + __email__ + ")"\n')
            f.write('__version__ = "0.1.0"\n')
            f.write('\n')
            f.write('\n')
            f.write('# +\n')
            f.write('# SAL constant(s)\n')
            f.write('# -\n')

            # write out the contants from the contents list
            if contents:
                for elem in contents:
                    f.write(str(elem)+'\n')
    except IOError as e2:
        print(e2)


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
