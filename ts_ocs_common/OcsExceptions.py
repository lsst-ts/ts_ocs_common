#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsLogger import *
from ocs_common import *


# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/OcsExceptions.py, contains custom exception handling for the OCS coponents.
The error codes and strings are held within a dictionary specific to each error. The defined class either
inherits from the base class (Exception) or the base OCS class (OCsGenericEntityException). Higher level
code can reference an errstr (see examples). Python (unit) tests are provided in
$TS_OCS_COMMON_TESTS/test_OcsExceptions.py or all can be run from $TS_OCS_COMMON_BIN/test_ocs_common.sh

Import:

    from OcsExceptions import *

Example:

    camera = None
    try:
        camera = OcsGenericEntity('CCS', "Camera', False)
    except OcsGenericEntityException as e:
        print(e.errstr)

API:
    pyvers = 'Python v' + str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2])
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOROI, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOTIM, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOFIL, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOIMG, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOEXP, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOSHT, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOSCI, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOGDR, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOWFS, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NONAM, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOMOD, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOCLS, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOCLR, pyvers)
    raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOROW, pyvers)
    raise OcsCameraEntityException(OCS_EVENTS_ERROR_NOSIM, pyvers)
    raise OcsEventsException(OCS_EVENTS_ERROR_NOVAL, pyvers)
    raise OcsEventsException(OCS_EVENTS_ERROR_NOERR, pyvers)
    raise OCsGeneralException(OCS_GENERAL_ERROR_NOFIL, pyvers)
    raise OCsGeneralException(OCS_GENERAL_ERROR_NOPAR, pyvers)
    raise OCsGeneralException(OCS_GENERAL_ERROR_NOERR, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOSYS, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOENT, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOPAR, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOVAL, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NODEV, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOSID, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOSIM, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOMOD, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOATT, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOCMD, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOVBS, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NORSE, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOOPS, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOTIM, pyvers)
    raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOERR, pyvers)
    raise OcsSequencerException(OCS_SEQUENCER_ENTITY_ERROR_NOSEQ, pyvers)
    raise OcsSequencerException(OCS_SEQUENCER_ENTITY_ERROR_NOSCR, pyvers)
    raise OcsXmlException(OCS_XML_ERROR_NOXSD, pyvers)
    raise OcsXmlException(OCS_XML_ERROR_NOXML, pyvers)
    raise OcsXmlException(OCS_XML_ERROR_NOPRS, pyvers)
    raise OcsXmlException(OCS_XML_ERROR_NOERR, pyvers)

CLI:

    None

"""

# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__email__ = "pdaly@@lsst.org"
__file__ = "OcsExceptions.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsGenericEntityException() inherits from Exception class
# -
class OcsGenericEntityException(Exception):

    # +
    # __init__
    # -
    def __init__(self, inval=OCS_GENERIC_ENTITY_ERROR_NOERR, instr=pyvers):
        """
            :param inval: input error value [OCS_GENERIC_ENTITY_ERROR_NOERR]
            :param instr: input string for extra context [pyvers]
            :return: None but sets self.errstr
        """

        # declare some variables and initialize them
        self.inval = inval
        self.instr = instr
        self.errstr = ''

        # if inval is invalid, set default value
        if not isinstance(inval, int) or self.inval not in ocsGenericEntityErrorDictionary:
            self.instr = "inval={0:d}, instr=\'{1:s}\'".format(int(self.inval), str(self.instr))
            self.inval = OCS_GENERIC_ENTITY_ERROR_NOERR

        # format errstr
        self.errstr = "{0:s} ({1:s}), errval={2:d}".format(
            ocsGenericEntityErrorDictionary[self.inval], str(self.instr), self.inval)


# +
# class: OcsCameraEntityException() inherits from OcsGenericEntityException class
# -
class OcsCameraEntityException(OcsGenericEntityException):

    # +
    # __init__
    # -
    def __init__(self, inval=OCS_GENERIC_ENTITY_ERROR_NOERR, instr=pyvers):
        """
             :param inval: input error value [OCS_GENERIC_ENTITY_ERROR_NOERR]
             :param instr: input string for extra context [pyvers]
             :return: None but sets self.errstr
         """

        # declare some variables and initialize them
        self.inval = inval
        self.instr = instr
        self.errstr = ''

        # if not a camera error, invoke the super class
        if not isinstance(inval, int) or self.inval not in ocsCameraEntityErrorDictionary:
            super(OcsCameraEntityException, self).__init__(self.inval, self.instr)

        # format errstr
        else:
            self.errstr = "{0:s} ({1:s}), errval={2:d}".format(
                ocsCameraEntityErrorDictionary[self.inval], str(self.instr), self.inval)


# +
# class: OcsSequencerEntityException() inherits from OcsGenericEntityException class
# -
class OcsSequencerEntityException(OcsGenericEntityException):

    # +
    # __init__
    # -
    def __init__(self, inval=OCS_GENERIC_ENTITY_ERROR_NOERR, instr=pyvers):
        """
            :param inval: input error value [OCS_GENERIC_ENTITY_ERROR_NOERR]
            :param instr: input string for extra context [pyvers]
            :return: None but sets self.errstr
        """

        # declare some variables and initialize them
        self.inval = inval
        self.instr = instr
        self.errstr = ''

        # if not a camera error, invoke the super class
        if not isinstance(inval, int) or self.inval not in ocsSequencerEntityErrorDictionary:
            super(OcsSequencerEntityException, self).__init__(self.inval, self.instr)

        # format errstr
        else:
            self.errstr = "{0:s} ({1:s}), errval={2:d}".format(
                        ocsSequencerEntityErrorDictionary[self.inval], str(self.instr), self.inval)


# +
# class: OcsEventsException() inherits from base Exception class
# -
class OcsEventsException(Exception):

    # +
    # __init__
    # -
    def __init__(self, inval=OCS_EVENTS_ERROR_NOERR, instr=pyvers):
        """
            :param inval: input error value [OCS_EVENTS_ERROR_NOERR]
            :param instr: input string for extra context [pyvers]
            :return: None but sets self.errstr
        """

        # declare some variables and initialize them
        self.inval = inval
        self.instr = instr
        self.errstr = ''

        # if inval is invalid, set default value
        if not isinstance(inval, int) or self.inval not in ocsEventsErrorDictionary:
            self.instr = "inval={0:d}, instr=\'{1:s}\'".format(int(self.inval), str(self.instr))
            self.inval = OCS_EVENTS_ERROR_NOERR

        # format instr
        self.errstr = "{0:s} ({1:s}), errval={2:d}".format(
            ocsEventsErrorDictionary[self.inval], str(self.instr), self.inval)


# +
# class: OcsGeneralException() inherits from base Exception class
# -
class OcsGeneralException(Exception):

    # +
    # __init__
    # -
    def __init__(self, inval=OCS_GENERAL_ERROR_NOERR, instr=pyvers):
        """
            :param inval: input error value [OCS_GENERAL_ERROR_NOERR]
            :param instr: input string for extra context [pyvers]
            :return: None but sets self.errstr
        """

        # declare some variables and initialize them
        self.inval = inval
        self.instr = instr
        self.errstr = ''

        # if inval is invalid, set default value
        if not isinstance(inval, int) or self.inval not in ocsGeneralErrorDictionary:
            self.instr = "inval={0:d}, instr=\'{1:s}\'".format(int(self.inval), str(self.instr))
            self.inval = OCS_GENERAL_ERROR_NOERR

        # format instr
        self.errstr = "{0:s} ({1:s}), errval={2:d}".format(
            ocsGeneralErrorDictionary[self.inval], str(self.instr), self.inval)


# +
# class: OcsXmlException() inherits from base Exception class
# -
class OcsXmlException(Exception):

    # +
    # __init__
    # -
    def __init__(self, inval=OCS_XML_ERROR_NOERR, instr=pyvers):
        """
            :param inval: input error value [OCS_XML_ERROR_NOERR]
            :param instr: input string for extra context [pyvers]
            :return: None but sets self.errstr
        """

        # declare some variables and initialize them
        self.inval = inval
        self.instr = instr
        self.errstr = ''

        # if inval is invalid, set default value
        if not isinstance(inval, int) or self.inval not in ocsXmlErrorDictionary:
            self.instr = "inval={0:d}, instr=\'{1:s}\'".format(int(self.inval), str(self.instr))
            self.inval = OCS_XML_ERROR_NOERR

        # format instr
        self.errstr = "{0:s} ({1:s}), errval={2:d}".format(
            ocsXmlErrorDictionary[self.inval], str(self.instr), self.inval)


# +
# main()
# -
if __name__ == "__main__":

    # get a logger
    logger = OcsLogger().logger

    # log all camera errors
    for E in ocsCameraEntityErrorDictionary:
        try:
            raise OcsCameraEntityException(E, pyvers)
        except OcsCameraEntityException as e:
            logger.critical(e.errstr)

    # log all generic errors
    for E in ocsGenericEntityErrorDictionary:
        try:
            raise OcsGenericEntityException(E, pyvers)
        except OcsGenericEntityException as e:
            logger.critical(e.errstr)

    # log all general errors
    for E in ocsGeneralErrorDictionary:
        try:
            raise OcsGeneralException(E, pyvers)
        except OcsGeneralException as e:
            logger.critical(e.errstr)

    # log all events errors
    for E in ocsEventsErrorDictionary:
        try:
            raise OcsEventsException(E, pyvers)
        except OcsEventsException as e:
            logger.critical(e.errstr)

    # log all xml errors
    for E in ocsXmlErrorDictionary:
        try:
            raise OcsXmlException(E, pyvers)
        except OcsXmlException as e:
            logger.critical(e.errstr)

    # try some unknown errors
    try:
        raise OcsGenericEntityException(-1, pyvers)
    except OcsGenericEntityException as e:
        logger.critical(e.errstr)

    try:
        raise OcsCameraEntityException(-1, pyvers)
    except OcsCameraEntityException as e:
        logger.critical(e.errstr)
