#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from ocs_common import *
from astropy.time import Time
import argparse
import re
import sys


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Functions for manipulating identifiers in the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "ocs_id.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: ocs_id()
# -
def ocs_id(date_flag=False):
    """
        :param date_flag: if date_flag==True, returns an ISO-8660 string, if date_flag==False, returns a MJD string
        :return: string representation of a date
    """
    if isinstance(date_flag, bool) and date_flag:
        return Time.now().iso.replace(' ', 'T')
    else:
        return ocs_iso_to_mjd(Time.now().iso)


# +
# function: ocs_iso_to_mjd()
# +
def ocs_iso_to_mjd(iso_string=''):
    """
        :param iso_string: input ISO-8660 date
        :return: string representation of date_string as MJD
    """
    if not isinstance(iso_string, str) or iso_string == '':
        return ''
    else:
        return '{0:23.17f}'.format(Time(str(iso_string)).mjd)


# +
# function: ocs_mjd_to_iso()
# +
def ocs_mjd_to_iso(mjd_string=''):
    """
        :param mjd_string: input MJD date
        :return: string representation of mjd_string as ISO-8660
    """
    if not isinstance(mjd_string, str) or mjd_string == "":
        return ''
    else:
        return Time(float(mjd_string) + 2400000.5, format='jd', precision=3).iso.replace(' ', 'T')


# +
# main()
# -
if __name__ == "__main__":

    # add parsers
    parser = argparse.ArgumentParser()

    # add exclusive group
    group = parser.add_mutually_exclusive_group()

    # add argument(s) that require a parameter value
    parser.add_argument("-c", "--convert", help="convert CONVERT = { ISO | MJD } string to other format")

    # add exclusive argument(s)
    group.add_argument('-a', '--ascii', action="store_true", help="return an ISO8660 date string from the current time")
    group.add_argument('-d', '--digital', action="store_true", help="return a MJD string from the current time")
    group.add_argument('-i', '--iso', action="store_true", help="return an ISO8660 date string from the current time")
    group.add_argument('-m', '--mjd', action="store_true", help="return a MJD string from the current time")

    # parse the command line arguments
    args = parser.parse_args()

    # if -a or --ascii or -i or --iso is specified on the command line, return an ISO8668 string
    if args.ascii or args.iso:
        print(ocs_id(True))

    # handle -c or --convert, convert the supplied argument if it is recognized
    elif args.convert:
        amatch = re.search(ISO_PATTERN, args.convert)
        dmatch = re.search(MJD_PATTERN, args.convert)
        if amatch or dmatch:
            if amatch:
                print(args.convert + ' = ' + ocs_iso_to_mjd(args.convert))
            elif dmatch:
                print(args.convert + ' = ' + ocs_mjd_to_iso(args.convert))
        else:
            print('ERROR> Unrecognized input value, ' + args.convert)

    # if -d or --digital or -m or --mjd is specified on the command line, return a MJD string
    elif args.digital or args.mjd:
        print(ocs_id(False))

    # nothing specified on the command line
    else:
        print('No command line arguments specified')
        print('Use: python ' + sys.argv[0] + ' --help for more information')

