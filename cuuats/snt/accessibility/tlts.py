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
        stop_times_col = ['trip_id', 'arrival_time', 'stop_id', 'stop_sequence']
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
        stops_col = ['stop_id', 'node_id', 'stop_lon', 'stop_lat']
        self.stops = stops[stops_col]

    def _set_trips(self):
        trips_col = ['route_id', 'service_id', 'trip_id']
        trips = pd.read_csv('trips.txt')
        self.trips = trips[trips_col]

    def _set_routes(self):
        self.routes = pd.read_csv('routes.txt')

    def export(self):
        var = self.stops.to_file('stops.js', driver='GeoJSON')

    def calculate_head_time(self, time_range=['07:00:00', '10:00:00']):
        start_time = timedelta(hours=int(time_range[0][0:2]),
                               minutes=int(time_range[0][3:5]))
        end_time = timedelta(hours=int(time_range[1][0:2]),
                             minutes=int(time_range[1][3:5]))
        stop_times = self.stop_times
        cond1 = stop_times['arrival_time'] > start_time
        cond2 = stop_times['arrival_time'] < end_time
        peak_trips = stop_times[cond1 & cond2]
        self.peak_trips = pd.merge(peak_trips, self.trips,
                                   on='trip_id', how='inner')
        first_stop = peak_trips.loc[peak_trips['stop_sequence'] == 1]
        return self.peak_trips

    def _append_nodes(self):
        pass

    def create_transit_network(self):
        stop_nodes_peak = pd.merge(self.peak_trips, self.stops,
                                   on='stop_id', how='inner')
        stop_nodes_peak = stop_nodes_peak.sort_values(
                                    ['trip_id', 'stop_sequence'])
        edges = self.network.edges_df
        stop = self.network.nodes_df.index.max() + 1
        nodes = self.network.nodes_df

        prev_trip = None
        prev_intersection = None
        prev_stop = None
        prev_time = None
        count = 0
        for row in stop_nodes_peak.iterrows():
            if count == 500:
                break
            headway = {'route_id': 10}
            intersection = row[1].node_id
            arrival_time = row[1].arrival_time
            trip = row[1].trip_id

            same_trip = prev_trip == trip
            if prev_stop and same_trip:
                # getting off the bus
                edges = edges.append(pd.DataFrame({'from': [stop],
                                                   'to': [intersection],
                                                   'weight': [0]}))
                # transit time between stop
                time_diff = (arrival_time - prev_time).seconds / 60.0
                edges = edges.append(
                    pd.DataFrame({'from': [prev_stop],
                                  'to': [stop],
                                  'weight': [time_diff]}))
                # getting on the busW
                edges = edges.append(
                    pd.DataFrame({'from': [prev_intersection],
                                  'to': [prev_stop],
                                  'weight': [headway.get('route_id')]}))

            # adding stop to transit nodes
            nodes = nodes.append(
                pd.DataFrame({'x': [row[1].stop_lon],
                              'y': [row[1].stop_lat]},
                             index=[stop])
            )

            prev_trip = trip
            prev_intersection = intersection
            prev_stop = stop
            prev_time = arrival_time
            stop = stop + 1
            count = count + 1

        edges['weight'] = edges['weight'].replace(0, 0.01)
        self.transit_nodes = nodes
        self.transit_edges = edges

        transit_network = pdna.Network(
            node_x=self.transit_nodes.x,
            node_y=self.transit_nodes.y,
            edge_from=self.transit_edges["from"],
            edge_to=self.transit_edges["to"],
            edge_weights=self.transit_edges[["weight"]]
        )
        self.transit_network = transit_network

    def set_poi(self, poi):
        transit_network = self.transit_network
        # set point of interest to find out the weight to nearest poi
        transit_network.set_pois(category="poi",
                                 maxdist=3600,
                                 maxitems=10,
                                 x_col=poi['x'],
                                 y_col=poi['y'])
        nearest_poi = transit_network.nearest_pois(distance=3600,
                                                   category="poi",
                                                   num_pois=10)

        import pdb; pdb.set_trace()
