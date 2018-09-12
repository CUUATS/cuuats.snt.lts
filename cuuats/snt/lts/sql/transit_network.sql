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
