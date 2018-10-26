import pandas as pd
import psycopg2
from env import DB
from config import NODES_SQL, EDGES_SQL, EDGES_GEOM_SQL
from config import CAR_SQL, INSTITUTION_SQL, JOB_SQL
from cuuatsaccess import CuuatsAccess
import geopandas as geopd

# connect with database to query the data
with psycopg2.connect(**DB) as conn:
    nodes = pd.read_sql_query(NODES_SQL, conn, index_col='id')
    edges = pd.read_sql_query(EDGES_SQL, conn)
    edges_geom = geopd.GeoDataFrame.from_postgis(
        EDGES_GEOM_SQL, conn, geom_col='geom')

    fuel_station = pd.read_sql_query(CAR_SQL, conn)
    institution = pd.read_sql_query(INSTITUTION_SQL, conn)
    job = pd.read_sql_query(JOB_SQL, conn)

# edges_geom.index = edges_geom.segment_id

cuuatsaccess = CuuatsAccess()
# cuuatsaccess.create_bicycle_network(nodes, edges, 'bike_weight')
# cuuatsaccess.create_pedestrian_network(nodes, edges, 'ped_weight')
# gtfs_path = 'gtfs_data'
# cuuatsaccess.create_bus_network(gtfs_path,
#                                 date=20181016,
#                                 time_range=['07:00:00', '09:00:00'])
# cuuatsaccess.save_networks()
cuuatsaccess.load_networks('gtfs_data')
cuuatsaccess.set_pois(fuel_station,
                      'fuel_station',
                      method='nearest',
                      nearest_num=1)
cuuatsaccess.set_pois(institution,
                      'institution',
                      method='nearest',
                      nearest_num=3)
cuuatsaccess.set_pois(job, 'job', method='aggregation', agg_field='emp_num')
cuuatsaccess.set_max_unit({'bicycle_network': 15000,
                           'pedestrian_network': 7000,
                           'bus_network': 3600})
cuuatsaccess.calculate_accessibility()
cuuatsaccess.join_intersection_segment(edges_geom)
cuuatsaccess.to_geojson('pois_access_segment.geojson')

# cuuatsaccess = CuuatsAccess()
# cuuatsaccess.set_neigborhood('/home/edmondlai/Desktop/cu_neighborhood.shp')
# cuuatsaccess.set_intersections('/home/edmondlai/Git/cuuats.snt.lts/cuuats/snt/accessibility/gtfs_data/pois_access.geojson')
# cuuatsaccess.calculate_neighborhood_avg()
# cuuatsaccess.export_neighborhoods('/home/edmondlai/Desktop/neighborhoods_avg.geojson')
