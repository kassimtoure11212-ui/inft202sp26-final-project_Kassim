import math
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "final.db"

app = Flask(__name__)


def query_db(sql, params=()):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(sql, params).fetchall()
    con.close()
    return [dict(row) for row in rows]


def query_one(sql, params=()):
    rows = query_db(sql, params)
    return rows[0] if rows else {}


def read_text(path):
    return (BASE_DIR / path).read_text(encoding="utf-8").strip()


def read_sql(path):
    return read_text(path).rstrip(";")


@app.route("/")
def index():
    stats = {
        "titles": query_one("SELECT COUNT(*) AS value FROM titles")["value"],
        "ratings": query_one("SELECT COUNT(*) AS value FROM ratings")["value"],
        "avg_rating": round(query_one("SELECT AVG(averageRating) AS value FROM ratings")["value"], 2),
        "movie_count": query_one("SELECT COUNT(*) AS value FROM titles WHERE titleType = 'movie'")["value"],
    }

    title_type_counts = query_db(
        """
        SELECT titleType AS label, COUNT(*) AS value
        FROM titles
        GROUP BY titleType
        ORDER BY value DESC
        LIMIT 8
        """
    )

    average_ratings = query_db(
        """
        SELECT titles.titleType AS label, ROUND(AVG(ratings.averageRating), 2) AS value
        FROM titles
        JOIN ratings ON titles.tconst = ratings.tconst
        GROUP BY titles.titleType
        ORDER BY value DESC
        LIMIT 8
        """
    )

    return render_template(
        "index.html",
        stats=stats,
        title_type_counts=title_type_counts,
        average_ratings=average_ratings,
    )


@app.route("/browse")
def browse():
    page = max(request.args.get("page", 1, type=int), 1)
    q = request.args.get("q", "").strip()
    per_page = 25
    offset = (page - 1) * per_page

    where = ""
    params = []
    if q:
        where = "WHERE primaryTitle LIKE ?"
        params.append(f"%{q}%")

    total = query_one(f"SELECT COUNT(*) AS value FROM titles {where}", params)["value"]
    rows = query_db(
        f"""
        SELECT tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres
        FROM titles
        {where}
        ORDER BY primaryTitle
        LIMIT ? OFFSET ?
        """,
        params + [per_page, offset],
    )

    pages = max(math.ceil(total / per_page), 1)
    return render_template("browse.html", rows=rows, q=q, page=page, pages=pages, total=total)


@app.route("/insights")
def insights():
    runtime_rows = query_db(read_sql("discussion/discussion_1.sql"))
    genre_rows = query_db(read_sql("discussion/discussion_2.sql") + "\nLIMIT 15")

    cards = [
        {
            "question": "Which title types have the longest average runtime?",
            "explanation": read_text("discussion/discussion_1_explanation.md"),
            "rows": runtime_rows,
        },
        {
            "question": "Which genres appear most often among highly rated titles?",
            "explanation": read_text("discussion/discussion_2_explanation.md"),
            "rows": genre_rows,
        },
    ]

    return render_template("insights.html", cards=cards)


if __name__ == "__main__":
    app.run(debug=True)
