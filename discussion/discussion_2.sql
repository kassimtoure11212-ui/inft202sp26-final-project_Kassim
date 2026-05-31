SELECT titles.genres, COUNT(*) AS total_titles
FROM titles
JOIN ratings
ON titles.tconst = ratings.tconst
WHERE ratings.averageRating >= 8.0
GROUP BY titles.genres
ORDER BY total_titles DESC;
