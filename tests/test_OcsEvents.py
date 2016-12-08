#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from OcsEvents import *
from ocs_id import *


# +
# function: test_instantiate()
# -
def test_instantiate():
    evh = None
    try:
        evh = OcsEvents(False)
    except OcsEcentsException as a:
        print(a.errstr)
        assert False
    if evh is not None:
        assert True

# +
# function: test_send_event()
# -
def test_send_event():
    evh = None
    try:
        evh = OcsEvents(False)
    except OcsEcentsException as a:
        print(a.errstr)
        assert False

    if evh is not None:
        ocsid = ocs_id(False)
        evh.sendEvent('ocsEntityStartup', Name='Test', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)
        assert True

