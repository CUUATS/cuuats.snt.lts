CREATE OR REPLACE VIEW pedestrian.sidewalk_singlepart AS
SELECT
	s.id,
	(st_dump(s.geom)).geom AS sw_geom,
	path_type as sw_type,
	width as sw_width,
	score_condition,
	buffer_type,
	buffer_width,
	segment_id
FROM pedestrian.sidewalk_segment as s;
