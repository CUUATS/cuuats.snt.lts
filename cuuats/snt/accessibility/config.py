NODES_SQL = """
SELECT intersection_id AS id,
    ST_X(geom) AS x,
    ST_Y(geom) AS y
FROM street.intersection
WHERE is_node = 'Yes'
"""

EDGES_SQL = """
SELECT s.id,
    s.start_intersection_id AS from,
    s.end_intersection_id AS to,
    (ST_Length(geom) * l.blts)::numeric AS blts_weight,
    (ST_Length(geom) * l.plts)::numeric AS plts_weight
FROM street.segment s
    JOIN street.lts_score l
        ON s.id = l.id
WHERE s.start_intersection_id IS DISTINCT FROM NULL AND
    s.end_intersection_id IS DISTINCT FROM NULL
"""

POI_SQL = """
SELECT id,
    ST_X(shape) AS x,
    ST_Y(shape) AS y
FROM vehicle.car_share_location
"""
