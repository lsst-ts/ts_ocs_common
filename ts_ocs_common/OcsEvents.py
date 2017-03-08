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


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 December 2016"
__doc__ = """Events class for the OCS"""
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
        self.__archiver = None
        self.__catchuparchiver = None
        self.__processingcluster = None
        self.__ocs = None

        self.__mgr_archiver = None
        self.__mgr_catchuparchiver = None
        self.__mgr_processingcluster = None
        self.__mgr_ocs = None

        self.__address = None
        self.__commands = None
        self.__command_source = None
        self.__command_sent = None
        self.__commands = None
        self.__configurations = None
        self.__current_state = None
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

        self.__archiverEntityStartupC = None
        self.__catchuparchiverEntityStartupC = None
        self.__processingclusterEntityStartupC = None
        self.__ocsEntityStartupC = None

        self.__archiverEntityShutdownC = None
        self.__catchuparchiverEntityShutdownC = None
        self.__processingclusterEntityShutdownC = None
        self.__ocsEntityShutdownC = None

        self.__ocsCommandIssuedC = None
        self.__ocsCommandStatusC = None

        # event methods
        self.__event_methods = {
            'archiverEntitySummaryState': self._archiverEntitySummaryState,
            'catchuparchiverEntitySummaryState': self._catchuparchiverEntitySummaryState,
            'processingclusterEntitySummaryState': self._processingclusterEntitySummaryState,
            'ocsEntitySummaryState': self._ocsEntitySummaryState,
            'archiverEntityStartup': self._archiverEntityStartup,
            'catchuparchiverEntityStartup': self._catchuparchiverEntityStartup,
            'processingclusterEntityStartup': self._processingclusterEntityStartup,
            'ocsEntityStartup': self._ocsEntityStartup,
            'archiverEntityShutdown': self._archiverEntityShutdown,
            'catchuparchiverEntityShutdown': self._catchuparchiverEntityShutdown,
            'processingclusterEntityShutdown': self._processingclusterEntityShutdown,
            'ocsEntityShutdown': self._ocsEntityShutdown,
            'ocsCommandIssued': self._ocsCommandIssued,
            'ocsCommandStatus': self._ocsCommandStatus
            }

        # import the SAL_archiver (cf. from SALPY_archiver import *)
        mname = 'SALPY_archiver'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__archiver = ocs_sal_import(mname)
        if self.__archiver:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # import the SAL_catchuparchiver (cf. from SALPY_catchuparchiver import *)
        mname = 'SALPY_catchuparchiver'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__catchuparchiver = ocs_sal_import(mname)
        if self.__catchuparchiver:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # import the SAL_processingcluster (cf. from SALPY_processingcluster import *)
        mname = 'SALPY_processingcluster'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__processingcluster = ocs_sal_import(mname)
        if self.__processingcluster:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # import the SAL_ocs (cf. from SALPY_ocs import *)
        mname = 'SALPY_ocs'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__ocs = ocs_sal_import(mname)
        if self.__ocs:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # get mgr object (cf. mgr = SAL_archiver())
        aname = 'SAL_archiver'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__archiver, aname)
        if mgr:
            self.__mgr_archiver = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get mgr object (cf. mgr = SAL_catchuparchiver())
        aname = 'SAL_catchuparchiver'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__catchuparchiver, aname)
        if mgr:
            self.__mgr_catchuparchiver = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get mgr object (cf. mgr = SAL_processingcluster())
        aname = 'SAL_processingcluster'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__processingcluster, aname)
        if mgr:
            self.__mgr_processingcluster = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get mgr object (cf. mgr = SAL_ocs())
        aname = 'SAL_ocs'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__ocs, aname)
        if mgr:
            self.__mgr_ocs = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get data structure(s) (cf. data = ocs_logevent_ocsEntityStartupC())
        self.__archiverEntitySummaryStateC = self._get_sal_logC(self.__archiver, 'archiver_logevent_archiverEntitySummaryStateC')
        self.__catchuparchiverEntitySummaryStateC = self._get_sal_logC(self.__catchuparchiver, 'catchuparchiver_logevent_catchuparchiverEntitySummaryStateC')
        self.__processingclusterEntitySummaryStateC = self._get_sal_logC(self.__processingcluster, 'processingcluster_logevent_processingclusterEntitySummaryStateC')
        self.__ocsEntitySummaryStateC = self._get_sal_logC(self.__ocs, 'ocs_logevent_ocsEntitySummaryStateC')

        self.__archiverEntityStartupC = self._get_sal_logC(self.__archiver, 'archiver_logevent_archiverEntityStartupC')
        self.__catchuparchiverEntityStartupC = self._get_sal_logC(self.__catchuparchiver, 'catchuparchiver_logevent_catchuparchiverEntityStartupC')
        self.__processingclusterEntityStartupC = self._get_sal_logC(self.__processingcluster, 'processingcluster_logevent_processingclusterEntityStartupC')
        self.__ocsEntityStartupC = self._get_sal_logC(self.__ocs, 'ocs_logevent_ocsEntityStartupC')

        self.__archiverEntityShutdownC = self._get_sal_logC(self.__archiver, 'archiver_logevent_archiverEntityShutdownC')
        self.__catchuparchiverEntityShutdownC = self._get_sal_logC(self.__catchuparchiver, 'catchuparchiver_logevent_catchuparchiverEntityShutdownC')
        self.__processingclusterEntityShutdownC = self._get_sal_logC(self.__processingcluster, 'processingcluster_logevent_processingclusterEntityShutdownC')
        self.__ocsEntityShutdownC = self._get_sal_logC(self.__ocs, 'ocs_logevent_ocsEntityShutdownC')

        self.__ocsCommandIssuedC = self._get_sal_logC(self.__ocs, 'ocs_logevent_ocsCommandIssuedC')
        self.__ocsCommandStatusC = self._get_sal_logC(self.__ocs, 'ocs_logevent_ocsCommandStatusC')

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
    # (hidden) method: _get_sal_logC()
    # -
    def _get_sal_logC(self, salobj=None, event=''):
        self.logger.debug("Getting attribute {0:s}".format(event))
        so = ocs_sal_attribute(salobj, event)
        if so:
            self.logger.debug("Got attribute {0:s} ok".format(event))
            return so()
        else:
            return None

    # +
    # method: sendEvent()
    # -
    def sendEvent(self, event='', **kwargs):
        self.logger.debug("sendEvent() enter")

        # check input(s)
        if not isinstance(event, str) or event == '':
            raise OcsEventsException(OCS_EVENTS_ERROR_NOVAL, "event={0:s}".format(str(event)))
        else:
            self._event = event

        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("sendEvent(), in simulation with sleep={0:s}".format(str(stime)))

        # invoke method
        else:
            self.__method = self.__event_methods.get(event, None)
            if self.__method:
                self.__method(**kwargs)
        self.logger.debug("sendEvent() exit")

    # +
    # (hidden) method: archiverEntitySummaryState()
    # -
    def _archiverEntitySummaryState(self, **kwargs):
        self.logger.debug("_archiverEntitySummaryState() enter")
        if self.__mgr_archiver and self.__archiverEntitySummaryStateC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

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

            # set up payload (cf. data = archiver_logevent_archiverEntitySummaryState(); data.Name = 'Something')
            self.__archiverEntitySummaryStateC.Address = long(self.__address)
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
            lname = 'archiver_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_archiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_archiverEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_archiver.logEvent_archiverEntitySummaryState(self.__archiverEntitySummaryStateC, self.__archiverEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_archiverEntitySummaryState() exit")

    # +
    # (hidden) method: catchuparchiverEntitySummaryState()
    # -
    def _catchuparchiverEntitySummaryState(self, **kwargs):
        self.logger.debug("_catchuparchiverEntitySummaryState() enter")
        if self.__mgr_catchuparchiver and self.__catchuparchiverEntitySummaryStateC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

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

            # set up payload (cf. data = catchuparchiver_logevent_catchuparchiverEntitySummaryState(); data.Name = 'Something')
            self.__catchuparchiverEntitySummaryStateC.Address = long(self.__address)
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
            lname = 'catchuparchiver_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_catchuparchiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_catchuparchiverEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_catchuparchiver.logEvent_catchuparchiverEntitySummaryState(self.__catchuparchiverEntitySummaryStateC, self.__catchuparchiverEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_catchuparchiverEntitySummaryState() exit")

    # +
    # (hidden) method: processingclusterEntitySummaryState()
    # -
    def _processingclusterEntitySummaryState(self, **kwargs):
        self.logger.debug("_processingclusterEntitySummaryState() enter")
        if self.__mgr_processingcluster and self.__processingclusterEntitySummaryStateC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

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

            # set up payload (cf. data = processingcluster_logevent_processingclusterEntitySummaryState(); data.Name = 'Something')
            self.__processingclusterEntitySummaryStateC.Address = long(self.__address)
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
            lname = 'processingcluster_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_processingcluster.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_processingclusterEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_processingcluster.logEvent_processingclusterEntitySummaryState(self.__processingclusterEntitySummaryStateC, self.__processingclusterEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_processingclusterEntitySummaryState() exit")

    # +
    # (hidden) method: ocsEntitySummaryState()
    # -
    def _ocsEntitySummaryState(self, **kwargs):
        self.logger.debug("_ocsEntitySummaryState() enter")
        if self.__mgr_ocs and self.__ocsEntitySummaryStateC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

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

            # set up payload (cf. data = ocs_logevent_ocsEntitySummaryState(); data.Name = 'Something')
            self.__ocsEntitySummaryStateC.Address = long(self.__address)
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
            lname = 'ocs_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsEntitySummaryState(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsEntitySummaryState(self.__ocsEntitySummaryStateC, self.__ocsEntitySummaryStateC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_ocsEntitySummaryState() exit")

    # +
    # (hidden) method: archiverEntityStartup()
    # -
    def _archiverEntityStartup(self, **kwargs):
        self.logger.debug("_archiverEntityStartup() enter")
        if self.__mgr_archiver and self.__archiverEntityStartupC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = archiver_logevent_archiverEntityStartup(); data.Name = 'Something')
            self.__archiverEntityStartupC.Name = str(self.__name)
            self.__archiverEntityStartupC.Identifier = float(self.__identifier)
            self.__archiverEntityStartupC.Timestamp = str(self.__timestamp)
            self.__archiverEntityStartupC.Address = long(self.__address)
            self.__archiverEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("archiver_logevent_archiverEntityStartup"))
            lname = 'archiver_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_archiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_archiverEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_archiver.logEvent_archiverEntityStartup(self.__archiverEntityStartupC, self.__archiverEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_archiverEntityStartup() exit")

    # +
    # (hidden) method: catchuparchiverEntityStartup()
    # -
    def _catchuparchiverEntityStartup(self, **kwargs):
        self.logger.debug("_catchuparchiverEntityStartup() enter")
        if self.__mgr_catchuparchiver and self.__catchuparchiverEntityStartupC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = catchuparchiver_logevent_catchuparchiverEntityStartup(); data.Name = 'Something')
            self.__catchuparchiverEntityStartupC.Name = str(self.__name)
            self.__catchuparchiverEntityStartupC.Identifier = float(self.__identifier)
            self.__catchuparchiverEntityStartupC.Timestamp = str(self.__timestamp)
            self.__catchuparchiverEntityStartupC.Address = long(self.__address)
            self.__catchuparchiverEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("catchuparchiver_logevent_catchuparchiverEntityStartup"))
            lname = 'catchuparchiver_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_catchuparchiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_catchuparchiverEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_catchuparchiver.logEvent_catchuparchiverEntityStartup(self.__catchuparchiverEntityStartupC, self.__catchuparchiverEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_catchuparchiverEntityStartup() exit")

    # +
    # (hidden) method: processingclusterEntityStartup()
    # -
    def _processingclusterEntityStartup(self, **kwargs):
        self.logger.debug("_processingclusterEntityStartup() enter")
        if self.__mgr_processingcluster and self.__processingclusterEntityStartupC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = processingcluster_logevent_processingclusterEntityStartup(); data.Name = 'Something')
            self.__processingclusterEntityStartupC.Name = str(self.__name)
            self.__processingclusterEntityStartupC.Identifier = float(self.__identifier)
            self.__processingclusterEntityStartupC.Timestamp = str(self.__timestamp)
            self.__processingclusterEntityStartupC.Address = long(self.__address)
            self.__processingclusterEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("processingcluster_logevent_processingclusterEntityStartup"))
            lname = 'processingcluster_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_processingcluster.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_processingclusterEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_processingcluster.logEvent_processingclusterEntityStartup(self.__processingclusterEntityStartupC, self.__processingclusterEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_processingclusterEntityStartup() exit")

    # +
    # (hidden) method: ocsEntityStartup()
    # -
    def _ocsEntityStartup(self, **kwargs):
        self.logger.debug("_ocsEntityStartup() enter")
        if self.__mgr_ocs and self.__ocsEntityStartupC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = ocs_logevent_ocsEntityStartup(); data.Name = 'Something')
            self.__ocsEntityStartupC.Name = str(self.__name)
            self.__ocsEntityStartupC.Identifier = float(self.__identifier)
            self.__ocsEntityStartupC.Timestamp = str(self.__timestamp)
            self.__ocsEntityStartupC.Address = long(self.__address)
            self.__ocsEntityStartupC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsEntityStartup"))
            lname = 'ocs_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsEntityStartup(self.__ocsEntityStartupC, self.__ocsEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_ocsEntityStartup() exit")

    # +
    # (hidden) method: archiverEntityShutdown()
    # -
    def _archiverEntityShutdown(self, **kwargs):
        self.logger.debug("_archiverEntityShutdown() enter")
        if self.__mgr_archiver and self.__archiverEntityShutdownC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = archiver_logevent_archiverEntityShutdown(); data.Name = 'Something')
            self.__archiverEntityShutdownC.Name = str(self.__name)
            self.__archiverEntityShutdownC.Identifier = float(self.__identifier)
            self.__archiverEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__archiverEntityShutdownC.Address = long(self.__address)
            self.__archiverEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("archiver_logevent_archiverEntityShutdown"))
            lname = 'archiver_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_archiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_archiverEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_archiver.logEvent_archiverEntityShutdown(self.__archiverEntityShutdownC, self.__archiverEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_archiverEntityShutdown() exit")

    # +
    # (hidden) method: catchuparchiverEntityShutdown()
    # -
    def _catchuparchiverEntityShutdown(self, **kwargs):
        self.logger.debug("_catchuparchiverEntityShutdown() enter")
        if self.__mgr_catchuparchiver and self.__catchuparchiverEntityShutdownC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = catchuparchiver_logevent_catchuparchiverEntityShutdown(); data.Name = 'Something')
            self.__catchuparchiverEntityShutdownC.Name = str(self.__name)
            self.__catchuparchiverEntityShutdownC.Identifier = float(self.__identifier)
            self.__catchuparchiverEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__catchuparchiverEntityShutdownC.Address = long(self.__address)
            self.__catchuparchiverEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("catchuparchiver_logevent_catchuparchiverEntityShutdown"))
            lname = 'catchuparchiver_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_catchuparchiver.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_catchuparchiverEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_catchuparchiver.logEvent_catchuparchiverEntityShutdown(self.__catchuparchiverEntityShutdownC, self.__catchuparchiverEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_catchuparchiverEntityShutdown() exit")

    # +
    # (hidden) method: processingclusterEntityShutdown()
    # -
    def _processingclusterEntityShutdown(self, **kwargs):
        self.logger.debug("_processingclusterEntityShutdown() enter")
        if self.__mgr_processingcluster and self.__processingclusterEntityShutdownC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = processingcluster_logevent_processingclusterEntityShutdown(); data.Name = 'Something')
            self.__processingclusterEntityShutdownC.Name = str(self.__name)
            self.__processingclusterEntityShutdownC.Identifier = float(self.__identifier)
            self.__processingclusterEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__processingclusterEntityShutdownC.Address = long(self.__address)
            self.__processingclusterEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("processingcluster_logevent_processingclusterEntityShutdown"))
            lname = 'processingcluster_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_processingcluster.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_processingclusterEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_processingcluster.logEvent_processingclusterEntityShutdown(self.__processingclusterEntityShutdownC, self.__processingclusterEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_processingclusterEntityShutdown() exit")

    # +
    # (hidden) method: ocsEntityShutdown()
    # -
    def _ocsEntityShutdown(self, **kwargs):
        self.logger.debug("_ocsEntityShutdown() enter")
        if self.__mgr_ocs and self.__ocsEntityShutdownC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

            # get values from kwargs dictionary
            self.__address = kwargs.get('Address', SAL__ERROR)
            self.__identifier = kwargs.get('Identifier', ocs_id(False))
            self.__name = kwargs.get('Name', os.getenv('USER'))
            self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
            self.__timestamp = kwargs.get('Timestamp', '')

            self.__match = re.search(ISO_PATTERN, self.__timestamp)
            if not self.__match:
                self.__timestamp = ocs_mjd_to_iso(self.__identifier)

            # set up payload (cf. data = ocs_logevent_ocsEntityShutdown(); data.Name = 'Something')
            self.__ocsEntityShutdownC.Name = str(self.__name)
            self.__ocsEntityShutdownC.Identifier = float(self.__identifier)
            self.__ocsEntityShutdownC.Timestamp = str(self.__timestamp)
            self.__ocsEntityShutdownC.Address = long(self.__address)
            self.__ocsEntityShutdownC.priority = int(self.__priority)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsEntityShutdown"))
            lname = 'ocs_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsEntityShutdown(self.__ocsEntityShutdownC, self.__ocsEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_ocsEntityShutdown() exit")

    # +
    # (hidden) method: ocsCommandIssued()
    # -
    def _ocsCommandIssued(self, **kwargs):
        self.logger.debug("_ocsCommandIssued() enter")
        if self.__mgr_ocs and self.__ocsCommandIssuedC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

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

            # set up payload (cf. data = ocs_logevent_ocsCommandIssued(); data.Name = 'Something')
            self.__ocsCommandIssuedC.CommandSource = str(self.__command_source)
            self.__ocsCommandIssuedC.CommandSent = str(self.__command_sent)
            self.__ocsCommandIssuedC.Identifier = float(self.__identifier)
            self.__ocsCommandIssuedC.priority = int(self.__priority)
            self.__ocsCommandIssuedC.ReturnValue = long(self.__return_value)
            self.__ocsCommandIssuedC.SequenceNumber = long(self.__sequence_number)
            self.__ocsCommandIssuedC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsCommandIssued"))
            lname = 'ocs_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsCommandIssued(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsCommandIssued(self.__ocsCommandIssuedC, self.__ocsCommandIssuedC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_ocsCommandIssued() exit")

    # +
    # (hidden) method: ocsCommandStatus()
    # -
    def _ocsCommandStatus(self, **kwargs):
        self.logger.debug("_ocsCommandStatus() enter")
        if self.__mgr_ocs and self.__ocsCommandStatusC and kwargs:

            # dump dictionary
            for k, v in kwargs.items():
                self.logger.debug("{0:s}={1:s}".format(str(k),str(v)))

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

            # set up payload (cf. data = ocs_logevent_ocsCommandStatus(); data.Name = 'Something')
            self.__ocsCommandStatusC.CommandSource = str(self.__command_source)
            self.__ocsCommandStatusC.CommandSent = str(self.__command_sent)
            self.__ocsCommandStatusC.Identifier = float(self.__identifier)
            self.__ocsCommandStatusC.priority = int(self.__priority)
            self.__ocsCommandStatusC.Status = str(self.__status)
            self.__ocsCommandStatusC.StatusValue = long(self.__status_value)
            self.__ocsCommandStatusC.SequenceNumber = long(self.__sequence_number)
            self.__ocsCommandStatusC.Timestamp = str(self.__timestamp)

            # set up event (cf. mgr.salEvent("ocs_logevent_ocsCommandStatus"))
            lname = 'ocs_logevent_{0:s}'.format(self._event)
            self.logger.debug("setting up for event {0:s}".format(lname))
            self.__mgr_ocs.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsCommandStatus(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr_ocs.logEvent_ocsCommandStatus(self.__ocsCommandStatusC, self.__ocsCommandStatusC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_ocsCommandStatus() exit")

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

    ehv = None
    try:
        evh = OcsEvents(False)
    except OcsEventsException as e:
        print(e.errstr)

    if evh:

        # send event with payload
        ocsid = ocs_id(False)
        evh.sendEvent('archiverEntityStartup', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)
        evh.sendEvent('catchuparchiverEntityStartup', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)
        evh.sendEvent('processingclusterEntityStartup', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)
        evh.sendEvent('ocsEntityStartup', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)

        # send event with payload
        ocsid = ocs_id(False)
        evh.sendEvent('archiverEntityShutdown', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)
        evh.sendEvent('catchuparchiverEntityShutdown', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)
        evh.sendEvent('processingclusterEntityShutdown', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)
        evh.sendEvent('ocsEntityShutdown', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)

