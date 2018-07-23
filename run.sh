#!/usr/bin/env bash
set -ex

cd $ce_root
./install.sh

python3 setup.py bdist_wheel
pip3 install --upgrade dist/CE-0.0.2-py3-none-any.whl

cd $ce_tasks
run_ce.py --config $ce_config
