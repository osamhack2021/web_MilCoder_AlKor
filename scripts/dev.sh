#!/usr/bin/env bash

command=$1
opt=$2
readonly CURRENT_DIR=$(dirname "$(realpath "$0")")
readonly VARS_SH="$CURRENT_DIR/vars.sh"
readonly PY=$(which python3)

# Load common variables
. $VARS_SH

function nvm_check() {
  current_node_version=$(cat ~/.nvm/alias/default)
  echo $NVM_BIN
  if [[ ! -f "$NVM_SH" ]]; then
    echo "NVM is not installed. Run:"
    echo "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
    return 1
  elif [[ ! -f "$HOME/.nvm/versions/node/v8.12.0/bin/node" ]]; then
    echo "Current node version is not $NODE_VERSION. Run:"
    echo "nvm install $NODE_VERSION"
    return 1
  elif [[ ! $NVM_BIN =~ .*8.12.*/bin ]]; then
    echo "Current node version is not $NODE_VERSION"
    echo "nvm use $NODE_VERSION"
    return 1
  fi

  return 0
}

function virtualenv_check() {
  py_prefix=$(python3 -c "import sys;print(sys.prefix)")
  if [[ "$py_prefix" =~ .*virtualenvs.* ]] \
       || [[ "$py_prefix" =~ ^/Users/$(whoami).* ]] \
       || [[ "$py_prefix" =~ ^/home/$(whoami).* ]]; then
    return 0
   fi
   echo "python virtual environment is not set."
   return 1
}

function setup() {
  docker-compose -f docker-compose.dev.yml up -d

  db_online=1
  while [ $db_online -eq 1 ]; do
    docker-compose ps --status running -q oj-postgres-dev >/dev/null
    db_online=$?
    sleep 1
  done

  pushd $FRONT_ROOT
    npm install
  popd

  pushd $API_ROOT
    pushd deploy
      pip install -r requirements.txt
    popd

    $PY manage.py migrate --no-input
    $PY manage.py inituser --username=root --password=rootroot --action=create_super_admin
  popd
}

function start() {
  echo "Launching API server..."
  pushd $API_ROOT
    export JUDGE_SERVER_TOKEN
    $PY manage.py runserver >> $API_OUT 2>&1 &
    echo $! > $API_PID_FILE
  popd

  echo "Launching FRONT..."
  pushd $FRONT_ROOT
    npm run build:dll 2>/dev/null
    NODE_ENV=development TARGET=http://127.0.0.1:$API_PORT npm run dev >> $FRONT_OUT 2>&1 &
  popd
}

function stop() {
  pushd $PROJECT_ROOT
    echo "Kill API server"
    pkill -TERM $(cat $API_PID_FILE) && rm $API_PID_FILE || echo "Failed to kill API Server"
    ps -ef | grep "manage.py runserver" | awk '{print $2}' | xargs kill -9 2>/dev/null

    echo "Kill FRONT"
    killall -9 npm node open || echo "Failed to kill FRONT"
  popd
}

nvm_check || exit 1
virtualenv_check || exit 1

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
