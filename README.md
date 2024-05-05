[![pytest](https://github.com/berdal84/split-column-csv/actions/workflows/pytest.yml/badge.svg)](https://github.com/berdal84/split-column-csv/actions/workflows/pytest.yml)

# Split Column CSV

This is a small Python script to split a given column from a CSV.

Example:

Let's consider the example file `csv/example/example_01.csv`:

| title    | version |
| -------- | ------- |
| Matrix   | 1;2;3;4 |

By running the command `python main.py --input csv/example/example_01.csv --columns version`, we can generate a new file `csv/example/example_01_output.csv` with the following content:

| title    | version |
| -------- | ------- |
| Matrix   | 1       |
| Matrix   | 2       |
| Matrix   | 3       |
| Matrix   | 4       |

> Did you know? You can specify multiple columns by separating them using a comma, example: `--columns col1,col2,col3`.

## How to install ?

Download and unzip this repository

Make sure [python](https://www.python.org/) (>= 3.10) is installed:

```
python --version
```

Create a virtual environment to install the project:

```
python -m venv .venv
```

Activate the environment

```
source .venv/bin/activate
```

Install the packages

```
pip install -r requirements.txt
```

## How to run ?

Make sure to open a command line in the unzipped install folder.

> Make sure the environment you installed the packages in is active by running:
> `source .venv/bin/activate`

 folder, run:

```
python main.py --path "path/to/your/file.csv" --column "column name"
```

## Help

For more information about the program, run the following command:

```
python main.py --help
```


## Tests

To run *the* single test, run the command:

```
pytest
```

The script will process all the files present in `csv/pytest/input` and generate a split version for each of them into `csv/pytest/output`. Once done, expected files in `csv/pytest/expected` are compared to the output to ensure program produces the correct result.
