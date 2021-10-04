#!/usr/bin/env bash

readonly SCRIPTS_DIR=$(dirname "$(realpath "$0")")
readonly PROJECT_ROOT=$(dirname $SCRIPTS_DIR)
readonly API_ROOT="$PROJECT_ROOT/OnlineJudge"
readonly FRONT_ROOT="$PROJECT_ROOT/OnlineJudgeFE"
readonly JUDGER_ROOT="$PROJECT_ROOT/Judger"
readonly SYSTEM=$(uname -s)

readonly POSTGRESQL_PORT=5435
