-- DROP FUNCTION set_blts(int) CASCADE;
CREATE OR REPLACE FUNCTION
set_blts(idot_aadt int,
		 bicycle_facility_width int,
		 posted_speed int,
		 parking_lane_width int,
		 lanes_per_direction int,
		 functional_classification int,
		 bike_path_width float,
		 lane_configuration text,
		 right_turn_length int,
		 bike_approach_alignment text,
		 path_category text
		) RETURNS INT AS
'
from cuuats.snt.lts.model.Segment import Segment
from cuuats.snt.lts.model.Approach import Approach
from cuuats.snt.lts.model.BikePath import BikePath

segment = Segment(lanes_per_direction=lanes_per_direction,
				  parking_lane_width=parking_lane_width,
				  aadt=idot_aadt,
				  functional_class=functional_classification,
				  posted_speed=posted_speed)
approaches = [Approach(lane_configuration=lane_configuration,
				     right_turn_length=right_turn_length,
				     bike_lane_approach=bike_approach_alignment)]
bike_paths = [BikePath(width=bike_path_width,
					   path_category=path_category)]

score = segment.blts_score(approaches, bike_paths)
return score
'
LANGUAGE 'plpython3u';

-- DROP MATERIALIZED VIEW street.blts_mat_view
CREATE MATERIALIZED VIEW street.blts_mat_view AS
SELECT s.id,
		s.name,
		s.geom,
		s.idot_aadt,
		s.posted_speed,
		s.parking_lane_width,
		s.lanes_per_direction,
		s.functional_classification,
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
GROUP BY s.id,
		s.name,
		s.geom,
		s.idot_aadt,
		s.posted_speed,
		s.parking_lane_width,
		s.lanes_per_direction,
		s.functional_classification;
		
-- REFRESH MATERIALIZED VIEW street.blts_mat_view;

SELECT * FROM street.blts_mat_view;
