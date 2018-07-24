import os
import unittest
import ce.data_view as dv
from ce.kpi import GreaterWorseKpi, LessWorseKpi, TrueAssertionKpi
from ce.environ import Environ


class GreaterWorseKpiTester(unittest.TestCase):
    def setUp(self):
        dv.DB.Instance().delete_db('test')
        self.name = 'kpi0'

        self.kpi = GreaterWorseKpi(
            name=self.name,
            actived=True,
            threshold=0.01,
            unit_repr='cm',
            short_description='some desc', )

        Environ.set_commit('commit0')
        Environ.set_task('task0')

        self.assertFalse(dv.KpiBaseline.get('task0', self.name))

        dv.KpiBaseline.update('task0', self.name, 1.)

    def test_evaluate(self):
        cur = 1.3
        self.kpi.add_record(cur)
        self.assertFalse(self.kpi.evaluate())

        self.kpi.records.clear()
        cur = 1.001
        self.kpi.add_record(cur)
        self.assertTrue(self.kpi.evaluate())

    def test_compare_with(self):
        cur = 1.3
        other = 1.
        ratio = (cur - other) / other
        self.assertEqual(self.kpi.compare_with(cur, other), ratio)

    def tearDown(self):
        dv.DB.Instance().delete_db('test')


class LessWorseKpiTester(unittest.TestCase):
    def setUp(self):
        dv.DB.Instance().delete_db('test')

        self.kpi = LessWorseKpi(
            name='kpi0',
            actived=True,
            threshold=0.01,
            unit_repr='cm',
            short_description='some desc', )

        Environ.set_commit('commit0')
        Environ.set_task('task0')
        self.name = 'kpi0'

        self.assertFalse(dv.KpiBaseline.get('task0', self.name))
        dv.KpiBaseline.update('task0', self.name, 1.)

    def test_evaluate(self):
        cur = 1.3
        self.kpi.add_record(cur)
        self.assertTrue(self.kpi.evaluate())

    def test_compare_with(self):
        cur = 1.3
        other = 1.
        ratio = (cur - other) / other
        self.assertEqual(self.kpi.compare_with(cur, other), ratio)

    def tearDown(self):
        dv.DB.Instance().delete_db('test')


class TrueAssertionKpiTester(unittest.TestCase):
    def setUp(self):
        dv.DB.Instance().delete_db('test')

        self.kpi = TrueAssertionKpi(
            name='true_kpi0',
            actived=True,
            short_description='some desc', )

    def test_record_num(self):
        # can only take one record
        self.kpi.add_record(True)
        self.kpi.add_record(False)

        suc = True
        try:
            # should raise exception here.
            self.kpi.evaluate()
            suc = False
        except:
            self.assertEqual(len(self.kpi.records), 2)
            pass
        self.assertTrue(suc)

    def test_evaluate(self):
        self.kpi.add_record(True)
        self.assertTrue(self.kpi.evaluate())

    def test_evaluate_fail(self):
        self.kpi.add_record(False)
        self.assertFalse(self.kpi.evaluate())


if __name__ == '__main__':
    unittest.main()
