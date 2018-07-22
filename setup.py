from __future__ import absolute_import

import os, sys
from sys import platform
from distutils import log
from distutils.spawn import find_executable
import setuptools.command.build_py
import setuptools
from setuptools import setup, Extension
import subprocess

TOP_DIR = os.path.realpath(os.path.dirname(__file__))


def read(file):
    return open(os.path.join(TOP_DIR, file)).read()


VERSION_NUMBER = read('VERSION_NUMBER')

install_requires = read('requirements.txt').split()
execute_requires = ['git', 'mongod', 'redis-server']


def die(msg):
    log.error(msg)
    sys.exit(1)


def CHECK(cond, msg):
    if not cond:
        die(msg)


for exe in execute_requires:
    CHECK(find_executable(exe), "command {} can not be found".format(exe))

packages = [
    'ce',
    'ce.web',
]

scripts = [
    'ce/run_ce.py',
    'ce/web/ce_web.py',
]

setup(
    name='CE',
    version=VERSION_NUMBER,
    author="Superjomn",
    description="Continuous Evaluation for any tasks.",
    license="",
    keywords="continuous evaluation dnn model",
    long_description=read('README.md'),
    install_requires=install_requires,
    package_data={
        'ce.web': ['html/*', 'static/*', 'static/bootstrap-4.1.2/*']
    },
    packages=packages,
    scripts=scripts, )
