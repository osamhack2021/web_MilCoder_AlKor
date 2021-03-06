#!/usr/bin/env bash

# Common variables
readonly SYSTEM=$(uname -s)
readonly NODE_VERSION="8.12.0"
readonly NVM_SH="$HOME/.nvm/nvm.sh"

# Project variables
readonly SCRIPTS_DIR=$(dirname "$(realpath "$0")")
readonly PROJECT_ROOT=$(dirname $SCRIPTS_DIR)

# Service variables
readonly JUDGE_SERVER_TOKEN="e23db591aae7131eaff626d896a30c440435524acfc837224f5391709a15fa63"

readonly API_ROOT="$PROJECT_ROOT/OnlineJudge"
readonly API_PID_FILE="$PROJECT_ROOT/run/api.pid"
readonly API_OUT="$PROJECT_ROOT/run/api.log"

readonly FRONT_ROOT="$PROJECT_ROOT/OnlineJudgeFE"
readonly FRONT_PID_FILE="$PROJECT_ROOT/run/front.pid"
readonly FRONT_OUT="$PROJECT_ROOT/run/front.log"

readonly JUDGER_ROOT="$PROJECT_ROOT/Judger"

# Service network variables
readonly API_PORT=8000
readonly FRONT_PORT=8080
readonly POSTGRESQL_PORT=5435
readonly JUDGE0_PORT=2358

# Common jobs
mkdir -p $PROJECT_ROOT/run
