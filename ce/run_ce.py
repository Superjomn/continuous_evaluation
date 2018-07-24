#!/usr/bin/env python
'''
This file contains all the commands.
'''
import argparse
import os
import sys

import ce.data_view as dv
from ce import repo
from ce.environ import Environ
from ce.utils import local, __, __check_type__
from ce.utils import log

log.info = print
log.warn = print


def evaluate_all_tasks():
    '''
    Evaluate all the tasks
    :return: list of status.
    '''
    log.warn('environ.workspace', Environ.workspace())
    with local.cwd(Environ.workspace()):
        log.info('Evaluate all the tasks in %s' % __('pwd'))

        # Set a environment so that all the tasks can get the commit.
        Environ.set_commit(
            repo.get_commit(Environ.config().get('repo', 'local_path')))

        commit = dv.Commit(
            commitid=Environ.commit(), tasks=tasks_to_evaluate())
        commit.persist()

        dirs = __('ls').split()
        sucs = []
        for task_name in dirs:
            suc = evaluate_task(task_name)
            sucs.append(suc)
        return sucs

    update_commit_status()


def update_commit_status():
    '''
    Update the status of a commit.
    :return: None
    '''
    suc = True
    for task in tasks_to_evaluate():
        task = dv.Task(commitid=Environ.commit(), name=task)
        info = task.fetch_info()
        for kpi in info.kpis:
            kpi = dv.Kpi(commitid=Environ.commit(), task=task, name=kpi)
            data = kpi.fetch_infos()
            if not data.passed:
                suc = False
                break
    state = 'passed' if suc else 'failed'
    commit = dv.Commit(commitid=Environ.commit())
    dv.DB.Instance().update_fields(commit.record_id, {'state': state})


def evaluate_task(task_name):
    '''
    Evaluate a task.
    :param task_name:
    :return: True for success, False for failure.
    '''
    __check_type__.match_str(task_name)
    if '.' in task_name or task_name.startswith('__'):
        log.warn('skip path', task_name)
        return

    log.warn('evaluating task [%s]' % task_name)
    # Set a environment so that all the kpis can get the task_name.
    Environ.set_task(task_name)

    task_dir = os.path.join(Environ.workspace(), task_name)
    with local.cwd(task_dir):
        if not os.path.isfile('run.xsh'):
            log.warn('Skip no-task path %s' % __('pwd'))
            return

        suc = False

        logs = __('./run.xsh')
        log.info(logs)
        suc = True

        print('tasks_root', Environ.workspace())
        kpis = [kpi.name for kpi in load_kpis(Environ.workspace(), task_name)]
        task = dv.Task(commitid=Environ.commit(), name=task_name, kpis=kpis)
        task.persist()

        return suc


def tasks_to_evaluate():
    '''
    Get all the task names.
    :return: list of str.
    '''
    with local.cwd(Environ.workspace()):
        dirs = __('ls').split()
        dirs = filter(lambda _: not _.startswith('__'), dirs)
        dirs = filter(lambda _: os.path.isdir(_) and os.path.isfile(os.path.join(_, 'run.xsh')), dirs)
        print('dirs', [_ for _ in dirs])
        return [_ for _ in dirs]


def parse_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('--config', type=str, default='')
    arg.add_argument('--is_test', type=bool, default=False)
    arg.add_argument('--workspace', type=str, default='.')
    args = arg.parse_args()

    if not args.config:
        print(arg.format_help())
        sys.exit(-1)

    # expose all the configs as environ for easier usage.
    Environ.set_workspace(
        os.path.realpath(os.path.join(os.getcwd(), args.workspace)))
    Environ.set_test_mode(args.is_test)
    Environ.set_config(
        os.path.realpath(os.path.join(os.getcwd(), args.config)))
    return args


def load_kpis(root, task_name):
    module = os.path.basename(root)
    with local.cwd(os.path.join(root, '..')):
        print('load_kpis path', os.getcwd())
        env = {}
        cmd = 'from %s.%s.continuous_evaluation import tracking_kpis' % (
            module, task_name)
        print('cmd', cmd)
        exec (cmd, env)
        tracking_kpis = env['tracking_kpis']
        return tracking_kpis


if __name__ == '__main__':
    args = parse_args()

    evaluate_all_tasks()
