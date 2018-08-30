SELECT DISTINCT ON (s.stop_id) s.stop_id, i.id, ST_Distance(s.geom, i.shape) dist 
FROM gtfs.stops AS s
	JOIN street.intersection AS i
		ON ST_DWithin(s.geom, i.shape, 50)
ORDER BY s.stop_id;

-- select id, shape from street.intersection;