# Flask AI Stock Chat - Challenge 4

A chatbot application powered by Flask, Google Gemini AI, and Alpha Vantage API to provide users with stock information through a conversational interface. The AI can fetch stock data, explain it in a user-friendly manner, and respond to follow-up questions seamlessly.

## Features

- **Chatbot Interface**: Users interact with the AI through a clean and modern chat UI.
- **Real-Time Stock Data**: Fetches current stock data using the Alpha Vantage API.
- **AI-Powered Responses**: Google Gemini AI generates insightful and markdown-styled responses.
- **Markdown Support**: Proper rendering of **bold**, *italics*, lists, and more.
- **Error Handling**: Friendly fallback messages for API errors or invalid inputs.

## Technologies Used

- **Backend**:
  - Flask (Python web framework)
  - Google Gemini AI (Generative AI for responses)
  - Alpha Vantage API (Stock data provider)
- **Frontend**:
  - HTML, CSS, and Bootstrap (UI)
  - JavaScript (Chat functionality and interactivity)
- **Additional Tools**:
  - `markdown` (for rendering AI responses)
  - Logging for debugging and monitoring

## Installation

### Prerequisites
- Python 3.8 or higher
- Alpha Vantage API key
- Google Gemini API key

### Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys**:
   Create a `config.py` file in the root directory with the following content:
   ```python
   GENAI_API_KEY = "your_google_gemini_api_key"
   ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_api_key"
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the App**:
   Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

1. Enter your query in the chat box (e.g., "Tell me about Apple stock").
2. The AI will process your request and fetch real-time stock data from the Alpha Vantage API.
3. View the formatted and user-friendly response in the chat interface.
4. Continue asking follow-up questions or explore other stocks.

## Project Structure

```
├── app.py             # Main Flask application
├── templates/
│   └── index.html     # Frontend template
├── static/            # CSS, JavaScript, and images
├── requirements.txt   # Python dependencies
├── config.py          # API keys (user-generated)
└── README.md          # Project documentation
```

## Example Query

**User**: "Tell me about AAPL"

**AI**:
```
**Apple Inc. (AAPL)**
**Last Refreshed**: 2024-12-07 16:00:00
- **Open**: $150.00
- **High**: $155.00
- **Low**: $148.00
- **Price**: $154.00
- **Volume**: 1,200,000
- **Change**: $+4.00 (+2.67%)

Apple Inc. is a multinational technology company known for its iconic products like the iPhone, iPad, and MacBook. This information is for reference and not financial advice.
```

## Known Limitations

- API rate limits may affect the availability of real-time data.
- Only supports stocks available through the Alpha Vantage API.


## Contact

For any questions or feedback, please contact [finn.waehlt@whu.edu].

