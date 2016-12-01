========
CLI
========

python $TS_OCS_COMMON_SRC/ocs_id.py [-h] [-c CONVERT] [-a | -d | -i | -m]

 [<args>]::

  -h, --help            show this help message and exit
  -c CONVERT, --convert CONVERT
                        convert CONVERT = { ISO | MJD } string to other format
  -a, --ascii           return an ISO8660 date string from the current time
  -d, --digital         return a MJD string from the current time
  -i, --iso             return an ISO8660 date string from the current time
  -m, --mjd             return a MJD string from the current time

python $TS_OCS_COMMON_SRC/ocs_sal.py [-h] [-m MODULE] [-a ATTRIBUTE]

 [<args>]::

  -h, --help            show this help message and exit
  -m MODULE, --module MODULE
                        input SAL module
  -a ATTRIBUTE, --attribute ATTRIBUTE
                        input SAL module attribute
python $TS_OCS_COMMON_SRC/ocs_xml.py [-h] [-s XSDFILE] [-f XMLFILE]

 [<args>]::

  -h, --help            show this help message and exit
  -s XSDFILE, --xsdfile XSDFILE
                        input XSD file
  -f XMLFILE, --xmlfile XMLFILE
                        input XML file
