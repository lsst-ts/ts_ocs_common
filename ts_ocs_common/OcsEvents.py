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
        self.__ocs = None
        self.__mgr = None

        self.__address = None
        self.__command_source = None
        self.__command_sent = None
        self.__method = None
        self.__identifier = None
        self.__match = None
        self.__name = None
        self.__priority = None
        self.__return_value = None
        self.__retval = None
        self.__sequence_number = None
        self.__status_value = None
        self.__status = None
        self.__timestamp = None

        # container(s)
        self.__ocsEntityStartupC = None
        self.__ocsEntityShutdownC = None
        self.__ocsCommandIssuedC = None
        self.__ocsCommandStatusC = None

        # event methods
        self.__event_methods = {
            'ocsEntityStartup': self._ocsEntityStartup,
            'ocsEntityShutdown': self._ocsEntityShutdown,
            'ocsCommandIssued': self._ocsCommandIssued,
            'ocsCommandStatus': self._ocsCommandStatus
            }

        # import the SAL (cf. from SALPY_ocs import *)
        mname = 'SALPY_ocs'
        self.logger.debug("Importing {0:s}".format(mname))
        self.__ocs = ocs_sal_import(mname)
        if self.__ocs:
            self.logger.debug("Imported {0:s} ok".format(mname))

        # get mgr object (cf. mgr = SAL_ocs())
        aname = 'SAL_ocs'
        self.logger.debug("Getting attribute {0:s}".format(aname))
        mgr = ocs_sal_attribute(self.__ocs, aname)
        if mgr:
            self.__mgr = mgr()
            self.logger.debug("Got attribute {0:s} ok".format(aname))

        # get data structure(s) (cf. data = ocs_logevent_ocsEntityStartupC())
        self.__ocsEntityStartupC = self._get_sal_logC('ocsEntityStartup')
        self.__ocsEntityShutdownC = self._get_sal_logC('ocsEntityShutdown')
        self.__ocsCommandIssuedC = self._get_sal_logC('ocsCommandIssued')
        self.__ocsCommandStatusC = self._get_sal_logC('ocsCommandStatus')

        # set up a default event (cf. mgr.salEvent("ocs_logevent_ocsEntityStartup"))
        cname = 'ocs_logevent_ocsEntityStartup'
        if self.__mgr:
            self.__mgr.salEvent(cname)

        self.logger.debug("Started {0:s} {1:s} ok".format(self._system, self._component))

    # +
    # (hidden) method: _get_sal_logC()
    # -
    def _get_sal_logC(self, event=''):
        sname = 'ocs_logevent_{0:s}C'.format(event)
        self.logger.debug("Getting attribute {0:s}".format(sname))
        so = ocs_sal_attribute(self.__ocs, sname)
        if so:
            self.logger.debug("Got attribute {0:s} ok".format(sname))
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
    # (hidden) method: ocsEntityStartup()
    # -
    def _ocsEntityStartup(self, **kwargs):
        self.logger.debug("_ocsEntityStartup() enter")
        if self.__mgr and self.__ocsEntityStartupC and kwargs:

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
            self.__mgr.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsEntityStartup(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr.logEvent_ocsEntityStartup(self.__ocsEntityStartupC, self.__ocsEntityStartupC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_ocsEntityStartup() exit")


    # +
    # (hidden) method: ocsEntityShutdown()
    # -
    def _ocsEntityShutdown(self, **kwargs):
        self.logger.debug("_ocsEntityShutdown() enter")
        if self.__mgr and self.__ocsEntityShutdownC and kwargs:

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
            self.__mgr.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsEntityShutdown(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr.logEvent_ocsEntityShutdown(self.__ocsEntityShutdownC, self.__ocsEntityShutdownC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_ocsEntityShutdown() exit")

    # +
    # (hidden) method: ocsCommandIssued()
    # -
    def _ocsCommandIssued(self, **kwargs):
        self.logger.debug("_ocsCommandIssued() enter")
        if self.__mgr and self.__ocsCommandIssuedC and kwargs:

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
            self.__mgr.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsCommandIssued(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr.logEvent_ocsCommandIssued(self.__ocsCommandIssuedC, self.__ocsCommandIssuedC.priority)
            self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
        self.logger.debug("_ocsCommandIssued() exit")

    # +
    # (hidden) method: ocsCommandStatus()
    # -
    def _ocsCommandStatus(self, **kwargs):
        self.logger.debug("_ocsCommandStatus() enter")
        if self.__mgr and self.__ocsCommandStatusC and kwargs:

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
            self.__mgr.salEvent(lname)

            # issue event (cf. retval = mgr.logEvent_ocsCommandStatus(data, priority))
            self.logger.debug("issuing event {0:s}".format(lname))
            self.__retval = self.__mgr.logEvent_ocsCommandStatus(self.__ocsCommandStatusC, self.__ocsCommandStatusC.priority)
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
    except OcsEventsEntityException as e:
        print(e.errstr)

    if evh:

        # send event with payload
        ocsid = ocs_id(False)
        evh.sendEvent('ocsEntityStartup', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)

        # send event with payload
        ocsid = ocs_id(False)
        evh.sendEvent('ocsEntityShutdown', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)

