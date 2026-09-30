from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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


    # Base demand
    predictions = {
        "Veg Burger": 45,
        "Veg Sandwich": 35,
        "Masala Dosa": 55,
        "Veg Fried Rice": 65,
        "Idli": 40,
        "Paneer Roll": 30
    }


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


    # Prevent negative demand
    for item in predictions:
        predictions[item] = max(0, predictions[item])


    # Suggested preparation
    preparation = {}

    for item, demand in predictions.items():
        preparation[item] = demand + 5


    return jsonify({

        "success": True,

        "input": {
            "day": day,
            "weather": weather,
            "holiday": holiday,
            "college_event": college_event
        },

        "predictions": predictions,

        "preparation": preparation

    })


if __name__ == "__main__":
    app.run(debug=True, port=5000) 