-- Create a singlepart line string for the bike paths

-- DROP MATERIALIZED VIEW bicycle.path_singlepart CASCADE;

CREATE MATERIALIZED VIEW bicycle.path_singlepart AS
SELECT
	path.id, (st_dump(path.geom)).geom AS bike_geom,
	width AS bike_width,
	buffer_width,
	buffer_type,
	path_category,
	path_subtype,
	path_type
FROM bicycle.path;

SELECT * FROM bicycle.path_singlepart;



-- SELECT * FROM bicycle.path;
-- SELECT * FROM street.intersection_approach;
