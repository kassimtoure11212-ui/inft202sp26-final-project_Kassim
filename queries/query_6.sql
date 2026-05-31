SELECT titles.titleType, AVG(ratings.numVotes) AS avg_votes, COUNT(*) AS rated_titles
FROM titles
JOIN ratings
ON titles.tconst = ratings.tconst
GROUP BY titles.titleType
ORDER BY avg_votes DESC;
