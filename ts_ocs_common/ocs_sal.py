#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsExceptions import *
import argparse


# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/ocs_sal.py, contains code for importing and retrieving attributes of
ts_sal code. It uses argparse to provide a command line interface as demonstrated in
$TS_OCS_COMMON_BIN/ocs_sal.sh.

Import:

    from ocs_sal import *

API:

    ocs_sal_import(module='')
        if module='', returns None. If module!='' returns the object = __import(module)__.
        If the specified module cannot be imported, raises an OcsGenericEntityException

    ocs_sal_attribute(sal_object=None, attribute='')
        if the input arguments are invalid, returns None. If the inputs are valid, returns the
        object = getattr(sal_object, attribute). On error, raises an OcsGenericEntityException

CLI:

    python $TS_OCS_COMMON_SRC/ocs_sal.py --help
    usage: ocs_sal.py [-h] [-m MODULE] [-a ATTRIBUTE]

    optional arguments:
    -h, --help              show this help message and exit
    -m MODULE, --module MODULE
                            input SAL module
    -a ATTRIBUTE, --attribute ATTRIBUTE
                            input SAL module attribute

    python $TS_OCS_COMMON_SRC/ts_ocs_common/ocs_sal.py -h
    usage: ocs_sal.py [-h] [-m MODULE] [-a ATTRIBUTE]

    optional arguments:
    -h, --help              show this help message and exit
    -m MODULE, --module MODULE
                            input SAL module
    -a ATTRIBUTE, --attribute ATTRIBUTE
                            input SAL module attribute

    Examples:

    python $TS_OCS_COMMON_SRC/ocs_sal.py --module=SALPY_camera --attribute=SAL_camera
    Imported module SALPY_camera OK
    Got attribute SAL_camera OK

    python $TS_OCS_COMMON_SRC/ocs_sal.py -m=SALPY_camera -a=SAL_camera
    Imported module SALPY_camera OK
    Got attribute SAL_camera OK

    For further examples, see $TS_OCS_COMMON_BIN/ocs_sal.sh

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
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
