import pandas as pd
import pandana as pdna
import os
from datetime import timedelta


class Tlts(object):
    def __init__(self, gtfs_path, pandana_network):
        os.chdir(gtfs_path)
        self._set_network(pandana_network)
        self._set_stop_times()
        self._set_stops()
        self._set_trips()
        self._set_routes()

    def _set_stop_times(self):
        stop_times_col = ['trip_id', 'arrival_time', 'stop_id']
        stop_times = pd.read_csv('stop_times.txt')
        stop_times = stop_times[stop_times_col]
        stop_times.arrival_time = stop_times.arrival_time.apply(
            lambda x: timedelta(hours=int(x[0:2]),
                                minutes=int(x[3:5])))
        self.stop_times = stop_times

    def _set_network(self, pandana_network):
        if isinstance(pandana_network, pdna.Network):
            self.network = pandana_network
        else:
            raise TypeError('pandana_network must be a pandana object')

    def _set_stops(self):
        stops = pd.read_csv('stops.txt')
        x, y = stops.stop_lon, stops.stop_lat
        stops['node_id'] = self.network.get_node_ids(x, y)
        stops_col = ['stop_id', 'node_id']
        self.stops = stops[stops_col]

    def _set_trips(self):
        trips_col = ['route_id', 'service_id', 'trip_id']
        trips = pd.read_csv('trips.txt')
        self.trips = trips[trips_col]

    def _set_routes(self):
        self.routes = pd.read_csv('routes.txt')

    def export(self):
        self.stops.to_file('stops.js', driver='GeoJSON')

    def calculate_head_time(self, time_range=['07:00:00', '10:00:00']):
        start_time = timedelta(hours=int(time_range[0][0:2]),
                               minutes=int(time_range[0][3:5]))
        end_time = timedelta(hours=int(time_range[1][0:2]),
                             minutes=int(time_range[1][3:5]))
        stop_times = self.stop_times

        return start_time
