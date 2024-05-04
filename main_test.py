from src.App import App
import filecmp

CSV_PYTEST_PATH = "csv/pytest"
CSV_INPUT = f"{CSV_PYTEST_PATH}/input"
CSV_OUTPUT = f"{CSV_PYTEST_PATH}/output"
CSV_EXPECTED = f"{CSV_PYTEST_PATH}/expected"

app = App()
    
def test_01_single_column():
    split_and_compare("test_01_single_column.csv")

def test_02_two_columns():
    split_and_compare("test_02_two_columns.csv" )

def split_and_compare(test_file_name: str):

    input=f"{CSV_INPUT}/{test_file_name}"
    output=f"{CSV_OUTPUT}/{test_file_name}"
    expected=f"{CSV_EXPECTED}/{test_file_name}"
    
    # First we try using long argument names
    app.init(["--input", input, "--output", output, "--column", "version"])
    app.run()

    same = filecmp.cmp(output, expected, shallow=False)
    if not same:
        raise Exception(f"Files {output} and {expected} differs")
    
    # Then with short argument names
    app.init(["-i", input, "-o", output, "-c", "version"])
    app.run()

    same = filecmp.cmp(output, expected, shallow=False)
    if not same:
        raise Exception(f"Files {output} and {expected} differs")

