import pandas as pd
import pandana as pdna
import psycopg2

from config import NODES_SQL, EDGES_SQL, POI_SQL
from env import DB

# connect with database to query the data
with psycopg2.connect(**DB) as conn:
    nodes = pd.read_sql_query(NODES_SQL, conn, index_col='id')
    edges = pd.read_sql_query(EDGES_SQL, conn)
    poi = pd.read_sql_query(POI_SQL, conn)

# create the network object
network = pdna.Network(
    node_x=nodes.x,
    node_y=nodes.y,
    edge_from=edges["from"],
    edge_to=edges["to"],
    edge_weights=edges[["plts_weight"]])

network.precompute(3000)

# set point of interest to find out the weight to nearest poi
network.set_pois(category="poi",
                 maxdist=7000,
                 maxitems=10,
                 x_col=poi['x'],
                 y_col=poi['y'])

# set nearest poi weight from nearest to tenth closet
nearest_poi = network.nearest_pois(distance=7000,
                                   category="poi",
                                   num_pois=10)

# merge the nodes coordinate with score
plts_n = pd.merge(nodes, nearest_poi, left_index=True, right_index=True)

# find the nearest poi node id
x, y = poi.x, poi.y
poi_ids = network.get_node_ids(x, y)

network.set(poi_ids)
y = network.aggregate(distance=7000,
                      type="sum",
                      decay="linear")

plts_n = pd.merge(plts_n, pd.DataFrame(y), left_index=True, right_index=True)
plts_n = plts_n.rename(columns={'0': 'aggregate'})
