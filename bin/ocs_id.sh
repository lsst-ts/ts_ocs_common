#!/bin/sh

# +
# long form command line example(s):
# -
for CLI in '--help' '--ascii' '--iso' '--digital' '--mjd'; do
  tput setaf 2
  echo "Executing> python $TS_OCS_COMMON_SRC/ocs_id.py $CLI"
  tput setaf 4
  python $TS_OCS_COMMON_SRC/ocs_id.py $CLI
done

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_id.py --convert \`python $TS_OCS_COMMON_SRC/ocs_id.py --ascii\`"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_id.py --convert `python $TS_OCS_COMMON_SRC/ocs_id.py --ascii`

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_id.py --convert \`python $TS_OCS_COMMON_SRC/ocs_id.py --digital\`"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_id.py --convert `python $TS_OCS_COMMON_SRC/ocs_id.py --digital`

# +
# short form command line example(s)
# -
for CLI in '-h' '-a' '-i' '-d' '-m'; do
  tput setaf 2
  echo "Executing> python $TS_OCS_COMMON_SRC/ocs_id.py $CLI"
  tput setaf 4
  python $TS_OCS_COMMON_SRC/ocs_id.py $CLI
done

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_id.py -c \`python $TS_OCS_COMMON_SRC/ocs_id.py -a\`"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_id.py -c `python $TS_OCS_COMMON_SRC/ocs_id.py -a`

tput setaf 2
echo "Executing> python $TS_OCS_COMMON_SRC/ocs_id.py -c \`python $TS_OCS_COMMON_SRC/ocs_id.py -d\`"
tput setaf 4
python $TS_OCS_COMMON_SRC/ocs_id.py -c `python $TS_OCS_COMMON_SRC/ocs_id.py -d`

tput setaf sgr0
