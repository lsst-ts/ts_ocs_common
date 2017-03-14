#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from ocs_sal import *

# +
# __doc__ string
# _
__doc__ = """test of ocs_sal"""


# +
# function: test_sal_import()
# -
def test_sal_import():
    """
        :return: true | false
    """
    sio = None
    try:
        sio = ocs_sal_import('SALPY_camera')
    except OcsGenericEntityException as m:
        print(m.errstr)
    if sio is None:
        assert False
    else:
        assert True


# +
# function: test_sal_noimport()
# -
def test_sal_noimport():
    """
        :return: true | false
    """
    sno = None
    try:
        sno = ocs_sal_import('SALPY_nosuchmodule')
    except OcsGenericEntityException as m:
        print(m.errstr)
    if sno is None:
        assert True
    else:
        assert False


# +
# function: test_sal_attribute()
# -
def test_sal_attribute():
    """
        :return: true | false
    """
    mio = None
    try:
        mio = ocs_sal_attribute(ocs_sal_import('SALPY_camera'), 'SAL_camera')
    except OcsGenericEntityException as n:
        print (n.errstr)
    if mio is None:
        assert False
    else:
        assert True


# +
# function: test_sal_noattribute()
# -
def test_sal_noattribute():
    """
        :return: true | false
    """
    mno = None
    try:
        mno = ocs_sal_attribute(ocs_sal_import('SALPY_camera'), 'SAL_noattribute')
    except OcsGenericEntityException as n:
        print(n.errstr)
    if mno is None:
        assert True
    else:
        assert False
