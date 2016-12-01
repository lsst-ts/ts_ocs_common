#!/bin/sh

# +
# long form command line example(s)
# -
tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_sal.py --help"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_sal.py --help

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_sal.py --module=SALPY_camera --attribute=SAL_camera"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_sal.py --module=SALPY_camera --attribute=SAL_camera

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_sal.py --module=SALPY_$$"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_sal.py --module=SALPY_$$

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_sal.py --module=SALPY_camera --attribute=SAL_$$"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_sal.py --module=SALPY_camera --attribute=SAL_$$

# +
# short form command line example(s)
# -
tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_sal.py -h"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_sal.py -h

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_sal.py -m=SALPY_camera -a=SAL_camera"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_sal.py -m=SALPY_camera -a=SAL_camera

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_sal.py -m=SALPY_$$"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_sal.py -m=SALPY_$$

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_sal.py -m=SALPY_camera -a=SAL_$$"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_sal.py -m=SALPY_camera -a=SAL_$$

tput setaf sgr0
