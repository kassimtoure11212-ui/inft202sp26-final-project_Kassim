SELECT titleType, AVG(runtimeMinutes) AS avg_runtime
FROM titles
WHERE runtimeMinutes IS NOT NULL
GROUP BY titleType
ORDER BY avg_runtime DESC;
