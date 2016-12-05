#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from lxml import etree
from OcsExceptions import *
import glob
import sys


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Functions for validating XML files in the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "ocs_xml.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: ocs_xml_get_parser()
# -
def ocs_xml_get_parser(xs=''):
    """
        :param xs: XML schema file
        :return: returns a parser object or raises an exception
    """

    # read in the schema
    try:
        with open(xs, 'rb') as f:
            sroot = etree.XML(f.read())
    except IOError as n:
        raise OcsXmlException(OCS_XML_ERROR_NOXSD, n)

    # return parser object
    xml_retval = etree.XMLParser(schema=etree.XMLSchema(sroot))
    if xml_retval:
        return xml_retval
    else:
        raise OcsXmlException(OCS_XML_ERROR_NOPRS, str(xs))


# +
# function: ocs_xml_validate()
# -
def ocs_xml_validate(xs='', xf=''):
    """
        :param xs: input schema
        :param xf: input XML file to validate
        :return: True if file validates, False otherwise
    """

    # validate the file against the schema
    try:
        with open(xf, 'rb') as f:
            etree.fromstring(f.read(), xs)
    except IOError:
        raise OcsXmlException(OCS_XML_ERROR_NOXML, str(xf))
    except etree.XMLSchemaError:
        return False
    return True


# +
# main()
# -
if __name__ == '__main__':

    # add parser
    parser = argparse.ArgumentParser()

    # add argument(s) that require a parameter value
    parser.add_argument("-s", "--xsdfile", help="input XSD file")
    parser.add_argument("-f", "--xmlfile", help="input XML file")

    # parse the command line arguments
    args = parser.parse_args()

    # continue if all command line arguments are present
    if args.xsdfile and args.xmlfile:

        # validate xml file using schema
        try:
            ocs_xml_validate(ocs_xml_get_parser(args.xsdfile), args.xmlfile)
            print(args.xmlfile+' validates against '+args.xsdfile)
        except OcsXmlException as m:
            print(m.errstr)
            print(args.xmlfile+' does not validate against '+args.xsdfile)

    else:
        print('No command line arguments specified')
        print('Use: python ' + sys.argv[0] + ' --help for more information')

