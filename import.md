# SQLite CSV Import Guide

Database file: `final.db`

Use Beekeeper Studio to import the two IMDb CSV files into the tables you created.

## Import `titles`

1. Open Beekeeper Studio.
2. Connect to `final.db`.
3. Right-click the `titles` table.
4. Choose the CSV import option.
5. Select `imdb_datasets/title.basics.csv`.
6. Make sure the CSV columns map to these table columns:
   - `tconst`
   - `titleType`
   - `primaryTitle`
   - `originalTitle`
   - `isAdult`
   - `startYear`
   - `endYear`
   - `runtimeMinutes`
   - `genres`
7. Run the import.

## Import `ratings`

1. Right-click the `ratings` table.
2. Choose the CSV import option.
3. Select `imdb_datasets/title.ratings.csv`.
4. Make sure the CSV columns map to these table columns:
   - `tconst`
   - `averageRating`
   - `numVotes`
5. Run the import.

## Verify Row Counts

After importing, run these checks in Beekeeper Studio:

```sql
SELECT COUNT(*) FROM titles;
```

```sql
SELECT COUNT(*) FROM ratings;
```

Each table should have about 1,000,000 rows if the full CSV files imported successfully.
