import argparse
import json
import logging

from core import InvalidConfigError, RSSFeedDownloader, RSSFeedError, load_config

logger = logging.getLogger(__name__)


def sync(selected_feeds: list[str], feed_groups: dict[str, list[str]]):
    with RSSFeedDownloader() as downloader:
        for name in selected_feeds:
            urls = feed_groups.get(name)
            if not urls:
                logger.error(f"Feed '{name}' not found")
                continue
            for url in urls:
                try:
                    result = downloader.fetch_feed(url)
                    print(result)
                except RSSFeedError as e:
                    logger.error(f"Feed group '{name}': {e}")


def main():
    parser = argparse.ArgumentParser(
        prog="feeds", description="downloading and storing RSS feeds"
    )
    parser.add_argument(
        "-n", "--name", action="store_true", help="show feed group names"
    )
    parser.add_argument(
        "-s",
        "--sync",
        nargs="+",
        metavar="name",
        help="download RSS feeds, parse them, and store titles/links",
    )
    args = parser.parse_args()

    logging.basicConfig(format="[%(levelname)s] %(asctime)s - %(message)s")

    try:
        feeds = load_config()
        if args.name:
            print("\n".join(feeds.keys()))
        if args.sync:
            sync(args.sync, feeds)
    except FileNotFoundError as e:
        logger.error(f"Config missing: {e}")
        exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Bad JSON: {e}")
        exit(1)
    except InvalidConfigError as e:
        logger.error(f"Invalid config: {e}")
        exit(1)
    except Exception as e:
        logger.error(str(e))
        exit(1)


if __name__ == "__main__":
    main()
