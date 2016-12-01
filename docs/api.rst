========
API
========

ocs_id::

   ocs_id(date_flag=False)
     - if date_flag is True, returns an ISO date-string
     - if date_flag is False, returns a MJD date-string
   ocs_iso_to_mjd(iso_string='')
     - converts ISO date-string to MJD date-string
   ocs_mjd_to_iso(mjd_string='')
     - converts MJD date-string to ISO date-string

ocs_sal::

   ocs_sal_import(module='')
     - imports a SAL module and returns object or None
   ocs_sal_attribute(sal_object=None, attribute='')
     - returns an attribute instance of a sal_object or None

ocs_xml::

   ocs_xml_get_parser(xs='')
     - returns a parser object for given schema, or None
   ocs_xml_validate(xs='', xf='')
     - returns True is file (xf) validates against schema (xs), otherwise returns False
