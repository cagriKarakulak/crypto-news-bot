import requests
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsFetcher:

    def __init__(self, api_key: str, endpoint: str):
        if not api_key or api_key == "YOUR_NEWS_API_KEY_HERE":
            raise ValueError("API Key (NEWS_API_KEY) is not set in config.py or .env file.")
        self.api_key = api_key
        self.endpoint = endpoint
        self.session = requests.Session()
        self.session.headers.update({'X-Api-Key': self.api_key})
        logging.info("NewsFetcher initialized.")

    def fetch_news(self, query: str, language: str = 'en', sort_by: str = 'publishedAt', page_size: int = 20) -> Optional[List[Dict]]:
        params = {
            'q': query,
            'language': language,
            'sortBy': sort_by,
            'pageSize': min(page_size, 100),
        }
        try:
            logging.debug(f"Sending request to News API: {self.endpoint} Params: {params}")
            response = self.session.get(self.endpoint, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            if data.get("status") == "ok":
                articles = data.get("articles", [])
                logging.info(f"Successfully fetched {len(articles)} articles (Query: '{query[:50]}...').")
                valid_articles = [
                    article for article in articles
                    if article.get('title') and article.get('url')
                ]
                if len(valid_articles) != len(articles):
                    logging.warning(f"{len(articles) - len(valid_articles)} articles were skipped due to missing 'title' or 'url'.")
                return valid_articles
            else:
                error_message = data.get("message", "Unknown API error.")
                logging.error(f"Error response from News API: {error_message} (Code: {data.get('code')})")
                return None

        except requests.exceptions.RequestException as e:
            logging.error(f"Error connecting to News API: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while fetching news: {e}")
            return None

    def close_session(self):
        self.session.close()
        logging.info("Requests session closed.")