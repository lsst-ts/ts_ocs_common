#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from ocs_xml import *


# +
# function: test_ocs_xml()
# -
def test_ocs_xml():
    """
        :return: true | false
    """
    xsd = glob.glob(os.getenv('TS_OCS_COMMON_XSD')+'/*.xsd')
    xml = glob.glob(os.getenv('TS_OCS_COMMON_XML')+'/*.xml')
    for S in xsd:
        for F in xml:
            try:
                ocs_xml_validate(ocs_xml_get_parser(S), F)
            except OcsXmlException:
                assert False
    assert True
