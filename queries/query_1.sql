SELECT tconst, averageRating, numVotes
FROM ratings
WHERE averageRating >= 8.0
ORDER BY numVotes DESC
LIMIT 10;
