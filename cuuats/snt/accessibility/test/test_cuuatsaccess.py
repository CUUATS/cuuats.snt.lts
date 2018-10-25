import unittest
import pandana as pdna
import pandas as pd
from cuuats.snt.accessibility import CuuatsAccess


class TestCuuatsAccess(unittest.TestCase):
    node_data = {'x': [],
                 'y': []}
    for x in range(0, 3):
        for y in range(0, 3):
            node_data['x'].append(x)
            node_data['y'].append(y)
    node_index = [i for i in range(1, len(node_data['x']) + 1)]
    node_df = pd.DataFrame(node_data, index=node_index)

    edge_data = {
        'from': [],
        'to': []
    }
    edge_data = {'from':        [1, 2, 4, 5, 7, 8, 1, 4, 2, 5, 3, 6, 8],
                 'to':          [2, 3, 5, 6, 8, 9, 4, 7, 5, 8, 6, 9, 6],
                 'ped_weight':  [1, 2, 3, 1, 4, 3, 2, 2, 2, 2, 2, 4, 2],
                 'bike_weight': [1, 2, 3, 1, 4, 3, 2, 2, 2, 2, 2, 4, 2]}

    edge_df = pd.DataFrame(edge_data)
    new_df = edge_df.rename(columns={'from': 'to', 'to': 'from'})
    edge_df = pd.concat([edge_df, new_df])

    stop_times_data = {'trip_id': ['green', 'green', 'green',
                                   'red', 'red', 'red'],
                       'arrival_time': ['08:00:00', '08:01:00', '08:02:00',
                                        '08:00:00', '08:01:00', '08:02:00'],
                       'date': [20181016] * 6,
                       'stop_sequence': [1, 4, 7, 7, 8, 9],
                       'stop_id': ['A', 'B', 'C', 'C', 'D', 'E'],
                       'node_id': [1, 4, 7, 7, 8, 9]}
    stop_times_df = pd.DataFrame(stop_times_data)

    def test_dataframe(self):
        self.assertTrue(isinstance(self.node_df, pd.DataFrame))
        self.assertTrue(isinstance(self.edge_df, pd.DataFrame))
        self.assertEqual(len(self.node_df), 9)
        self.assertEqual(len(self.edge_df), 26)

    def test_create_bike_network(self):
        ca = CuuatsAccess()
        ca.create_bike_network(self.node_df, self.edge_df, 'bike_weight')
        self.assertTrue(isinstance(ca.bike_network, pdna.Network))

    def test_create_ped_network(self):
        ca = CuuatsAccess()
        ca.create_ped_network(self.node_df, self.edge_df, 'ped_weight')
        self.assertTrue(isinstance(ca.ped_network, pdna.Network))

    def test_agg_transit_ped(self):
        ca = CuuatsAccess()
        ca.create_ped_network(self.node_df, self.edge_df, 'ped_weight')
        ca._agg_transit_ped()


if __name__ == '__main__':
    unittest.main()
