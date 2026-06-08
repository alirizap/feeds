import argparse
from pathlib import Path





def main():
    parser = argparse.ArgumentParser(prog="feeds",
                description="downloading and storing RSS feeds")
    parser.add_argument("-n", "--name", action="store_true",
                        help="show feed group names")
    parser.add_argument("-s", "--sync", nargs="+", metavar="name",
                        help="download RSS feeds, parse them, and store titles/links")
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()
