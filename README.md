# Crypto News Bot

![Untitled](https://github.com/user-attachments/assets/2b933244-bc8e-4eea-ae54-dcbd7e890976)


[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## Overview

This Python bot is designed to monitor news related to cryptocurrency markets, analyze incoming articles for relevance and potential impact, and provide notifications.

The bot fetches news from configured API sources, analyzes articles for:
*   **Sentiment:** Positive, Negative, or Neutral market feeling.
*   **Importance:** Low, Medium, High, or Critical potential impact based on keywords.
*   **Related Coins:** Identifies which tracked cryptocurrencies are mentioned.

It then filters these articles based on user-defined importance and sentiment thresholds before displaying them in the console and triggering optional sound alerts.

## Key Features

*   **News Fetching:** Retrieves news articles from the NewsAPI based on configurable keywords.
*   **Sentiment Analysis:** Uses `textblob` to determine the sentiment of news articles.
*   **Importance Scoring:** Assigns an importance score and level based on predefined keywords and thresholds in the news content.
*   **Coin Identification:** Detects mentions of tracked cryptocurrencies (symbols and names) within articles.
*   **Configurable Filtering:** Displays news only if it meets minimum importance criteria and specific sentiment rules (e.g., show Positive/Negative, or only Neutral if High/Critical importance).
*   **Duplicate Prevention:** Keeps track of processed news URLs (`seen_news.json`) to avoid repeat notifications.
*   **Sound Notifications:** Plays a `.wav` sound alert for new, filtered news (optional, uses `winsound` on Windows or `playsound` elsewhere).
*   **Console Output:** Clean console output showing only filtered, important news summaries.
*   **Detailed Logging:** Comprehensive logging of all activities, information, warnings, and errors to `crypto_news_bot.log`.
*   **Local Timestamps:** Displays news publication times in the user's local timezone.
*   **Environment Variable Support:** Securely load API keys using a `.env` file.

## Project Structure
crypto-news-bot/
├── main.py # Main execution script orchestrating the bot
├── config.py # Configuration settings (API keys, keywords, filters, etc.)
├── news_fetcher.py # Module for fetching news from the API
├── news_analyzer.py # Module for analyzing news articles (sentiment, importance, coins)
├── notifier.py # Module for handling sound notifications
├── persistence.py # Module for managing the history of seen news articles
├── requirements.txt # List of Python package dependencies
├── .env.example # Example file for environment variables (API Key)
├── seen_news.json # Stores URLs of processed news (auto-generated)
├── crypto_news_bot.log # Log file for detailed bot activity (auto-generated)
└── notification.wav # Optional sound file for notifications


## Requirements

*   Python 3.7+
*   pip (Python package installer)
*   A NewsAPI API Key ([Get one for free here](https://newsapi.org/))
*   *(Optional)* For sound notifications on Linux, you might need `gstreamer` or related libraries for `playsound` (`sudo apt install python3-gst-1.0` on Debian/Ubuntu). Windows usually uses `winsound` (included) or `playsound` may work directly.

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/crypto-news-bot.git
    cd crypto-news-bot
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API Key:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Open the `.env` file in a text editor.
    *   Replace `YOUR_NEWS_API_KEY_HERE` with your actual NewsAPI key obtained from [newsapi.org](https://newsapi.org/).
        ```.env
        NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```
    *   *(Alternative)* You can skip the `.env` file and directly edit the `NEWS_API_KEY` variable in `config.py`, but using `.env` is more secure and standard practice.

5.  **Configure the Bot (Review `config.py`):**
    *   **`NEWS_QUERY`**: Adjust the keywords used to fetch news. **Important:** NewsAPI has limits on query length (around 500 characters). If you get `400 Bad Request` errors, you need to shorten this query.
    *   **`TRACKED_COINS`**: Add or remove cryptocurrencies you want the bot to specifically identify. Use lowercase symbols and names.
    *   **`IMPORTANCE_KEYWORDS`**: Modify keywords and their assigned points (1, 2, or 3) to fine-tune how importance is calculated.
    *   **`IMPORTANCE_THRESHOLDS`**: Adjust the score thresholds required for "Medium", "High", and "Critical" importance levels.
    *   **`MIN_DISPLAY_IMPORTANCE_LEVEL`**: Set the *minimum* importance level (e.g., "Medium", "High") a news article must have to be considered for display.
    *   **Filtering Logic (in `main.py`)**: The current logic displays news if it meets `MIN_DISPLAY_IMPORTANCE_LEVEL` AND (is Positive/Negative OR is Neutral but meets "High" importance). You can adjust this logic in `main.py`'s `check_and_process_news` function if needed.
    *   **`CHECK_INTERVAL_SECONDS`**: Change how often (in seconds) the bot checks for new news. Be mindful of API rate limits (free plans are often limited). 60 seconds is aggressive for free plans; 300 (5 minutes) is safer. **For scalping, a faster interval is desired, but likely requires a paid API plan or a streaming API.**
    *   **`SOUND_NOTIFICATION_ENABLED`**: Set to `False` to disable sound alerts.
    *   **`NOTIFICATION_SOUND_FILE`**: Change the name of the `.wav` file used for alerts. Ensure the file exists in the project directory.

## How to Run

Ensure your virtual environment is activated. Then run:

```bash
python main.py
```
The bot will start checking for news at the specified interval. Filtered news articles will be printed to the console. Detailed logs can be found in crypto_news_bot.log.

Press CTRL+C to stop the bot gracefully.
