import argparse
import logging
from parsers.parse import parse_data_from_multiple_sources
from deduplication.deduplicate import deduplicate_file
from utils.logging_utils import setup_logging

def main():
    """Main entry point for the CLI."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Telemonitoring Wearable Devices Review Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Parser for the 'parse' command
    parse_parser = subparsers.add_parser("parse", help="Parse raw data files into structured CSVs.")
    parse_parser.add_argument(
        "--databases",
        nargs="+",
        required=True,
        help="List of databases to parse (e.g., embase, ieee_xplore, pubmed, scopus)."
    )
    parse_parser.add_argument(
        "--sub_topics",
        nargs="+",
        required=True,
        help="List of sub-topics to parse (e.g., ai_methods, accessibility)."
    )
    parse_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV file path (optional, default is data/parsed/{sub_topics}_{total}_records.csv)."
    )
    
    # Parser for the 'deduplicate' command
    dedup_parser = subparsers.add_parser("deduplicate", help="Deduplicate parsed CSV files.")
    dedup_parser.add_argument(
        "--topics",
        nargs="+",
        required=True,
        help="List of topics to deduplicate (e.g., ai_methods, accessibility)."
    )
    
    args = parser.parse_args()
    
    if args.command == "parse":
        parse_data_from_multiple_sources(
            databases=args.databases,
            sub_topics=args.sub_topics,
            output_file=args.output
        )
    elif args.command == "deduplicate":
        for topic in args.topics:
            deduplicate_file(topic)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
