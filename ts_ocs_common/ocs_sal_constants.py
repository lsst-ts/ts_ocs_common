#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/ocs_sal_constants.py, contains contains the ts_sal constants in Python
format. It is generated, automatically, by $TS_OCS_COMMON_BIN/ocs_sal_get_constants.sh which, in turn,
calls $TS_OCS_COMMON_SRC/ocs_get_sal_constants.py.
Import:

    from ocs_sal_constants import *

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__email__ = "pdaly@lsst.org"
__file__ = "ocs_sal_constants.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# SAL constant(s)
# -
SAL__OK = 0
SAL__ERR = -1
SAL__ERROR = -1
SAL__EVENT_INFO = 200
SAL__EVENT_WARN = -200
SAL__EVENT_ERROR = -201
SAL__EVENT_ABORT = -202
SAL__CMD_ACK = 300
SAL__CMD_INPROGRESS = 301
SAL__CMD_STALLED = 302
SAL__CMD_COMPLETE = 303
SAL__CMD_NOPERM = -300
SAL__CMD_NOACK = -301
SAL__CMD_FAILED = -302
SAL__CMD_ABORTED = -303
SAL__CMD_TIMEOUT = -304
