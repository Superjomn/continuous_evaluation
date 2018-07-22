#!/usr/bin/env bash
python3 setup.py bdist_wheel
pip3 install --upgrade dist/CE-0.0.2-py3-none-any.whl
