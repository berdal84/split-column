# Split CSV Column

## How to install ?

Download and unzip this repository

Make sure [python](https://www.python.org/) is installed:

```
python
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

This will process the file `./file/example.csv` for the column `version`, and compare the output with an expected file (`./file/example_expected_split`)