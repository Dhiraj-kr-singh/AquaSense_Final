from flask import Flask, render_template
import requests

app = Flask(__name__)

# Your GNews API Key
API_KEY = "+++"
NEWS_URL = f"https://gnews.io/api/v4/top-headlines?lang=en&topic=weather&token={API_KEY}"

def get_weather_news():
    try:
        response = requests.get(NEWS_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        news_data = response.json()
        return news_data['articles']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather news: {e}")
        return []

@app.route("/")
def home():
    news_articles = get_weather_news()
    return render_template("index.html", articles=news_articles)

if __name__ == "__main__":
    app.run(debug=True)
    
