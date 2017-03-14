#!/bin/sh

# +
# set the default path below
# -
export TS_OCS_COMMON_PATH=/usr/local/ts_ocs_common

# +
# set derived environmental variable(s)
# -
export TS_OCS_COMMON_BIN=${TS_OCS_COMMON_PATH}/bin
export TS_OCS_COMMON_CONF=${TS_OCS_COMMON_PATH}/conf
export TS_OCS_COMMON_DOCS=${TS_OCS_COMMON_PATH}/docs
export TS_OCS_COMMON_LOG=${TS_OCS_COMMON_PATH}/log
export TS_OCS_COMMON_SRC=${TS_OCS_COMMON_PATH}/ts_ocs_common
export TS_OCS_COMMON_TESTS=${TS_OCS_COMMON_PATH}/tests
export TS_OCS_COMMON_XML=${TS_OCS_COMMON_PATH}/xml
export TS_OCS_COMMON_XSD=${TS_OCS_COMMON_PATH}/xsd

# +
# adjust PATH and PYTHONPATH
# -
export PATH=${TS_OCS_COMMON_BIN}:${TS_OCS_COMMON_SRC}:${PATH}
export PYTHONPATH=${TS_OCS_COMMON_SRC}:${PYTHONPATH}
export PYTHONPATH=/usr/local/ts_sal/lib:${PYTHONPATH}
