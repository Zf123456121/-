

SELECT
	count(*) AS user_num
FROM
	(
		SELECT
			user_id,
			count(user_id) AS nums
		FROM
			(
				SELECT
        	user_id
				FROM
					event_log
				WHERE
					DATE_FORMAT(DATE(FROM_UNIXTIME(event_timestamp)),'%Y-%m') = "2022-09"
			) t
		GROUP BY
			user_id
		HAVING
			nums >= 1000	AND nums < 2000
	) t2;
	
	
	
	
	