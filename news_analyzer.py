from textblob import TextBlob
import logging
import re
from typing import Dict, List, Tuple, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsAnalyzer:

    def __init__(self, tracked_coins: Dict[str, str], importance_keywords: Dict[str, int], importance_thresholds: Dict[str, int]):
        self.tracked_coins = {k.lower(): v.lower() for k, v in tracked_coins.items()}
        self.importance_keywords = {k.lower(): v for k, v in importance_keywords.items()}
        self.importance_thresholds = sorted(importance_thresholds.items(), key=lambda item: item[1], reverse=True)
        logging.info("NewsAnalyzer initialized.")
        logging.debug(f"Tracked coins: {list(self.tracked_coins.keys())}")
        logging.debug(f"Importance keywords: {self.importance_keywords}")
        logging.debug(f"Importance thresholds: {self.importance_thresholds}")


    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        if not text:
            return "Neutral", 0.0

        try:
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity

            if polarity > 0.1:
                sentiment = "Positive"
            elif polarity < -0.1:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            return sentiment, round(polarity, 3)
        except Exception as e:
            logging.error(f"Error during sentiment analysis: {e}")
            return "Error", 0.0

    def identify_coins(self, text: str) -> List[str]:
        if not text:
            return ["MARKET_WIDE"]

        found_coins = set()
        text_lower = text.lower()

        for symbol, name in self.tracked_coins.items():
            if re.search(r'\b' + re.escape(symbol) + r'\b', text_lower):
                found_coins.add(symbol.upper())
            if re.search(r'\b' + re.escape(name) + r'\b', text_lower):
                found_coins.add(symbol.upper())

        if not found_coins:
            return ["MARKET_WIDE"]
        else:
            return sorted(list(found_coins))

    def analyze_importance(self, text: str) -> Tuple[str, int]:
        if not text:
            return "Low", 0

        total_score = 0
        text_lower = text.lower()
        found_keywords = []

        for keyword, score in self.importance_keywords.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                total_score += score
                found_keywords.append(keyword)

        importance_level = "Low"
        for level, threshold in self.importance_thresholds:
            if total_score >= threshold:
                importance_level = level
                break

        logging.debug(f"Importance analysis complete. Score: {total_score}, Level: {importance_level}, Keywords: {found_keywords}")
        return importance_level, total_score

    def analyze_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        title = article.get('title', '')
        description = article.get('description', '')
        content = article.get('content', '')

        text_to_analyze = f"{title}. {description or ''}"
        if content:
             text_to_analyze += f". {content[:250]}"

        sentiment, sentiment_score = self.analyze_sentiment(text_to_analyze)
        related_coins = self.identify_coins(text_to_analyze)
        importance, importance_score = self.analyze_importance(text_to_analyze)

        analysis_results = {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "related_coins": related_coins,
            "importance": importance,
            "importance_score": importance_score,
        }
        logging.debug(f"Article analysis complete: '{title[:50]}...' -> {analysis_results}")
        return analysis_results