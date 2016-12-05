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
import logging
import logging.config


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
__doc__ = """Logger class for the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsLogger.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsLogger()
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

        # logger dictionary
        logname = 'ocs.{0:s}.{1:s}'.format(self._name.lower(), self._subname.lower())
        logfile = '{0:s}/{1:s}.log'.format(OCS_LOGGER_DIR, logname)
        ocslog = '{0:s}/{1:s}'.format(OCS_LOGGER_DIR, OCS_LOGGER_FILE)
        ocsLoggerDictionary = {

            # logging version
            'version': 1,

            # do not disable any existing loggers
            'disable_existing_loggers' : False,


            # use the same formatter for everything
            'formatters': {
                'OcsFileFormatter': {
                    'format' : OCS_LOGGER_FILE_FORMAT
                },
                'OcsConsoleFormatter': {
                    'format' : OCS_LOGGER_CONSOLE_FORMAT
                }
            },

            # define file and console handlers
            'handlers': {
                'console': {
                    'class' : 'logging.StreamHandler',
                    'formatter' :'OcsConsoleFormatter',
                    'level' : 'DEBUG',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'backupCount' : 10,
                    'class' : 'logging.handlers.RotatingFileHandler',
                    'formatter' :'OcsFileFormatter',
                    'filename' : logfile,
                    'level' : 'DEBUG',
                    'maxBytes' : 1048576
                },
                'ocs': {
                    'backupCount' : 10,
                    'class' : 'logging.handlers.RotatingFileHandler',
                    'formatter' :'OcsFileFormatter',
                    'filename' : ocslog,
                    'level' : 'DEBUG',
                    'maxBytes' : 1048576
                }
            },        

            # make this logger use file and console handlers
            'loggers': {
                logname : {
                    'handlers' : ['console', 'file', 'ocs'],
                    'level' : 'DEBUG',
                    'propagate' : True
                }
            }
        }

        # configure logger 
        logging.config.dictConfig(ocsLoggerDictionary)

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
        self.logger.critical('name={0:s} cannot be reset!'.format(self._name))

    @property
    def subname(self):
        self.logger.debug("subname={0:s}".format(self._subname))
        return self._subname

    @subname.setter
    def subname(self, subname=''):
        self.logger.critical('subname={0:s} cannot be reset!'.format(self._subname))


# +
# main()
# -
if __name__ == "__main__":

    camlog = OcsLogger('CCS', 'camera')
    camlog.logger.info(camlog.name)
    camlog.logger.info(camlog.subname)

