DROP MATERIALIZED VIEW street.lts_mat_view;
CREATE MATERIALIZED VIEW street.lts_mat_view AS
SELECT s.id, s.geom , b.blts, p.plts 
FROM street.segment as s
LEFT JOIN street.blts_mat_view as b
	ON s.id = b.id
LEFT JOIN street.plts_mat_view as p
	ON s.id = p.id;
	
SELECT * FROM street.lts_mat_view;