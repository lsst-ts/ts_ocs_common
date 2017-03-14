#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsExceptions import *


# +
# __doc__ string
# _
__doc__ = """test of OcsExceptions"""


# +
# function: test_camera_exception()
# -
def test_camera_exception():
    """
        :return: true
    """
    try:
        raise OcsCameraEntityException(OCS_CAMERA_ENTITY_ERROR_NOEXP, pyvers)
    except OcsCameraEntityException:
        assert True


# +
# function: test_camera_noexception()
# -
def test_camera_noexception():
    """
        :return: true
    """
    try:
        raise OcsCameraEntityException(-1, pyvers)
    except OcsCameraEntityException:
        assert True


# +
# function: test_camera_generic_exception()
# -
def test_camera_generic_exception():
    """
        :return: true
    """
    try:
        raise OcsCameraEntityException(OCS_GENERIC_ENTITY_ERROR_NOMOD, pyvers)
    except OcsGenericEntityException:
        assert True


# +
# function: test_generic_exception()
# -
def test_generic_exception():
    """
        :return: true
    """
    try:
        raise OcsGenericEntityException(OCS_GENERIC_ENTITY_ERROR_NOERR, pyvers)
    except OcsGenericEntityException:
        assert True


# +
# function: test_events_exception()
# -
def test_events_exception():
    """
        :return: true
    """
    try:
        raise OcsEventsException(OCS_EVENTS_ERROR_NOVAL, pyvers)
    except OcsEventsException:
        assert True


# +
# function: test_events_noexception()
# -
def test_events_noexception():
    """
        :return: true
    """
    try:
        raise OcsEventsException(-1, pyvers)
    except OcsEventsException:
        assert True


# +
# function: test_general_exception()
# -
def test_general_exception():
    """
        :return: true
    """
    try:
        raise OcsGeneralException(OCS_GENERAL_ERROR_NOFIL, pyvers)
    except OcsGeneralException:
        assert True


# +
# function: test_general_noexception()
# -
def test_general_noexception():
    """
        :return: true
    """
    try:
        raise OcsGeneralException(-1, pyvers)
    except OcsGeneralException:
        assert True


# +
# function: test_generic_noexception()
# -
def test_generic_noexception():
    """
        :return: true
    """
    try:
        raise OcsGenericEntityException(-1, pyvers)
    except OcsGenericEntityException:
        assert True


# +
# function: test_xml_exception()
# -
def test_xml_exception():
    """
        :return: true
    """
    try:
        raise OcsXmlException(OCS_XML_ERROR_NOXSD, pyvers)
    except OcsXmlException:
        assert True


# +
# function: test_xml_noexception()
# -
def test_xml_noexception():
    """
        :return: true
    """
    try:
        raise OcsXmlException(-1, pyvers)
    except OcsXmlException:
        assert True
