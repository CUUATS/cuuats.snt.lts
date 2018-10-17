NODES_SQL = """
SELECT intersection_id AS id,
    ST_X(ST_Transform(geom, 4326)) AS x,
    ST_Y(ST_Transform(geom, 4326)) AS y
FROM street.intersection
WHERE is_node = 'Yes'
"""

EDGES_SQL = """
SELECT s.segment_id as id,
    s.start_intersection_id AS from,
    s.end_intersection_id AS to,
    (ST_Length(geom) * l.blts)::numeric AS bike_weight,
    (ST_Length(geom) * l.plts)::numeric AS ped_weight
FROM street.segment s
    JOIN street.lts_score l
        ON s.segment_id = l.segment_id
WHERE s.start_intersection_id IS DISTINCT FROM NULL AND
    s.end_intersection_id IS DISTINCT FROM NULL
UNION
SELECT s.segment_id as id,
    s.end_intersection_id AS from,
    s.start_intersection_id AS to,
    (ST_Length(geom) * l.blts)::numeric AS bike_weight,
    (ST_Length(geom) * l.plts)::numeric AS ped_weight
FROM street.segment s
    JOIN street.lts_score l
        ON s.segment_id = l.segment_id
WHERE s.start_intersection_id IS DISTINCT FROM NULL AND
    s.end_intersection_id IS DISTINCT FROM NULL
"""
# 
# POI_SQL = """
# SELECT id,
# 	ST_X(shape) AS x,
# 	ST_Y(shape) AS y
# FROM vehicle.alternative_fuel_station
# """

TRANSIT_POI_SQL = """
SELECT id,
	ST_X(ST_Transform(shape, 4326)) AS x,
	ST_Y(ST_Transform(shape, 4326)) AS y
FROM vehicle.alternative_fuel_station
"""

TRANSIT_INSTITUTION_SQL = """
SELECT id,
	ST_X(ST_Transform(geom, 4326)) AS x,
	ST_Y(ST_Transform(geom, 4326)) AS y
FROM public_facility.institution
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

TRANSIT_JOB_SQL = """
SELECT duns_num AS id,
	ST_X(ST_Transform(geom, 4326)) AS x,
	ST_Y(ST_Transform(geom, 4326)) AS y,
	CASE WHEN emp_num = 0 THEN 1::float
	ELSE emp_num::float
	END
	AS emp_num
FROM business."esri_2014
";
"""
