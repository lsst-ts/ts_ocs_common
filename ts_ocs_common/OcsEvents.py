#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from ocs_sal_constants import *
from ocs_id import *
from ocs_sal import *
from OcsExceptions import *
from OcsLogger import *
import time


# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/OcsEvents.py, contains code for handling known OCS events.
Python (unit) tests are provided in $TS_OCS_COMMON_TESTS/test_OcsEvents.py or all can be
run from $TS_OCS_COMMON_BIN/test_ocs_common.sh

Import:

    from OcsEvents import *

Example:

    evh = None
    try:
        evh = OcsEvents(False)
    except OcsEventsException as e:
        print(e.errstr)

API:

    send_event(self, event='', **kwargs)
        sends the event specified populated by the payload within kwargs. If no ecent is specified, an
        OcsEventsException is raised,

CLI:

    None

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 December 2016"
__email__ = "pdaly@lsst.org"
__file__ = "OcsEvents.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsEvents() inherits from the object class
# -
class OcsEvents(object):

    # +
    # method: __init__
    # -
    def __init__(self, simulate=True):
        """
            :param simulate: if True, use simulation
            :return: None or object representing the events
        """

        # get arguments(s)
        self._simulate = simulate
        self._system = 'OCS'
        self._component = 'Events'

        # check simulate
        if not isinstance(self._simulate, bool):
            self._simulate = True

        # set up logging
        self.logger = OcsLogger(self._system, self._component).logger
        self.logger.debug("Starting {0:s} {1:s}".format(self._system, self._component))

        # declare some variables and initialize them
        self.__sal_archiver = None
        self.__sal_catchuparchiver = None
        self.__sal_processingcluster = None
        self.__sal_ocs = None
        self.__sal_sequencer = None

        self.__mgr_archiver = None
        self.__mgr_catchuparchiver = None
        self.__mgr_processingcluster = None
        self.__mgr_ocs = None
        self.__mgr_sequencer = None

        self.__address = None
        self.__command_source = None
        self.__command_sent = None
        self.__commands = None
        self.__configurations = None
        self.__current_state = None
        self.__event = None
        self.__executing = None
        self.__method = None
        self.__identifier = None
        self.__match = None
        self.__name = None
        self.__previous_state = None
        self.__priority = None
        self.__return_value = None
        self.__retval = None
        self.__sequence_number = None
        self.__status_value = None
        self.__status = None
        self.__timestamp = None

        # container(s)
        self.__archiverEntitySummaryStateC = None
        self.__catchuparchiverEntitySummaryStateC = None
        self.__processingclusterEntitySummaryStateC = None
        self.__ocsEntitySummaryStateC = None
        self.__sequencerEntitySummaryStateC = None

        self.__archiverEntityStartupC = None
        self.__catchuparchiverEntityStartupC = None
        self.__processingclusterEntityStartupC = None
        self.__ocsEntityStartupC = None
        self.__sequencerEntityStartupC = None

        self.__archiverEntityShutdownC = None
        self.__catchuparchiverEntityShutdownC = None
        self.__processingclusterEntityShutdownC = None
        self.__ocsEntityShutdownC = None
        self.__sequencerEntityShutdownC = None

        self.__ocsCommandIssuedC = None
        self.__sequencerCommandIssuedC = None

        self.__ocsCommandStatusC = None
        self.__sequencerCommandStatusC = None

        # event methods
        self.__event_methods = {
            'archiverEntitySummaryState': self._archiver_entity_summary_state,
            'catchuparchiverEntitySummaryState': self._catchuparchiver_entity_summary_state,
            'processingclusterEntitySummaryState': self._processingcluster_entity_summary_state,
            'ocsEntitySummaryState': self._ocs_entity_summary_state,
            'sequencerEntitySummaryState': self._sequencer_entity_summary_state,
            'archiverEntityStartup': self._archiver_entity_startup,
            'catchuparchiverEntityStartup': self._catchuparchiver_entity_startup,
            'processingclusterEntityStartup': self._processingcluster_entity_startup,
            'ocsEntityStartup': self._ocs_entity_startup,
            'sequencerEntityStartup': self._sequencer_entity_startup,
            'archiverEntityShutdown': self._archiver_entity_shutdown,
            'catchuparchiverEntityShutdown': self._catchuparchiver_entity_shutdown,
            'processingclusterEntityShutdown': self._processingcluster_entity_shutdown,
            'ocsEntityShutdown': self._ocs_entity_shutdown,
            'sequencerEntityShutdown': self._sequencer_entity_shutdown,
            'ocsCommandIssued': self._ocs_command_issued,
            'sequencerCommandIssued': self._sequencer_command_issued,
            'ocsCommandStatus': self._ocs_command_status,
            'sequencerCommandStatus': self._sequencer_command_status
            }

        # import the SAL_archiver (cf. from SALPY_archiver import *)
        mname = 'SALPY_archiver'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__sal_archiver = ocs_sal_import(mname)
        if self.__sal_archiver:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # import the SAL_catchuparchiver (cf. from SALPY_catchuparchiver import *)
        mname = 'SALPY_catchuparchiver'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__sal_catchuparchiver = ocs_sal_import(mname)
        if self.__sal_catchuparchiver:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # import the SAL_processingcluster (cf. from SALPY_processingcluster import *)
        mname = 'SALPY_processingcluster'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__sal_processingcluster = ocs_sal_import(mname)
        if self.__sal_processingcluster:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # import the SAL_ocs (cf. from SALPY_ocs import *)
        mname = 'SALPY_ocs'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__sal_ocs = ocs_sal_import(mname)
        if self.__sal_ocs:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # import the SAL_sequencer (cf. from SALPY_sequencer import *)
        mname = 'SALPY_sequencer'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__sal_sequencer = ocs_sal_import(mname)
        if self.__sal_sequencer:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # get mgr object (cf. mgr = SAL_archiver())
        aname = 'SAL_archiver'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__sal_archiver, aname)
        if mgr:
            self.__mgr_archiver = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get mgr object (cf. mgr = SAL_catchuparchiver())
        aname = 'SAL_catchuparchiver'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__sal_catchuparchiver, aname)
        if mgr:
            self.__mgr_catchuparchiver = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get mgr object (cf. mgr = SAL_processingcluster())
        aname = 'SAL_processingcluster'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__sal_processingcluster, aname)
        if mgr:
            self.__mgr_processingcluster = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get mgr object (cf. mgr = SAL_ocs())
        aname = 'SAL_ocs'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__sal_ocs, aname)
        if mgr:
            self.__mgr_ocs = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get mgr object (cf. mgr = SAL_sequencer())
        aname = 'SAL_sequencer'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__sal_sequencer, aname)
        if mgr:
            self.__mgr_sequencer = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get data structure(s) (cf. data = ocs_logevent_ocsEntityStartupC())
        self.__archiverEntitySummaryStateC = self._get_sal_log_c(
            self.__sal_archiver, 'archiver_logevent_archiverEntitySummaryStateC')
        self.__catchuparchiverEntitySummaryStateC = self._get_sal_log_c(
            self.__sal_catchuparchiver, 'catchuparchiver_logevent_catchuparchiverEntitySummaryStateC')
        self.__processingclusterEntitySummaryStateC = self._get_sal_log_c(
            self.__sal_processingcluster, 'processingcluster_logevent_processingclusterEntitySummaryStateC')
        self.__ocsEntitySummaryStateC = self._get_sal_log_c(
            self.__sal_ocs, 'ocs_logevent_ocsEntitySummaryStateC')
        self.__sequencerEntitySummaryStateC = self._get_sal_log_c(
            self.__sal_sequencer, 'sequencer_logevent_sequencerEntitySummaryStateC')

        self.__archiverEntityStartupC = self._get_sal_log_c(
            self.__sal_archiver, 'archiver_logevent_archiverEntityStartupC')
        self.__catchuparchiverEntityStartupC = self._get_sal_log_c(
            self.__sal_catchuparchiver, 'catchuparchiver_logevent_catchuparchiverEntityStartupC')
        self.__processingclusterEntityStartupC = self._get_sal_log_c(
            self.__sal_processingcluster, 'processingcluster_logevent_processingclusterEntityStartupC')
        self.__ocsEntityStartupC = self._get_sal_log_c(
            self.__sal_ocs, 'ocs_logevent_ocsEntityStartupC')
        self.__sequencerEntityStartupC = self._get_sal_log_c(
            self.__sal_sequencer, 'sequencer_logevent_sequencerEntityStartupC')

        self.__archiverEntityShutdownC = self._get_sal_log_c(
            self.__sal_archiver, 'archiver_logevent_archiverEntityShutdownC')
        self.__catchuparchiverEntityShutdownC = self._get_sal_log_c(
            self.__sal_catchuparchiver, 'catchuparchiver_logevent_catchuparchiverEntityShutdownC')
        self.__processingclusterEntityShutdownC = self._get_sal_log_c(
            self.__sal_processingcluster, 'processingcluster_logevent_processingclusterEntityShutdownC')
        self.__ocsEntityShutdownC = self._get_sal_log_c(
            self.__sal_ocs, 'ocs_logevent_ocsEntityShutdownC')
        self.__sequencerEntityShutdownC = self._get_sal_log_c(
            self.__sal_sequencer, 'sequencer_logevent_sequencerEntityShutdownC')

        self.__ocsCommandIssuedC = self._get_sal_log_c(self.__sal_ocs, 'ocs_logevent_ocsCommandIssuedC')
        self.__sequencerCommandIssuedC = self._get_sal_log_c(
            self.__sal_sequencer, 'sequencer_logevent_sequencerCommandIssuedC')
 
        self.__ocsCommandStatusC = self._get_sal_log_c(self.__sal_ocs, 'ocs_logevent_ocsCommandStatusC')
        self.__sequencerCommandStatusC = self._get_sal_log_c(
            self.__sal_sequencer, 'sequencer_logevent_sequencerCommandStatusC')

        # set up a default event (cf. mgr.salEvent("archiver_logevent_archiverEntityStartup"))
        cname = 'archiver_logevent_archiverEntityStartup'
        if self.__mgr_archiver:
            self.__mgr_archiver.salEvent(cname)

        # set up a default event (cf. mgr.salEvent("catchuparchiver_logevent_catchuparchiverEntityStartup"))
        cname = 'catchuparchiver_logevent_catchuparchiverEntityStartup'
        if self.__mgr_catchuparchiver:
            self.__mgr_catchuparchiver.salEvent(cname)

        # set up a default event (cf. mgr.salEvent("processingcluster_logevent_processingclusterEntityStartup"))
        cname = 'processingcluster_logevent_processingclusterEntityStartup'
        if self.__mgr_processingcluster:
            self.__mgr_processingcluster.salEvent(cname)

        # set up a default event (cf. mgr.salEvent("ocs_logevent_ocsEntityStartup"))
        cname = 'ocs_logevent_ocsEntityStartup'
        if self.__mgr_ocs:
            self.__mgr_ocs.salEvent(cname)

        self.logger.debug("Started {0:s} {1:s} ok".format(self._system, self._component))

    # +
    # (hidden) method: _get_sal_log_c()
    # -
    def _get_sal_log_c(self, salobj=None, event=''):
        self.logger.debug("Getting attribute {0:s}".format(event))
        s = ocs_sal_attribute(salobj, event)
        if s:
            self.logger.debug("Got attribute {0:s} ok".format(event))
            return s()
        else:
            return None

    # +
    # method: send_event()
    # -
    def send_event(self, event='', **kwargs):

        # entry message
        self.logger.debug("send_event() enter")

        # check input(s)
        if not isinstance(event, str) or event == '':
            raise OcsEventsException(OCS_EVENTS_ERROR_NOVAL, "event={0:s}".format(str(event)))
        else:
            self.__event = event

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("send_event(), in simulation with sleep={0:s}".format(str(stime)))

        # invoke method
        else:
            self.__method = self.__event_methods.get(self.__event, None)
            if self.__method:
                self.__method(**kwargs)

        # exit message
        self.logger.debug("send_event() exit")

    # +
    # (hidden) method: _archiver_entity_summary_state()
    # -
    def _archiver_entity_summary_state(self, **kwargs):

        # entry message
        self.logger.debug("_archiver_entity_summary_state() enter")

        if self.__mgr_archiver and self.__archiverEntitySummaryStateC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__commands = kwargs.get('CommandsAvailable', '')
            self.__configurations = kwargs.get('ConfigurationsAvailable', '')
            self.__current_state = kwargs.get('CurrentState', 'UNKNOWN')
            self.__executing = kwargs.get('Executing', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__previous_state = kwargs.get('PreviousState', 'UNKNOWN')
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = archiver_logevent_archiverEntitySummaryState() etc)
            # self.__archiverEntitySummaryStateC.Address = int(self.__address)
            self.__archiverEntitySummaryStateC.Address = int(0)
            self.__archiverEntitySummaryStateC.CommandsAvailable = str(self.__commands)
            self.__archiverEntitySummaryStateC.ConfigurationsAvailable = str(self.__configurations)
            self.__archiverEntitySummaryStateC.CurrentState = str(self.__current_state)
            self.__archiverEntitySummaryStateC.Executing = str(self.__executing)
            self.__archiverEntitySummaryStateC.Identifier = float(self.__identifier)
            self.__archiverEntitySummaryStateC.Name = str(self.__name)
            self.__archiverEntitySummaryStateC.PreviousState = str(self.__previous_state)
            self.__archiverEntitySummaryStateC.priority = int(self.__priority)
            self.__archiverEntitySummaryStateC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("archiver_logevent_archiverEntitySummaryState"))
            lname = 'archiver_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_archiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_archiverEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_archiver.logEvent_archiverEntitySummaryState(
                self.__archiverEntitySummaryStateC, self.__archiverEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_archiver_entity_summary_state() exit")

    # +
    # (hidden) method: _catchuparchiver_entity_summary_state()
    # -
    def _catchuparchiver_entity_summary_state(self, **kwargs):

        # entry message
        self.logger.debug("_catchuparchiver_entity_summary_state() enter")

        if self.__mgr_catchuparchiver and self.__catchuparchiverEntitySummaryStateC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__commands = kwargs.get('CommandsAvailable', '')
            self.__configurations = kwargs.get('ConfigurationsAvailable', '')
            self.__current_state = kwargs.get('CurrentState', 'UNKNOWN')
            self.__executing = kwargs.get('Executing', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__previous_state = kwargs.get('PreviousState', 'UNKNOWN')
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = catchuparchiver_logevent_catchuparchiverEntitySummaryState() etc)
            # self.__catchuparchiverEntitySummaryStateC.Address = int(self.__address)
            self.__catchuparchiverEntitySummaryStateC.Address = int(0)
            self.__catchuparchiverEntitySummaryStateC.CommandsAvailable = str(self.__commands)
            self.__catchuparchiverEntitySummaryStateC.ConfigurationsAvailable = str(self.__configurations)
            self.__catchuparchiverEntitySummaryStateC.CurrentState = str(self.__current_state)
            self.__catchuparchiverEntitySummaryStateC.Executing = str(self.__executing)
            self.__catchuparchiverEntitySummaryStateC.Identifier = float(self.__identifier)
            self.__catchuparchiverEntitySummaryStateC.Name = str(self.__name)
            self.__catchuparchiverEntitySummaryStateC.PreviousState = str(self.__previous_state)
            self.__catchuparchiverEntitySummaryStateC.priority = int(self.__priority)
            self.__catchuparchiverEntitySummaryStateC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("catchuparchiver_logevent_catchuparchiverEntitySummaryState"))
            lname = 'catchuparchiver_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_catchuparchiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_catchuparchiverEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_catchuparchiver.logEvent_catchuparchiverEntitySummaryState(
                self.__catchuparchiverEntitySummaryStateC, self.__catchuparchiverEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_catchuparchiver_entity_summary_state() exit")

    # +
    # (hidden) method: _processingcluster_entity_summary_state()
    # -
    def _processingcluster_entity_summary_state(self, **kwargs):

        # entry message
        self.logger.debug("_processingcluster_entity_summary_state() enter")

        if self.__mgr_processingcluster and self.__processingclusterEntitySummaryStateC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__commands = kwargs.get('CommandsAvailable', '')
            self.__configurations = kwargs.get('ConfigurationsAvailable', '')
            self.__current_state = kwargs.get('CurrentState', 'UNKNOWN')
            self.__executing = kwargs.get('Executing', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__previous_state = kwargs.get('PreviousState', 'UNKNOWN')
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = processingcluster_logevent_processingclusterEntitySummaryState() etc)
            # self.__processingclusterEntitySummaryStateC.Address = int(self.__address)
            self.__processingclusterEntitySummaryStateC.Address = int(0)
            self.__processingclusterEntitySummaryStateC.CommandsAvailable = str(self.__commands)
            self.__processingclusterEntitySummaryStateC.ConfigurationsAvailable = str(self.__configurations)
            self.__processingclusterEntitySummaryStateC.CurrentState = str(self.__current_state)
            self.__processingclusterEntitySummaryStateC.Executing = str(self.__executing)
            self.__processingclusterEntitySummaryStateC.Identifier = float(self.__identifier)
            self.__processingclusterEntitySummaryStateC.Name = str(self.__name)
            self.__processingclusterEntitySummaryStateC.PreviousState = str(self.__previous_state)
            self.__processingclusterEntitySummaryStateC.priority = int(self.__priority)
            self.__processingclusterEntitySummaryStateC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("processingcluster_logevent_processingclusterEntitySummaryState"))
            lname = 'processingcluster_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_processingcluster.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_processingclusterEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_processingcluster.logEvent_processingclusterEntitySummaryState(
                self.__processingclusterEntitySummaryStateC, self.__processingclusterEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_processingcluster_entity_summary_state() exit")

    # +
    # (hidden) method: _ocs_entity_summary_state()
    # -
    def _ocs_entity_summary_state(self, **kwargs):

        # entry message
        self.logger.debug("_ocs_entity_summary_state() enter")

        if self.__mgr_ocs and self.__ocsEntitySummaryStateC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__commands = kwargs.get('CommandsAvailable', '')
            self.__configurations = kwargs.get('ConfigurationsAvailable', '')
            self.__current_state = kwargs.get('CurrentState', 'UNKNOWN')
            self.__executing = kwargs.get('Executing', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__previous_state = kwargs.get('PreviousState', 'UNKNOWN')
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = ocs_logevent_ocsEntitySummaryState() etc)
            # self.__ocsEntitySummaryStateC.Address = int(self.__address)
            self.__ocsEntitySummaryStateC.Address = int(0)
            self.__ocsEntitySummaryStateC.CommandsAvailable = str(self.__commands)
            self.__ocsEntitySummaryStateC.ConfigurationsAvailable = str(self.__configurations)
            self.__ocsEntitySummaryStateC.CurrentState = str(self.__current_state)
            self.__ocsEntitySummaryStateC.Executing = str(self.__executing)
            self.__ocsEntitySummaryStateC.Identifier = float(self.__identifier)
            self.__ocsEntitySummaryStateC.Name = str(self.__name)
            self.__ocsEntitySummaryStateC.PreviousState = str(self.__previous_state)
            self.__ocsEntitySummaryStateC.priority = int(self.__priority)
            self.__ocsEntitySummaryStateC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsEntitySummaryState"))
            lname = 'ocs_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsEntitySummaryState(
                self.__ocsEntitySummaryStateC, self.__ocsEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_ocs_entity_summary_state() exit")

    # +
    # (hidden) method: _sequencer_entity_summary_state()
    # -
    def _sequencer_entity_summary_state(self, **kwargs):

        # entry message
        self.logger.debug("_sequencer_entity_summary_state() enter")

        if self.__mgr_sequencer and self.__sequencerEntitySummaryStateC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__commands = kwargs.get('CommandsAvailable', '')
            self.__configurations = kwargs.get('ConfigurationsAvailable', '')
            self.__current_state = kwargs.get('CurrentState', 'UNKNOWN')
            self.__executing = kwargs.get('Executing', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__previous_state = kwargs.get('PreviousState', 'UNKNOWN')
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = s_logevent_sEntitySummaryState() etc)
            # self.__sequencerEntitySummaryStateC.Address = int(self.__address)
            self.__sequencerEntitySummaryStateC.Address = int(0)
            self.__sequencerEntitySummaryStateC.CommandsAvailable = str(self.__commands)
            self.__sequencerEntitySummaryStateC.ConfigurationsAvailable = str(self.__configurations)
            self.__sequencerEntitySummaryStateC.CurrentState = str(self.__current_state)
            self.__sequencerEntitySummaryStateC.Executing = str(self.__executing)
            self.__sequencerEntitySummaryStateC.Identifier = float(self.__identifier)
            self.__sequencerEntitySummaryStateC.Name = str(self.__name)
            self.__sequencerEntitySummaryStateC.PreviousState = str(self.__previous_state)
            self.__sequencerEntitySummaryStateC.priority = int(self.__priority)
            self.__sequencerEntitySummaryStateC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("sequencer_logevent_sequencerEntitySummaryState"))
            lname = 'sequencer_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_sequencer.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_sequencerEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_sequencer.logEvent_sequencerEntitySummaryState(
                self.__sequencerEntitySummaryStateC, self.__sequencerEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_sequencer_entity_summary_state() exit")

    # +
    # (hidden) method: _archiver_entity_startup()
    # -
    def _archiver_entity_startup(self, **kwargs):

        # entry message
        self.logger.debug("_archiver_entity_startup() enter")

        if self.__mgr_archiver and self.__archiverEntityStartupC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = archiver_logevent_archiverEntityStartup() etc)
            # self.__archiverEntityStartupC.Address = int(self.__address)
            self.__archiverEntityStartupC.Address = int(0)
            self.__archiverEntityStartupC.Name = str(self.__name)
            self.__archiverEntityStartupC.Identifier = float(self.__identifier)
            self.__archiverEntityStartupC.Timestamp = str(self.__timestamp)
            self.__archiverEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("archiver_logevent_archiverEntityStartup"))
            lname = 'archiver_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_archiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_archiverEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_archiver.logEvent_archiverEntityStartup(
                self.__archiverEntityStartupC, self.__archiverEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_archiver_entity_startup() exit")

    # +
    # (hidden) method: _catchuparchiver_entity_startup()
    # -
    def _catchuparchiver_entity_startup(self, **kwargs):

        # entry message
        self.logger.debug("_catchuparchiver_entity_startup() enter")

        if self.__mgr_catchuparchiver and self.__catchuparchiverEntityStartupC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = catchuparchiver_logevent_catchuparchiverEntityStartup() etc)
            # self.__catchuparchiverEntityStartupC.Address = int(self.__address)
            self.__catchuparchiverEntityStartupC.Address = int(0)
            self.__catchuparchiverEntityStartupC.Name = str(self.__name)
            self.__catchuparchiverEntityStartupC.Identifier = float(self.__identifier)
            self.__catchuparchiverEntityStartupC.Timestamp = str(self.__timestamp)
            self.__catchuparchiverEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("catchuparchiver_logevent_catchuparchiverEntityStartup"))
            lname = 'catchuparchiver_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_catchuparchiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_catchuparchiverEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_catchuparchiver.logEvent_catchuparchiverEntityStartup(
                self.__catchuparchiverEntityStartupC, self.__catchuparchiverEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_catchuparchiver_entity_startup() exit")

    # +
    # (hidden) method: _processingcluster_entity_startup()
    # -
    def _processingcluster_entity_startup(self, **kwargs):

        # entry message
        self.logger.debug("_processingcluster_entity_startup() enter")

        if self.__mgr_processingcluster and self.__processingclusterEntityStartupC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = processingcluster_logevent_processingclusterEntityStartup() etc)
            # self.__processingclusterEntityStartupC.Address = int(self.__address)
            self.__processingclusterEntityStartupC.Address = int(0)
            self.__processingclusterEntityStartupC.Name = str(self.__name)
            self.__processingclusterEntityStartupC.Identifier = float(self.__identifier)
            self.__processingclusterEntityStartupC.Timestamp = str(self.__timestamp)
            self.__processingclusterEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("processingcluster_logevent_processingclusterEntityStartup"))
            lname = 'processingcluster_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_processingcluster.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_processingclusterEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_processingcluster.logEvent_processingclusterEntityStartup(
                self.__processingclusterEntityStartupC, self.__processingclusterEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_processingcluster_entity_startup() exit")

    # +
    # (hidden) method: _ocs_entity_startup()
    # -
    def _ocs_entity_startup(self, **kwargs):

        # entry message
        self.logger.debug("_ocs_entity_startup() enter")

        if self.__mgr_ocs and self.__ocsEntityStartupC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = ocs_logevent_ocsEntityStartup() etc)
            #self.__ocsEntityStartupC.Address = int(self.__address)
            self.__ocsEntityStartupC.Address = int(0)
            self.__ocsEntityStartupC.Name = str(self.__name)
            self.__ocsEntityStartupC.Identifier = float(self.__identifier)
            self.__ocsEntityStartupC.Timestamp = str(self.__timestamp)
            self.__ocsEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsEntityStartup"))
            lname = 'ocs_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsEntityStartup(
                self.__ocsEntityStartupC, self.__ocsEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_ocs_entity_startup() exit")

    # +
    # (hidden) method: _sequencer_entity_startup()
    # -
    def _sequencer_entity_startup(self, **kwargs):

        # entry message
        self.logger.debug("_sequencer_entity_startup() enter")

        if self.__mgr_sequencer and self.__sequencerEntityStartupC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = sequencer_logevent_sequencerEntityStartup() etc)
            # self.__sequencerEntityStartupC.Address = int(self.__address)
            self.__sequencerEntityStartupC.Address = int(0)
            self.__sequencerEntityStartupC.Name = str(self.__name)
            self.__sequencerEntityStartupC.Identifier = float(self.__identifier)
            self.__sequencerEntityStartupC.Timestamp = str(self.__timestamp)
            self.__sequencerEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("sequencer_logevent_sequencerEntityStartup"))
            lname = 'sequencer_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_sequencer.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_sequencerEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_sequencer.logEvent_sequencerEntityStartup(
                self.__sequencerEntityStartupC, self.__sequencerEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_sequencer_entity_startup() exit")

    # +
    # (hidden) method: _archiver_entity_shutdown()
    # -
    def _archiver_entity_shutdown(self, **kwargs):

        # entry message
        self.logger.debug("_archiver_entity_shutdown() enter")

        if self.__mgr_archiver and self.__archiverEntityShutdownC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = archiver_logevent_archiverEntityShutdown() etc)
            # self.__archiverEntityShutdownC.Address = int(self.__address)
            self.__archiverEntityShutdownC.Address = int(0)
            self.__archiverEntityShutdownC.Name = str(self.__name)
            self.__archiverEntityShutdownC.Identifier = float(self.__identifier)
            self.__archiverEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__archiverEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("archiver_logevent_archiverEntityShutdown"))
            lname = 'archiver_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_archiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_archiverEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_archiver.logEvent_archiverEntityShutdown(
                self.__archiverEntityShutdownC, self.__archiverEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_archiver_entity_shutdown() exit")

    # +
    # (hidden) method: _catchuparchiver_entity_shutdown()
    # -
    def _catchuparchiver_entity_shutdown(self, **kwargs):

        # entry message
        self.logger.debug("_catchuparchiver_entity_shutdown() enter")

        if self.__mgr_catchuparchiver and self.__catchuparchiverEntityShutdownC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = catchuparchiver_logevent_catchuparchiverEntityShutdown() etc)
            # self.__catchuparchiverEntityShutdownC.Address = int(self.__address)
            self.__catchuparchiverEntityShutdownC.Address = int(0)
            self.__catchuparchiverEntityShutdownC.Name = str(self.__name)
            self.__catchuparchiverEntityShutdownC.Identifier = float(self.__identifier)
            self.__catchuparchiverEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__catchuparchiverEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("catchuparchiver_logevent_catchuparchiverEntityShutdown"))
            lname = 'catchuparchiver_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_catchuparchiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_catchuparchiverEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_catchuparchiver.logEvent_catchuparchiverEntityShutdown(
                self.__catchuparchiverEntityShutdownC, self.__catchuparchiverEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_catchuparchiver_entity_shutdown() exit")

    # +
    # (hidden) method: _processingcluster_entity_shutdown()
    # -
    def _processingcluster_entity_shutdown(self, **kwargs):

        # entry message
        self.logger.debug("_processingcluster_entity_shutdown() enter")

        if self.__mgr_processingcluster and self.__processingclusterEntityShutdownC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = processingcluster_logevent_processingclusterEntityShutdown() etc)
            # self.__processingclusterEntityShutdownC.Address = int(self.__address)
            self.__processingclusterEntityShutdownC.Address = int(0)
            self.__processingclusterEntityShutdownC.Name = str(self.__name)
            self.__processingclusterEntityShutdownC.Identifier = float(self.__identifier)
            self.__processingclusterEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__processingclusterEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("processingcluster_logevent_processingclusterEntityShutdown"))
            lname = 'processingcluster_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_processingcluster.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_processingclusterEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_processingcluster.logEvent_processingclusterEntityShutdown(
                self.__processingclusterEntityShutdownC, self.__processingclusterEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_processingcluster_entity_shutdown() exit")

    # +
    # (hidden) method: ocs_entity_shutdown()
    # -
    def _ocs_entity_shutdown(self, **kwargs):

        # entry message
        self.logger.debug("_ocs_entity_shutdown() enter")

        if self.__mgr_ocs and self.__ocsEntityShutdownC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = ocs_logevent_ocsEntityShutdown() etc)
            # self.__ocsEntityShutdownC.Address = int(self.__address)
            self.__ocsEntityShutdownC.Address = int(0)
            self.__ocsEntityShutdownC.Name = str(self.__name)
            self.__ocsEntityShutdownC.Identifier = float(self.__identifier)
            self.__ocsEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__ocsEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsEntityShutdown"))
            lname = 'ocs_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsEntityShutdown(
                self.__ocsEntityShutdownC, self.__ocsEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_ocs_entity_shutdown() exit")

    # +
    # (hidden) method: _sequencer_entity_shutdown()
    # -
    def _sequencer_entity_shutdown(self, **kwargs):

        # entry message
        self.logger.debug("_sequencer_entity_shutdown() enter")

        if self.__mgr_sequencer and self.__sequencerEntityShutdownC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = sequencer_logevent_sequencerEntityShutdown() etc)
            # self.__sequencerEntityShutdownC.Address = int(self.__address)
            self.__sequencerEntityShutdownC.Address = int(0)
            self.__sequencerEntityShutdownC.Name = str(self.__name)
            self.__sequencerEntityShutdownC.Identifier = float(self.__identifier)
            self.__sequencerEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__sequencerEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("sequencer_logevent_sequencerEntityShutdown"))
            lname = 'sequencer_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_sequencer.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_sequencerEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_sequencer.logEvent_sequencerEntityShutdown(
                self.__sequencerEntityShutdownC, self.__sequencerEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_sequencer_entity_shutdown() exit")

    # +
    # (hidden) method: _ocs_command_issued()
    # -
    def _ocs_command_issued(self, **kwargs):

        # entry message
        self.logger.debug("_ocs_command_issued() enter")

        if self.__mgr_ocs and self.__ocsCommandIssuedC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__command_source = kwargs.get('CommandSource', '')
            self.__command_sent = kwargs.get('CommandSent', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__return_value = kwargs.get('ReturnValue', '')
            self.__sequence_number = kwargs.get('SequenceNumber', '')
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = ocs_logevent_ocsCommandIssued() etc)
            self.__ocsCommandIssuedC.CommandSource = str(self.__command_source)
            self.__ocsCommandIssuedC.CommandSent = str(self.__command_sent)
            self.__ocsCommandIssuedC.Identifier = float(self.__identifier)
            self.__ocsCommandIssuedC.priority = int(self.__priority)
            self.__ocsCommandIssuedC.ReturnValue = int(self.__return_value)
            self.__ocsCommandIssuedC.SequenceNumber = int(self.__sequence_number)
            self.__ocsCommandIssuedC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsCommandIssued"))
            lname = 'ocs_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsCommandIssued(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsCommandIssued(
                self.__ocsCommandIssuedC, self.__ocsCommandIssuedC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_ocs_command_issued() exit")

    # +
    # (hidden) method: _sequencer_command_issued()
    # -
    def _sequencer_command_issued(self, **kwargs):

        # entry message
        self.logger.debug("_sequencer_command_issued() enter")

        if self.__mgr_sequencer and self.__sequencerCommandIssuedC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__command_source = kwargs.get('CommandSource', '')
            self.__command_sent = kwargs.get('CommandSent', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__return_value = kwargs.get('ReturnValue', '')
            self.__sequence_number = kwargs.get('SequenceNumber', '')
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = sequencer_logevent_sequencerCommandIssued() etc)
            self.__sequencerCommandIssuedC.CommandSource = str(self.__command_source)
            self.__sequencerCommandIssuedC.CommandSent = str(self.__command_sent)
            self.__sequencerCommandIssuedC.Identifier = float(self.__identifier)
            self.__sequencerCommandIssuedC.priority = int(self.__priority)
            self.__sequencerCommandIssuedC.ReturnValue = int(self.__return_value)
            self.__sequencerCommandIssuedC.SequenceNumber = int(self.__sequence_number)
            self.__sequencerCommandIssuedC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("sequencer_logevent_sequencerCommandIssued"))
            lname = 'sequencer_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_sequencer.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_sequencerCommandIssued(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_sequencer.logEvent_sequencerCommandIssued(
                self.__sequencerCommandIssuedC, self.__sequencerCommandIssuedC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_sequencer_command_issued() exit")

    # +
    # (hidden) method: _ocs_command_status()
    # -
    def _ocs_command_status(self, **kwargs):

        # entry message
        self.logger.debug("_ocs_command_status() enter")

        if self.__mgr_ocs and self.__ocsCommandStatusC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__command_source = kwargs.get('CommandSource', '')
            self.__command_sent = kwargs.get('CommandSent', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__status = kwargs.get('Status', '')
            self.__status_value = kwargs.get('StatusValue', '')
            self.__sequence_number = kwargs.get('SequenceNumber', '')
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = ocs_logevent_ocsCommandStatus() etc)
            self.__ocsCommandStatusC.CommandSource = str(self.__command_source)
            self.__ocsCommandStatusC.CommandSent = str(self.__command_sent)
            self.__ocsCommandStatusC.Identifier = float(self.__identifier)
            self.__ocsCommandStatusC.priority = int(self.__priority)
            self.__ocsCommandStatusC.Status = str(self.__status)
            self.__ocsCommandStatusC.StatusValue = int(self.__status_value)
            self.__ocsCommandStatusC.SequenceNumber = int(self.__sequence_number)
            self.__ocsCommandStatusC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsCommandStatus"))
            lname = 'ocs_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsCommandStatus(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsCommandStatus(
                self.__ocsCommandStatusC, self.__ocsCommandStatusC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_ocs_command_status() exit")

    # +
    # (hidden) method: _sequencer_command_status()
    # -
    def _sequencer_command_status(self, **kwargs):

        # entry message
        self.logger.debug("_sequencer_command_status() enter")

        if self.__mgr_sequencer and self.__sequencerCommandStatusC and kwargs:

            # dump dictionary
            #for k, v in kwargs.items():
            #    self.logger.debug("{0:s}={1:s}".format(str(k), str(v)))

            # get values from kwargs dictionary
            self.__command_source = kwargs.get('CommandSource', '')
            self.__command_sent = kwargs.get('CommandSent', '')
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__status = kwargs.get('Status', '')
            self.__status_value = kwargs.get('StatusValue', '')
            self.__sequence_number = kwargs.get('SequenceNumber', '')
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = sequencer_logevent_sequencerCommandStatus() etc)
            self.__sequencerCommandStatusC.CommandSource = str(self.__command_source)
            self.__sequencerCommandStatusC.CommandSent = str(self.__command_sent)
            self.__sequencerCommandStatusC.Identifier = float(self.__identifier)
            self.__sequencerCommandStatusC.priority = int(self.__priority)
            self.__sequencerCommandStatusC.Status = str(self.__status)
            self.__sequencerCommandStatusC.StatusValue = int(self.__status_value)
            self.__sequencerCommandStatusC.SequenceNumber = int(self.__sequence_number)
            self.__sequencerCommandStatusC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("sequencer_logevent_sequencerCommandStatus"))
            lname = 'sequencer_logevent_{0:s}'.format(self.__event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_sequencer.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_sequencerCommandStatus(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_sequencer.logEvent_sequencerCommandStatus(
                self.__sequencerCommandStatusC, self.__sequencerCommandStatusC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname, self.__retval))

        # exit message
        self.logger.debug("_sequencer_command_status() exit")

    # +
    # decorator(s)
    # -
    @property
    def simulate(self):
        return self._simulate

    @simulate.setter
    def simulate(self, simulate):
        if not isinstance(simulate, bool):
            raise OcsEventsException(OCS_EVENTS_ERROR_NOSIM, "simulate={0:s}".format(str(simulate)))
        else:
            self._simulate = simulate

    # +
    # method: __str__
    # -
    def __str__(self):
        return 'OcsEvents(\'{0:s}\', \'{1:s}\', simulate={2:s}) created at address {3:s}'.format(
            self._system, self._component, str(self._simulate), hex(id(self)))


# +
# main()
# -
if __name__ == "__main__":

    evh = None
    try:
        evh = OcsEvents(False)
    except OcsEventsException as e:
        print(e.errstr)

    if evh:

        # send event with payload
        ocsid = ocs_id(False)
        evh.send_event('archiverEntityStartup',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
        evh.send_event('catchuparchiverEntityStartup',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
        evh.send_event('processingclusterEntityStartup',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
        evh.send_event('ocsEntityStartup',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
        evh.send_event('sequencerEntityStartup',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)

        # send event with payload
        ocsid = ocs_id(False)
        evh.send_event('archiverEntityShutdown',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
        evh.send_event('catchuparchiverEntityShutdown',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
        evh.send_event('processingclusterEntityShutdown',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
        evh.send_event('ocsEntityShutdown',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
        evh.send_event('sequencerEntityShutdown',
                       Name='Junk',
                       Identifier=float(ocsid),
                       Timestamp=ocs_mjd_to_iso(ocsid),
                       Address=id(evh),
                       priority=SAL__EVENT_INFO)
