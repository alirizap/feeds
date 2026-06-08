import logging
import argparse
import json
from pathlib import Path
from dataclasses import dataclass


logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
FEEDS_CONFIG_FILE = BASE_DIR / "feeds.json"

class InvalidConfigError(Exception):
    """Raised when config file format is invalid"""

def validate_feeds_config(data: list[dict]) -> bool:
    
    if not isinstance(data, list):
        raise InvalidConfigError(
            f"Config must be a JSON array, got {type(data).__name__}")

    if len(data) == 0:
        raise InvalidConfigError("Config array cannot be empty")

    for index, feed_group in enumerate(data):
            if not isinstance(feed_group, dict):
                raise InvalidConfigError(
                    f"Feed group at index {index} must be a dict, got {type(feed_group).__name__}")
            
            if "name" not in feed_group:
                raise InvalidConfigError(
                    f"Feed group at index {index} missing 'name' field")
            
            if "urls" not in feed_group:
                raise InvalidConfigError(
                    f"Feed group at index {index} missing 'urls' field")
            
            # Validate field types
            if not isinstance(feed_group["name"], str):
                raise InvalidConfigError(
                    f"Feed group {index}: 'name' must be string")
            
            if not isinstance(feed_group["urls"], list):
                raise InvalidConfigError(
                    f"Feed group {index}: 'urls' must be a list")
            
            if len(feed_group["urls"]) == 0:
                raise InvalidConfigError(
                    f"Feed group '{feed_group['name']}': 'urls' cannot be empty")

            for url_index, url in enumerate(feed_group["urls"]):
                if not isinstance(url, str):
                    raise InvalidConfigError(
                        f"Feed group '{feed_group['name']}': "
                        f"URL at index {url_index} must be string")
                
                if len(url) == 0:
                    raise InvalidConfigError(
                        f"Feed group '{feed_group['name']}': URL cannot be empty")

def load_config() -> list[dict]:
    try:
        with open(FEEDS_CONFIG_FILE) as f:
            data = json.load(f)
        
        validate_feeds_config(data)
        return data

    except FileNotFoundError:
        logger.error(f"Config file '{FEEDS_CONFIG_FILE}' not found")
        exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        exit(1)
    except InvalidConfigError as e:
        logger.error(f"Invalid config format: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(prog="feeds",
                description="downloading and storing RSS feeds")
    parser.add_argument("-n", "--name", action="store_true",
                        help="show feed group names")
    parser.add_argument("-s", "--sync", nargs="+", metavar="name",
                        help="download RSS feeds, parse them, and store titles/links")
    args = parser.parse_args()

    logging.basicConfig(format="[%(levelname)s] %(asctime)s - %(message)s")
    feeds = load_config()
    print(feeds)

if __name__ == "__main__":
    main()
