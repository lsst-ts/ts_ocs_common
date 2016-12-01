#!/bin/sh

. setup.env.sh

python -m pytest $TS_OCS_COMMON_TESTS/test_ocs_common.py
python -m pytest $TS_OCS_COMMON_TESTS/test_ocs_id.py
python -m pytest $TS_OCS_COMMON_TESTS/test_ocs_sal.py
python -m pytest $TS_OCS_COMMON_TESTS/test_ocs_xml.py
python -m pytest $TS_OCS_COMMON_TESTS/test_OcsExceptions.py
python -m pytest $TS_OCS_COMMON_TESTS/test_OcsLogger.py

