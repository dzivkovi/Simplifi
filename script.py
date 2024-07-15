"""
This script converts a CSV file from Canadian Tire Bank format to Quicken Simplifi format.
It can read from an input file or stdin and write to an output file or stdout.
"""

import csv
import sys
import os


def convert_csv(input_file, output_file):
    """
    Convert CSV from Canadian Tire Bank format to Quicken Simplifi format.

    Args:
    input_file: File object to read from
    output_file: File object to write to
    """
    try:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)

        # Skip the first three lines
        for _ in range(3):
            next(reader, None)

        # Skip the header row
        next(reader, None)

        # Write the header for the output file
        writer.writerow(['Date', 'Payee', 'Amount', 'Tags'])

        # Process the remaining lines
        for row in reader:
            if len(row) != 7:  # Validate row length
                continue

            date = row[1]  # TRANSACTION DATE
            payee = row[4]  # DESCRIPTION
            amount = float(row[6])  # AMOUNT
            transaction_type = row[3]  # TYPE
            tags = row[5]  # Category

            # Convert amount to negative for PURCHASE transactions
            if transaction_type == 'PURCHASE':
                amount = -amount

            writer.writerow([date, payee, f'{amount:.2f}', tags])

    except csv.Error as e:
        print(f"Error processing CSV file: {e}", file=sys.stderr)
    except ValueError as e:
        print(f"Error converting data: {e}", file=sys.stderr)
    # pylint: disable=broad-except
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


def main():
    """
    Main function to handle command-line arguments and call convert_csv.
    """
    if len(sys.argv) == 1:
        # No arguments: read from stdin, write to stdout
        convert_csv(sys.stdin, sys.stdout)
    elif len(sys.argv) == 2:
        # One argument: input file, write to stdout
        input_filename = sys.argv[1]
        if not os.path.exists(input_filename):
            print(f"Input file '{input_filename}' does not exist.",
                  file=sys.stderr)
            sys.exit(1)
        with open(input_filename, 'r', newline='', encoding='utf-8') as input_file:
            convert_csv(input_file, sys.stdout)
    elif len(sys.argv) == 3:
        # Two arguments: input file and output file
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        if not os.path.exists(input_filename):
            print(f"Input file '{input_filename}' does not exist.",
                  file=sys.stderr)
            sys.exit(1)
        with open(input_filename, 'r', newline='', encoding='utf-8') as input_file:
            with open(output_filename, 'w', newline='',
                      encoding='utf-8') as output_file:
                convert_csv(input_file, output_file)
    else:
        print("Usage: python script.py [input_file] [output_file]",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
