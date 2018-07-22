#!/usr/bin/env bash

cd $ce_root
./install.sh

python3 setup.py bdist_wheel
pip install --upgrade dist/CE-0.0.2-py3-none-any.whl

cd $ce_tasks
run_ce.py
