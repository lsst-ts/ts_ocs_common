#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from OcsExceptions import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Functions for manipulating the SAL in the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "ocs_sal.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# function: ocs_sal_import()
# +
def ocs_sal_import(module=''):
    """
        :param module: name of module to be imported
        :return: None or reference to imported object
    """

    # declare some variable(s) and initialize them
    sal_retval = None

    # check input module name
    if not isinstance(module, str) or module == '':
        return sal_retval

    # try to import the named module
    try:
        sal_retval = __import__(module)
    except ImportError:
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOMOD, "import('{0:s}')".format(module))

    # return object or None
    return sal_retval


# +
# function: ocs_sal_attribute()
# +
def ocs_sal_attribute(sal_object=None, attribute=''):
    """
        :param sal_object: a valid SAL object (returned from ocs_sal_import(), for example)
        :param attribute: an attribute of the input SAL object
        :return: None or reference to attribute object
    """

    # declare some variable(s) and initialize them
    sal_retval = None

    # check input sal_object
    if sal_object is None or not isinstance(attribute, str) or attribute == '':
        return sal_retval

    # try to getattr the named attribute
    try:
        sal_retval = getattr(sal_object, attribute)
    except AttributeError:
        raise OcsGenericEntityException(
            OCS_GENERIC_ENTITY_ERROR_NOATT, "getattr('{0:s}', '{1:s}')".format(sal_object.__name__, attribute))

    # return object or None
    return sal_retval


# +
# main()
# -
if __name__ == "__main__":

    # add parser
    parser = argparse.ArgumentParser()

    # add argument(s) that require a parameter value
    parser.add_argument("-m", "--module", help="input SAL module")
    parser.add_argument("-a", "--attribute", help="input SAL module attribute")

    # parse the command line arguments
    args = parser.parse_args()

    # load the sal module
    so = None
    if args.module:
        try:
            so = ocs_sal_import(args.module)
        except OcsGenericEntityException as e:
            print(e.errstr)
        else:
            print('Imported module {0:s} OK'.format(args.module))

        # load attribute
        if args.attribute and so:
            mo = None
            try:
                mo = ocs_sal_attribute(so, args.attribute)
            except OcsGenericEntityException as e:
                print(e.errstr)
            else:
                print('Got attribute {0:s} OK'.format(args.attribute))
    else:
        print('Insufficient command line arguments specified')
        print('Use: python ' + sys.argv[0] + ' --help for more information')

