select * From street.intersection_approach;
select * from street.segment;
select * from street.intersection;

-- query to look for the closet two approach to the segment and the two closet lanes
SELECT t.ori_seg, t. r_seg, t.lane_configuration, t.total_lanes, t.posted_speed FROM (
	SELECT s.id ori_seg, i.intersection_id, rs.id r_seg, ra.lane_configuration, rs.total_lanes, rs.posted_speed,
		ROW_NUMBER() OVER (PARTITION BY s.id, i.intersection_id ORDER BY ST_Azimuth(ST_LineInterpolatePoint(s.geom, 0.5), ST_LineInterpolatePoint(rs.geom,0.5)) DESC) AS ran
	FROM street.segment s
		LEFT JOIN street.intersection i
			ON s.start_intersection_id = i.intersection_id 
 			OR s.end_intersection_id = i.intersection_id
		RIGHT OUTER JOIN street.segment rs
			ON (i.intersection_id = rs.start_intersection_id OR
				i.intersection_id = rs.end_intersection_id) AND
				rs.id <> s.id
		JOIN street.intersection_approach ra
			ON ra.segment_id = rs.segment_id AND
				ra.intersection_id = i.intersection_id
	WHERE s.id > 13000 AND s.id < 14000
	ORDER BY ori_seg
	) t
WHERE t.ran <= 2
ORDER by t.ori_seg;



-- test query
SELECT s.id ori_seg, i.intersection_id, rs.id r_seg, ra.lane_configuration, rs.total_lanes, rs.posted_speed,
	ST_Azimuth(
		ST_Line_Interpolate_Point(
			s.geom, ST_LineLocatePoint(
				s.geom, i.shape)
		), 
		ST_Line_Interpolate_Point(
			rs.geom, ST_LineLocatePoint(
				rs.geom, i.shape)
		)),
	ROW_NUMBER() OVER (PARTITION BY s.id, i.intersection_id ORDER BY 
	ST_Azimuth(
		ST_LineInterpolatePoint(
			s.geom, ST_LineLocatePoint(
				s.geom, i.shape)
		), 
		ST_LineInterpolatePoint(
			rs.geom, ST_LineLocatePoint(
 				rs.geom, i.shape)
		)) DESC
	) AS ran
FROM street.segment s
	LEFT JOIN street.intersection i
		ON s.start_intersection_id = i.intersection_id 
		OR s.end_intersection_id = i.intersection_id
	RIGHT OUTER JOIN street.segment rs
		ON (i.intersection_id = rs.start_intersection_id OR
			i.intersection_id = rs.end_intersection_id) AND
			rs.id <> s.id
	JOIN street.intersection_approach ra
		ON ra.segment_id = rs.segment_id AND
			ra.intersection_id = i.intersection_id
WHERE s.id = 12693
ORDER BY ori_seg

select * from street.intersection_approach;


--
SELECT * FROM street.intersection;