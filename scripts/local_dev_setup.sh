#!/usr/bin/env bash

readonly CURRENT_DIR=$(dirname "$(realpath "$0")")
readonly VARS_SH="$CURRENT_DIR/vars.sh"
readonly PY=$(which python3)

# Load common variables
. $VARS_SH

pushd $FRONT_ROOT
   npm install
popd

pushd $API_ROOT
  py_prefix=$(python3 -c "import sys;print(sys.prefix)")
  if [[ "$py_prefix" =~ .*virtualenvs.* ]] \
     || [[ "$py_prefix" =~ ^/Users/$(whoami).* ]] \
     || [[ "$py_prefix" =~ ^/home/$(whoami).* ]]; then
    pushd deploy
      pip install -r requirements.txt
    popd
  else
    echo "python virtual environment is not set." && exit 1
  fi

  # Check PostgresQL is running
  lsof -nP -i4TCP:$POSTGRESQL_PORT | grep LISTEN > /dev/null
  if [[ $? -eq 1 ]] ; then
    echo "PostgresQL is not running." && exit 1
  fi

  $PY manage.py migrate --no-input
  $PY manage.py inituser --username=root --password=rootroot --action=create_super_admin
popd
