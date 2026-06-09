import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RSSFeedError(Exception):
    pass


class RSSFeedDownloader:
    def __init__(self, timeout=10, max_retries=3) -> None:
        """Initialize RSS feed downloader

        Args:
            timeout: Request timeout in seconds
            max_retries: Number of retry attempt for failed operation
        """

        self.timeout = timeout
        self.max_retries = max_retries
        self.session = self._make_session()

    def _make_session(self) -> requests.Session:
        """Create HTTP session with retry strategy"""

        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({"User-Agent": "Mozilla/5.0 (RSS Feed Reader)"})

        return session

    def fetch_feed(self, url: str) -> str:
        """Fetch RSS feed content from URL.

        Args:
            feed_url: URL of RSS feed

        Returns:
            RSS feed content as string

        Raises:
            RSSFeedError: If download fails
        """

        if not url or not isinstance(url, str):
            raise RSSFeedError("Invalid feed URL")

        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()

            if not resp.content:
                raise RSSFeedError(f"Empty response from {url}")

            return resp.text

        except requests.exceptions.Timeout:
            raise RSSFeedError(f"Timout: {url}")

        except requests.exceptions.ConnectionError:
            raise RSSFeedError(f"Connection error: {url}")

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            raise RSSFeedError(f"HTTP {status}: {url}")

        except requests.exceptions.InvalidURL:
            raise RSSFeedError(f"Invalid URL: {url}")

        except Exception as e:
            raise RSSFeedError(f"Fetching {url}: {str(e)}")

    def close(self):
        """Close session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
