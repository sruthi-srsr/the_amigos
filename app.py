from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)
FILE = "data.json"

def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- CREATE ACCOUNT ----------------
@app.route("/create", methods=["POST"])
def create():
    data = load_data()
    acc_no = request.form["acc_no"]
    name = request.form["name"]
    pin = request.form["pin"]

    if acc_no not in data:
        data[acc_no] = {
            "name": name,
            "pin": pin,
            "balance": 0,
            "transactions": []
        }
        save_data(data)

    return redirect("/")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = load_data()
    acc_no = request.form["acc_no"]
    pin = request.form["pin"]

    if acc_no in data and data[acc_no]["pin"] == pin:
        return redirect(f"/dashboard/{acc_no}")
    return "Invalid login!"

# ---------------- DASHBOARD ----------------
@app.route("/dashboard/<acc_no>")
def dashboard(acc_no):
    data = load_data()
    user = data[acc_no]
    return render_template("dashboard.html", acc_no=acc_no, user=user)

# ---------------- DEPOSIT ----------------
@app.route("/deposit/<acc_no>", methods=["POST"])
def deposit(acc_no):
    data = load_data()
    amount = float(request.form["amount"])

    data[acc_no]["balance"] += amount
    data[acc_no]["transactions"].append({"type": "Credit", "amount": amount})

    save_data(data)
    return redirect(f"/dashboard/{acc_no}")

# ---------------- WITHDRAW ----------------
@app.route("/withdraw/<acc_no>", methods=["POST"])
def withdraw(acc_no):
    data = load_data()
    amount = float(request.form["amount"])

    if amount <= data[acc_no]["balance"]:
        data[acc_no]["balance"] -= amount
        data[acc_no]["transactions"].append({"type": "Debit", "amount": amount})

    save_data(data)
    return redirect(f"/dashboard/{acc_no}")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)