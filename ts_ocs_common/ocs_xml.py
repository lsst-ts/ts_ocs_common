#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from lxml import etree
from OcsExceptions import *
import argparse
import sys


# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/ocs_xml.py, contains code for validating XML files against a given
schema. It uses argparse to provide a command line interface as demonstrated in
$TS_OCS_COMMON_BIN/ocs_xml.sh

Import:

    from ocs_xml import *

API:

    ocs_xml_get_parser(xs=''):
        returns a parser object for the input schema, xs, otherwise raises an OcsXmlException

    ocs_xml_validate(xs='', xf='')
        validates the input file, xf, against the schema, xs, and returns True if successful, False otherwise

CLI:

    python $TS_OCS_COMMON_SRC/ocs_xml.py --help
    usage: ocs_xml.py [-h] [-s XSDFILE] [-f XMLFILE]

    optional arguments:
      -h, --help            show this help message and exit
      -s XSDFILE, --xsdfile XSDFILE
                            input XSD file
      -f XMLFILE, --xmlfile XMLFILE
                            input XML file

    python $TS_OCS_COMMON_SRC/ocs_xml.py -h
    usage: ocs_xml.py [-h] [-s XSDFILE] [-f XMLFILE]

    optional arguments:
      -h, --help            show this help message and exit
      -s XSDFILE, --xsdfile XSDFILE
                            input XSD file
      -f XMLFILE, --xmlfile XMLFILE
                            input XML file

    Examples:

    python $TS_OCS_COMMON_SRC/ocs_xml.py --xsdfile=$TS_OCS_COMMON_XSD/ocs.xsd --xmlfile=$TS_OCS_COMMON_XML/test_ccs.xml
    $TS_OCS_COMMON_XML/test_atecs.xml validates against $TS_OCS_COMMON_XSD/ocs.xsd

    python $TS_OCS_COMMON_SRC/ocs_xml.py -s=$TS_OCS_COMMON_XSD/ocs.xsd -f=$TS_OCS_COMMON_XML/test_visit.xml
    $TS_OCS_COMMON_XML/test_visit.xml validates against $TS_OCS_COMMON_XSD/ocs.xsd

    For further examples, see $TS_OCS_COMMON_BIN/ocs_xml.sh

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
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
