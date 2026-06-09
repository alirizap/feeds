from typing import Any


def print_item(item: dict[str, Any]):
    print(f"Group: {item['group']}")
    print(f"Title: {item['title']}")
    print(f"Link: {item['link']}")
    print(f"Publish Date: {item['pub_date']}\n")


def print_items(items: list[dict[str, Any]]):
    for item in items:
        print_item(item)
