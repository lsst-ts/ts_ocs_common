============
Installation
============

If the code tree is installed in /usr/local/ts_ocs_common (for example), do this::

  1. Edit /usr/local/ts_ocs_common/bin/setup.env.sh and set the root environmental variable:

       export TS_OCS_COMMON_PATH=/usr/local/ts_ocs_common

  2. Execute the file, once only (for this session):

       . $TS_OCS_COMMON_BIN/setup.env.sh

  3. Place the following in ~/.bashrc, ~/.profile, /etc/bashrc or /etc/profile:

       if [ -f /usr/local/ts_ocs_common/bin/setup.env.sh ]; then
         . /usr/local/ts_ocs_common/bin/setup.env.sh
       fi

  4. Edit $TS_OCS_COMMON_BIN/ocs_sal_get_constants.sh and change the location of the SAL_defines.h file:

       SAL_DEFINE_H="/usr/local/ts_sal/lsstsal/include/SAL_defines.h"

  5. Execute that file, once only:

       . $TS_OCS_COMMON_BIN/ocs_sal_get_constants.sh

