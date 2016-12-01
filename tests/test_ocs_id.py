#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from ocs_id import *


# +
# function: test_iso_to_mjd()
# -
def test_iso_to_mjd():
    """
        :return: true | false
    """
    iso = ocs_id(True)
    assert iso == ocs_mjd_to_iso(ocs_iso_to_mjd(iso))


# +
# function: test_mjd_to_iso()
# -
def test_mjd_to_iso():
    """
        :return: true | false
    """
    mjd = ocs_id(False)
    assert mjd == ocs_iso_to_mjd(ocs_mjd_to_iso(mjd))


# +
# function: test_accuracy_1()
# -
def test_accuracy_1():
    """
        :return: true | false
    """
    x = ocs_id(True)
    y = ocs_iso_to_mjd(x)
    z = ocs_mjd_to_iso(y)
    conversion_error = float(y) - float(ocs_iso_to_mjd(z))
    assert conversion_error == 0.0


# +
# function: test_accuracy_2()
# -
def test_accuracy_2():
    """
        :return: true | false
    """
    x = ocs_id(False)
    y = ocs_mjd_to_iso(x)
    z = ocs_iso_to_mjd(y)
    conversion_error = float(x) - float(ocs_iso_to_mjd(y))
    assert conversion_error == 0.0

