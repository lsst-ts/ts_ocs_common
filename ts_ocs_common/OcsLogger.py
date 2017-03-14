#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
import logging.config
from OcsExceptions import *
from ocs_common import *
import os

# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/OcsLogger.py, contains code for log handling for the OCS components.
Python (unit) tests are provided in $TS_OCS_COMMON_TESTS/test_OcsLogger.py or all can be run from
$TS_OCS_COMMON_BIN/test_ocs_common.sh

Import:

    from OcsLogger import *

Example:

    log = None
    try:
        log = OcsLogger('Name', 'Subname')
    except:
        pass
    if log:
        log.logger.info(log.name)
        log.logger.info(log.subname)
        log.logger.info('This is an info message')
        log.logger.debug('This is a debug mesage')
        log.logger.error('This is an error message')
        log.logger.critical('This is a critical message')


API:

    OcsLogger(name='', subname='')
        connects to the (singleton) logger object for given 'name' and 'subname'. A log is created in 3 places:
        the console,  /tmp/ocs.name.subname.log and the shared log file /tmp/ocs.log. The format of each log is
        associated with the constants OCS_LOGGER_FILE_FORMAT or OCS_LOGGER_CONSOLE_FORMAT. It supports debug, info,
        error and critical log messages.

CLI:

    None

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__email__ = "pdaly@lsst.org"
__file__ = "OcsLogger.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsLogger() inherits from the object class
# -
class OcsLogger(object):

    # +
    # method: __init__
    # -
    def __init__(self, name='', subname=''):
        """
            :param name: name of logger
            :param subname: subname name of logger
            :return: None or object representing the logger
        """

        # get arguments(s)
        self._name = name
        self._subname = subname

        # check name
        if not isinstance(self._name, str) or self._name == '':
            self._name = os.getenv('USER')

        # check subname
        if not isinstance(self._subname, str) or self._subname == '':
            self._subname = str(os.getpid())

        # define some variables and initialize them
        self._msg = None

        # logger dictionary
        logname = 'ocs.{0:s}.{1:s}'.format(self._name, self._subname)
        logfile = '{0:s}/{1:s}.log'.format(OCS_LOGGER_DIR, logname)
        ocslog = '{0:s}/{1:s}'.format(OCS_LOGGER_DIR, OCS_LOGGER_FILE)
        ocs_logger_dictionary = {

            # logging version
            'version': 1,

            # do not disable any existing loggers
            'disable_existing_loggers': False,


            # use the same formatter for everything
            'formatters': {
                'OcsFileFormatter': {
                    'format': OCS_LOGGER_FILE_FORMAT
                },
                'OcsConsoleFormatter': {
                    'format': OCS_LOGGER_CONSOLE_FORMAT
                }
            },

            # define file and console handlers
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'OcsConsoleFormatter',
                    'level': 'DEBUG',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'backupCount': 10,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'OcsFileFormatter',
                    'filename': logfile,
                    'level': 'DEBUG',
                    'maxBytes': 1048576
                },
                'ocs': {
                    'backupCount': 10,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'OcsFileFormatter',
                    'filename': ocslog,
                    'level': 'DEBUG',
                    'maxBytes': 1048576
                }
            },        

            # make this logger use file and console handlers
            'loggers': {
                logname: {
                    'handlers': ['console', 'file', 'ocs'],
                    'level': 'DEBUG',
                    'propagate': True
                }
            }
        }

        # configure logger 
        logging.config.dictConfig(ocs_logger_dictionary)

        # get logger 
        self.logger = logging.getLogger(logname)
        self.logger.debug("Started {0:s} {1:s} logger".format(self._name, self._subname))

    # +
    # Decorator(s)
    # -
    @property
    def name(self):
        self.logger.debug("name={0:s}".format(self._name))
        return self._name

    @name.setter
    def name(self, name=''):
        self._msg = 'name={0:s} cannot be reset!'.format(name)
        self.logger.critical(self._msg)
        raise OcsGeneralException(OCS_GENERAL_ERROR_NOPAR, self._msg)

    @property
    def subname(self):
        self.logger.debug("subname={0:s}".format(self._subname))
        return self._subname

    @subname.setter
    def subname(self, subname=''):
        self._msg = 'subname={0:s} cannot be reset!'.format(subname)
        self.logger.critical(self._msg)
        raise OcsGeneralException(OCS_GENERAL_ERROR_NOPAR, self._msg)


# +
# main()
# -
if __name__ == "__main__":

    camlog = OcsLogger('CCS', 'camera')
    camlog.logger.info(camlog.name)
    camlog.logger.info(camlog.subname)
