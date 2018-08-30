SELECT AddGeometryColumn('gtfs', 'stops', 'geom', 3435, 'POINT', 2);
UPDATE gtfs.stops SET geom = ST_Transform(ST_SetSRID(ST_MakePoint(stop_lon, stop_lat), 4326), 3435);

-- ALTER TABLE gtfs.stops
-- DROP COLUMN geom;