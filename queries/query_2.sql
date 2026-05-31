SELECT titleType, COUNT(*) AS total_titles
FROM titles
GROUP BY titleType
ORDER BY total_titles DESC;
