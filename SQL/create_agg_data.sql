CREATE TABLE proddis.agg_data AS 
WITH e1 AS (Select a.entity_name, a.entity_sentiment_score, a.entity_sentiment_magnitude, a.comment_id, b.comment_score, b.post_ratio, b.post_comments, b.comment_date
			from proddis.entities as a 
            left join proddis.comments as b 
            on a.post_id = b.post_id and a.comment_id = b.comment_id)
, c1 AS (SELECT entity_name, COUNT(distinct comment_id) AS comment_mentions
			, avg(entity_sentiment_score) AS avg_sentiment
			, avg(entity_sentiment_magnitude) AS avg_magnitude
            , sum(comment_score) AS comment_total_votes
            , avg(post_ratio) AS avg_post_ratio
            , sum(post_comments) as post_total_comments
            , FROM_UNIXTIME(max(comment_date)) AS latest_mention
			from e1
			group by entity_name)       
SELECT *
from c1
ORDER BY comment_total_votes DESC, avg_sentiment DESC