import pandas as pd;
import argparse;

if __name__ == '__main__':

    print("Split ..")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        type=str,
        default="./input.csv",
        required=True,
        help="relative/absolute path to a csv file",
        dest="path"
        )
    
    parser.add_argument(
        '--column',
        type=str,
        default="miRNAs/precursors",
        help="Column to split",
        dest="column"
        )
    
    parser.add_argument(
        '--separator',
        type=str,
        default=";",
        help="Separator character for split",
        dest="separator"
        )
    
    args = parser.parse_args()

    # Configuration
    file_path= args.path
    output_file_path=f"{file_path}_split.csv"
    base_id = 1 # Excel is 1-based

    # Load CSV as a pandas DataFrame
    print("Read csv ..")
    file = open(file_path)
    dataframe = pd.read_csv(file)

    # Split rows
    print("Transform data ..")
    data_split = dict()
    next_id = 0
    for [id, original_row] in dataframe.to_dict("index").items():

        # Split the miRNAs column
        value: str = original_row[args.column]
        split_values = value.split(args.separator)
        split_count = len(split_values)
        is_split = split_count > 1

        for each_split_value in split_values:

            # Copy original values
            new_values = dict(original_row)

            # Overwrite cell with a single value
            new_values[args.column] = each_split_value

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
    file_split = open(output_file_path, "w")
    dataframe_split = pd.DataFrame.from_dict(data_split, 'index')
    dataframe_split.to_csv(file_split, mode = 'w', index=False)

    print('Split DONE, see output file: "{}"'.format(output_file_path))

