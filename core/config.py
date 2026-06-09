import json
from typing import Any
from dataclasses import dataclass
from core.constants import FEEDS_CONFIG_FILE


class InvalidConfigError(Exception):
    """Raised when config file format is invalid"""
    pass

def _validate_feeds_config(data: Any) -> bool:
    
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

def load_config() -> dict[str, list[str]]:
    """Load and validate feeds configuration.

    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config is invalid JSON
        InvalidConfigError: If config format is invalid
    """

    with open(FEEDS_CONFIG_FILE) as f:
        data = json.load(f)
    
    _validate_feeds_config(data)
    return {fg["name"]: fg["urls"] for fg in data}

