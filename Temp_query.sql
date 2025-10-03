--Manchester United home matches result in the 2011/2012 season 
WITH home_match AS (
 SELECT id, season, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal
FROM Match
WHERE home_team_api_id =10260 AND season = '2011/2012'
)

SELECT  h.home_team_goal, h.away_team_goal, t.team_long_name,
 CASE WHEN home_team_goal > away_team_goal THEN 'United win'
      WHEN home_team_goal < away_team_goal THEN 'United lose'
 ELSE 'Draw'  END AS result
FROM Team as t
INNER JOIN home_match as h
ON h.away_team_api_id = t.team_api_id

--Manchester United away matches result in 2011/2012 season 
WITH away_match AS (
 SELECT id, season, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal
FROM Match
WHERE away_team_api_id =10260 AND season = '2011/2012'
)

SELECT a.home_team_goal, a.away_team_goal, t.team_long_name,
 CASE WHEN home_team_goal > away_team_goal THEN 'United Lose'
      WHEN home_team_goal < away_team_goal THEN 'United Win'
 ELSE 'Draw'  END AS result
FROM Team as t
INNER JOIN away_match as a
ON a.home_team_api_id = t.team_api_id
ORDER BY a.id

--Goals Scored Across All leagues in the 2011/2012 season
SELECT l.name, SUM(m.home_team_goal + m.away_team_goal) AS total_goals_2011_2012
FROM Match as m
INNER JOIN League as l
ON m.country_id = l.country_id
WHERE season = '2011/2012'
GROUP BY l.name
ORDER BY total_goals_2011_2012 DESC

--Matches Played Across All Leagues in 2011/2012 season
SELECT l.name, COUNT(l.country_id)
FROM Team AS t
LEFT JOIN Match as m
ON t.team_api_id = m.home_team_api_id
INNER JOIN League as l
ON m.country_id = l.country_id
WHERE m.season = '2011/2012'
GROUP BY l.name

--Total goals per season across all leagues in the data using a CTE
WITH match_list AS (
 SELECT l.name AS league, m.season, m.home_team_goal, m.away_team_goal, (m.home_team_goal + m.away_team_goal) AS total_goals
 FROM Match AS m
 INNER JOIN League AS l
 ON m.country_id = l.country_id )

 SELECT league, season, SUM(total_goals) AS total_goals_per_season
 FROM match_list
 GROUP BY league,season
 ORDER BY 1,2

--Matches where sum of goals in a match exceeds the average by 3 times (outliers)
SELECT main.country_id, main.home_team_goal, main.away_team_goal, main.season
FROM Match AS main
WHERE (home_team_goal + away_team_goal) >
    (SELECT AVG(sub.home_team_goal + sub.away_team_goal) * 3 FROM Match AS sub WHERE main.country_id = sub.country_id )

--Highest scoring matches for each country in each season
SELECT main.country_id, main.home_team_goal, main.away_team_goal, main.season
FROM Match AS main
WHERE (home_team_goal + away_team_goal) =
    (SELECT MAX(sub.home_team_goal + sub.away_team_goal) 
	FROM Match AS sub 
	WHERE main.country_id = sub.country_id AND main.season = sub.season )

--Average number of matches per season where total goals scored was 5 or more
SELECT country_id, 
AVG(matches_per_season) AS avg_matches
FROM (
     SELECT 
	 country_id,
	 season,
	 COUNT(*) AS matches_per_season
	 FROM Match 
	 WHERE home_team_goal + away_team_goal >= 5 
	 GROUP BY country_id, season) AS subquery
GROUP BY country_id

--Matches that recorded 10 or more goals across all leagues
WITH match_list AS (
 SELECT l.name AS league, m.season, m.home_team_goal, m.away_team_goal, (m.home_team_goal + m.away_team_goal) AS total_goals
 FROM Match AS m
 LEFT JOIN League AS l
 ON m.country_id = l.country_id )

SELECT league, season, home_team_goal, away_team_goal, (SELECT (home_team_goal + away_team_goal)) AS total
FROM match_list
WHERE total_goals >= 10 
ORDER BY 1,2

