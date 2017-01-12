#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsLogger import *


# +
# function: test_logger()
# -
def test_logger():
    log = OcsLogger()
    if log:
        assert True
    else:
        assert False


# +
# function: test_change_name()
# -
def test_change_name():
    log = OcsLogger()
    if not log:
        assert False
    else:
        try:
            log.name = 'JUNK'
        except:
            assert True


# +
# function: test_change_subname()
# -
def test_change_subname():
    log = OcsLogger()
    if not log:
        assert False
    else:
        try:
            log.subname = 'Junk'
        except:
            assert True


