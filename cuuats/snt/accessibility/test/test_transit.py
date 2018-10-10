import unittest
from cuuats.snt.accessibility import Tlts
import pandana as pdna
import pandas as pd


class TestTLTS(unittest.TestCase):
    node_data = {'x': [0, 1, 2, 1],
                 'y': [0, 0, 0, -1]}
    node_index = [1, 2, 3, 4]
    node_df = pd.DataFrame(node_data, index=node_index)
    edge_data = {'from': [1, 2, 3, 2, 3, 4],
                 'to': [2, 3, 4, 1, 2, 3],
                 'weight': [1, 2, 3, 1, 2, 3]}
    edge_df = pd.DataFrame(edge_data)
    network = pdna.Network(
        node_x=node_df.x,
        node_y=node_df.y,
        edge_from=edge_df["from"],
        edge_to=edge_df["to"],
        edge_weights=edge_df[["weight"]],
        twoway=False)

    stop_times_data = {'trip_id': ['green', 'green', 'green'],
                       'arrival_time': ['08:00:00', '08:15:00', '08:30:00'],
                       'stop_sequence': [1, 2, 3],
                       'stop_id': ['A', 'B', 'C']}
    stop_times_df = pd.DataFrame(stop_times_data)

    def test_dataframe(self):
        self.assertTrue(isinstance(self.node_df, pd.DataFrame))
        self.assertTrue(isinstance(self.edge_df, pd.DataFrame))
        self.assertTrue(isinstance(self.network, pdna.Network))
        self.assertEqual(len(self.node_df), 4)
        self.assertEqual(len(self.edge_df), 6)

    def test_gtfs_data(self):
        self.assertTrue(isinstance(self.stop_times_df, pd.DataFrame))
        Tlts.

if __name__ == '__main__':
    unittest.main()
