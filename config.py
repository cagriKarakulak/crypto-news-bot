import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWS_API_KEY_HERE")
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_QUERY = 'crypto OR bitcoin OR ethereum OR xrp OR solana OR cardano OR bnb OR blockchain OR nasdaq OR s&p500 OR fed OR "interest rate" OR inflation OR recession OR "stock market" OR defi OR nft OR binance OR coinbase OR kraken OR grayscale OR microstrategy OR sec OR cftc OR regulation OR etf OR volatility OR "bull market" OR "bear market" OR correction OR sentiment OR halving OR staking OR polkadot OR chainlink OR avalanche OR polygon OR tether OR usdc OR litecoin'
NEWS_LANGUAGE = "en"
NEWS_SORT_BY = "publishedAt"
NEWS_PAGE_SIZE = 10

TRACKED_COINS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "xrp": "ripple",
    "doge": "dogecoin",
    "shib": "shiba inu",
    "ada": "cardano",
    "avax": "avalanche",
    "dot": "polkadot",
    "link": "chainlink",
    "matic": "polygon",
    "bnb": "binance coin",
    "ltc": "litecoin",
    "bch": "bitcoin cash",
}

IMPORTANCE_KEYWORDS = {
    "breaking": 3, "alert": 3, "urgent": 3, "flash": 3,
    "sec": 3, "cftc": 3, "doj": 3, "fincen": 3,
    "regulation": 3, "enforcement": 3, "compliance": 3, "clampdown": 3, "crackdown": 3,
    "lawsuit": 3, "settlement": 3, "indictment": 3, "subpoena": 3, "freeze": 3,
    "government": 3, "ban": 3, "sanctions": 3, "investigation": 3,
    "major": 3, "significant": 3, "critical": 3,
    "hack": 3, "exploit": 3, "vulnerability": 3, "security breach": 3, "51% attack": 3, "double spend": 3, "rug pull": 3,
    "insolvency": 3, "bankruptcy": 3, "default": 3, "liquidity crisis": 3,
    "listing": 3, "delisting": 3, "trading halt": 3,
    "partnership": 3, "acquisition": 3, "merger": 3, "takeover": 3,
    "institutional adoption": 3, "institutional investment": 3, "custody": 3,
    "launch": 3, "mainnet": 3, "protocol upgrade": 3,
    "upgrade": 3, "fork": 3, "hard fork": 3, "halving": 3,
    "fed": 3, "fomc": 3, "interest rate decision": 3, "rate hike": 3, "rate cut": 3, "monetary policy": 3, "quantitative easing": 3, "qt": 3,
    "crash": 3, "surge": 3, "rally": 3, "plummet": 3, "nosedive": 3, "squeeze": 3, "liquidations": 3,
    "etf approval": 3, "etf rejection": 3, "etf launch": 3,
    "cbdc": 3, "central bank digital currency": 3,

    "analysis": 2, "research": 2, "prediction": 2, "forecast": 2, "projection": 2,
    "price": 2, "market": 2, "trend": 2, "outlook": 2, "momentum": 2,
    "update": 2, "report": 2, "earnings": 2, "revenue": 2, "profit": 2,
    "investment": 2, "funding": 2, "capital": 2, "raise": 2, "venture capital": 2, "vc": 2,
    "volatility": 2, "correction": 2, "dip": 2, "rebound": 2, "recovery": 2, "consolidation": 2,
    "bull market": 2, "bull": 2, "bullish": 2, "bear market": 2, "bear": 2, "bearish": 2, "sentiment": 2,
    "inflation": 2, "cpi": 2, "ppi": 2, "gdp": 2, "unemployment": 2, "recession risk": 2, "economic data": 2,
    "stablecoin": 2, "algorithmic stablecoin": 2, "depeg": 2, "peg": 2,
    "defi": 2, "decentralized finance": 2, "nft": 2, "non-fungible token": 2, "metaverse": 2, "web3": 2,
    "staking": 2, "yield": 2, "liquidity pool": 2, "apy": 2, "apr": 2,
    "mining": 2, "hashrate": 2,
    "layer 2": 2, "l2": 2, "scaling solution": 2, "gas fees": 2,
    "interoperability": 2, "cross-chain": 2, "bridge": 2,
    "governance": 2, "dao": 2, "proposal": 2, "vote": 2,
    "oracle": 2,
    "binance": 2, "coinbase": 2, "kraken": 2, "grayscale": 2, "microstrategy": 2, "blackrock": 2, "fidelity": 2, "ark invest": 2,
    "tether": 2, "usdt": 2, "circle": 2, "usdc": 2,
    "roadmap": 2, "milestone": 2,

    "opinion": 1, "viewpoint": 1, "perspective": 1,
    "guide": 1, "tutorial": 1, "how-to": 1, "explanation": 1, "definition": 1, "glossary": 1,
    "community": 1, "social media": 1, "reddit": 1, "twitter": 1, "telegram": 1, "discord": 1,
    "discussion": 1, "debate": 1, "ama": 1,
    "poll": 1, "survey": 1, "data": 1,
    "beginners": 1, "introduction": 1, "basics": 1,
    "conference": 1, "event": 1, "webinar": 1, "summit": 1, "meetup": 1,
    "review": 1, "comparison": 1, "alternative": 1,
    "podcast": 1, "blog post": 1, "article": 1,
    "whitepaper": 1,
}

IMPORTANCE_THRESHOLDS = {
    "Critical": 7,
    "High": 5,
    "Medium": 3,
    "Low": 0,
}

MIN_DISPLAY_IMPORTANCE_LEVEL = "Medium"

IMPORTANCE_ORDER = {
    "Low": 0,
    "Medium": 1,
    "High": 2,
    "Critical": 3,
    "N/A": -1
}

SOUND_NOTIFICATION_ENABLED = True
NOTIFICATION_SOUND_FILE = "notification.wav"

CHECK_INTERVAL_SECONDS = 60

SEEN_NEWS_FILE = "seen_news.json"