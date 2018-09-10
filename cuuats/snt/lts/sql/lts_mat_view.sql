DROP MATERIALIZED VIEW street.lts_mat_view;
CREATE MATERIALIZED VIEW street.lts_mat_view AS
SELECT s.id, s.geom , b.blts, p.plts 
FROM street.segment as s
LEFT JOIN street.blts_mat_view as b
	ON s.id = b.id
LEFT JOIN street.plts_mat_view as p
	ON s.id = p.id;

CREATE MATERIALIZED VIEW street.lts_mat_view AS
SELECT b1.id, b1.blts, b2.plts FROM 
	(SELECT s.id,
			max(set_blts(idot_aadt,
					 bicycle_facility_width,
					 posted_speed,
					 parking_lane_width,
					 lanes_per_direction,
					 functional_classification,
					 bike_width,
					 lane_configuration,
					 right_turn_length,
					 bike_approach_alignment,
					 path_category)) as blts
	FROM street.segment AS s
	LEFT JOIN bicycle.path_singlepart as b
		ON ST_DWithin(s.geom, b.bike_geom, 100) AND
		  pcd_segment_match(s.geom, b.bike_geom, 100)
	LEFT JOIN street.intersection_approach as i
		ON s.id = i.segment_id
	GROUP BY s.id) b1
LEFT JOIN
	(SELECT s.id,
			max(set_plts(score_condition,
						 sw_width,
						 posted_speed,
						 buffer_type,
						 total_lanes,
						 buffer_width,
						 overall_land_use)) as plts
	FROM street.segment AS s
	LEFT JOIN pedestrian.sidewalk_singlepart as w
		ON ST_DWithin(s.geom, w.sw_geom, 100) AND
		  pcd_segment_match(s.geom, w.sw_geom, 100)
	GROUP BY s.id) b2
ON b1.id = b2.id;

SELECT * FROM street.lts_mat_view LIMIT 5;