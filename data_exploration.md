# Data Exploration: IMDb Dataset

## Dataset Overview

The project dataset is an IMDb data bundle extracted from `archive (1).zip`. It contains several related CSV files about titles, people, ratings, crews, episodes, alternate titles, and cast/crew participation.

Each CSV has 1,000,000 rows, so this project should focus on a smaller set of related tables rather than trying to use every file at once.

## Files

| File | Rows | What One Row Represents |
| --- | ---: | --- |
| `imdb_datasets/name.basics.csv` | 1,000,000 | One person in IMDb, such as an actor, director, writer, or crew member |
| `imdb_datasets/title.akas.csv` | 1,000,000 | One alternate/localized title for a movie, episode, show, or other title |
| `imdb_datasets/title.basics.csv` | 1,000,000 | One IMDb title, such as a movie, TV episode, short, video, or TV series |
| `imdb_datasets/title.crew.csv` | 1,000,000 | Crew ID lists for one title |
| `imdb_datasets/title.episode.csv` | 1,000,000 | One TV episode linked to its parent series |
| `imdb_datasets/title.principals.csv` | 1,000,000 | One important cast or crew credit for a title |
| `imdb_datasets/title.ratings.csv` | 1,000,000 | One rating summary for a title |

## Important Columns

### `title.basics.csv`

Important columns:
- `tconst`: candidate primary key; uniquely identifies a title.
- `titleType`: category such as movie, short, tvEpisode, tvSeries, video, or videoGame.
- `primaryTitle`: main title shown to users.
- `isAdult`: 0 or 1 flag.
- `startYear`: year the title started or was released.
- `runtimeMinutes`: length of the title, when available.
- `genres`: comma-separated genres.

Data quality notes:
- `startYear` is missing in 117,546 rows.
- `runtimeMinutes` is missing in 641,155 rows.
- `endYear` is missing in 987,331 rows, which makes sense because most titles are not ongoing series with an end year.
- `genres` is missing in 43,165 rows.

### `title.ratings.csv`

Important columns:
- `tconst`: foreign key candidate that connects to `title.basics.tconst`.
- `averageRating`: numeric rating.
- `numVotes`: number of votes behind the rating.

Data quality notes:
- No missing values were reported in this file.
- This is one of the cleanest tables for analysis.

### `name.basics.csv`

Important columns:
- `nconst`: candidate primary key; uniquely identifies a person.
- `primaryName`: person's display name.
- `birthYear` and `deathYear`: numeric year fields, often blank.
- `primaryProfession`: comma-separated profession list.
- `knownForTitles`: comma-separated title IDs.

Data quality notes:
- `birthYear` is missing in 955,788 rows.
- `deathYear` is missing in 982,953 rows.
- `primaryProfession` is missing in 201,605 rows.
- `knownForTitles` is missing in 119,565 rows.

### `title.principals.csv`

Important columns:
- `tconst`: connects to `title.basics.tconst`.
- `nconst`: connects to `name.basics.nconst`.
- `category`: role category, such as actor, actress, director, writer, composer, or producer.
- `characters`: character names for some acting credits.

Data quality notes:
- `job` is missing in 808,522 rows.
- `characters` is missing in 511,715 rows.
- This file is useful for joins, but it is large and has many repeated title/person combinations.

### `title.akas.csv`

Important columns:
- `titleId`: connects to `title.basics.tconst`.
- `ordering`: order number for the alternate title.
- `title`: alternate title text.
- `region`: country/region code.
- `language`: language code.
- `isOriginalTitle`: 0 or 1 flag.

Data quality notes:
- `region` is missing in 219,226 rows.
- `language` is missing in 328,225 rows.
- `attributes` is missing in 994,559 rows.

### `title.crew.csv`

Important columns:
- `tconst`: connects to `title.basics.tconst`.
- `directors`: comma-separated person IDs.
- `writers`: comma-separated person IDs.

Data quality notes:
- `directors` is missing in 441,689 rows.
- `writers` is missing in 491,541 rows.
- The comma-separated ID lists are harder to use in beginner SQL.

### `title.episode.csv`

Important columns:
- `tconst`: episode title ID.
- `parentTconst`: parent series title ID.
- `seasonNumber`: season number.
- `episodeNumber`: episode number.

Data quality notes:
- `seasonNumber` and `episodeNumber` are each missing in 207,513 rows.
- This table is useful if the project focuses on TV episodes and series.

## Candidate Keys And Relationships

Strong primary key candidates:
- `title.basics.tconst`
- `title.ratings.tconst`
- `name.basics.nconst`

Strong foreign key candidates:
- `title.ratings.tconst` points to `title.basics.tconst`
- `title.principals.tconst` points to `title.basics.tconst`
- `title.principals.nconst` points to `name.basics.nconst`
- `title.akas.titleId` points to `title.basics.tconst`
- `title.episode.parentTconst` points to `title.basics.tconst`

## Recommended Project Focus

The clearest beginner-friendly table pair is:

1. `titles`, based on `title.basics.csv`
2. `ratings`, based on `title.ratings.csv`

These two tables connect through `tconst`, and they support useful analysis with filtering, sorting, grouping, averages, and joins.

A stronger three-table option is:

1. `titles`, based on `title.basics.csv`
2. `ratings`, based on `title.ratings.csv`
3. `principals`, based on `title.principals.csv`

This adds cast/crew role analysis, but it makes the database larger and more complex.

## Possible Analysis Questions

1. Which title types have the highest average ratings?
2. Which genres appear most often in the dataset?
3. Which highly rated titles have the largest number of votes?
4. Do movies, TV episodes, and shorts have different average runtimes?
5. Which cast/crew categories appear most often in the principals table?

## Notes For Schema Design

SQLite data types to consider:
- IDs such as `tconst` and `nconst`: `TEXT`
- names and titles: `TEXT`
- years: `INTEGER`
- flags like `isAdult`: `INTEGER`
- ratings: `REAL`
- vote counts and runtimes: `INTEGER`

Some fields contain comma-separated values, especially `genres`, `directors`, `writers`, `primaryProfession`, and `knownForTitles`. Those can be kept as `TEXT` for this project, but they are not ideal for advanced relational design.
