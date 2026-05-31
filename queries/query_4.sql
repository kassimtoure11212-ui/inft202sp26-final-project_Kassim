SELECT titles.titleType, AVG(ratings.averageRating) AS avg_rating, COUNT(*) AS total_titles
FROM titles
JOIN ratings
ON titles.tconst = ratings.tconst
GROUP BY titles.titleType
HAVING COUNT(*) > 1000
ORDER BY avg_rating DESC;
