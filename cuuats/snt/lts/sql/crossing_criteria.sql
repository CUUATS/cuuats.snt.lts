CREATE OR REPLACE VIEW street.crossing_criteria AS
WITH approach_angle AS (
  SELECT approach.segment_id,
    approach.intersection_id,
	segment.posted_speed,
    segment.functional_classification,
    segment.idot_aadt,
    intersection.control_type,
    approach.median_refuge_type,
    CASE WHEN approach.lane_configuration IS DISTINCT FROM NULL THEN
      char_length(approach.lane_configuration) ELSE segment.total_lanes END
      AS lanes,
    degrees(ST_Azimuth(
      ST_PointN(segment.geom, CASE WHEN
        approach.intersection_id = segment.start_intersection_id
        THEN 1 ELSE -1 END),
      ST_PointN(segment.geom, CASE WHEN
        approach.intersection_id = segment.start_intersection_id
        THEN 2 ELSE -2 END)
    )) AS angle
  FROM street.intersection_approach AS approach
  LEFT JOIN street.segment AS segment
    ON approach.segment_id = segment.segment_id
  JOIN street.intersection AS intersection
    ON approach.intersection_id = intersection.id
) SELECT seg.segment_id,
  seg.control_type,
  seg.median_refuge_type,
  max(crossed.idot_aadt) AS aadt,
  min(crossed.functional_classification) AS functional_class,
  max(crossed.posted_speed) AS posted_speed,
  max(coalesce(crossed.lanes, 0)) AS max_lanes_crossed
FROM approach_angle AS seg
LEFT JOIN approach_angle AS crossed
  ON seg.intersection_id = crossed.intersection_id
    AND seg.segment_id <> crossed.segment_id
    AND (CASE WHEN abs(seg.angle - crossed.angle) > 180
      THEN 360 - abs(seg.angle - crossed.angle)
      ELSE abs(seg.angle - crossed.angle) END) < 135
GROUP BY seg.segment_id, seg.control_type, seg.median_refuge_type
ORDER BY seg.segment_id
