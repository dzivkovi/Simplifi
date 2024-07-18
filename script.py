#!/usr/bin/env python3
"""
This script converts a CSV file from Canadian Tire Bank format to Quicken Simplifi format.
It can read from an input file or stdin and write to an output file or stdout.
"""
# flake8: noqa: E302, E305

import csv
import sys
import logging
from datetime import datetime
import argparse
import chardet

def detect_encoding(file_path):
    """Detect the encoding of a file."""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def parse_date(date_string):
    """Parse date string and return in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        logging.warning("Invalid date format: %s", date_string)
        return date_string

def parse_amount(amount_string):
    """Parse amount string and return as float."""
    try:
        return float(amount_string.replace('$', '').replace(',', ''))
    except ValueError:
        logging.error("Invalid amount format: %s", amount_string)
        raise

def convert_csv(input_file, output_file):
    """
    Convert CSV from Canadian Tire Bank format to Quicken Simplifi format.

    Args:
    input_file: File object to read from
    output_file: File object to write to
    """
    reader = csv.reader(input_file)
    writer = csv.writer(output_file, lineterminator='\n')

    # Skip the first three lines
    for _ in range(3):
        next(reader, None)

    # Read and validate the header
    header = next(reader, None)
    expected_header = ['REF', 'TRANSACTION DATE', 'POSTED DATE', 'TYPE', 'DESCRIPTION', 'Category', 'AMOUNT']
    if header != expected_header:
        logging.error("Invalid header: %s", header)
        raise ValueError("CSV file does not match expected Canadian Tire Bank format")

    writer.writerow(['Date', 'Payee', 'Amount', 'Tags'])

    for row in reader:
        if len(row) != 7:
            logging.warning("Skipping invalid row: %s", row)
            continue

        try:
            date = parse_date(row[1])
            payee = row[4]
            amount = parse_amount(row[6])
            tags = row[5]

            # Always flip the sign of the amount
            amount = -amount

            writer.writerow([date, payee, f'{amount:.2f}', tags])
        except ValueError as e:
            logging.error("Error processing row: %s. Error: %s", row, str(e))
            raise

def main():
    """Main function to handle command-line arguments and call convert_csv."""
    parser = argparse.ArgumentParser(
        description="Convert Canadian Tire Bank CSV to Quicken Simplifi format",
        epilog="Use '-' as the input filename to read from stdin, or as the output filename to write to stdout."
    )
    parser.add_argument('-i', '--input', required=True,
                        help="Input file (use '-' for stdin)")
    parser.add_argument('-o', '--output', default='-',
                        help="Output file (use '-' for stdout, default: stdout)")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Enable verbose logging")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        input_file = sys.stdin if args.input == '-' else open(args.input, 'r', newline='', encoding='utf-8')
        output_file = sys.stdout if args.output == '-' else open(args.output, 'w', newline='', encoding='utf-8')

        if args.input != '-':
            encoding = detect_encoding(args.input)
            input_file = open(args.input, 'r', encoding=encoding, newline='')

        convert_csv(input_file, output_file)

    # pylint: disable=broad-except
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        sys.exit(1)
    finally:
        if args.input != '-' and 'input_file' in locals():
            input_file.close()
        if args.output != '-' and 'output_file' in locals():
            output_file.close()

if __name__ == "__main__":
    main()
