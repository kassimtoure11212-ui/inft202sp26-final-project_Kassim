SELECT titles.titleType, AVG(ratings.averageRating) AS avg_rating
FROM titles
JOIN ratings
ON titles.tconst = ratings.tconst
GROUP BY titles.titleType
ORDER BY avg_rating DESC;
