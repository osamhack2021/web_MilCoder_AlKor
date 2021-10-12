#!/usr/bin/env bash

command=$1
readonly CURRENT_DIR=$(dirname "$(realpath "$0")")
readonly VARS_SH="$CURRENT_DIR/vars.sh"
readonly PY=$(which python3)

# Load common variables
. $VARS_SH

function setup() {
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
      sudo lsof -nP -i4TCP:$POSTGRESQL_PORT | grep LISTEN > /dev/null
      if [[ $? -eq 1 ]] ; then
        echo "PostgresQL is not running." && exit 1
      fi
    fi

    $PY manage.py migrate --no-input
    $PY manage.py inituser --username=root --password=rootroot --action=create_super_admin
  popd
}

function start() {
  echo "Launching API server..."
  pushd $API_ROOT
    $PY manage.py runserver >> $API_OUT 2>&1 &
    sleep 2
    ps aux | grep manage.py | grep -v grep | awk '{print $2}' > $API_PID_FILE
  popd

  echo "Launching FRONT..."
  pushd $FRONT_ROOT
    npm run build:dll 2>/dev/null
    NODE_ENV=development TARGET=http://127.0.0.1:$API_PORT npm run dev >> $FRONT_OUT 2>&1 &
    echo $! > $FRONT_PID_FILE
    sleep 4
    ps aux | grep dev-server.js | grep -v grep | awk '{print $2}' >> $FRONT_PID_FILE
  popd
}

function stop() {
  echo "Kill API server"
  cat $API_PID_FILE | xargs kill -9 $1
  rm $API_PID_FILE

  echo "Kill FRONT"
  cat $FRONT_PID_FILE | xargs kill -9 $1
  ps aux | grep open | grep $FRONT_PORT | awk '{print $2}' | xargs kill -9 2>/dev/null
  rm $FRONT_PID_FILE
}

case "$command" in
  setup)
    setup
    ;;
  start)
    start
    ;;
  stop)
    stop
    ;;
  *)
    echo "Usage: $(basename "$0") [setup|start|stop]"
esac
