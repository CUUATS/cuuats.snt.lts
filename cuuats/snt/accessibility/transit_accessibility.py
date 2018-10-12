import pandas as pd
import pandana as pdna
import psycopg2
from env import DB
from config import TRANSIT_POI_SQL, PED_TRANSIT_EDGES_SQL, TRANSIT_NODES_SQL, TRANSIT_INSTITUTION_SQL
from transitaccess import TransitAccess


# connect with database to query the data
with psycopg2.connect(**DB) as conn:
    nodes = pd.read_sql_query(TRANSIT_NODES_SQL, conn, index_col='id')
    edges = pd.read_sql_query(PED_TRANSIT_EDGES_SQL, conn)
    poi = pd.read_sql_query(TRANSIT_POI_SQL, conn)
    institution = pd.read_sql_query(TRANSIT_INSTITUTION_SQL, conn)


network = pdna.Network(
    node_x=nodes.x,
    node_y=nodes.y,
    edge_from=edges["from"],
    edge_to=edges["to"],
    edge_weights=edges[["weight"]],
    twoway=False)

network.precompute(3000)

transitaccess = TransitAccess()
transitaccess = transitaccess.create_transit_network(
    'gtfs_data',
    network
)
transitaccess.save_transit_network('transit_network','gtfs_data')

# create the network object
# network = pdna.Network(
#     node_x=nodes.x,
#     node_y=nodes.y,
#     edge_from=comb_edges["from"],
#     edge_to=comb_edges["to"],
#     edge_weights=comb_edges[["weight"]])
#
# network.precompute(3000)
#
# # set point of interest to find out the weight to nearest poi
# network.set_pois(category="poi",
#                  maxdist=3600,
#                  maxitems=10,
#                  x_col=poi['x'],
#                  y_col=poi['y'])
#
# # set nearest poi weight from nearest to tenth closet
# nearest_poi = network.nearest_pois(distance=3600,
#                                    category="poi",
#                                    num_pois=10)
#
# # merge the nodes coordinate with score
# blts_n = pd.merge(nodes, nearest_poi, left_index=True, right_index=True)
#
# # find the nearest poi node id
# x, y = poi.x, poi.y
# poi_ids = network.get_node_ids(x, y)
#
# network.set(poi_ids)
# y = network.aggregate(distance=3600,
#                       type="sum",
#                       decay="flat")

# tlts_n = pd.merge(blts_n, pd.DataFrame(y), left_index=True, right_index=True)
# tlts_n.to_csv('~/Git/cuuats.snt.lts/cuuats/snt/accessibility/results/transit.csv')
