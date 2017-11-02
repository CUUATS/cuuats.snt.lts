import os

DB = {
    'Server': os.environ['SN_SERVER'],
    'Database': os.environ['SN_DATABASE'],
    'UID': os.environ['SN_USER'],
    'PWD': os.environ['SN_PASSWORD'],
    'Driver': os.environ['SN_DRIVER']
}

NODES_SQL = """
SELECT IntersectionID AS id,
    Shape.STX AS x,
    Shape.STY AS y
FROM %s
WHERE IsNode = 'Yes'
""" % (os.environ['SN_NODES_TABLE'],)

EDGES_SQL = """
SELECT StreetID AS id,
    StartIntersectionID AS 'from',
    EndIntersectionID AS 'to',
    Shape.STLength() AS weight
FROM %s
WHERE StartIntersectionID <> EndIntersectionID
""" % (os.environ['SN_EDGES_TABLE'],)

INSTITUTIONS_SQL = """
SELECT OBJECTID AS id,
    Shape.STX AS x,
    Shape.STY AS y
FROM %s
""" % (os.environ['SN_INSTITUTIONS_TABLE'],)
