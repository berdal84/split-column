import sys
import pandas as pd
import argparse

class App:
    def __init__(self, override_args: list[str]|None = None):
        self.is_initialized = False
        # argument_default=argparse.SUPPRESS to allow parsing programmatic arguments
        self.parser = argparse.ArgumentParser("python main.py", argument_default=argparse.SUPPRESS)
        self.args: any = None
        self.parser.add_argument(
            '-i',
            '--input',
            type=str,
            required=True,
            help="Path to a CSV file (absolute or relative)",
            dest="input"
            )
        
        self.parser.add_argument(
            '-o',
            '--output',
            type=str,
            default=None,
            required=False,
            help="Path to the output CSV file (absolute or relative)",
            dest="output"
            )
        
        self.parser.add_argument(
            '-c',
            '--columns',
            type=str,
            required=True,
            help="The column(s) name to split, coma separated values (in development)",
            dest="columns"
            )
        
        self.parser.add_argument(
            '-s'
            '--separator',
            type=str,
            default=";",
            help="The character to use to split a cell",
            dest="separator"
            )
        
        self.parser.add_argument(
            '-m',
            '--metadata-columns',
            type=str,
            default=False,
            help="When this argument is present, two extra columns (id, original_id) will be added to have a reference between the new and the old CSV in terms of row number",
            dest="insert_metadata",
            )

    def init(self, override_args: list[str]|None = None):
        self.args = self.parser.parse_args(override_args)
        self.is_initialized = True
        
    def run(self):

        if not self.is_initialized:
            raise Exception("You are trying to run a non initialized app. Check if you properly called init() prior to call run()")

        print("Split ..")

        # Configuration
        input_file_path= self.args.input
        output_file_path=self.args.output if self.args.output != None else input_file_path.replace(".csv", "_output.csv")
        base_id = 1 # Excel is 1-based

        # Load CSV as a pandas DataFrame
        print("Read csv ..")
        if not input_file_path.endswith(".csv"):
            raise Exception("Input's file path must be a CSV file (ending in '.csv')")
        file = open(input_file_path)
        dataframe = pd.read_csv(file)

        # Split rows
        print("Transform data ..")
        data_split = dict()
        next_id = 0
        column = self.args.columns.split(",")[0] # Only one column is handled
        for [id, original_row] in dataframe.to_dict("index").items():

            # Split the column            
            value: str = original_row[column]
            split_values = value.split(self.args.separator)

            for each_split_value in split_values:

                # Copy original values
                new_values = dict(original_row)

                # Overwrite cell with a single value
                new_values[column] = each_split_value

                if self.args.insert_metadata:
                    # Add extra columns
                    new_values['original_id'] = base_id + id # this is the line id from the source csv
                    new_values['new_id'] = base_id + next_id # this is the current line id from the split csv

                # Uncomment this line if you want to see output in the console while running script
                # print(new_values)

                # Append the new values to the split data
                data_split[next_id] = new_values

                # Increment to give a new id to the next new value
                next_id += 1

        # Write data split to a CSV file
        print("Write output .. ")
        with open(output_file_path, "w") as file_split:
            dataframe_split = pd.DataFrame.from_dict(data_split, 'index')
            dataframe_split.to_csv(file_split, mode = 'w', index=False)

        print('Split DONE, see output file: "{}"'.format(output_file_path))