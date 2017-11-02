import pandas
import pyodbc
from pandana import Network
from config import DB, NODES_SQL, EDGES_SQL

def save_network(db, nodes_sql, edges_sql, filename):
    with pyodbc.connect(';'.join(['='.join(i) for i in db.items()])) as conn:
        nodes = pandas.read_sql_query(nodes_sql, conn, index_col='id')
        edges = pandas.read_sql_query(edges_sql, conn)

    network = Network(
        nodes['x'], nodes['y'], edges['from'], edges['to'], edges[['weight']])

    network.save_hdf5(filename)

if __name__ == '__main__':
    print('Saving network...')
    save_network(DB, NODES_SQL, EDGES_SQL, 'sn_network.h5')
