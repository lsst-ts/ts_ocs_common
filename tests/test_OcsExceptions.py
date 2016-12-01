#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


# +
# import(s)
# -
from OcsExceptions import *


# +
# function: test_generic_exception()
# -
def test_generic_exception():
    """
        :return: true | false
    """
    try:
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOERR, pyvers)
    except OcsGenericEntityException as e:
        assert True
    else:
        assert False


# +
# function: test_generic_noexception()
# -
def test_generic_noexception():
    """
        :return: true | false
    """
    try:
        raise OcsGenericEntityException(-1, pyvers)
    except OcsGenericEntityException as e:
        assert True
    else:
        assert False


# +
# function: test_camera_exception()
# -
def test_camera_exception():
    """
        :return: true | false
    """
    try:
        raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOEXP, pyvers)
    except OcsCameraEntityException as e:
        assert True
    else:
        assert False


# +
# function: test_camera_noexception()
# -
def test_camera_noexception():
    """
        :return: true | false
    """
    try:
        raise OcsCameraEntityException(-1, pyvers)
    except OcsCameraEntityException as e:
        assert True
    else:
        assert False


# +
# function: test_camera_generic_exception()
# -
def test_camera_generic_exception():
    """
        :return: true | false
    """
    try:
        raise OcsCameraEntityException(OCS_GENERIC_ENTITY_ERROR_NOMOD, pyvers)
    except OcsGenericEntityException as e:
        assert True
    else:
        assert False


# +
# function: test_xml_exception()
# -
def test_xml_exception():
    """
        :return: true | false
    """
    try:
        raise OcsXmlException(OCS_XML_ERROR_NOXSD, pyvers)
    except OcsXmlException as e:
        assert True
    else:
        assert False


# +
# function: test_xml_noexception()
# -
def test_xml_noexception():
    """
        :return: true | false
    """
    try:
        raise OcsXmlException(-1, pyvers)
    except OcsXmlException as e:
        assert True
    else:
        assert False

