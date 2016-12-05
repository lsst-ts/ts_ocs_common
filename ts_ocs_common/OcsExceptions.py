#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from ocs_id import *
from ocs_common import *
from OcsLogger import *
import os
import re
import socket


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Exception classes for  the OCS components"""
__email__ = "pdaly@@lsst.org"
__file__ = "OcsExceptions.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsGenericEntityException inherits from base Exception class
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
# class: OcsCameraEntityException inherits from OcsGenericEntityException
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
# class: OcsXmlException inherits from base Exception class
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
# class: OcsGeneralException inherits from base Exception class
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
# main()
# -
if __name__ == "__main__":

    # get a logger
    logger = OcsLogger().logger

    # log all generic errors
    for E in ocsGenericEntityErrorDictionary:
        try:
            raise OcsGenericEntityException(E, pyvers)
        except OcsGenericEntityException as e:
            logger.critical(e.errstr)

    # log all camera errors
    for E in ocsCameraEntityErrorDictionary:
        try:
            raise OcsCameraEntityException(E, pyvers)
        except OcsCameraEntityException as e:
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

    # log all xml errors
    for E in ocsXmlErrorDictionary:
        try:
            raise OcsXmlException(E, pyvers)
        except OcsXmlException as e:
            logger.critical(e.errstr)

