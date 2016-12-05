#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


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
__date__ = "30 November 2016"
__doc__ = """Events class for the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsEvents.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsEvents()
# -
class OcsEvents(object):

    # +
    # method: __init__
    # -
    def __init__(self, simulate=True):
        """
            :param simulate: if True, use simulation
            :return: None or object representing the entity
        """

        # get arguments(s)
        self._simulate = simulate
        self._system = 'OCS'
        self._entity = 'Events'

        # check simulate
        if not isinstance(self._simulate, bool):
            self._simulate = True

        # set up logging
        self.logger = OcsLogger(self._system, self._entity).logger
        self.logger.debug("Starting {0:s} {1:s}".format(self._system, self._entity))

        # declare some variables and initialize them
        self.logger.debug("Initializing variables")
        self.__ocs = None
        self.__mgr = None

        self.__address = None
        self.__handler = None
        self.__identifier = None
        self.__match = None
        self.__name = None
        self.__priority = None
        self.__retval = None
        self.__timestamp = None

        # container(s)
        self.__ocsCommandableEntityStartupC = None
        self.__ocsCommandableEntityShutdownC = None

        # event handlers
        self.__event_handlers = {
            'ocsCommandableEntityStartup': self._ocsCommandableEntityStartup,
            'ocsCommandableEntityShutdown': self._ocsCommandableEntityShutdown
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

        # get data structure(s) (cf. data = ocs_logevent_ocsCommandableEntityStartupC())
        self.__ocsCommandableEntityStartupC = self._get_sal_logC('ocsCommandableEntityStartup')
        self.__ocsCommandableEntityShutdownC = self._get_sal_logC('ocsCommandableEntityShutdown')

        # set up a default event (cf. mgr.salEvent("ocs_logevent_ocsCommandableEntityStartup"))
        cname = 'ocs_logevent_ocsCommandableEntityStartup'
        if self.__mgr:
            self.__mgr.salEvent(cname)

        self.logger.debug("Started {0:s} {1:s} ok".format(self._system, self._entity))

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

    # +
    # method: sendEvent()
    # -
    def sendEvent(self, event='', **kwargs):
        self.logger.debug("sendEvent() enter")
        # check input(s)
        if not isinstance(event, str) or event == '':
            raise OcsGenericException(OCS_GENERIC_ENTITY_ERROR_NOVAL, "event={0:s}".format(str(event)))
        else:
            self._event = event
        # in simulation, sleep for a random time
        if self._simulate:
            stime = time.sleep(random.uniform(0, 5))
            self.logger.debug("sendEvent(), in simulation with sleep={0:s}".format(str(stime)))
        else:
            self.__handler = self.__event_handlers.get(event, None)
            if self.__handler:
                self.__handler(**kwargs)
        self.logger.debug("sendEvent() exit")


    # +
    # (hidden) method: ocsCommandableEntityStartup()
    # -
    def _ocsCommandableEntityStartup(self, **kwargs):
        if self.__mgr and self.__ocsCommandableEntityStartupC:
            self.logger.debug("ocsCommandableEntityStartup() enter")
            if kwargs:
                for k, v in kwargs.items():
                    self.logger.debug("ocsCommandableEntityStartup(), {0:s}={1:s}".format(str(k),str(v)))

                # get values from kwargs dictionary
                self.__address = kwargs.get('Address', SAL__ERROR)
                self.__identifier = kwargs.get('Identifier', ocs_id(False))
                self.__name = kwargs.get('Name', os.getenv('USER'))
                self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
                self.__timestamp = kwargs.get('Timestamp', '')
                self.__match = re.search(ISO_PATTERN, self.__timestamp)
                if not self.__match:
                    self.__timestamp = ocs_mjd_to_iso(self.__identifier)

                # set up payload (cf. data = ocs_logevent_ocsCommandableEntityStartup(); data.Name = 'Something')
                self.__ocsCommandableEntityStartupC.Name = str(self.__name)
                self.__ocsCommandableEntityStartupC.Identifier = float(self.__identifier)
                self.__ocsCommandableEntityStartupC.Timestamp = str(self.__timestamp)
                self.__ocsCommandableEntityStartupC.Address = long(self.__address)
                self.__ocsCommandableEntityStartupC.priority = int(self.__priority)

                self.logger.debug("Name={0:s}".format(self.__ocsCommandableEntityStartupC.Name))
                self.logger.debug("Identifier={0:f}".format(self.__ocsCommandableEntityStartupC.Identifier))
                self.logger.debug("Timestamp={0:s}".format(self.__ocsCommandableEntityStartupC.Timestamp))
                self.logger.debug("Address={0:d}".format(self.__ocsCommandableEntityStartupC.Address))
                self.logger.debug("priority={0:d}".format(self.__ocsCommandableEntityStartupC.priority))

                # set up event (cf. mgr.salEvent("ocs_logevent_ocsCommandableEntityStartup"))
                lname = 'ocs_logevent_{0:s}'.format(self._event)
                self.logger.debug("setting up for event {0:s}".format(lname))
                self.__mgr.salEvent(lname)

                # issue event (cf. retval = mgr.logEvent_ocsCommandableEntityStartup(data, priority))
                self.logger.debug("issuing event {0:s}".format(lname))
                self.__retval = self.__mgr.logEvent_ocsCommandableEntityStartup(self.__ocsCommandableEntityStartupC, self.__ocsCommandableEntityStartupC.priority)
                self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
            self.logger.debug("ocsCommandableEntityStartup() exit")


    # +
    # (hidden) method: ocsCommandableEntityShutdown()
    # -
    def _ocsCommandableEntityShutdown(self, **kwargs):
        if self.__mgr and self.__ocsCommandableEntityShutdownC:
            self.logger.debug("ocsCommandableEntityShutdown() enter")
            if kwargs:
                for k, v in kwargs.items():
                    self.logger.debug("ocsCommandableEntityShutdown(), {0:s}={1:s}".format(str(k),str(v)))

                # get values from kwargs dictionary
                self.__address = kwargs.get('Address', SAL__ERROR)
                self.__identifier = kwargs.get('Identifier', ocs_id(False))
                self.__name = kwargs.get('Name', os.getenv('USER'))
                self.__priority = kwargs.get('priority', SAL__EVENT_INFO)
                self.__timestamp = kwargs.get('Timestamp', '')
                self.__match = re.search(ISO_PATTERN, self.__timestamp)
                if not self.__match:
                    self.__timestamp = ocs_mjd_to_iso(self.__identifier)

                # set up payload (cf. data = ocs_logevent_ocsCommandableEntityShutdown(); data.Name = 'Something')
                self.__ocsCommandableEntityShutdownC.Name = str(self.__name)
                self.__ocsCommandableEntityShutdownC.Identifier = float(self.__identifier)
                self.__ocsCommandableEntityShutdownC.Timestamp = str(self.__timestamp)
                self.__ocsCommandableEntityShutdownC.Address = long(self.__address)
                self.__ocsCommandableEntityShutdownC.priority = int(self.__priority)

                self.logger.debug("Name={0:s}".format(self.__ocsCommandableEntityShutdownC.Name))
                self.logger.debug("Identifier={0:f}".format(self.__ocsCommandableEntityShutdownC.Identifier))
                self.logger.debug("Timestamp={0:s}".format(self.__ocsCommandableEntityShutdownC.Timestamp))
                self.logger.debug("Address={0:d}".format(self.__ocsCommandableEntityShutdownC.Address))
                self.logger.debug("priority={0:d}".format(self.__ocsCommandableEntityShutdownC.priority))

                # set up event (cf. mgr.salEvent("ocs_logevent_ocsCommandableEntityShutdown"))
                lname = 'ocs_logevent_{0:s}'.format(self._event)
                self.logger.debug("setting up for event {0:s}".format(lname))
                self.__mgr.salEvent(lname)

                # issue event (cf. retval = mgr.logEvent_ocsCommandableEntityShutdown(data, priority))
                self.logger.debug("issuing event {0:s}".format(lname))
                self.__retval = self.__mgr.logEvent_ocsCommandableEntityShutdown(self.__ocsCommandableEntityShutdownC, self.__ocsCommandableEntityShutdownC.priority)
                self.logger.debug("issued event {0:s}, retval={1:d}".format(lname,self.__retval))
            self.logger.debug("ocsCommandableEntityShutdown() exit")

    # +
    # decorator(s)
    # -
    @property
    def simulate(self):
        return self._simulate

    @simulate.setter
    def simulate(self, simulate):
        if not isinstance(simulate, bool):
            raise OcsGenericException(OCS_GENERIC_ENTITY_ERROR_NOSIM, "simulate={0:s}".format(str(simulate)))
        else:
            self._simulate = simulate

    # +
    # method: __str__
    # -
    def __str__(self):
        return 'OcsEvents(\'{0:s}\', \'{1:s}\', simulate={2:s}) created at address {3:s}'.format(
            self._system, self._entity, str(self._simulate), hex(id(self)))

    # +
    # staticmethod: __dump__
    # -
    @staticmethod
    def __dump__(xv):
        if isinstance(xv, tuple) and not ():
            return ''.join("{:s}\n".format(str(v)) for v in xv)[:-1]
        elif isinstance(xv, list) and not []:
            return ''.join("{:s}\n".format(str(v)) for v in xv)[:-1]
        elif isinstance(x, dict) and not {}:
            return ''.join("{:s} : {:s}\n".format(str(k), str(v)) for k, v in xv.items())[:-1]
        else:
            return ''.join("{:s}\n".format(str(x)))


# +
# main()
# -
if __name__ == "__main__":

    ehv = None
    try:
        evh = OcsEvents(False)
    except OcsGenericEntityException as e:
        print(e.errstr)

    if evh:

        # send event with payload
        ocsid = ocs_id(False)
        evh.sendEvent('ocsCommandableEntityStartup', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)

        # send event with payload
        ocsid = ocs_id(False)
        evh.sendEvent('ocsCommandableEntityShutdown', Name='Junk', Identifier=float(ocsid), Timestamp=ocs_mjd_to_iso(ocsid), Address=id(evh), priority=SAL__EVENT_INFO)

