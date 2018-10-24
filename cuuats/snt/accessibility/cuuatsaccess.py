import pandas as pd
import pandana as pdna
import os
import geopandas as geopd
from shapely.geometry import Point
from datetime import timedelta
from sklearn import preprocessing


class CuuatsAccess(object):
    def __init__(self):
        self.bike_network = ""
        self.ped_network = ""
        self.transit_network = ""
        self.pois = {}
        self.max_unit = {'bike_network': 15000,
                         'ped_network': 7000,
                         'transit_network': 3600}

    def create_bike_network(self, nodes, edges, weight):
        network = pdna.Network(
            node_x=nodes.x,
            node_y=nodes.y,
            edge_from=edges["from"],
            edge_to=edges["to"],
            edge_weights=edges[[weight]],
            twoway=False)
        network.precompute(3000)
        self.bike_network = network
        return self

    def create_ped_network(self, nodes, edges, weight):
        network = pdna.Network(
            node_x=nodes.x,
            node_y=nodes.y,
            edge_from=edges["from"],
            edge_to=edges["to"],
            edge_weights=edges[[weight]],
            twoway=False)
        network.precompute(3000)
        self.ped_network = network
        return self

    def create_transit_network(self,
                               gtfs_path,
                               date=20181016,
                               time_range=['07:00:00', '09:00:00']):
        self._process_gtfs(gtfs_path)
        self._filter_trips(date, time_range)
        self._agg_transit_ped()
        return self

    def save_networks(self, path=None):
        if path:
            os.chdir(path)
        self.transit_network.save_hdf5('transit_network.hdf5')
        self.ped_network.save_hdf5('ped_network.hdf5')
        self.bike_network.save_hdf5('bike_network.hdf5')
        return self

    def load_networks(self, path=None):
        if path:
            os.chdir(path)
        self.transit_network = pdna.Network.from_hdf5('transit_network.hdf5')
        self.ped_network = pdna.Network.from_hdf5('ped_network.hdf5')
        self.bike_network = pdna.Network.from_hdf5('bike_network.hdf5')
        return self

    def set_pois(self,
                 data,
                 name,
                 method='nearest',
                 nearest_num=1,
                 agg_field=''):
        self.pois[name] = [data, nearest_num, method, agg_field]
        return self

    def set_max_unit(self, max_unit):
        self.max_unit = max_unit
        return self

    def calculate_accessibility(self):
        transit_network = self.transit_network
        ped_network = self.ped_network
        bike_network = self.bike_network
        networks = {'transit_network': transit_network,
                    'ped_network': ped_network,
                    'bike_network': bike_network}
        geometry = [Point(x, y) for x, y in zip(transit_network.nodes_df.x,
                                                transit_network.nodes_df.y)]
        crs = {'init': 'epsg:4326'}
        geodf = geopd.GeoDataFrame(transit_network.nodes_df,
                                   crs=crs,
                                   geometry=geometry)
        geodf = geodf.drop(['x', 'y'], axis=1)

        for network_name, network in networks.items():
            prefix = network_name.split('_')[0] + '_'
            dist = self.max_unit.get(network_name)
            for key, param in self.pois.items():
                data = param[0]
                item = param[1]
                method = param[2]
                agg_field = param[3]
                if method == 'nearest':
                    network.set_pois(category=key,
                                     maxdist=dist,
                                     maxitems=item,
                                     x_col=data['x'],
                                     y_col=data['y'])
                    nearest_poi = network.nearest_pois(distance=dist,
                                                       category=key,
                                                       num_pois=item)
                    nearest_poi = self._rescale(nearest_poi, reverse=False)
                    nearest_poi.columns = [str(i) for i in range(1, item + 1)]

                    geodf = pd.concat([geodf, nearest_poi[str(item)]], axis=1)
                    geodf = geodf.rename(columns={str(item): prefix + key})
                elif method == 'aggregation':
                    data['node_ids'] = network.get_node_ids(data.x,
                                                            data.y)
                    network.set(data.node_ids,
                                variable=data[agg_field],
                                name=key)
                    df = network.aggregate(dist,
                                           type='sum',
                                           decay='flat',
                                           name=key)
                    df = self._rescale(df, reverse=True)
                    geodf = pd.concat([geodf, df], axis=1)
                    geodf = geodf.rename(columns={0: prefix + key})

        geodf = geodf[geodf['geometry'] != Point(0, 0)]
        self.pois_access = self._find_mean(geodf)
        return self

    def to_geojson(self, filename='pois_access.geojson', path=None):
        if path:
            os.chdir(path)
        self.pois_access.to_file(filename, driver='GeoJSON')
        return self

    def _find_mean(self, geodf, ignore_col='geometry'):
        geodf['avg'] = geodf.loc[:, geodf.columns != ignore_col].mean(axis=1)
        return geodf

    def _rescale(self, df, reverse=False):
        if not reverse:
            min = df.min()
            max = df.max()
            df = (1 - (df - min) / (max - min)) * 100
            return df
        else:
            min = df.min()
            max = df.max()
            df = (df - min) / (max - min) * 100
            return df

    def _process_gtfs(self, gtfs_path):
        os.chdir(gtfs_path)
        self.stop_times = self._set_stop_times()
        self.stops = self._set_stops()
        self.trips = self._set_trips()
        self.routes = self._set_routes()
        self.calendar_dates = self._set_calendar_dates()

    def _set_stop_times(self):
        stop_times_col = ['trip_id', 'arrival_time', 'stop_id',
                          'stop_sequence']
        stop_times = pd.read_csv('stop_times.txt')
        stop_times = stop_times[stop_times_col]
        stop_times.arrival_time = stop_times.arrival_time.apply(
            lambda x: timedelta(hours=int(x[0:2]),
                                minutes=int(x[3:5])))
        return stop_times

    def _set_stops(self):
        stops = pd.read_csv('stops.txt')
        x, y = stops.stop_lon, stops.stop_lat
        stops['node_id'] = self.ped_network.get_node_ids(x, y)
        stops_col = ['stop_id', 'node_id', 'stop_lon', 'stop_lat']
        return stops[stops_col]

    def _set_trips(self):
        trips_col = ['route_id', 'service_id', 'trip_id']
        trips = pd.read_csv('trips.txt')
        return trips[trips_col]

    def _set_calendar_dates(self):
        return pd.read_csv('calendar_dates.txt')

    def _set_routes(self):
        return pd.read_csv('routes.txt')

    def _filter_trips(self,
                      date,
                      time_range=['07:00:00', '09:00:00']):
        date = int(date)
        start_time = timedelta(hours=int(time_range[0][0:2]),
                               minutes=int(time_range[0][3:5]))
        end_time = timedelta(hours=int(time_range[1][0:2]),
                             minutes=int(time_range[1][3:5]))
        stop_times = self.stop_times
        calendar_dates = self.calendar_dates
        trips = self.trips
        cond1 = stop_times['arrival_time'] > start_time
        cond2 = stop_times['arrival_time'] < end_time

        peak_stop_times = stop_times[cond1 & cond2]
        peak_trips = pd.merge(peak_stop_times, trips,
                              on='trip_id', how='inner')
        unique_date = calendar_dates.loc[calendar_dates['date'] == date]
        date_peak_trips = pd.merge(peak_trips, unique_date,
                                   on='service_id', how='inner')
        self.date_peak_trips = date_peak_trips
        self.headway = self._calculate_headway(date_peak_trips)
        return self.date_peak_trips

    def _calculate_headway(self, date_peak_trips):
        first_stop = date_peak_trips.loc[
                date_peak_trips['stop_sequence'] == 1]
        groupby_service = first_stop.groupby(first_stop['service_id'])
        max_arrival = groupby_service.max().arrival_time
        min_arrival = groupby_service.min().arrival_time
        service_count = groupby_service.count().arrival_time
        time_diff = (max_arrival - min_arrival)
        headway = {}

        for item in zip(time_diff.iteritems(), service_count):

            service = item[0][0]
            time = item[0][1]
            count = item[1]
            if time == timedelta():
                headway[service] = timedelta(seconds=3600).seconds
            else:
                headway[service] = (time / (count - 1)).seconds
        return headway

    def _agg_transit_ped(self,
                         date=20181016,
                         time_range=['07:00:00', '09:00:00']):

        stop_nodes_peak = pd.merge(self.date_peak_trips, self.stops,
                                   on='stop_id', how='inner')
        stop_nodes_peak = stop_nodes_peak.sort_values(
                                    ['trip_id', 'stop_sequence'])
        # convert into seconds based on 3 miles per hour
        edges = self.ped_network.edges_df
        edges['weight'] = (edges['ped_weight'] / 5280) / 3 * 60 * 60
        stop = self.ped_network.nodes_df.index.max() + 1
        nodes = self.ped_network.nodes_df
        headway = self.headway
        prev_trip = None
        prev_intersection = None
        prev_stop = None
        prev_time = None
        for row in stop_nodes_peak.iterrows():
            intersection = row[1].node_id
            arrival_time = row[1].arrival_time
            trip = row[1].trip_id
            service_id = row[1].service_id
            same_trip = prev_trip == trip

            if same_trip:
                # getting on the bus
                on_bus = pd.DataFrame({'from': [prev_intersection],
                                       'to': [prev_stop],
                                       'weight': [headway.get(service_id,
                                                              3600)]},
                                      index=[edges.index.max() + 1])
                edges = edges.append(on_bus)

                # getting off the bus
                off_bus = pd.DataFrame({'from': [stop],
                                        'to': [intersection],
                                        'weight': [0]},
                                       index=[edges.index.max() + 1])
                edges = edges.append(off_bus)

                # transit time between stop
                time_diff = (arrival_time - prev_time).seconds
                edges = edges.append(
                    pd.DataFrame({'from': [prev_stop],
                                  'to': [stop],
                                  'weight': [time_diff]},
                                 index=[edges.index.max() + 1]))

            # adding stop to transit nodes
            nodes = nodes.append(
                pd.DataFrame({'x': [0],
                              'y': [0]},
                             index=[stop])
            )

            prev_trip = trip
            prev_intersection = intersection
            prev_stop = stop
            prev_time = arrival_time
            stop = stop + 1

        edges['weight'] = edges['weight'].replace(0, 0.01)

        transit_network = pdna.Network(
            node_x=nodes.x,
            node_y=nodes.y,
            edge_from=edges["from"],
            edge_to=edges["to"],
            edge_weights=edges[["weight"]],
            twoway=False
        )
        self.transit_network = transit_network
