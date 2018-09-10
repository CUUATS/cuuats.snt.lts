-- create a view for matching stops to intersection
CREATE OR REPLACE VIEW gtfs.int_stop AS
SELECT s.stop_id,
  (SELECT i.id 
   FROM street.intersection as i
   ORDER BY s.geom <#> i.shape LIMIT 1) AS int_id
FROM gtfs.stops AS s;

-- create a view for all the common routes based on having at least 50 services to that route
CREATE OR REPLACE VIEW gtfs.common_routes AS
SELECT 
	r.route_id
FROM gtfs.routes r
 	JOIN gtfs.trips t 
		ON t.route_id = r.route_id
GROUP BY r.route_id, r.route_short_name
HAVING count(t.service_id) > 50;


-- use the common routes to find routes that has service greater than 10
CREATE OR REPLACE VIEW gtfs.common_routes AS
SELECT cr.route_id, t.service_id
FROM 
	(
	SELECT 
		r.route_id
	FROM gtfs.routes r
		JOIN gtfs.trips t 
			ON t.route_id = r.route_id
	GROUP BY r.route_id, r.route_short_name
	HAVING count(t.service_id) > 50
	) cr
	JOIN gtfs.trips t
		ON t.route_id = cr.route_id
GROUP BY cr.route_id, t.service_id
HAVING COUNT(t.service_id) > 10
ORDER BY cr.route_id;

-- for each of the trip in the trip table, find the starting intersection and the end intersection
-- also create a weight for the edge based on the arrival time between two stops
SELECT 
	st.trip_id, 
	st.stop_id, 
	st.arrival_time, 
	st.stop_sequence,
	int_id start_int, 
	lag(int_id, 1) OVER (PARTITION BY st.trip_id ORDER BY st.stop_sequence) end_int,
	arrival_time::interval - lag(arrival_time::interval, 1) OVER (PARTITION BY st.trip_id) weight
FROM gtfs.stop_times st
	JOIN gtfs.int_stop i
		ON st.stop_id = i.stop_id
ORDER BY st.trip_id