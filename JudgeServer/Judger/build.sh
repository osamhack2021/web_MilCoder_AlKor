#!/usr/bin/env bash
readonly CURRENT_DIR=$(dirname "$(realpath "$0")")
readonly VARS_SH="$(dirname $CURRENT_DIR)/scripts/vars.sh"

echo $VARS_SH
. $VARS_SH

case "$SYSTEM" in
  Linux)
    sudo apt-get install build-essential libseccomp-dev cmake
    ;;
  *)
    echo "Judger does not support $SYSTEM system."
    exit 1
esac

BUILD_DIR="$JUDGER_ROOT/build"
if [[ -f "$BUILD_DIR" ]] ; then
  rm -rf $BUILD_DIR
fi
mkdir $BUILD_DIR
pushd $BUILD_DIR
  cmake ..
  make -j$(nproc)
  make install
popd
