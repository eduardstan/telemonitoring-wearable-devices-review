import argparse
from filtering.filter import process_topic
from parsers.parse import parse_sources
from deduplication.deduplicate import deduplicate_file
from utils.logging_utils import setup_logging

DEFAULT_DATABASES = ['embase', 'ieee_xplore', 'pubmed', 'scopus']

def main():
    """Main entry point for the CLI."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Telemonitoring Wearable Devices Review Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Parser for the 'parse' command
    parse_parser = subparsers.add_parser("parse", help="Parse raw data files into structured CSVs.")
    parse_parser.add_argument(
        "-d",
        "--databases",
        nargs="+",
        default=DEFAULT_DATABASES,
        help=f"List of databases to parse (default: {', '.join(DEFAULT_DATABASES)})."
    )
    parse_parser.add_argument(
        "-t",
        "--topics",
        nargs="+",
        required=True,
        help="List of sub-topics to parse (e.g., ai_methods, accessibility)."
    )
    
    # Parser for the 'deduplicate' command
    dedup_parser = subparsers.add_parser("deduplicate", help="Deduplicate parsed CSV files.")
    dedup_parser.add_argument(
        "-t",
        "--topics",
        nargs="+",
        required=True,
        help="List of topics to deduplicate (e.g., ai_methods, accessibility)."
    )

    # Parser for the 'filter' command
    filter_parser = subparsers.add_parser("filter", help="Filter records based on titles and abstracts using GPT.")
    filter_parser.add_argument(
        "-t",
        "--topics",
        nargs="+",
        required=True,
        help="List of topics to filter (e.g., ai_methods, usability)."
    )
    
    args = parser.parse_args()
    
    if args.command == "parse":
        for topic in args.topics:
            parse_sources(databases=args.databases, topic=topic)
    elif args.command == "deduplicate":
        for topic in args.topics:
            deduplicate_file(topic=topic)
    elif args.command == "filter":
        for topic in args.topics:
            process_topic(topic)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
