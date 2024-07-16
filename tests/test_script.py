import io
import pytest
from script import convert_csv

# Mock input data
MOCK_INPUT_1 = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-01-01,2024-01-31,1000.00,5000.00
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#123,2024-01-15,2024-01-16,PURCHASE,GROCERY STORE,Groceries,50.00
#124,2024-01-20,2024-01-21,PURCHASE,GAS STATION,Gas,30.00
#125,2024-01-25,2024-01-26,PAYMENT,CREDIT CARD PAYMENT,,-100.00
"""

MOCK_INPUT_2 = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-02-01,2024-02-29,900.00,5100.00
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#126,2024-02-05,2024-02-06,PURCHASE,RESTAURANT,Dining,75.50
#127,2024-02-10,2024-02-11,PURCHASE,ONLINE STORE,Shopping,120.25
#128,2024-02-15,2024-02-16,CREDIT,RETURN,Shopping,-20.00
"""

EXPECTED_OUTPUT_1 = """Date,Payee,Amount,Tags
2024-01-15,GROCERY STORE,-50.00,Groceries
2024-01-20,GAS STATION,-30.00,Gas
2024-01-25,CREDIT CARD PAYMENT,100.00,
"""

EXPECTED_OUTPUT_2 = """Date,Payee,Amount,Tags
2024-02-05,RESTAURANT,-75.50,Dining
2024-02-10,ONLINE STORE,-120.25,Shopping
2024-02-15,RETURN,20.00,Shopping
"""


def test_convert_csv_basic():
    input_file = io.StringIO(MOCK_INPUT_1)
    output_file = io.StringIO()
    convert_csv(input_file, output_file)
    assert output_file.getvalue() == EXPECTED_OUTPUT_1


def test_convert_csv_with_credit():
    input_file = io.StringIO(MOCK_INPUT_2)
    output_file = io.StringIO()
    convert_csv(input_file, output_file)
    assert output_file.getvalue() == EXPECTED_OUTPUT_2


def test_convert_csv_empty_input():
    input_file = io.StringIO("MY ACCOUNT TRANSACTIONS\nStart Date,End Date,Current Balance,Available Credit\n2024-01-01,2024-01-31,0,0\nREF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT\n")
    output_file = io.StringIO()
    convert_csv(input_file, output_file)
    assert output_file.getvalue() == "Date,Payee,Amount,Tags\n"


def test_convert_csv_invalid_amount():
    invalid_input = """MY ACCOUNT TRANSACTIONS
Start Date,End Date,Current Balance,Available Credit
2024-01-01,2024-01-31,1000.00,5000.00
REF,TRANSACTION DATE,POSTED DATE,TYPE,DESCRIPTION,Category,AMOUNT
#123,2024-01-15,2024-01-16,PURCHASE,GROCERY STORE,Groceries,NOT_A_NUMBER
"""
    input_file = io.StringIO(invalid_input)
    output_file = io.StringIO()
    with pytest.raises(ValueError):
        convert_csv(input_file, output_file)
