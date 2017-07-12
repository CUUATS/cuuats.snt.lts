import pandas
import pyodbc
from pandana import Network
from config import DB, INSTITUTIONS_SQL

def load_pois(db, sql, index_col='id'):
    with pyodbc.connect(';'.join(['='.join(i) for i in db.items()])) as conn:
        return pandas.read_sql_query(sql, conn, index_col=index_col)

network = Network.from_hdf5('sn_network.h5')
network.precompute(5280)

institutions = load_pois(DB, INSTITUTIONS_SQL)
network.set_pois('institutions', 2640, 10, institutions['x'], institutions['y'])
near_inst = network.nearest_pois(2640, 'institutions', num_pois=10)
