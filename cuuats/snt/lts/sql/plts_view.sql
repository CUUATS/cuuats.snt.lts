CREATE OR REPLACE FUNCTION
set_plts(score_condition float,
		 sidewalk_width float,
		 posted_speed int,
		 buffer_type char,
		 total_lanes int,
		 buffer_width int,
		 overall_landuse char,
		 crossing_speed int,
		 control_type text,
		 lanes int,
		 functional_class int,
		 aadt int,
		 median text
		) RETURNS INT AS
'
from cuuats.snt.lts import Segment, Sidewalk, Crossing

segment = Segment(total_lanes=total_lanes,
				  posted_speed=posted_speed,
				  overall_landuse=overall_landuse)
sidewalks = [Sidewalk(sidewalk_width=sidewalk_width,
					  buffer_type=buffer_type,
					  buffer_width=buffer_width,
					  sidewalk_score=score_condition)]
crossings = [Crossing(
		crossing_speed=crossing_speed,
		control_type=control_type,
		lanes=lanes,
		median=median,
		functional_class=functional_class,
		aadt=aadt
)]

score = segment.plts_score(crossings, sidewalks)
return score
'
LANGUAGE 'plpython3u';

DROP MATERIALIZED VIEW street.plts_mat_view;
CREATE MATERIALIZED VIEW street.plts_mat_view AS
SELECT s.id,
		s.name,
		s.geom,
		s.idot_aadt,
		s.posted_speed,
		s.parking_lane_width,
		s.functional_classification,
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
GROUP BY s.id,
		s.name,
		s.geom,
		s.idot_aadt,
		s.posted_speed,
		s.parking_lane_width,
		s.lanes_per_direction,
		s.functional_classification;

-- update pedestrian.sidewalk_segment set buffer_type = 'landscaped with trees' where buffer_type = 'Landscaped with Trees';
