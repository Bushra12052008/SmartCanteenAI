from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
app = Flask(__name__)
CORS(app)
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")
def save_history(record):
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as file:
                history = json.load(file)
        else:
            history = []

    except (json.JSONDecodeError, FileNotFoundError):
        history = []

    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)
@app.route("/")
def home():
    return "Smart Canteen AI Backend is running!"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    day = data.get("day", "Monday")
    weather = data.get("weather", "Sunny")
    holiday = data.get("holiday", "No")
    college_event = data.get("college_event", "No")


    # Previous sales / historical average
    previous_sales = {
        "Veg Burger": 45,
        "Veg Sandwich": 35,
        "Masala Dosa": 55,
        "Veg Fried Rice": 65,
        "Idli": 40,
        "Paneer Roll": 30
    }


    # Start prediction from previous sales
    predictions = previous_sales.copy()


    # Day effect
    if day == "Friday":

        for item in predictions:
            predictions[item] += 5

    elif day == "Saturday":

        for item in predictions:
            predictions[item] -= 5


    # Weather effect
    if weather == "Rainy":

        predictions["Masala Dosa"] += 10
        predictions["Idli"] += 10
        predictions["Veg Burger"] -= 5

    elif weather == "Sunny":

        predictions["Veg Burger"] += 5
        predictions["Veg Sandwich"] += 5


    # Holiday effect
    if holiday == "Yes":

        for item in predictions:
            predictions[item] -= 10


    # College event effect
    if college_event == "Yes":

        for item in predictions:
            predictions[item] += 15


    # Prevent negative predictions
    for item in predictions:

        predictions[item] = max(0, predictions[item])
# Suggested preparation
    preparation = {}

    for item, demand in predictions.items():
        preparation[item] = demand + 5

# Save prediction to history
    history_record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input": {
            "day": day,
            "weather": weather,
            "holiday": holiday,
            "college_event": college_event
        },
        "predictions": predictions,
        "preparation": preparation
    }

    save_history(history_record)
    return jsonify({

        "success": True,

        "input": {
            "day": day,
            "weather": weather,
            "holiday": holiday,
            "college_event": college_event
        },

        "previous_sales": previous_sales,

        "predictions": predictions,

        "preparation": preparation

    })
@app.route("/history", methods=["GET"])
def get_history():

    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as file:
                history = json.load(file)
        else:
            history = []

        return jsonify({
            "success": True,
            "history": history
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

    

    