#!/usr/bin/env bash

readonly CURRENT_DIR=$(dirname "$(realpath "$0")")
readonly VARS_SH="$CURRENT_DIR/vars.sh"

# Load common variables
. $VARS_SH

pushd $FRONT_ROOT
   npm install
popd

pushd $API_ROOT
  py_prefix=$(python -c "import sys;print(sys.prefix)")
  if [[ "$py_prefix" =~ .*virtualenvs.* ]] \
     || [[ "$py_prefix" =~ ^/Users/$(whoami).* ]] \
     || [[ "$py_prefix" =~ ^/home/$(whoami).* ]]; then
    pushd deploy
      pip install -r requirements.txt
    popd
  else
    echo "python virtual environment is not set." && exit 1
  fi
  pushd deploy
    python manage.py migrate --no-input
    python manage.py inituser --username=root --password=rootroot --action=create_super_admin
  popd
popd
