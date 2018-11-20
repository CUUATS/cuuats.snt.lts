-- DROP FUNCTION set_blts(int) CASCADE;
CREATE OR REPLACE FUNCTION
set_alts(bike_path_width float,
		 path_category text,
		 buffer_width int,
		 buffer_type text,
		 path_type text
		) RETURNS INT AS
'
from cuuats.snt.lts import Segment, BikePath

segment = Segment()

bike_paths = [BikePath(width=bike_path_width,
					   path_category=path_category,
				   	   buffer_width=buffer_width,
				   	   buffer_type=buffer_type,
				   	   path_type=path_type)]

score = segment.alts_score(bike_paths)
return score

'
LANGUAGE 'plpython3u';
