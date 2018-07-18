import os
import unittest
from ce.utils import __, log, local
from ce import data_view as dv
from ce.config_util import Config
from ce.environ import Environ
from ce.repo import get_commit


class MainUnittest(unittest.TestCase):
    def setUp(self):
        Environ.set_config(os.path.join(os.getcwd(), 'default.conf'))
        with local.cwd('../test_env'):
            dv.init_shared_db(True)

        dv.KpiBaseline.update('demo0', 'kpi0', 0.11, 'original kpi0 baseline')
        dv.KpiBaseline.update('demo0', 'kpi1', 0.23, 'original kpi1 baseline')
        dv.KpiBaseline.update('demo0', 'kpi_to_update', 0.2,
                              'original kpi1 baseline')

    def test_add_record(self):
        config_path = os.path.join(os.getcwd(), '../ce/default.conf')
        logs = __(
            'python3 main.py --config %s --is_test 1 --workspace ../test_env' %
            config_path)
        log.info('logs', logs)
        kpi = dv.shared_db.gets({}, table='kpi')
        task = dv.shared_db.gets({}, table='task')
        commit = dv.shared_db.gets({}, table='commit')

        log.info('kpis', kpi)
        log.info('tasks', task)
        log.info('commits', commit)

        self.assertTrue(kpi)
        self.assertTrue(task)
        self.assertTrue(commit)

        commitid = get_commit('.')

        # kpi0, value: 0.11, should pass
        kpi = dv.Kpi(commitid=commitid, task='demo0', name='kpi0')
        info = kpi.fetch_infos()
        self.assertTrue(info.passed)
        self.assertEqual(info.unit, 'qps')
        self.assertTrue(info.actived)

        # kpi1, value: 0.2, baseline 0.23, should fail
        kpi = dv.Kpi(commitid=commitid, task='demo0', name='kpi1')
        info = kpi.fetch_infos()
        self.assertFalse(info.passed)
        self.assertEqual(info.unit, 'cm')
        self.assertTrue(info.actived)

        # kpi3, value: 0.3, baseline 0.1, should suc
        kpi = dv.Kpi(commitid=commitid, task='demo0', name='kpi_to_update')
        info = kpi.fetch_infos()
        self.assertTrue(info.passed)
        self.assertEqual(info.unit, 'qps')
        self.assertTrue(info.actived)
        self.assertEqual(info.value, 0.3)

        self.assertEqual(dv.KpiBaseline.get('demo0', 'kpi0'), 0.11)
        self.assertEqual(dv.KpiBaseline.get('demo0', 'kpi1'), 0.23)
        self.assertEqual(dv.KpiBaseline.get('demo0', 'kpi_to_update'), 0.3)

    def tearDown(self):
        log.warn('delete test db')

        dv.shared_db.client.drop_database('test')


if __name__ == '__main__':
    unittest.main()
