from continuous_evaluation import *

for i in range(10):
    kpi0.add_record(0.111)
    kpi1.add_record(0.2)

kpi_to_update.add_record(0.3)

for kpi in tracking_kpis:
    kpi.persist()
