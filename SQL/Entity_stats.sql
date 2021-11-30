SELECT 
e.entity_name
, e.entity_sentiment_score
, e.entity_sentiment_magnitude
, e.entity_salience
, p.post_ratio
, p.comment_score
, p.post_comments
, FROM_UNIXTIME(p.comment_date)
FROM proddis.entities as e
LEFT JOIN proddis.comments as p
ON e.post_id = p.post_id
WHERE e.entity_salience > 0.5