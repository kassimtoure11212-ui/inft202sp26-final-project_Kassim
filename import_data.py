import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "final.db"
TITLES_CSV = ROOT / "imdb_datasets" / "title.basics.csv"
RATINGS_CSV = ROOT / "imdb_datasets" / "title.ratings.csv"
BATCH_SIZE = 5000


def blank_to_none(value):
    value = (value or "").strip()
    return None if value == "" or value == r"\N" else value


def to_int(value):
    value = blank_to_none(value)
    if value is None:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def to_float(value):
    value = blank_to_none(value)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def title_genres(row):
    parts = []
    runtime_value = blank_to_none(row["runtimeMinutes"])
    if runtime_value is not None and to_int(runtime_value) is None:
        parts.append(runtime_value)

    genre_value = blank_to_none(row["genres"])
    if genre_value is not None:
        parts.append(genre_value)

    for extra in row.get(None) or []:
        extra_value = blank_to_none(extra)
        if extra_value is not None:
            parts.append(extra_value)

    return ",".join(parts) if parts else None


def import_titles(cur):
    title_ids = set()
    batch = []

    with TITLES_CSV.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title_id = blank_to_none(row["tconst"])
            title_ids.add(title_id)
            batch.append(
                (
                    title_id,
                    blank_to_none(row["titleType"]),
                    blank_to_none(row["primaryTitle"]),
                    blank_to_none(row["originalTitle"]),
                    to_int(row["isAdult"]),
                    to_int(row["startYear"]),
                    to_int(row["endYear"]),
                    to_int(row["runtimeMinutes"]),
                    title_genres(row),
                )
            )

            if len(batch) >= BATCH_SIZE:
                cur.executemany(
                    """
                    INSERT OR REPLACE INTO titles
                    (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    batch,
                )
                batch.clear()

    if batch:
        cur.executemany(
            """
            INSERT OR REPLACE INTO titles
            (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            batch,
        )

    return title_ids


def import_ratings(cur, title_ids):
    imported = 0
    skipped = 0
    batch = []

    with RATINGS_CSV.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title_id = blank_to_none(row["tconst"])
            if title_id not in title_ids:
                skipped += 1
                continue

            batch.append(
                (
                    title_id,
                    to_float(row["averageRating"]),
                    to_int(row["numVotes"]),
                )
            )
            imported += 1

            if len(batch) >= BATCH_SIZE:
                cur.executemany(
                    """
                    INSERT OR REPLACE INTO ratings
                    (tconst, averageRating, numVotes)
                    VALUES (?, ?, ?)
                    """,
                    batch,
                )
                batch.clear()

    if batch:
        cur.executemany(
            """
            INSERT OR REPLACE INTO ratings
            (tconst, averageRating, numVotes)
            VALUES (?, ?, ?)
            """,
            batch,
        )

    return imported, skipped


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("DELETE FROM ratings")
    cur.execute("DELETE FROM titles")

    title_ids = import_titles(cur)
    imported_ratings, skipped_ratings = import_ratings(cur, title_ids)
    con.commit()

    title_count = cur.execute("SELECT COUNT(*) FROM titles").fetchone()[0]
    rating_count = cur.execute("SELECT COUNT(*) FROM ratings").fetchone()[0]
    con.close()

    print(f"Imported titles: {title_count}")
    print(f"Imported ratings: {rating_count}")
    print(f"Skipped ratings without matching title: {skipped_ratings}")
    print("Done.")


if __name__ == "__main__":
    main()
