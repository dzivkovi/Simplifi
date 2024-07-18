"""
This module contains test cases for the CSV conversion script.
It includes tests for basic functionality, error handling, and edge cases.
"""

import io
import pytest
from script import convert_csv

def test_convert_csv_basic():
    """Test basic CSV conversion functionality."""
    input_data = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-01-01,2024-01-31,1000.00,5000.00
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#123,2024-01-15,2024-01-16,PURCHASE,GROCERY STORE,Groceries,50.00
#124,2024-01-20,2024-01-21,PURCHASE,GAS STATION,Gas,30.00
"""
    expected_output = """Date,Payee,Amount,Tags
2024-01-15,GROCERY STORE,-50.00,Groceries
2024-01-20,GAS STATION,-30.00,Gas
"""
    input_file = io.StringIO(input_data)
    output_file = io.StringIO()
    convert_csv(input_file, output_file)
    assert output_file.getvalue() == expected_output

def test_convert_csv_with_payment():
    """Test CSV conversion with a payment transaction."""
    input_data = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-01-01,2024-01-31,1000.00,5000.00
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#125,2024-01-25,2024-01-26,PAYMENT,CREDIT CARD PAYMENT,,-100.00
"""
    expected_output = """Date,Payee,Amount,Tags
2024-01-25,CREDIT CARD PAYMENT,100.00,
"""
    input_file = io.StringIO(input_data)
    output_file = io.StringIO()
    convert_csv(input_file, output_file)
    assert output_file.getvalue() == expected_output

def test_convert_csv_with_credit():
    """Test CSV conversion with a credit transaction."""
    input_data = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-01-01,2024-01-31,1000.00,5000.00
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#126,2024-01-30,2024-01-31,CREDIT,RETURN REFUND,Shopping,-25.00
"""
    expected_output = """Date,Payee,Amount,Tags
2024-01-30,RETURN REFUND,25.00,Shopping
"""
    input_file = io.StringIO(input_data)
    output_file = io.StringIO()
    convert_csv(input_file, output_file)
    assert output_file.getvalue() == expected_output

def test_convert_csv_with_invalid_data():
    """Test CSV conversion with invalid data to ensure proper error handling."""
    input_data = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-01-01,2024-01-31,1000.00,5000.00
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#127,2024-01-15,2024-01-16,PURCHASE,GROCERY STORE,Groceries,NOT_A_NUMBER
"""
    input_file = io.StringIO(input_data)
    output_file = io.StringIO()
    with pytest.raises(ValueError):
        convert_csv(input_file, output_file)
