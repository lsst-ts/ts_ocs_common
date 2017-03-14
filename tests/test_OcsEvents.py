#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsEvents import *
from ocs_id import *


# +
# __doc__ string
# _
__doc__ = """test of OcsEvents"""


# +
# function: test_instantiate()
# -
def test_instantiate():
    try:
        ev = OcsEvents(False)
    except OcsEventsException as a:
        print(a.errstr)
        assert False
    if ev is not None:
        assert True


# +
# function: test_send_event()
# -
def test_send_event():
    try:
        ev = OcsEvents(False)
    except OcsEventsException as a:
        print(a.errstr)
        assert False

    if ev is not None:
        ocsid2 = ocs_id(False)
        ev.send_event(
            'ocsEntityStartup',
            Name='Test',
            Identifier=float(ocsid2),
            Timestamp=ocs_mjd_to_iso(ocsid2),
            Address=id(ev),
            priority=SAL__EVENT_INFO)
        assert True
