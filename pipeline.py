import argparse
import sys

from data_pipeline.scraper import run_scraper
from data_pipeline.transform import run_transformation
from data_pipeline.db_setup import run_db_pipeline


def print_custom_help():
    print("""
🚀 BDE Data Pipeline

Usage:
  python pipeline.py [OPTIONS]

Pipeline Steps:
  --scrape        Scrape faculty data
  --transform     Clean & transform data
  --db            Load data into database
  --all           Run full pipeline (scrape → transform → db)

Valid Commands:
  python pipeline.py --scrape
  python pipeline.py --transform
  python pipeline.py --db
  python pipeline.py --scrape --transform
  python pipeline.py --transform --db
  python pipeline.py --all

""")


def main():
    parser = argparse.ArgumentParser(
        description="BDE Data Pipeline",
        add_help=False
    )

    parser.add_argument("--scrape", action="store_true")
    parser.add_argument("--transform", action="store_true")
    parser.add_argument("--db", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("-h", "--help", action="store_true")

    args = parser.parse_args()

    if args.help:
        print_custom_help()
        sys.exit(0)

    if args.all and (args.scrape or args.transform or args.db):
        print("Error: --all cannot be combined with other flags\n")
        print_custom_help()
        sys.exit(1)

    if not any([args.scrape, args.transform, args.db, args.all]):
        print("Error: No command provided\n")
        print_custom_help()
        sys.exit(1)

    if args.all:
        run_scraper()
        run_transformation()
        run_db_pipeline()
        return

    if args.scrape:
        run_scraper()

    if args.transform:
        run_transformation()

    if args.db:
        run_db_pipeline()


if __name__ == "__main__":
    main()
