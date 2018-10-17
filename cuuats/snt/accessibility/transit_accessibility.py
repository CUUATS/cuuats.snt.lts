import pandas as pd
import pandana as pdna
import psycopg2
from env import DB
from config import TRANSIT_POI_SQL, PED_TRANSIT_EDGES_SQL, TRANSIT_NODES_SQL, \
    TRANSIT_INSTITUTION_SQL, TRANSIT_JOB_SQL
from transitaccess import TransitAccess


# connect with database to query the data
with psycopg2.connect(**DB) as conn:
    nodes = pd.read_sql_query(TRANSIT_NODES_SQL, conn, index_col='id')
    edges = pd.read_sql_query(PED_TRANSIT_EDGES_SQL, conn)
    car = pd.read_sql_query(TRANSIT_POI_SQL, conn)
    institution = pd.read_sql_query(TRANSIT_INSTITUTION_SQL, conn)
    job = pd.read_sql_query(TRANSIT_JOB_SQL, conn)


# ped_network = pdna.Network(
#     node_x=nodes.x,
#     node_y=nodes.y,
#     edge_from=edges["from"],
#     edge_to=edges["to"],
#     edge_weights=edges[["weight"]],
#     twoway=False)
#
# ped_network.precompute(3000)

transitaccess = TransitAccess()
# transitaccess = transitaccess.create_transit_network(
#     'gtfs_data',
#     ped_network
# )
# transitaccess.save_transit_network('transit_network.network')
transitaccess.load_transit_network('transit_network.network', 'gtfs_data')
pois = {'car': [car, 1, 'nearest'],
        'institution': [institution, 3, 'nearest'],
        'job': [job, 1, 'aggregation']}
transitaccess.set_pois(pois)
# transitaccess.to_geojson()
