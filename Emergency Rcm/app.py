from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API key
genai.configure(api_key="+++")

# Sample rainfall data for the last month (you can dynamically input data if needed)
rainfall_data = [
    {"date": "2025-03-24", "precip": 0.004},
    {"date": "2025-03-25", "precip": 0.0},
    {"date": "2025-03-26", "precip": 0.0},
    {"date": "2025-03-27", "precip": 0.0},
    {"date": "2025-03-28", "precip": 0.0},
    {"date": "2025-03-29", "precip": 0.0},
    {"date": "2025-03-30", "precip": 0.0},
    {"date": "2025-03-31", "precip": 0.0},
    {"date": "2025-04-01", "precip": 0.0},
    {"date": "2025-04-02", "precip": 0.0},
    {"date": "2025-04-03", "precip": 0.0},
    {"date": "2025-04-04", "precip": 0.0},
    {"date": "2025-04-05", "precip": 0.0},
    {"date": "2025-04-06", "precip": 0.0},
    {"date": "2025-04-07", "precip": 0.0},
    {"date": "2025-04-08", "precip": 0.0},
    {"date": "2025-04-09", "precip": 0.0},
    {"date": "2025-04-10", "precip": 0.0},
    {"date": "2025-04-11", "precip": 0.0},
    {"date": "2025-04-12", "precip": 0.0},
    {"date": "2025-04-13", "precip": 0.0},
    {"date": "2025-04-14", "precip": 0.0},
    {"date": "2025-04-15", "precip": 0.0},
    {"date": "2025-04-16", "precip": 0.0},
    {"date": "2025-04-17", "precip": 0.0},
    {"date": "2025-04-18", "precip": 0.0},
    {"date": "2025-04-19", "precip": 0.0},
    {"date": "2025-04-20", "precip": 0.0},
    {"date": "2025-04-21", "precip": 0.0},
    {"date": "2025-04-22", "precip": 0.0},
    {"date": "2025-04-23", "precip": 0.0},
    {"date": "2025-04-24", "precip": 0.0}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Fetch rainfall data from the form or use the predefined data
        data = rainfall_data
        

        prompt = f"""
        Analyze this rainfall data for the past month:
        {data}

        Please answer with "yes", "no", "high", or "low" only:
        - Drought risk:
        - Heatwave chances:
        - Water shortage warnings:
        - Emergency alert chances:
        - Flood risk:
        - Agricultural impact:
        - Forest fire risk:
        """
        
        # Generate prediction with Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Get the output text from Gemini API
        result = response.text
        return render_template("index.html", result=result)

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
