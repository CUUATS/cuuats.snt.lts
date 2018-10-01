-- Create a singlepart line string for the bike paths
CREATE OR REPLACE VIEW bicycle.path_singlepart AS
SELECT
	path.id, (st_dump(path.geom)).geom AS bike_geom,
	width AS bike_width,
	buffer_width,
	buffer_type,
	path_category,
	path_subtype,
	path_type
FROM bicycle.path;
