import time
import logging
import sys
import schedule
from datetime import datetime
import pytz
from tzlocal import get_localzone

import config
from news_fetcher import NewsFetcher
from news_analyzer import NewsAnalyzer
from notifier import Notifier
from persistence import SeenNewsManager

log_format = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
log_formatter = logging.Formatter(log_format)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

for handler in logger.handlers[:]:
    logger.removeHandler(handler)

file_handler = logging.FileHandler("crypto_news_bot.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

try:
    import colorama
    colorama.init(autoreset=True)
    COLOR_POSITIVE = colorama.Fore.GREEN
    COLOR_NEGATIVE = colorama.Fore.RED
    COLOR_NEUTRAL = colorama.Fore.YELLOW
    COLOR_IMPORTANT = colorama.Fore.MAGENTA
    COLOR_RESET = ""
except ImportError:
    logging.warning("Colorama library not found. Colored console output is disabled.")
    COLOR_POSITIVE = COLOR_NEGATIVE = COLOR_NEUTRAL = COLOR_IMPORTANT = COLOR_RESET = ""


class CryptoNewsBot:

    def __init__(self):
        logging.info("Initializing Crypto News Bot...")
        self.is_first_run = True

        try:
            self.news_fetcher = NewsFetcher(config.NEWS_API_KEY, config.NEWS_API_ENDPOINT)
            self.seen_news_manager = SeenNewsManager(config.SEEN_NEWS_FILE)
            self.news_analyzer = NewsAnalyzer(
                config.TRACKED_COINS,
                config.IMPORTANCE_KEYWORDS,
                config.IMPORTANCE_THRESHOLDS
            )
            self.notifier = Notifier(
                config.NOTIFICATION_SOUND_FILE,
                config.SOUND_NOTIFICATION_ENABLED
            )
            self.check_interval = config.CHECK_INTERVAL_SECONDS

            self.min_importance_numeric = config.IMPORTANCE_ORDER.get(
                config.MIN_DISPLAY_IMPORTANCE_LEVEL, -1
            )

            if self.min_importance_numeric == -1 or config.MIN_DISPLAY_IMPORTANCE_LEVEL not in config.IMPORTANCE_ORDER:
                default_level = "Medium"
                logging.warning(
                    f"MIN_DISPLAY_IMPORTANCE_LEVEL ('{config.MIN_DISPLAY_IMPORTANCE_LEVEL}') in config.py "
                    f"is invalid or not defined in IMPORTANCE_ORDER. "
                    f"Setting to '{default_level}'."
                )
                config.MIN_DISPLAY_IMPORTANCE_LEVEL = default_level
                self.min_importance_numeric = config.IMPORTANCE_ORDER[default_level]

            logging.info(f"Minimum display importance level: {config.MIN_DISPLAY_IMPORTANCE_LEVEL} (Order >= {self.min_importance_numeric})")
            logging.info("All components initialized successfully.")
            logging.info(f"News check interval: {self.check_interval} seconds.")
            logging.info(f"Initial seen news count: {self.seen_news_manager.get_seen_count()}")

        except ValueError as ve:
            logging.critical(f"Bot failed to initialize! Configuration error: {ve}")
            sys.exit(1)
        except Exception as e:
            logging.critical(f"Critical error during bot initialization: {e}", exc_info=True)
            sys.exit(1)


    def check_and_process_news(self):
        logging.info("Checking for new articles...")
        articles = self.news_fetcher.fetch_news(
            query=config.NEWS_QUERY,
            language=config.NEWS_LANGUAGE,
            sort_by=config.NEWS_SORT_BY,
            page_size=config.NEWS_PAGE_SIZE
        )

        if articles is None:
            logging.warning("Failed to fetch news from API. Waiting for the next check.")
            return

        total_fetched = len(articles)
        if not articles:
            logging.info("No new articles found from API.")
            self.is_first_run = False
            return

        displayed_news_count = 0
        sound_played_this_cycle = False

        for article in reversed(articles):
            article_url = article.get('url')
            article_title = article.get('title', 'No Title')

            if not article_url:
                logging.warning(f"Skipping article with no URL: '{article_title}'")
                continue

            is_new = self.seen_news_manager.is_new(article_url)

            if is_new:
                try:
                    analysis = self.news_analyzer.analyze_article(article)
                    article_importance_level = analysis.get('importance', 'N/A')
                    article_importance_numeric = config.IMPORTANCE_ORDER.get(article_importance_level, -1)
                    article_sentiment = analysis.get('sentiment', 'N/A')

                except Exception as e:
                    logging.error(f"Error analyzing article ('{article_title}'): {e}", exc_info=True)
                    self.seen_news_manager.add_seen(article_url)
                    continue

                is_important_enough = article_importance_numeric >= self.min_importance_numeric
                should_display = False

                if is_important_enough:
                    if article_sentiment in ["Positive", "Negative"]:
                        should_display = True
                    elif article_sentiment == "Neutral":
                        high_importance_numeric = config.IMPORTANCE_ORDER.get("High", 99)
                        if article_importance_numeric >= high_importance_numeric:
                            should_display = True
                            logging.info(f"DISPLAYING Neutral article ({article_importance_level}) due to high importance: '{article_title}'")

                if should_display:
                    displayed_news_count += 1
                    logging.info(f"New, important, and displayable article found ({article_importance_level}, {article_sentiment}): '{article_title}'")

                    self.display_news(article, analysis)

                    play_sound_now = False
                    if self.is_first_run:
                        if not sound_played_this_cycle:
                            play_sound_now = True
                            sound_played_this_cycle = True
                    else:
                        play_sound_now = True

                    if play_sound_now:
                        self.notifier.play_notification()

                elif is_important_enough and article_sentiment == "Neutral":
                    logging.debug(f"Neutral article ({article_importance_level}, importance score: {article_importance_numeric}) not displayed due to not meeting high importance criteria: '{article_title}'")
                elif not is_important_enough:
                    logging.debug(f"New article found but below minimum importance level ({article_importance_level}). Not displaying: '{article_title}'")

                self.seen_news_manager.add_seen(article_url)


        self.is_first_run = False

        if displayed_news_count > 0:
            logging.info(f"Processed {displayed_news_count} new, important, and displayed articles.")
        else:
            logging.info(f"No new articles to display were found in this check cycle (Total {total_fetched} articles fetched from API).")


    def format_published_date_local(self, published_at_str: str) -> str:
        if not published_at_str:
            return "No Date"
        try:
            if published_at_str.endswith('Z'):
                published_at_str = published_at_str[:-1] + '+00:00'
            utc_dt = datetime.fromisoformat(published_at_str)
            try:
                local_tz = get_localzone()
            except pytz.UnknownTimeZoneError:
                logging.warning("Could not automatically detect local timezone. Using UTC.")
                local_tz = pytz.utc
            local_dt = utc_dt.astimezone(local_tz)
            formatted_date = local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')
            return formatted_date
        except ValueError:
            logging.warning(f"Could not parse date '{published_at_str}' as ISO format. Using original.")
            return published_at_str
        except Exception as e:
            logging.error(f"Unexpected error during date conversion: {e}", exc_info=False)
            return published_at_str


    def display_news(self, article: dict, analysis: dict):
        title = article.get('title', 'N/A')
        url = article.get('url', '#')
        source = article.get('source', {}).get('name', 'N/A')
        published_at_iso = article.get('publishedAt', None)
        formatted_published_at = self.format_published_date_local(published_at_iso)
        sentiment = analysis.get('sentiment', 'N/A')
        sentiment_score = analysis.get('sentiment_score', 0.0)
        related_coins = ", ".join(analysis.get('related_coins', ['N/A']))
        importance = analysis.get('importance', 'N/A')

        sentiment_color = COLOR_NEUTRAL
        if sentiment == "Positive": sentiment_color = COLOR_POSITIVE
        elif sentiment == "Negative": sentiment_color = COLOR_NEGATIVE

        importance_color = ""
        if importance in ["High", "Critical"]: importance_color = COLOR_IMPORTANT

        print("\n" + "="*80)
        print(f"📰 {importance_color}ARTICLE ({importance}) | {source} | {formatted_published_at}")
        print(f"📌 Title: {title}")
        print(f"🔗 URL: {url}")
        print(f"📊 Analysis:")
        print(f"   - Sentiment: {sentiment_color}{sentiment} (Score: {sentiment_score:.2f})")
        print(f"   - Related Coins: {COLOR_POSITIVE}{related_coins}")
        print("="*80 + "\n")


    def run(self):
        print("\n" + "*"*30)
        print("   Crypto News Bot Active")
        print(f"   Minimum Importance Level: {config.MIN_DISPLAY_IMPORTANCE_LEVEL}")
        print(f"   Check Interval: {self.check_interval} seconds")
        print("   Displaying new, important (Positive/Negative or high-importance Neutral) news in console.")
        print("   Check 'crypto_news_bot.log' for detailed logs and errors.")
        print("   Press CTRL+C to exit.")
        print("*"*30 + "\n")

        logging.info("Starting bot main loop and performing initial check...")
        try:
            self.check_and_process_news()
        except Exception as e:
             logging.critical(f"Critical error during initial news check: {e}", exc_info=True)
             self.is_first_run = False

        logging.info(f"Scheduled news check every {self.check_interval} seconds.")
        schedule.every(self.check_interval).seconds.do(self.check_and_process_news)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("CTRL+C detected. Stopping bot...")
            if hasattr(self.news_fetcher, 'close_session'):
                self.news_fetcher.close_session()
                logging.info("News fetcher session closed.")
            self.seen_news_manager._save_seen_urls()
            logging.info("Seen news saved. Exiting.")
            print("\nBot stopped gracefully. Logs saved. Goodbye!")
        except Exception as e:
            logging.critical(f"Unexpected critical error in main loop: {e}", exc_info=True)
            try:
                self.seen_news_manager._save_seen_urls()
            except Exception as save_e:
                 logging.error(f"Failed to save seen news during error handling: {save_e}")
            sys.exit(1)


if __name__ == "__main__":
    bot = CryptoNewsBot()
    bot.run()