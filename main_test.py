
from app import App
import filecmp

def test_example(mocker):

    example = "./files/example.csv"
    example_split = example.replace(".csv", "_split.csv")
    example_expected_split = example.replace(".csv", "_expected_split.csv")

    mocker.patch(
        "sys.argv",
        [
            "main-test",
            "--path", example,
            "--column", "version",
        ],
    )

    app = App()
    app.init()
    app.run()

    same = filecmp.cmp(example_split, example_expected_split, shallow=False)
    if not same:
        raise Exception("File differs")
    