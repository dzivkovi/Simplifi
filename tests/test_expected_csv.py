import io
import pytest
from script import convert_csv


def test_convert_csv_with_mock_data():
    with open('tests/mock_input.csv', 'r') as mock_input_file:
        input_data = mock_input_file.read()
    
    with open('tests/expected_output.csv', 'r') as expected_output_file:
        expected_output = expected_output_file.read()

    input_file = io.StringIO(input_data)
    output_file = io.StringIO()

    convert_csv(input_file, output_file)

    assert output_file.getvalue() == expected_output
