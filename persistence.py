import json
import os
import logging
from typing import Set

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SeenNewsManager:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.seen_urls: Set[str] = self._load_seen_urls()
        logging.info(f"Seen news manager initialized. Loaded {len(self.seen_urls)} URLs from: {filepath}")

    def _load_seen_urls(self) -> Set[str]:
        if os.path.exists(self.filepath):
            try:
                if os.path.getsize(self.filepath) == 0:
                    logging.info(f"Seen news file ('{self.filepath}') exists but is empty. Starting with an empty set.")
                    return set()

                with open(self.filepath, 'r', encoding='utf-8') as f:
                    try:
                        urls = json.load(f)
                        if isinstance(urls, list):
                            return set(urls)
                        else:
                            logging.warning(f"File '{self.filepath}' is not in the expected list format. Content: {urls}. Starting with an empty set.")
                            return set()
                    except json.JSONDecodeError as json_err:
                        logging.error(f"JSON decoding error reading '{self.filepath}' (file might be corrupted): {json_err}. Starting with an empty set.")
                        return set()
            except IOError as e:
                 logging.error(f"I/O error reading seen news file ('{self.filepath}'): {e}")
                 return set()
            except Exception as e:
                logging.error(f"Unexpected error loading seen URLs: {e}")
                return set()
        else:
            logging.info(f"Seen news file ('{self.filepath}') not found. Will create a new one.")
            return set()

    def _save_seen_urls(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(list(self.seen_urls), f, indent=4)
        except IOError as e:
            logging.error(f"I/O error writing seen news file ('{self.filepath}'): {e}")
        except Exception as e:
            logging.error(f"Unexpected error saving seen URLs: {e}")

    def is_new(self, url: str) -> bool:
        return url not in self.seen_urls

    def add_seen(self, url: str):
        if url not in self.seen_urls:
            self.seen_urls.add(url)
            self._save_seen_urls()

    def get_seen_count(self) -> int:
        return len(self.seen_urls)