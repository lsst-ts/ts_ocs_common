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
from ocs_sal_constants import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Declarations for common values in the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "ocs_common.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# constant(s)
# -
OCS_GENERIC_ENTITY_ERROR_NOSYS = -100
OCS_GENERIC_ENTITY_ERROR_NOENT = -101
OCS_GENERIC_ENTITY_ERROR_NOPAR = -102
OCS_GENERIC_ENTITY_ERROR_NOVAL = -103
OCS_GENERIC_ENTITY_ERROR_NODEV = -104
OCS_GENERIC_ENTITY_ERROR_NOSID = -105
OCS_GENERIC_ENTITY_ERROR_NOSIM = -106
OCS_GENERIC_ENTITY_ERROR_NOMOD = -107
OCS_GENERIC_ENTITY_ERROR_NOATT = -108
OCS_GENERIC_ENTITY_ERROR_NOCMD = -109
OCS_GENERIC_ENTITY_ERROR_NOVBS = -110
OCS_GENERIC_ENTITY_ERROR_NORSE = -111
OCS_GENERIC_ENTITY_ERROR_NOOPS = -112
OCS_GENERIC_ENTITY_ERROR_NOERR = -113

OCS_GENERIC_COMMAND_TIMEOUT = 10

OCS_CAMERA_ENTITY_ERROR_NOCFG = -200
OCS_CAMERA_ENTITY_ERROR_NOROI = -201
OCS_CAMERA_ENTITY_ERROR_NOTIM = -202
OCS_CAMERA_ENTITY_ERROR_NOFIL = -203
OCS_CAMERA_ENTITY_ERROR_NOIMG = -204
OCS_CAMERA_ENTITY_ERROR_NOEXP = -205
OCS_CAMERA_ENTITY_ERROR_NOSHT = -206
OCS_CAMERA_ENTITY_ERROR_NOSCI = -207
OCS_CAMERA_ENTITY_ERROR_NOGDR = -208
OCS_CAMERA_ENTITY_ERROR_NOWFS = -209
OCS_CAMERA_ENTITY_ERROR_NONAM = -210
OCS_CAMERA_ENTITY_ERROR_NOMOD = -211
OCS_CAMERA_ENTITY_ERROR_NOCLS = -212

OCS_CAMERA_COMMAND_TIMEOUT = 5

OCS_XML_ERROR_NOXSD = -300
OCS_XML_ERROR_NOXML = -301
OCS_XML_ERROR_NOPRS = -302
OCS_XML_ERROR_NOERR = -303

OCS_GENERAL_ERROR_NOFIL = -300
OCS_GENERAL_ERROR_NOERR = -301


# +
# dictionaries
# -
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
    OCS_GENERIC_ENTITY_ERROR_NOERR: "No valid generic error code defined"
    }

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
    OCS_CAMERA_ENTITY_ERROR_NOCLS: "No valid class of that name"
    }

ocsXmlErrorDictionary = {
    OCS_XML_ERROR_NOXSD: "No valid schema file",
    OCS_XML_ERROR_NOXML: "No valid XML file",
    OCS_XML_ERROR_NOPRS: "No valid parser object",
    OCS_XML_ERROR_NOERR: "No valid error"
    }

ocsGeneralErrorDictionary = {
    OCS_GENERAL_ERROR_NOFIL: "No valid file",
    OCS_GENERAL_ERROR_NOERR: "No valid error"
    }

ocsGenericEntitySystemDictionary = {
    "atcs": "ATCS",
    "calcs": "CALCS",
    "ccs": "CCS",
    "dmcs": "DMCS",
    "emcs": "EMCS",
    "sfcs": "SFCS",
    "tcs": "TCS",
    "test": "TEST"
    }

ocsGenericEntityEntityDictionary = {
    "ATCS": ['AuxiliaryMount', 'AuxiliaryEnclosure', 'AuxiliaryImager', 'AuxiliarySpectrograph'],
    "CALCS": ['CalibrationScreen', 'CalibrationIllumination', 'CalibrationDiodes',
              'CalibrationSpectrograph', 'CollimatedBeamProjector'],
    "CCS": ['Camera'],
    "DMCS": ['Archiver', 'CatchupArchiver', 'ProcessingCluster', 'EFDReplicator', 'CalibrationGenerator'],
    "EMCS": ['VisibleAllSkyCamera', 'InfraRedAllSkyCamera', 'DifferentialImageMotionMonitor'],
    "SFCS": ['AirConditioning', 'PowerConditioning'],
    "TCS": ['Mount', 'Enclosure'],
    "TEST": ['Test']
    }


# +
# format(s)
# -
OCS_LOGGER_DIR = '/tmp'
OCS_LOGGER_FILE = 'ocs.log'
OCS_LOGGER_FILE_FORMAT = '%(asctime)-20s %(levelname)-9s %(name)-15s %(filename)-15s %(funcName)-15s line:%(lineno)-5d PID:%(process)-6d Message: %(message)s'
OCS_LOGGER_CONSOLE_FORMAT = '%(asctime)-20s %(levelname)-9s %(filename)-15s %(funcName)-15s line:%(lineno)-5d Message: %(message)s'


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

