-- Create transit network based on the nodes connection frequency
SELECT edge.seq,
    avg(edge.time_diff),
    count(edge.seq)
FROM (
    SELECT
    	lag(stop_id)
    		OVER (PARTITION BY trip_id
                    ORDER BY stop_sequence) || ',' || stop_id
                        AS seq,
        arrival_time::interval -
        lag(arrival_time)
            OVER (PARTITION BY trip_id
                    ORDER BY stop_sequence)::interval
                        AS time_diff
    FROM gtfs.stop_times
) edge
GROUP BY edge.seq


-- Create view with intersection id join to bus stop id
CREATE OR REPLACE VIEW gtfs.int_stop AS
SELECT s.stop_id,
  (SELECT i.intersection_id
   FROM street.intersection as i
   ORDER BY s.geom <#> i.shape LIMIT 1) AS intersection_id
FROM gtfs.stops AS s;

-- Create intersection nodes with time between and count
CREATE MATERIALIZED VIEW gtfs.transit_edge AS
SELECT
    edge.start_intersection,
    edge.end_intersection,
    avg(edge.time_diff) AS travel_time,
    count(edge.start_intersection) AS trip_count
FROM
    (SELECT
    	lag(intersection_id)
    		OVER (PARTITION BY trip_id
                    ORDER BY stop_sequence)
                        AS start_intersection,
        intersection_id AS end_intersection,
        arrival_time::interval -
        lag(arrival_time)
            OVER (PARTITION BY trip_id
                    ORDER BY stop_sequence)::interval
                        AS time_diff
    FROM gtfs.stop_times AS stop_times
    JOIN gtfs.int_stop AS int_stop
        ON int_stop.stop_id =  stop_times.stop_id
) edge
WHERE edge.start_intersection <> edge.end_intersection
GROUP BY edge.start_intersection, edge.end_intersection
