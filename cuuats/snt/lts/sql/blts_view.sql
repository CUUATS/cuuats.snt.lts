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
		 path_category text,
		 crossing_speed int,
		 lanes_crossed int,
		 control_type text,
		 median text,
		 buffer_width int,
		 buffer_type text
		) RETURNS INT AS
'
from cuuats.snt.lts import Segment, Approach, BikePath, Crossing

segment = Segment(lanes_per_direction=lanes_per_direction,
				  parking_lane_width=parking_lane_width,
				  aadt=idot_aadt,
				  functional_class=functional_classification,
				  posted_speed=posted_speed)
approaches = [Approach(lane_configuration=lane_configuration,
				     right_turn_length=right_turn_length,
				     bike_lane_approach=bike_approach_alignment)]
crossings = [Crossing(crossing_speed=crossing_speed,
											 lanes_crossed=lanes_crossed,
										   control_type=control_type,
										   median=median)]
bike_paths = [BikePath(width=bike_path_width,
					   path_category=path_category,
				   	   buffer_width=buffer_width
				   	   buffer_type=buffer_type)]

score = segment.blts_score(approaches, crossings, bike_paths, 10000)
return score
'
LANGUAGE 'plpython3u';
