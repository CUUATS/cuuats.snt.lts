import pandas as pd
import psycopg2
from env import DB
from config import TRANSIT_POI_SQL, PED_TRANSIT_EDGES_SQL, TRANSIT_NODES_SQL, \
    TRANSIT_INSTITUTION_SQL, TRANSIT_JOB_SQL, NODES_SQL, EDGES_SQL
from cuuatsaccess import CuuatsAccess


# connect with database to query the data
with psycopg2.connect(**DB) as conn:
    nodes = pd.read_sql_query(NODES_SQL, conn, index_col='id')
    edges = pd.read_sql_query(EDGES_SQL, conn)

cuuatsaccess = CuuatsAccess()
cuuatsaccess.create_bike_network(nodes, edges, 'bike_weight')
cuuatsaccess.create_ped_network(nodes, edges, 'ped_weight')
gtfs_path = 'gtfs_data'
cuuatsaccess.create_transit_network(gtfs_path,
                                    date=20181016,
                                    time_range=['07:00:00', '09:00:00'])
import pdb; pdb.set_trace()
# transitaccess = transitaccess.create_transit_network(
#     'gtfs_data',
#     ped_network
# )
# transitaccess.save_transit_network('transit_network.network')
cuuatsaccess.load_transit_network('transit_network.network', 'gtfs_data')
pois = {'car': [car, 1, 'nearest'],
        'institution': [institution, 3, 'nearest'],
        'job': [job, 1, 'aggregation']}
cuuatsaccess.set_pois(pois)
# transitaccess.to_geojson()
