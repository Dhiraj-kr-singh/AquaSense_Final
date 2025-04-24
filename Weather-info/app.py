from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '==='  # Replace with your WeatherAPI key

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": city.title(),
                "temperature": data["current"]["temp_c"],  # Temperature in Celsius
                "description": data["current"]["condition"]["text"].title(),
                "icon": data["current"]["condition"]["icon"],  # URL for the weather icon
                "humidity": data["current"]["humidity"],  # Humidity percentage
                "wind_speed": data["current"]["wind_kph"],  # Wind speed in km/h
                "feels_like": data["current"]["feelslike_c"],  # Feels like temperature
                "precipitation": data["current"]["precip_mm"]  # Precipitation in mm
            }
        else:
            weather_data = {"error": "City not found or API issue!"}

    return render_template("index.html", weather=weather_data)
    
if __name__ == "__main__":
    app.run(debug=True)
