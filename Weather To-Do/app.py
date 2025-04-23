from flask import Flask, jsonify, render_template
import requests
import google.generativeai as genai
import json

app = Flask(__name__)

# 🔑 API KEYS
VISUAL_CROSSING_API_KEY = "FV9XNA5ZKKPZJR5ZZZJLXTGUU"
GEMINI_API_KEY = "AIzaSyB-oTIBdnBfY6H7P9GVFDWGhNKvByHH-hU"

# ⚙️ Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather-suggestion")
def weather_suggestion():
    try:
        # 1. ✅ Fetch weather data
        LOCATION = "bangalore"
        UNIT_GROUP = "metric"
        URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LOCATION}?unitGroup={UNIT_GROUP}&key={VISUAL_CROSSING_API_KEY}&contentType=json"

        response = requests.get(URL)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch weather data"}), 500

        data = response.json()
        today = data['days'][0]

        # 2. 💾 Save as Gemini-friendly JSON
        weather_info = {
            "date": today.get("datetime"),
            "temp": today.get("temp"),
            "tempmax": today.get("tempmax"),
            "tempmin": today.get("tempmin"),
            "feelslike": today.get("feelslike"),
            "humidity": today.get("humidity"),
            "dew": today.get("dew"),
            "precip": today.get("precip"),
            "precipprob": today.get("precipprob"),
            "windgust": today.get("windgust"),
            "windspeed": today.get("windspeed"),
            "winddir": today.get("winddir"),
            "pressure": today.get("pressure"),
            "cloudcover": today.get("cloudcover"),
            "visibility": today.get("visibility"),
            "solarradiation": today.get("solarradiation"),
            "solarenergy": today.get("solarenergy"),
            "uvindex": today.get("uvindex"),
            "conditions": today.get("conditions"),
            "description": today.get("description"),
            "sunrise": today.get("sunrise"),
            "sunset": today.get("sunset"),
            "moonphase": today.get("moonphase")
        }

        # Save JSON file (overwrite every time)
        with open("weather.json", "w") as f:
            json.dump(weather_info, f, indent=2)

        # 3. 🧠 Generate Gemini suggestion
        prompt = (
            f"You are a friendly weather assistant. Use this JSON data to create a short, fun, "
            f"engaging weather insight for the day. Include: date, max temp, conditions, UV index, "
            f"wind, rain chance. Format it naturally and make it engaging with emojis.\n\n"
            f"{json.dumps(weather_info, indent=2)}"
        )

        result = model.generate_content(prompt)
        suggestion = result.text.strip()

        # 4. 📤 Return response
        return jsonify({"suggestion": suggestion})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == "__main__":
    app.run(debug=True)
