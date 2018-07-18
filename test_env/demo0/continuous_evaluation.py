from ce.kpi import LessWorseKpi

kpi0 = LessWorseKpi(
    name='kpi0',
    actived=True,
    threshold=0.02,
    unit_repr='qps',
    short_description='Some description',
    description='some long description')

kpi1 = LessWorseKpi(
    name='kpi1',
    actived=True,
    threshold=0.02,
    unit_repr='cm',
    short_description='This kpi should failed',
    description='some long description')

kpi_to_update = LessWorseKpi(
    name='kpi_to_update',
    actived=True,
    threshold=0.01,
    unit_repr='qps',
    short_description='short desc',
    description='long desc', )

tracking_kpis = [kpi0, kpi1, kpi_to_update]
