#!/bin/sh

# +
# long form command line example(s)
# -
tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_xml.py --help"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_xml.py --help

for S in `ls $TS_OCS_COMMON_XSD/*.xsd`; do
  for F in `ls $TS_OCS_COMMON_XML/*.xml`; do
    tput setaf 2
    echo "Executing> python $TS_OCS_COMMON_SRC/ocs_xml.py --xsdfile=$S --xmlfile=$F"
    tput setaf 4
    python $TS_OCS_COMMON_SRC/ocs_xml.py --xsdfile=$S --xmlfile=$F
  done
done


# +
# short form command line example(s)
# -
tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_xml.py -h"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_xml.py -h

for S in `ls $TS_OCS_COMMON_XSD/*.xsd`; do
  for F in `ls $TS_OCS_COMMON_XML/*.xml`; do
    tput setaf 2
    echo "Executing> python $TS_OCS_COMMON_SRC/ocs_xml.py -s=$S -f=$F"
    tput setaf 4
    python $TS_OCS_COMMON_SRC/ocs_xml.py -s=$S -f=$F
  done
done

tput setaf sgr0
