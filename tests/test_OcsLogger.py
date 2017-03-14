#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsExceptions import *
from OcsLogger import *


# +
# __doc__ string
# _
__doc__ = """test of OcsLogger"""


# +
# function: test_logger()
# -
def test_logger():
    my_log = OcsLogger()
    if my_log:
        assert True
    else:
        assert False


# +
# function: test_change_name()
# -
def test_change_name():
    my_log = OcsLogger()
    if not my_log:
        assert False
    else:
        try:
            my_log._name = 'JUNK'
        except OcsGeneralException:
            assert True


# +
# function: test_change_subname()
# -
def test_change_subname():
    my_log = OcsLogger()
    if not my_log:
        assert False
    else:
        try:
            my_log._subname = 'Junk'
        except OcsGeneralException:
            assert True
