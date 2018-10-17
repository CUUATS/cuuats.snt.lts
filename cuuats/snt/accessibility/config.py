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

CAR_SQL = """
SELECT id,
	ST_X(ST_Transform(shape, 4326)) AS x,
	ST_Y(ST_Transform(shape, 4326)) AS y
FROM vehicle.alternative_fuel_station
"""

INSTITUTION_SQL = """
SELECT id,
	ST_X(ST_Transform(geom, 4326)) AS x,
	ST_Y(ST_Transform(geom, 4326)) AS y
FROM public_facility.institution
"""

JOB_SQL = """
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
