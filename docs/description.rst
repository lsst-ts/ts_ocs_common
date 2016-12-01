================
Description
================


ocs_common.py::

 This file contains all the common constants, SAL constants, dictionaries, 
 logging formats, pattern matches and variables used in the OCS code.

ocs_id.py::

 This file contains the ability to generate unique timestamps in ISO or 
 MJD format and convert between them. The ISO format is provided for 
 readablity whilst the MJD format can be used as a monotinically increasing 
 floating point number.

ocs_sal.py::

 This file contains code for accessing the SAL and returns instantiated 
 objects or None depending on success or failure.

ocs_xml.py::

 This file provides a means to validate any XML file against any schema and 
 returns with True (validates OK) or False (does not validate) plus a 
 traceback on the cause of the non-validation.

OcsExceptions.py::

 This file contains the (base and derived) exception classes used in the OCS.

OcsLogger.py::

 This file contains the common framework for using (singleton) logging in the OCS.
