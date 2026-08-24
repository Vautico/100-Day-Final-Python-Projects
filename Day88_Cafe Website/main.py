import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

DB_PATH = Path(__file__).with_name("cafes.db")


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def checkbox_value(name):
    return 1 if request.form.get(name) == "on" else 0


@app.route("/")
def home():
    connection = get_db_connection()
    cafes = connection.execute("SELECT * FROM cafe ORDER BY id DESC").fetchall()
    connection.close()
    return render_template("index.html", cafes=cafes)


@app.route("/cafes/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        name = request.form["name"].strip()
        map_url = request.form["map_url"].strip()
        img_url = request.form["img_url"].strip()
        location = request.form["location"].strip()
        seats = request.form.get("seats", "").strip()
        coffee_price = request.form.get("coffee_price", "").strip()

        if not all([name, map_url, img_url, location]):
            flash("Name, map URL, image URL, and location are required.")
            return render_template("add.html")

        connection = get_db_connection()
        connection.execute(
            """
            INSERT INTO cafe (
                name,
                map_url,
                img_url,
                location,
                has_sockets,
                has_toilet,
                has_wifi,
                can_take_calls,
                seats,
                coffee_price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                map_url,
                img_url,
                location,
                checkbox_value("has_sockets"),
                checkbox_value("has_toilet"),
                checkbox_value("has_wifi"),
                checkbox_value("can_take_calls"),
                seats,
                coffee_price,
            ),
        )
        connection.commit()
        connection.close()
        flash(f"{name} was added.")
        return redirect(url_for("home"))

    return render_template("add.html")


@app.post("/cafes/<int:cafe_id>/delete")
def delete_cafe(cafe_id):
    connection = get_db_connection()
    cafe = connection.execute("SELECT name FROM cafe WHERE id = ?", (cafe_id,)).fetchone()

    if cafe is None:
        flash("That cafe was not found.")
    else:
        connection.execute("DELETE FROM cafe WHERE id = ?", (cafe_id,))
        connection.commit()
        flash(f"{cafe['name']} was removed.")

    connection.close()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
