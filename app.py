from flask import Flask, render_template, request
import json

import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__)

# ✅ Define known wood types
WOOD_TYPES = [
    "Oak", "Mahogany", "Elm", "Ash", "Cherry", "Ironwood", "Ebony", "Pine", "Spruce",
    "Angelwood", "Grimewood", "Blood Oak", "Heartwood", "Pwnwood", "Inyolan Oak",
    "Moorian Hardwood", "Plumwood", "Lemonwood", "Red Oak", "Blue Pine", "Western Greenwood",
    "Maple", "Cedar", "Yew", "Osage", "Acacia"
]

def load_prices():
    with open(resource_path("prices.json")) as f:
        return json.load(f)

def load_ships():
    with open(resource_path("ships.json")) as f:
        return json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    prices = load_prices()
    ships = load_ships()
    result = None
    breakdown = None
    disclaimer = None

    # ✅ Filter only wood types for dropdown
    wood_prices = {k: v for k, v in prices.items() if k in WOOD_TYPES}

    if request.method == "POST":
        ship_name = request.form.get("ship")
        wood_type = request.form.get("wood_type")

        ship = ships.get(ship_name)
        if ship:
            total = 0
            breakdown = {}

            for material, amount in ship.items():
                # Handle wood separately using selected wood type
                if material.lower() == "wood":
                    price = prices.get(wood_type)
                    if price is None:
                        breakdown[f"{wood_type} ({amount})"] = "❌ Price not found"
                        continue
                    try:
                        cost = float(price) * amount
                        breakdown[f"{wood_type} ({amount})"] = cost
                        total += cost
                    except (TypeError, ValueError):
                        breakdown[f"{wood_type} ({amount})"] = "❌ Invalid price or amount"
                        continue

                # Handle Doubloons as flat currency
                elif material == "Doubloons":
                    breakdown[f"Doubloons ({amount})"] = amount
                    total += amount

                # Handle all other materials
                else:
                    price = prices.get(material)
                    if price is None:
                        breakdown[f"{material} ({amount})"] = "❌ Price not found"
                        continue
                    try:
                        cost = float(price) * amount
                        breakdown[f"{material} ({amount})"] = cost
                        total += cost
                    except (TypeError, ValueError):
                        breakdown[f"{material} ({amount})"] = "❌ Invalid price or amount"
                        continue

            result = f"Estimated material cost to build {ship_name}: ${total:,.2f}"
            disclaimer = (
                "Be sure to check that the amount of material needed to make your ship is accurate in the prices below. "
                "If the material requirement is inaccurate, please contact ferde0_nuneP through the Tradelands official Discord server. "
                "You may also contact ferde0_nuneP if you want anything to be added to the calculator, find a bug, or have a suggestion on how to improve it."
            )

    return render_template(
        "index.html",
        prices=wood_prices,
        ships=ships.keys(),
        result=result,
        breakdown=breakdown,
        disclaimer=disclaimer
    )

import webbrowser

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)  # Turn this off later for production