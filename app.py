from flask import Flask, render_template, request, jsonify
import requests
import google.generativeai as genai
import os
import logging
import markdown
from config import GENAI_API_KEY, ALPHA_VANTAGE_API_KEY

app = Flask(__name__)

genai.configure(api_key=GENAI_API_KEY)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Memory store for conversation context
conversation_memory = {}

# Function to fetch stock data using Alpha Vantage API
def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "Time Series (5min)" in data:
            return {
                "success": True,
                "symbol": symbol,
                "data": data["Time Series (5min)"]
            }
        return {
            "success": False,
            "message": "Invalid stock symbol or data unavailable."
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"API error: {e}")
        return {
            "success": False,
            "message": "Unable to fetch stock data."
        }

# Function to query Gemini API
def query_gemini(message, context=None):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        context_prompt = """
        You are a stock-focused chatbot. Fetch stock data using the Alpha Vantage API and explain it in a user-friendly way. You don't need to use the API only if the user asks about information other than financials.
        Format responses with appropriate markdown such as **bold** for important terms and *italics* for emphasis.
        Maintain a logical conversation based on the user's history.
        """
        formatted_context = "\n".join([f"User: {entry['user']}\nAI: {entry['ai']}" for entry in context]) if context else ""
        response = model.generate_content(
            f"{context_prompt}\n{formatted_context}\nUser: {message}"
        )
        return markdown.markdown(response.text)
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return markdown.markdown("Error processing your request with the AI.")

@app.route('/')
def chat():
    return render_template('index.html')

@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    user_message = request.json.get("message")
    session_id = request.json.get("session_id")  # Expect a session ID from the frontend

    if not user_message or not session_id:
        return jsonify({"response": "Please provide a message and session ID."})

    # Initialize memory for this session if it doesn't exist
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []

    try:
        # Retrieve conversation history
        context = conversation_memory[session_id]

        # Ask Gemini for a response
        gemini_reply = query_gemini(user_message, context)

        # If the message indicates a stock request, fetch data
        if "[getStockData]" in gemini_reply:
            stock_symbol = gemini_reply.split()[1].strip()
            stock_data = fetch_stock_data(stock_symbol)

            if stock_data["success"]:
                gemini_reply = query_gemini(f"Here is the stock data for {stock_symbol}:", context=stock_data["data"])
            else:
                gemini_reply = query_gemini(f"The stock data could not be fetched: {stock_data['message']}")

        # Update conversation memory
        conversation_memory[session_id].append({"user": user_message, "ai": gemini_reply})

        return jsonify({"response": gemini_reply})
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"response": markdown.markdown("An unexpected error occurred. Please try again later.")})

if __name__ == '__main__':
    if not GENAI_API_KEY or not ALPHA_VANTAGE_API_KEY:
        logger.error("API keys for Gemini and Alpha Vantage are required.")
        exit(1)

    logger.info("Starting Flask application.")
    app.run(debug=True)
