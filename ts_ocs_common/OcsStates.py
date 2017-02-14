#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from ocs_common import *
from ocs_id import *
from ocs_sal import *
from OcsExceptions import *
from OcsLogger import *

import threading

# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "13 February 2017"
__doc__ = """States class for the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsStates.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsStates() inherits from the object class
# -
class OcsStates(object):

    # +
    # method: __init__
    # -
    def __init__(self):
        """
            :return: None or object representing the state
        """

        # declare some variables and initialize them
        self._previous_state = OCS_SUMMARY_STATE_UNKNOWN
        self._current_state = OCS_SUMMARY_STATE_UNKNOWN
        self._shutdown = False
        self._flags = 0
        self._commands = ocsEntitySummaryStateCommands.get(self._current_state, [])
        self._configurations = ocsEntitySummaryStateConfigurations.get(self._current_state, [])
        self._lock = threading.Lock()

        # set up logging
        self.logger = OcsLogger('States', 'ocs').logger
        self.logger.debug("Starting {0:s} {1:s}".format('States', 'ocs'))

    # +
    # method: change_state()
    # -
    def change_state(self, from_state=0, to_state=0):
        self.logger.debug("Entering change_state(from_state={0:s}, to_state={1:s})".format(str(from_state), str(to_state)))
        self.logger.debug("\t changing state from {0:s} to {1:s}".format(ocsEntitySummaryState.get(from_state,'').upper(), ocsEntitySummaryState.get(to_state,'').upper()))

        # check input(s)
        if not isinstance(from_state, int):
            self.logger.error('invalid data type for from_state')
            return
        if not isinstance(to_state, int):
            self.logger.error('invalid data type for to_state')
            return
        if from_state not in ocsEntitySummaryState:
            self.logger.error('invalid data key for from_state')
            return
        if to_state not in ocsEntitySummaryState:
            self.logger.error('invalid data key for to_state')
            return

        # change things around 
        self._lock.acquire()
        try:
            self._previous_state = from_state
            self._current_state = to_state
            self._commands = ocsEntitySummaryStateCommands.get(to_state, [])
            self._configurations = ocsEntitySummaryStateConfigurations.get(to_state, [])
        finally:
            self._lock.release()

        # output some messages
        self.logger.debug('\t self._previous_state={0:s}'.format(ocsEntitySummaryState.get(self._previous_state,'')))
        self.logger.debug('\t self._current_state={0:s}'.format(ocsEntitySummaryState.get(self._current_state,'')))
        self.logger.debug('\t self._commands={0:s}'.format(str(self._commands)))
        self.logger.debug('\t self._configurations={0:s}'.format(str(self._configurations)))
        self.logger.debug("\t changed state from {0:s} to {1:s}".format(ocsEntitySummaryState.get(from_state,'').upper(), ocsEntitySummaryState.get(to_state,'').upper()))
        self.logger.debug("Exiting change_state(from_state={0:s}, to_state={1:s})".format(str(from_state), str(to_state)))
            
    # +
    # method: testBit()
    # -
    def testBit(self, ivalue=0, offset=0):
        """ testBit() returns True if the bit at 'offset' is 1 else returns False """
        if isinstance(ivalue, int) and isinstance(offset, int) and ivalue>=0 and offset>=0:
            self._lock.acquire()
            try:
                mask = 1 << offset
                result = (ivalue & mask)
            finally:
                self._lock.release()
            if result > 0:
                return True
            else:
                return False

    # +
    # method: setBit()
    # -
    def setBit(self, ivalue=0, offset=0):
        """ setBit() returns an integer with the bit at 'offset' set to 1 """
        if isinstance(ivalue, int) and isinstance(offset, int) and ivalue>=0 and offset>=0:
            self._lock.acquire()
            try:
                mask = 1 << offset
                self._flags = (ivalue | mask)
            finally:
                self._lock.release()

    # +
    # method: clearBit()
    # -
    def clearBit(self, ivalue=0, offset=0):
        """ clearBit() returns an integer with the bit at 'offset' cleared """
        if isinstance(ivalue, int) and isinstance(offset, int) and ivalue>=0 and offset>=0:
            self._lock.acquire()
            try:
                mask = ~(1 << offset)
                self._flags = (ivalue & mask)
            finally:
                self._lock.release()

    # +
    # method: toggleBit()
    # -
    def toggleBit(self, ivalue=0, offset=0):
        """ toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0 """
        if isinstance(ivalue, int) and isinstance(offset, int) and ivalue>=0 and offset>=0:
            self._lock.acquire()
            try:
                mask = 1 << offset
                self._flags = (ivalue ^ mask)
            finally:
                self._lock.release()

    # +
    # decorator(s)
    # -
    @property
    def previous_state(self):
        return self._previous_state

    @previous_state.setter
    def previous_state(self, previous_state):
        if isinstance(previous_state, int):
            self._lock.acquire()
            try:
                self._previous_state = previous_state
            finally:
                self._lock.release()

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, current_state):
        if isinstance(current_state, int):
            self._lock.acquire()
            try:
                self._current_state = current_state
            finally:
                self._lock.release()

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, flags):
        pass

    @property
    def shutdown(self):
        return self._shutdown

    @shutdown.setter
    def shutdown(self, shutdown):
        if isinstance(shutdown, bool):
            self._lock.acquire()
            try:
                self._shutdown = shutdown
            finally:
                self._lock.release()

    # +
    # method: __str__
    # -
    def __str__(self):
        return 'OcsStates(previous_state={0:s}, current_state={1:s}, shutdown={2:s}), address {3:s}'.format(
            str(self._previous_state), str(self._current_state), str(self._shutdown), hex(id(self)))


# +
# main()
# -
if __name__ == "__main__":

    states = OcsStates()

    if states:

        # log status
        stalog = states.logger
        stalog.info('{0:s}'.format(states.__str__()))
        stalog.info('states._previous_state={0:s}'.format(str(states._previous_state)))
        stalog.info('states._current_state={0:s}'.format(str(states._current_state)))
        stalog.info('states._commands={0:s}'.format(str(states._commands)))
        stalog.info('states._configurations={0:s}'.format(str(states._configurations)))
        stalog.info('states._shutdown={0:s}'.format(str(states._shutdown)))

        # set some flags
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_ABORT_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_DISABLE_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_ENABLE_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_ENTERCONTROL_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_EXITCONTROL_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_SETVALUE_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_STANDBY_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_START_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_STOP_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_SEQUENCE_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_SCRIPT_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))
        states.setBit(states._flags, OCS_SEQUENCER_SHUTDOWN_OFFSET)
        stalog.info('states._flags={0:s}'.format(str(states._flags)))

        # change state
        states.change_state(OCS_SUMMARY_STATE_OFFLINE, OCS_SUMMARY_STATE_STANDBY)
        states.change_state(OCS_SUMMARY_STATE_STANDBY, OCS_SUMMARY_STATE_DISABLED)
        states.change_state(OCS_SUMMARY_STATE_DISABLED, OCS_SUMMARY_STATE_ENABLED)
        states.change_state(OCS_SUMMARY_STATE_ENABLED, OCS_SUMMARY_STATE_DISABLED)
        states.change_state(OCS_SUMMARY_STATE_DISABLED, OCS_SUMMARY_STATE_STANDBY)
        states.change_state(OCS_SUMMARY_STATE_STANDBY, OCS_SUMMARY_STATE_OFFLINE)
        states.change_state(OCS_SUMMARY_STATE_ENABLED, OCS_SUMMARY_STATE_FAULT)

