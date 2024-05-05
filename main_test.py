import os
from src.App import App
import filecmp

CSV_PYTEST_PATH = "csv/pytest"
CSV_INPUT = f"{CSV_PYTEST_PATH}/input"
CSV_OUTPUT = f"{CSV_PYTEST_PATH}/output"
CSV_EXPECTED = f"{CSV_PYTEST_PATH}/expected"

app = App()
    
def test_01_single_column():
    split_and_compare("test_01_single_column.csv", "version")
    split_and_compare("test_01_single_column.csv", "version", use_flags=True)

def test_02_two_columns():
    split_and_compare("test_02_two_columns.csv", "title,version")
    split_and_compare("test_02_two_columns.csv", "title,version", use_flags=True)

def split_and_compare(
        test_file_name: str,
        columns: str,
        use_flags: bool = False
    ):

    input=f"{CSV_INPUT}/{test_file_name}"
    output=f"{CSV_OUTPUT}/{test_file_name}"
    expected=f"{CSV_EXPECTED}/{test_file_name}"
    
    # Ensure an old output is not present (a failing test would succeed then!)
    try:
        os.remove(output)
    except FileNotFoundError:
        pass

    # Run
    if use_flags:
        args = ["-i", input, "-o", output, "-c", columns]
    else:
        args = ["--input", input, "--output", output, "--columns", columns]
    
    app.init(args)
    app.run()

    # Compare the output with an expected file (hand-written one).
    same = filecmp.cmp(output, expected, shallow=False)
    if not same:
        raise Exception(f"Files {output} and {expected} differs")

