import pandas as pd
import psycopg2
from env import DB
from config import NODES_SQL, EDGES_SQL
from config import CAR_SQL, INSTITUTION_SQL, JOB_SQL
from cuuatsaccess import CuuatsAccess


# connect with database to query the data
with psycopg2.connect(**DB) as conn:
    nodes = pd.read_sql_query(NODES_SQL, conn, index_col='id')
    edges = pd.read_sql_query(EDGES_SQL, conn)

    car = pd.read_sql_query(CAR_SQL, conn)
    institution = pd.read_sql_query(INSTITUTION_SQL, conn)
    job = pd.read_sql_query(JOB_SQL, conn)

cuuatsaccess = CuuatsAccess()
cuuatsaccess.create_bike_network(nodes, edges, 'bike_weight')
cuuatsaccess.create_ped_network(nodes, edges, 'ped_weight')
gtfs_path = 'gtfs_data'
cuuatsaccess.create_transit_network(gtfs_path,
                                    date=20181016,
                                    time_range=['07:00:00', '09:00:00'])
cuuatsaccess.save_networks()
# cuuatsaccess.load_networks('gtfs_data')
cuuatsaccess.set_pois(car, 'car', method='nearest', nearest_num=1)
cuuatsaccess.set_pois(institution,
                      'institution',
                      method='nearest',
                      nearest_num=3)
cuuatsaccess.set_pois(job, 'job', method='aggregation', agg_field='emp_num')
cuuatsaccess.calculate_accessibility()
import pdb; pdb.set_trace()
# pois = {'car': [car, 1, 'nearest'],
#         'institution': [institution, 3, 'nearest'],
#         'job': [job, 1, 'aggregation']}


# cuuatsaccess.calculate_accessibility(pois)
# transitaccess.to_geojson()
