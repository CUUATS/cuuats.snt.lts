-- DROP MATERIALIZED VIEW street.lts_mat_view;
CREATE MATERIALIZED VIEW street.lts_score AS
SELECT b1.segment_id, b1.blts, b2.plts FROM
	(SELECT s.segment_id,
			max(set_blts(idot_aadt,
					 bicycle_facility_width,
					 s.posted_speed,
					 parking_lane_width,
					 lanes_per_direction,
					 functional_classification,
					 bike_width,
					 lane_configuration,
					 right_turn_length,
					 bike_approach_alignment,
					 path_category,
				     cc.posted_speed,
				     max_lanes_crossed,
				     control_type,
				     cc.median_refuge_type,
			         b.buffer_width,
				 	 b.buffer_type)) as blts
	FROM street.segment AS s
	LEFT JOIN bicycle.path_singlepart as b
		ON ST_DWithin(s.geom, b.bike_geom, 100) AND
		  pcd_segment_match(s.geom, b.bike_geom, 100)
	LEFT JOIN street.intersection_approach as i
		ON s.segment_id = i.segment_id
	LEFT JOIN street.crossing_criteria as cc
	 	ON s.segment_id = cc.segment_id
	GROUP BY s.segment_id) b1
LEFT JOIN
	(SELECT s.segment_id,
			max(set_plts(score_condition,
						 sw_width,
						 s.posted_speed,
						 buffer_type,
						 total_lanes,
						 buffer_width,
						 overall_land_use,
					 	 cc.posted_speed,
					 	 control_type,
					 	 max_lanes_crossed,
					 	 functional_class,
					 	 aadt,
					 	 median_refuge_type)) as plts
	FROM street.segment AS s
	LEFT JOIN pedestrian.sidewalk_singlepart as w
		ON ST_DWithin(s.geom, w.sw_geom, 100) AND
		  pcd_segment_match(s.geom, w.sw_geom, 100)
	LEFT JOIN street.crossing_criteria as cc
		ON s.segment_id = cc.segment_id
	GROUP BY s.segment_id) b2
ON b1.segment_id = b2.segment_id;
