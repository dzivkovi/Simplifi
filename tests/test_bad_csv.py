"""
This module contains negative tests for the CSV conversion script,
demonstrating error handling and logging.
"""

import io
import logging
import pytest
from script import convert_csv

def test_convert_csv_with_bad_data(caplog):
    """
    Test the CSV conversion with malformed data to verify error handling and logging.
    """
    caplog.set_level(logging.ERROR)

    input_data = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-01-01,2024-01-31,1000.00,5000.00
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#123,2024-01-15,2024-01-16,PURCHASE,GROCERY STORE,Groceries,NOT_A_NUMBER
#124,2024-01-20,2024-01-21,PURCHASE,GAS STATION,Gas,30.00
"""

    input_file = io.StringIO(input_data)
    output_file = io.StringIO()

    with pytest.raises(ValueError):
        convert_csv(input_file, output_file)

    assert "Invalid amount format: NOT_A_NUMBER" in caplog.text

def test_convert_csv_with_missing_header(caplog):
    """
    Test the CSV conversion with missing header to verify error handling and logging.
    """
    caplog.set_level(logging.ERROR)

    input_data = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-01-01,2024-01-31,1000.00,5000.00
#123,2024-01-15,2024-01-16,PURCHASE,GROCERY STORE,Groceries,50.00
"""

    input_file = io.StringIO(input_data)
    output_file = io.StringIO()

    with pytest.raises(ValueError):
        convert_csv(input_file, output_file)

    assert "Invalid header" in caplog.text
