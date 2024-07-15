# Automating CSV conversion to Quicken Simplifi CSV format

## How to Manually Import Transactions

Quicken Simplifi allows you to [manually import transactions from a CSV file](https://help.simplifimoney.com/en/articles/4413430-how-to-manually-import-transactions). This feature is useful when you need to add transactions from a bank or financial institution that doesn't support direct integration with Quicken Simplifi.

To format a CSV file for uploading transactions to Quicken Simplifi:

1. Download the CSV template from Quicken Simplifi's website: downloadable template.

2. Fill in the template with your bank transaction data, ensuring it matches the format provided.

3. To import the CSV file:

    - Go to the Transactions page on the Quicken Simplifi Web App
    - Select the account you want to import into
    - Click the import icon (cloud with up arrow) above the register
    - Choose your CSV file and click Import

## How to Automate CSV Conversion using Claude 3.5 Sonnet

This process it tedious and repetead montly so it need to be automated.

Anthopic has just announced the Prompt writing assitance through console ([https://console.anthropic.com/dashboard](https://console.anthropic.com/dashboard)) so it was a perfect opportunity to aks it to kelp me with the task.

Here is the prompt it arrived to:

```sh
You are tasked with creating a Python script that converts a CSV file from Canadian Tire Bank CSV format to Quicken Simplifi CSV format. The script should be able to read from an input file or stdin and write to an output file or stdout based on command-line arguments.

Input Format:
The input CSV file will have the following structure:
<input_format>
MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-06-15,2024-07-04,1326.66,8605.56
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#75446134168071014600878,2024-06-15,2024-06-17,PURCHASE,CANADIAN TIRE STORE #00087,Home stores,9.28
...
</input_format>

Output Format:
The output CSV file should have the following structure:
<output_format>
Date,Payee,Amount,Tags
2024-06-15,CANADIAN TIRE STORE #00087,-9.28,Home stores
...
</output_format>

Follow these steps to process the input file:
1. Skip the first three lines of the input file (header information).
2. Read the remaining lines and extract the relevant information.
3. Convert the data to the output format.
4. Write the converted data to the output file or stdout.

Handle command-line arguments as follows:
1. If no arguments are provided, read from stdin and write to stdout.
2. If one argument is provided, treat it as the input file and write to stdout.
3. If two arguments are provided, treat the first as the input file and the second as the output file.

When converting the data:
1. Use the TRANSACTION DATE as the Date in the output.
2. Use the DESCRIPTION as the Payee in the output.
3. Convert the AMOUNT to a negative number for PURCHASE transactions, and keep it positive for PAYMENT transactions.
4. Use the Category as the Tags in the output.

Handle potential errors and edge cases:
1. Check if the input file exists and is readable.
2. Validate the CSV format of the input file.
3. Handle potential encoding issues.
4. Gracefully handle any unexpected data in the input file.

Here's a template for your Python script:

<python_script>
import csv
import sys

def convert_csv(input_file, output_file):
    # Your conversion logic here
    pass

def main():
    # Handle command-line arguments
    # Call convert_csv with appropriate arguments
    pass

if __name__ == "__main__":
    main()
</python_script>


Implement the convert_csv function to read the input file,  process the data, and write to the output file. Use the csv module to read and write CSV files.

To test your script, create a sample input file named 'input.csv' with the provided format, and run the script using the following commands:
1. python script.py < input.csv > output.csv
2. python script.py input.csv > output.csv
3. python script.py input.csv output.csv

Ensure that the script produces the correct output in all cases and handles errors gracefully.
```
