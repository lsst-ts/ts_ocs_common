#!/bin/sh

# +
# NB: Edit the location of the SAL_defines.h input file!!
# -
SAL_DEFINE_H="${LSST_SDK_INSTALL}/lsstsal/include/SAL_defines.h"

# +
# Create the file $TS_OCS_COMMON_SRC/ocs_sal_constants.py
# -
python $TS_OCS_COMMON_SRC/ocs_get_sal_constants.py --salfile=$SAL_DEFINE_H --output=$TS_OCS_COMMON_SRC/ocs_sal_constants.py
chmod 755 $TS_OCS_COMMON_SRC/ocs_sal_constants.py
