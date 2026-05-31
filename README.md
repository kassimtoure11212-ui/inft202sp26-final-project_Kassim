# IMDb SQLite Database Project

## Project Overview

This project explores an IMDb dataset downloaded from Kaggle. The dataset includes title information and rating information for movies, TV episodes, shorts, videos, TV series, and other IMDb title types.

I used SQLite for the database because Docker was not working on this computer. The final database file is `final.db`, and the SQL queries were written and tested in Beekeeper Studio.

## Dataset

Dataset name: IMDb Datasets

Source: Kaggle

Files used:
- `imdb_datasets/title.basics.csv`
- `imdb_datasets/title.ratings.csv`

The full download also included other IMDb files, but this project focuses on two related tables so the schema and queries stay clear.

## Data Exploration

During exploration, I looked at the CSV headers, row counts, sample rows, possible ID columns, and missing values. Each selected CSV had 1,000,000 rows.

The `title.basics.csv` file describes IMDb titles, including title type, title name, year, runtime, and genres. The `title.ratings.csv` file describes ratings for titles, including average rating and number of votes.

## Schema

The database has two tables:

### `titles`

One row represents one IMDb title.

Important columns:
- `tconst`: title ID and primary key
- `titleType`: type of title, such as movie, tvEpisode, short, or tvSeries
- `primaryTitle`: main title name
- `originalTitle`: original title name
- `isAdult`: adult-content flag
- `startYear`: release or start year
- `endYear`: end year for series
- `runtimeMinutes`: runtime in minutes
- `genres`: genre text

### `ratings`

One row represents one rating summary for a title.

Important columns:
- `tconst`: title ID, primary key, and foreign key to `titles.tconst`
- `averageRating`: IMDb average rating
- `numVotes`: number of votes

Relationship:

```text
titles.tconst = ratings.tconst
```

## Guided Queries

The six guided SQL queries are saved in the `queries/` folder.

1. `query_1.sql`: Finds the 10 highly rated titles with the most votes.
2. `query_2.sql`: Counts how many titles there are for each title type.
3. `query_3.sql`: Calculates the average rating for each title type.
4. `query_4.sql`: Shows average rating by title type only for groups with more than 1,000 rated titles.
5. `query_5.sql`: Joins titles and ratings to show title name, title type, rating, and votes for the most-voted titles.
6. `query_6.sql`: Calculates average votes and rated-title counts for each title type.

## Discussion Queries

The two discussion queries are saved in the `discussion/` folder.

### Discussion Query 1

Question: Which title types have the longest average runtime?

Explanation:

The results show that movies have the longest average runtime, at about 89 minutes. TV specials, TV mini-series, and video games also have longer average runtimes, while shorts and TV shorts are much shorter. This makes sense because movies and specials are usually made as longer productions, while shorts are meant to be quick to watch.

### Discussion Query 2

Question: Which genres appear most often among highly rated titles?

Explanation:

The query shows that Comedy has the most highly rated titles, with 1,438 titles rated 8.0 or higher. Drama and Documentary also appear many times in the results. This tells me that many of the highest-rated titles in this IMDb dataset are comedies, dramas, or documentaries.

## Web Dashboard

The Flask web app has three pages:

- Dashboard: summary stats and charts
- Browse: searchable title browser
- Insights: discussion query results and explanations

Main files:
- `app.py`
- `run_app.py`
- `templates/base.html`
- `templates/index.html`
- `templates/browse.html`
- `templates/insights.html`

## How To Run The App

Open PowerShell in this project folder:

```powershell
cd C:\Users\Guttman\Documents\GitHub\inft202sp26-final-project_Kassim
```

Run the app:

```powershell
& 'C:\Users\Guttman\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' run_app.py
```

Open this URL in a browser:

```text
http://127.0.0.1:5000
```

## SQLite Setup

The project uses:

- Database type: SQLite
- Database file: `final.db`
- SQL tool: Beekeeper Studio

The `final.db` file is not included in GitHub because `.gitignore` excludes `*.db`.

## What I Built

In this project, I designed a relational database schema, imported real IMDb data, wrote SQL queries using filtering, sorting, grouping, aggregate functions, `HAVING`, and joins, and built a Flask dashboard connected to a SQLite database.
