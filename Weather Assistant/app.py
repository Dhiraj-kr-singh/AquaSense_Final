from flask import Flask, request, render_template, jsonify
import requests
import google.generativeai as genai

app = Flask(__name__)

# ---- API KEYS ----
WEATHER_API_KEY = "FV9XNA5ZKKPZJR5ZZZJLXTGUU"
GEMINI_API_KEY = "AIzaSyB-oTIBdnBfY6H7P9GVFDWGhNKvByHH-hU"

# ---- SETUP GEMINI ----
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def fetch_weather(location="bangalore"):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def smart_recommendation_engine(user_question, location="bangalore"):
    weather_data = fetch_weather(location)
    if not weather_data:
        return "❌ Unable to fetch weather data. Try again later."

    emoji_map = {
        "Rain": "🌧️", "Showers": "🌦️", "Clear": "☀️",
        "Partly Cloudy": "⛅", "Overcast": "☁️",
        "Snow": "❄️", "Thunderstorm": "⛈️", "Fog": "🌫️"
    }

    summary = ""
    for day in weather_data['days'][:3]:
        condition = day['conditions']
        emoji = next((e for k, e in emoji_map.items() if k.lower() in condition.lower()), "")
        summary += (
            f"📅 {day['datetime']}: {condition} {emoji}, "
            f"Temp: {day['temp']}°C, "
            f"Rain Prob: {day['precipprob']}%, UV: {day['uvindex']}\n"
        )

    prompt = f"""
You are a smart assistant giving lifestyle advice based on weather and user input.

User's location: {location}
User asked: "{user_question}"

Here's the 3-day weather forecast:
{summary}

Based on this:
1. Suggest suitable clothing.
2. Recommend food/drinks.
3. Share useful travel tips.
Be helpful, friendly, and use emojis.
"""

    response = model.generate_content(prompt)
    return response.text.strip()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommendation", methods=["POST"])
def recommendation():
    location = request.form.get("location") or "bangalore"
    question = request.form.get("question") or "What's the best way to stay cool this week?"

    reply = smart_recommendation_engine(question, location)
    return render_template("index.html", location=location, question=question, reply=reply)


if __name__ == "__main__":
    app.run(debug=True)
