import pandas as pd
import pandana as pdna
import time
import os
import urbanaccess as ua
from urbanaccess.config import settings
from urbanaccess.gtfsfeeds import feeds
from urbanaccess import gtfsfeeds
from urbanaccess.gtfs.gtfsfeeds_dataframe import gtfsfeeds_dfs
from urbanaccess.network import ua_network, load_network
import matplotlib.pyplot as plt

validation = True
verbose = True
# bbox for City of Oakland
bbox = (-88.358231,40.043386,-88.14537,40.161034)
remove_stops_outsidebbox = True
append_definitions = True
os.chdir('..')

# Load GTFS feed from data folder into dataframe
loaded_feeds = ua.gtfs.load.gtfsfeed_to_df(gtfsfeed_path=None,
                                           validation=validation,
                                           verbose=verbose,
                                           bbox=bbox,
                                           remove_stops_outsidebbox=remove_stops_outsidebbox,
                                           append_definitions=append_definitions)

# Create a network object from the feed
ua.gtfs.network.create_transit_net(gtfsfeeds_dfs=loaded_feeds,
                                   day='monday',
                                   timerange=['07:00:00', '23:00:00'],
                                   calendar_dates_lookup=None)

# Create an UrbanAccess network object
urbanaccess_net = ua.network.ua_network

# Download Data from OSM with bounding box
nodes, edges = ua.osm.load.ua_network_from_bbox(bbox=bbox,
                                                remove_lcn=True)

# Create OSM network object using osm data
ua.osm.network.create_osm_net(osm_edges=edges,
                              osm_nodes=nodes,
                              travel_speed_mph=3)

# Integrate the street network with transit network
ua.network.integrate_network(urbanaccess_network=urbanaccess_net,
                             headways=False)


# Plot pedestrian network
ua.plot.plot_net(nodes=urbanaccess_net.net_nodes,
                 edges=urbanaccess_net.net_edges[urbanaccess_net.net_edges['net_type']=='walk'],
                 bbox=None,
                 fig_height=30, margin=0.02,
                 edge_color='#999999', edge_linewidth=1, edge_alpha=1,
                 node_color='black', node_size=0, node_alpha=1, node_edgecolor='none', node_zorder=3, nodes_only=False)
plt.savefig('pednet.png')


# plot the whole network
ua.plot.plot_net(nodes=urbanaccess_net.net_nodes,
                 edges=urbanaccess_net.net_edges,
                 bbox=bbox,
                 fig_height=30, margin=0.02,
                 edge_color='#999999', edge_linewidth=1, edge_alpha=1,
                 node_color='black', node_size=1.1, node_alpha=1, node_edgecolor='none', node_zorder=3, nodes_only=False)
plt.savefig('whole_net.png')


# plot travel time network
edgecolor = ua.plot.col_colors(df=urbanaccess_net.net_edges, col='weight', cmap='gist_heat_r', num_bins=5)
ua.plot.plot_net(nodes=urbanaccess_net.net_nodes,
                 edges=urbanaccess_net.net_edges,
                 bbox=bbox,
                 fig_height=30, margin=0.02,
                 edge_color=edgecolor, edge_linewidth=1, edge_alpha=0.7,
                 node_color='black', node_size=0, node_alpha=1, node_edgecolor='none', node_zorder=3, nodes_only=False)
plt.savefig('traveltime.png')


# Save Network to disc
ua.network.save_network(urbanaccess_network=urbanaccess_net,
                        filename='test_cu_net.h5',
                        overwrite_key=True)