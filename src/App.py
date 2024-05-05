import pandas as pd
import argparse

class App:
    def __init__(self, override_args: list[str]|None = None):
        self.is_initialized = False
        self.FIRST_ROW_ID = 1 # Excel is 1-based

        # argument_default=argparse.SUPPRESS to allow parsing programmatic arguments
        PROG = "python -m main"
        self.parser = argparse.ArgumentParser(
            argument_default=argparse.SUPPRESS,
            prog=PROG,
            usage=f"{PROG} -m --input \"path/to/file.csv\" --columns \"title,version\"",
        )

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
            help="Path to the output CSV file (absolute or relative)",
            dest="output"
        )
        
        self.parser.add_argument(
            '-c',
            '--columns',
            type=str,
            required=True,
            help="The column(s) name to split, coma separated values (ex: title,author,version)",
            dest="columns"
        )
        
        self.parser.add_argument(
            '-s'
            '--separator',
            type=str,
            default=";",
            help="The character to use to split a cell",
            dest="separator",
        )
        
        self.parser.add_argument(
            '-m',
            '--metadata-columns',
            type=bool,
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

        # Determine in/out file path
        input_file_path= self.args.input
        output_file_path=self.args.output if self.args.output != None else input_file_path.replace(".csv", "_output.csv")

        # Load CSV as a pandas DataFrame
        #-------------------------------
        print("Read csv ..")
        if not input_file_path.endswith(".csv"):
            raise Exception("Input's file path must be a CSV file (ending in '.csv')")
        file = open(input_file_path)
        dataframe = pd.read_csv(file)

        # Split rows
        #-----------

        print("Transform data ..")
        # A dictionary to read from
        in_buffer = dataframe.to_dict("index")
        # A dictionary to write to
        out_buffer: dict|None = None # To store the result of the last pass
        next_id = 0
        columns = self.args.columns.split(",")

        # Insert "original_id" column to be able to find the source data from the split CSV.
        if self.args.insert_metadata:
            for [id, input_row] in in_buffer.items():
                input_row['original_id'] = self.FIRST_ROW_ID + id

        # Split each column specified by the user
        # This could be optimized by identifying how many columns needs to be split for a given line
        for column in columns:
            print(f"Processing for column: {column} ..")

            # Swap in/out buffer, so the last result is now the input
            if out_buffer is not None:
                in_buffer = out_buffer

            # Ensure out buffer is empty      
            out_buffer = dict()

            # Process each rows from the input buffer
            for [id, input_row] in in_buffer.items():
                print(f"Processing row: #{id} ..")
                last_id = self.split_cell_at_column_and_distribute_into_rows(
                    input_row=input_row,
                    column_to_split=column,   
                    output=out_buffer,
                    output_id=next_id,                                                       
                )
                next_id = last_id + 1

        # Last temp data IS not the result!
        output_data = out_buffer            

        # Write data split to a CSV file
        print("Write output .. ")
        with open(output_file_path, "w") as file_split:
            dataframe_split = pd.DataFrame.from_dict(output_data, 'index')
            dataframe_split.to_csv(file_split, mode = 'w', index=False)

        print('Split DONE, see output file: "{}"'.format(output_file_path))


    def split_cell_at_column_and_distribute_into_rows(
            self,
            input_row: dict,
            column_to_split: str,           
            output: dict,   
            output_id: int,                        
        ) -> int :
        
        """
        Takes a row and duplicate it to spread each values found in a given column.

        Ex:
            title, version   ---- becomes ---->  title, version, [id], [original_id]
            Alien, 1;2;                          Alien, 1      , 1   , 1        
                                                 Alien, 2      , 2   , 1
        """

        # Split the cell at given column            
        cell_value_to_split: str = input_row[column_to_split]
        split_values = cell_value_to_split.split(self.args.separator)

        if len(split_values) == 1:
            output[output_id] = input_row # by ref
            output_id += 1
        else:
            print(f"Found multiple values in column '{column_to_split}': '{cell_value_to_split}'")
            for each_split_value in split_values:
                print(f"-- making row for: '{each_split_value}'")

                # Copy original values
                new_values = dict(input_row) # by copy
                # Overwrite cell with a single value
                new_values[column_to_split] = each_split_value

                output[output_id] = new_values
                output_id += 1                

        return output_id