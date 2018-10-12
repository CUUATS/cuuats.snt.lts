import pandas as pd
import pandana as pdna
import os
import geopandas as geopd
from shapely.geometry import Point
from datetime import timedelta


class TransitAccess(object):
    def __init__(self):
        pass

    def create_transit_network(self,
                               gtfs_path,
                               ped_network,
                               date=20181016,
                               time_range=['07:00:00', '09:00:00']):
        self.ped_network = self._set_ped_network(ped_network)
        self._process_gtfs(gtfs_path)
        self._filter_trips(date, time_range)
        self._agg_transit_ped()
        return self

    def save_transit_network(self, filename, path=None):
        os.chdir(path)
        self.transit_network.save_hdf5('transit_network')

    def load_transit_network(self, transit_network):
        self.transit_network = transit_network
        return self

    def _set_ped_network(self, ped_network):
        if isinstance(ped_network, pdna.Network):
            return ped_network
        else:
            raise TypeError('ped_network must be a pandana object')

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
        edges = self.ped_network.edges_df
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

    def export_transit_network(self, path=None):
        if not path:
            self.transit_network.save_hdf5('transit_network')

    def load_transit_network(cls, path=None):
        if not path:
            os.chdir('gtfs_data')
            self.pdna.Network.from_hdf5('transit_network')

    def set_poi(self, poi):
        transit_network = self.transit_network
        import pdb; pdb.set_trace()
        geometry = [Point(x, y) for x, y in zip(transit_network.nodes_df.x,
                                                transit_network.nodes_df.y)]
        crs = {'init': 'epsg:4326'}
        geodf = geopd.GeoDataFrame(transit_network.nodes_df, crs, geometry)

        for key, data in poi.items():
            # set point of interest to find out the weight to nearest poi
            transit_network.set_pois(category=key,
                                     maxdist=3600,
                                     maxitems=1,
                                     x_col=data['x'],
                                     y_col=data['y'])
            nearest_poi = transit_network.nearest_pois(distance=3600,
                                                       category=key,
                                                       num_pois=1)

            import pdb; pdb.set_trace()

    def to_geojson(self, path=None):
        pass
