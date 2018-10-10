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
FROM vehicle.alternative_fuel_station
"""

TRANSIT_POI_SQL = """
SELECT id,
	ST_X(ST_Transform(shape, 4326)) AS x,
	ST_Y(ST_Transform(shape, 4326)) AS y
FROM vehicle.alternative_fuel_station
"""

TRANSIT_NODES_SQL = """
SELECT intersection_id AS id,
    ST_X(ST_Transform(geom, 4326)) AS X,
    ST_Y(ST_Transform(geom, 4326)) AS Y
FROM street.intersection
WHERE is_node = 'Yes'
"""

PED_TRANSIT_EDGES_SQL = """
SELECT
    s.start_intersection_id AS from,
    s.end_intersection_id AS to,
    ((ST_Length(geom) / 5280) / 3 * 60 * 60)::numeric * lts.plts AS weight
FROM street.segment s
JOIN street.lts_score as lts
	ON lts.segment_id = s.segment_id
WHERE s.start_intersection_id IS DISTINCT FROM NULL AND
    s.end_intersection_id IS DISTINCT FROM NULL
UNION
SELECT
    s1.end_intersection_id AS from,
    s1.start_intersection_id AS to,
    ((ST_Length(geom) / 5280) / 3 * 60 * 60)::numeric * lts1.plts AS weight
FROM street.segment s1
JOIN street.lts_score as lts1
	ON lts1.segment_id = s1.segment_id
WHERE s1.start_intersection_id IS DISTINCT FROM NULL AND
    s1.end_intersection_id IS DISTINCT FROM NULL
"""
