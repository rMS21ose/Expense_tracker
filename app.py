from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import date

app = Flask(__name__)

def load_data():
    try:
        with open("expenses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open("expenses.json", "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    expenses = load_data()

    if request.method == "POST":
        new_expense = {
            "amount": float(request.form["amount"]),
            "category": request.form["category"],
            "date": request.form["date"] or str(date.today()),
            "description": request.form["description"]
        }
        expenses.append(new_expense)
        save_data(expenses)
        return redirect(url_for("index"))

    # Calculate totals by category
    totals = {}
    for e in expenses:
        cat = e["category"]
        totals[cat] = totals.get(cat, 0) + e["amount"]

    return render_template("index.html", expenses=expenses, totals=totals)

if __name__ == "__main__":
    app.run(debug=True)
