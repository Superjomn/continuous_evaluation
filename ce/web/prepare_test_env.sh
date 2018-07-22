#!/usr/bin/env bash
set -ex

CE_ROOT="$PWD/.."
TEST_ENV_PATH="$CE_ROOT/../test_env"
CONFIG_PATH=$CE_ROOT/../default.conf

export PYTHONPATH="$CE_ROOT/.."

cd $TEST_ENV_PATH
python3 $CE_ROOT/main.py --config $CONFIG_PATH --is_test 1 --workspace $TEST_ENV_PATH
