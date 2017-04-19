#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
import os
import random
import sys


# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/ocs_common.py, contains common declarations for the OCS components.
It provides constants, error codes, dictionaries, state machine structures, (output) formats,
(regular expression) patterns and variables utilized in other code within the ts_ocs_<component>
hierarchy.

Import:

    from ocs_common import *

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__email__ = "pdaly@lsst.org"
__file__ = "ocs_common.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# constant(s)
# -
OCS_CAMERA_COMMAND_TIMEOUT = 5
OCS_CAMERA_FILTER_COMMAND_TIMEOUT = 65
OCS_CAMERA_IMAGE_COMMAND_TIMEOUT = 40
OCS_GENERIC_COMMAND_TIMEOUT = 10
OCS_SEQUENCER_COMMAND_TIMEOUT = 10

OCS_SEQUENCER_ABORT_OFFSET = 1
OCS_SEQUENCER_DISABLE_OFFSET = 2
OCS_SEQUENCER_ENABLE_OFFSET = 3
OCS_SEQUENCER_ENTERCONTROL_OFFSET = 4
OCS_SEQUENCER_EXITCONTROL_OFFSET = 5
OCS_SEQUENCER_SETVALUE_OFFSET = 6
OCS_SEQUENCER_STANDBY_OFFSET = 7
OCS_SEQUENCER_START_OFFSET = 8
OCS_SEQUENCER_STOP_OFFSET = 9
OCS_SEQUENCER_SEQUENCE_OFFSET = 10
OCS_SEQUENCER_SCRIPT_OFFSET = 11
OCS_SEQUENCER_SHUTDOWN_OFFSET = 12


# +
# error code(s)
# -
OCS_CAMERA_ENTITY_ERROR_NOCFG = -1000
OCS_CAMERA_ENTITY_ERROR_NOROI = -1001
OCS_CAMERA_ENTITY_ERROR_NOTIM = -1002
OCS_CAMERA_ENTITY_ERROR_NOFIL = -1003
OCS_CAMERA_ENTITY_ERROR_NOIMG = -1004
OCS_CAMERA_ENTITY_ERROR_NOEXP = -1005
OCS_CAMERA_ENTITY_ERROR_NOSHT = -1006
OCS_CAMERA_ENTITY_ERROR_NOSCI = -1007
OCS_CAMERA_ENTITY_ERROR_NOGDR = -1008
OCS_CAMERA_ENTITY_ERROR_NOWFS = -1009
OCS_CAMERA_ENTITY_ERROR_NONAM = -1010
OCS_CAMERA_ENTITY_ERROR_NOMOD = -1011
OCS_CAMERA_ENTITY_ERROR_NOCLS = -1012
OCS_CAMERA_ENTITY_ERROR_NOCLR = -1013
OCS_CAMERA_ENTITY_ERROR_NOROW = -1014

OCS_EVENTS_ERROR_NOSIM = -2000
OCS_EVENTS_ERROR_NOVAL = -2001
OCS_EVENTS_ERROR_NOERR = -2002

OCS_GENERAL_ERROR_NOFIL = -3000
OCS_GENERAL_ERROR_NOPAR = -3001
OCS_GENERAL_ERROR_NOERR = -3002

OCS_GENERIC_ENTITY_BACKGROUND_COLOUR = '#f0f8ff'

OCS_GENERIC_ENTITY_ERROR_NOSYS = -4000
OCS_GENERIC_ENTITY_ERROR_NOENT = -4001
OCS_GENERIC_ENTITY_ERROR_NOPAR = -4002
OCS_GENERIC_ENTITY_ERROR_NOVAL = -4003
OCS_GENERIC_ENTITY_ERROR_NODEV = -4004
OCS_GENERIC_ENTITY_ERROR_NOSID = -4005
OCS_GENERIC_ENTITY_ERROR_NOSIM = -4006
OCS_GENERIC_ENTITY_ERROR_NOMOD = -4007
OCS_GENERIC_ENTITY_ERROR_NOATT = -4008
OCS_GENERIC_ENTITY_ERROR_NOCMD = -4009
OCS_GENERIC_ENTITY_ERROR_NOVBS = -4010
OCS_GENERIC_ENTITY_ERROR_NORSE = -4011
OCS_GENERIC_ENTITY_ERROR_NOOPS = -4012
OCS_GENERIC_ENTITY_ERROR_NOTIM = -4013
OCS_GENERIC_ENTITY_ERROR_NOERR = -4014

OCS_SEQUENCER_ENTITY_ERROR_NOSEQ = -5000
OCS_SEQUENCER_ENTITY_ERROR_NOSCR = -5001

OCS_XML_ERROR_NOXSD = -6000
OCS_XML_ERROR_NOXML = -6001
OCS_XML_ERROR_NOPRS = -6002
OCS_XML_ERROR_NOERR = -6003


# +
# dictionaries
# -
ocsCameraEntityErrorDictionary = {
    OCS_CAMERA_ENTITY_ERROR_NOCFG: "No valid configuration defined",
    OCS_CAMERA_ENTITY_ERROR_NOROI: "No valid region-of-interest defined",
    OCS_CAMERA_ENTITY_ERROR_NOTIM: "No valid deltaT time defined",
    OCS_CAMERA_ENTITY_ERROR_NOFIL: "No valid filter name defined",
    OCS_CAMERA_ENTITY_ERROR_NOIMG: "No valid number of images defined",
    OCS_CAMERA_ENTITY_ERROR_NOEXP: "No valid exposure time defined",
    OCS_CAMERA_ENTITY_ERROR_NOSHT: "No valid shutter condition defined",
    OCS_CAMERA_ENTITY_ERROR_NOSCI: "No valid science area defined",
    OCS_CAMERA_ENTITY_ERROR_NOGDR: "No valid guide area defined",
    OCS_CAMERA_ENTITY_ERROR_NOWFS: "No valid wfs area defined",
    OCS_CAMERA_ENTITY_ERROR_NONAM: "No valid sequence name defined",
    OCS_CAMERA_ENTITY_ERROR_NOMOD: "No valid module of that name",
    OCS_CAMERA_ENTITY_ERROR_NOCLS: "No valid class of that name",
    OCS_CAMERA_ENTITY_ERROR_NOCLR: "No valid number of clears defined",
    OCS_CAMERA_ENTITY_ERROR_NOROW: "No valid number of rows defined"
}

ocsEventsErrorDictionary = {
    OCS_EVENTS_ERROR_NOSIM: "No simulation flag defined",
    OCS_EVENTS_ERROR_NOVAL: "No value defined",
    OCS_EVENTS_ERROR_NOERR: "No valid error"
    }

ocsGeneralErrorDictionary = {
    OCS_GENERAL_ERROR_NOFIL: "No valid file",
    OCS_GENERAL_ERROR_NOPAR: "No parameter change allowed",
    OCS_GENERAL_ERROR_NOERR: "No valid error"
    }

ocsGenericEntityErrorDictionary = {
    OCS_GENERIC_ENTITY_ERROR_NOSYS: "No valid system defined",
    OCS_GENERIC_ENTITY_ERROR_NOENT: "No valid entity defined",
    OCS_GENERIC_ENTITY_ERROR_NOPAR: "No valid parameter defined",
    OCS_GENERIC_ENTITY_ERROR_NOVAL: "No valid value defined",
    OCS_GENERIC_ENTITY_ERROR_NODEV: "No valid device defined",
    OCS_GENERIC_ENTITY_ERROR_NOSID: "No valid startid defined",
    OCS_GENERIC_ENTITY_ERROR_NOSIM: "No valid simulation flag defined",
    OCS_GENERIC_ENTITY_ERROR_NOMOD: "No valid module of that name",
    OCS_GENERIC_ENTITY_ERROR_NOATT: "No valid module attribute",
    OCS_GENERIC_ENTITY_ERROR_NOCMD: "No valid command container",
    OCS_GENERIC_ENTITY_ERROR_NOVBS: "No valid verbose flag defined",
    OCS_GENERIC_ENTITY_ERROR_NORSE: "No valid raise flag defined",
    OCS_GENERIC_ENTITY_ERROR_NOOPS: "No valid operation defined",
    OCS_GENERIC_ENTITY_ERROR_NOTIM: "No valid timeout defined",
    OCS_GENERIC_ENTITY_ERROR_NOERR: "No valid generic error code defined"
    }

ocsSequencerEntityErrorDictionary = {
    OCS_SEQUENCER_ENTITY_ERROR_NOSEQ: "No valid sequence defined",
    OCS_SEQUENCER_ENTITY_ERROR_NOSCR: "No valid script defined"
}

ocsGenericEntityLogicDictionary = {
    "active": True,
    "enable": True,
    "enabled": True,
    "open": True,
    "t": True,
    "closed": False,
    "disable": False,
    "disabled": False,
    "f": False,
    "inactive": False,
    }

ocsXmlErrorDictionary = {
    OCS_XML_ERROR_NOXSD: "No valid schema file",
    OCS_XML_ERROR_NOXML: "No valid XML file",
    OCS_XML_ERROR_NOPRS: "No valid parser object",
    OCS_XML_ERROR_NOERR: "No valid error"
    }

ocsGenericEntitySystemDictionary = {
    "atcs": "ATCS",
    "calcs": "CALCS",
    "ccs": "CCS",
    "dmcs": "DMCS",
    "emcs": "EMCS",
    "ocs": "OCS",
    "sfcs": "SFCS",
    "tcs": "TCS",
    "test": "TEST"
    }

ocsGenericEntityEntityDictionary = {
    "ATCS": ['AuxiliaryMount', 'AuxiliaryEnclosure', 'AuxiliaryImager', 'AuxiliarySpectrograph'],
    "CALCS": ['CalibrationScreen', 'CalibrationIllumination', 'CalibrationDiodes',
              'CalibrationSpectrograph', 'CollimatedBeamProjector'],
    "CCS": ['Camera'],
    "DMCS": ['Archiver', 'CatchupArchiver', 'ProcessingCluster'],
    "EMCS": ['VisibleAllSkyCamera', 'InfraRedAllSkyCamera', 'DifferentialImageMotionMonitor'],
    "OCS": ['Sequencer'],
    "SFCS": ['AirConditioning', 'PowerConditioning'],
    "TCS": ['Tcs', 'Mount', 'Enclosure'],
    "TEST": ['Test']
    }

ocsGenericEntityBackgroundColour = {
    'ATCS': '#fff8dc',
    'CALCS': '#fffff0',
    'CCS': '#fffacd',
    'DMCS': '#fff5ee',
    'EMCS': '#f0fff0',
    'OCS': OCS_GENERIC_ENTITY_BACKGROUND_COLOUR,
    'SFCS': '#f5fffa',
    'TCS': '#f0ffff',
    'TEST': OCS_GENERIC_ENTITY_BACKGROUND_COLOUR
    }


# +
# state machine crap
# -
OCS_SUMMARY_STATE_OFFLINE = 0x1000
OCS_SUMMARY_STATE_STANDBY = 0x1001
OCS_SUMMARY_STATE_DISABLED = 0x1002
OCS_SUMMARY_STATE_ENABLED = 0x1003
OCS_SUMMARY_STATE_FAULT = 0x1004
OCS_SUMMARY_STATE_UNKNOWN = 0x1005

ocsEntitySummaryState = {
    OCS_SUMMARY_STATE_OFFLINE: 'offline',
    OCS_SUMMARY_STATE_STANDBY: 'standby',
    OCS_SUMMARY_STATE_DISABLED: 'disabled',
    OCS_SUMMARY_STATE_ENABLED: 'enabled',
    OCS_SUMMARY_STATE_FAULT: 'fault',
    OCS_SUMMARY_STATE_UNKNOWN: 'unknown'
    }

ocsEntitySummaryStateCommands = {
    OCS_SUMMARY_STATE_OFFLINE: ['enterControl'],
    OCS_SUMMARY_STATE_STANDBY: ['exitControl', 'start'],
    OCS_SUMMARY_STATE_DISABLED: ['enable', 'standby'],
    OCS_SUMMARY_STATE_ENABLED: ['abort', 'disable', 'setValue', 'stop'],
    OCS_SUMMARY_STATE_FAULT: [],
    OCS_SUMMARY_STATE_UNKNOWN: []
    }

ocsEntitySummaryStateConfigurations = {
    OCS_SUMMARY_STATE_OFFLINE: [],
    OCS_SUMMARY_STATE_STANDBY: ['Normal'],
    OCS_SUMMARY_STATE_DISABLED: [],
    OCS_SUMMARY_STATE_ENABLED: [],
    OCS_SUMMARY_STATE_FAULT: [],
    OCS_SUMMARY_STATE_UNKNOWN: []
    }

OcsSummaryStateEnum = {
    'disable': 0,
    'enable': 1,
    'fault': 2,
    'offline': 3,
    'standby': 4,
    'unknown': -1
    }


# +
# format(s)
# -
OCS_LOGGER_DIR = '/tmp'
OCS_LOGGER_FILE = 'ocs.log'
OCS_LOGGER_FILE_FORMAT = '%(asctime)-20s %(levelname)-9s %(name)-15s %(filename)-15s %(funcName)-15s ' \
                         'line:%(lineno)-5d PID:%(process)-6d Message: %(message)s'
OCS_LOGGER_CONSOLE_FORMAT = '%(asctime)-20s %(levelname)-9s %(filename)-15s %(funcName)-15s line:%(lineno)-5d ' \
                            'Message: %(message)s'


# +
# pattern(s)
# -
ISO_PATTERN = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}'
MJD_PATTERN = '^[0-9]{5}\.[0-9]{17}'


# +
# variable(s)
# -
pyvers = 'Python v' + str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2])
rseed = random.seed(os.getpid())
