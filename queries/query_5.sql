SELECT titles.primaryTitle, titles.titleType, ratings.averageRating, ratings.numVotes
FROM titles
JOIN ratings
ON titles.tconst = ratings.tconst
ORDER BY ratings.numVotes DESC
LIMIt 10;
