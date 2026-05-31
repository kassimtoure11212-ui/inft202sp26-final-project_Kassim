# Schema Plan: IMDb Titles And Ratings

## Project Focus

This project will use two related IMDb tables:

1. `titles`, based on `imdb_datasets/title.basics.csv`
2. `ratings`, based on `imdb_datasets/title.ratings.csv`

The relationship is based on `tconst`, the IMDb title ID. Each row in `ratings` describes the rating summary for one title from `titles`.

## Table: `titles`

One row represents one IMDb title, such as a movie, TV episode, TV series, short, video, or video game.

| Column | Suggested SQLite Type | Key? | Why |
| --- | --- | --- | --- |
| `tconst` | `TEXT` | Primary key | IMDb title ID; identifies one title |
| `titleType` | `TEXT` |  | Category such as movie, tvEpisode, short, video, or tvSeries |
| `primaryTitle` | `TEXT` |  | Main title name |
| `originalTitle` | `TEXT` |  | Original title name |
| `isAdult` | `INTEGER` |  | 0 or 1 flag |
| `startYear` | `INTEGER` |  | Release/start year when available |
| `endYear` | `INTEGER` |  | End year for series when available |
| `runtimeMinutes` | `INTEGER` |  | Runtime in minutes when available |
| `genres` | `TEXT` |  | Comma-separated genre labels |

Notes:
- `tconst` should identify one row in this table.
- `startYear` and `endYear` appear as values like `2015.0` in the CSV, so imports may need cleanup or SQLite may store them loosely.
- `genres` contains comma-separated values. For this beginner project, keeping it as `TEXT` is acceptable.
- Many rows are missing `runtimeMinutes`, so that column should allow blanks/nulls.

## Table: `ratings`

One row represents the rating summary for one IMDb title.

| Column | Suggested SQLite Type | Key? | Why |
| --- | --- | --- | --- |
| `tconst` | `TEXT` | Primary key and foreign key | Connects this rating row to one title in `titles` |
| `averageRating` | `REAL` |  | Decimal rating such as 7.7 |
| `numVotes` | `INTEGER` |  | Number of votes behind the rating |

Notes:
- `ratings.tconst` connects to `titles.tconst`.
- `averageRating` should be numeric because later queries can average, sort, or compare ratings.
- `numVotes` should be numeric because later queries can sort by popularity or filter to titles with many votes.

## Relationship

`ratings.tconst` should reference `titles.tconst`.

In plain English: the ratings table does not repeat title names, years, genres, or title types. It stores rating facts and uses `tconst` to connect back to the title details.

## Columns To Keep

Keep all columns from both selected CSV files for now:

- `titles`: `tconst`, `titleType`, `primaryTitle`, `originalTitle`, `isAdult`, `startYear`, `endYear`, `runtimeMinutes`, `genres`
- `ratings`: `tconst`, `averageRating`, `numVotes`

## Columns To Skip

Skip the other IMDb files for this project:

- `name.basics.csv`
- `title.akas.csv`
- `title.crew.csv`
- `title.episode.csv`
- `title.principals.csv`

These files are useful, but they add extra complexity. The two-table design is enough to practice filtering, sorting, grouping, aggregates, and joins.

## Questions This Schema Can Answer

1. Which title types have the most records?
2. Which titles have the highest ratings among titles with many votes?
3. What is the average rating for each title type?
4. Which title types have the longest average runtime?
5. How do ratings and vote counts differ across movies, TV episodes, shorts, and videos?
