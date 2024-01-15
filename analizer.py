import csv
import os
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CSVData:
    """Class for keeping track of analyzed CSV properties"""

    file_name: str
    column_name: str
    total_rows: int
    longest_value_len: int
    longest_value_row: int


class CSVAnalyzer:
    """Class for analyzing csv"""

    def __init__(self):
        self.data = CSVData

    def analyze_csv_file(self, csv_reader, column_name):
        longest_value_len = 0
        longest_value_row = 0
        row_idx = 0

        for row_idx, row in enumerate(csv_reader, start=1):
            # Access the specified column
            column_value = row[column_name]

            # Check if current value length is bigger than last longest
            column_value_len = len(column_value)
            if column_value_len > longest_value_len:
                longest_value_len = column_value_len
                longest_value_row = row_idx

        self.data.total_rows = row_idx
        self.data.longest_value_row = longest_value_row
        self.data.longest_value_len = longest_value_len

    def create_results_file(self):
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{self.data.file_name}_results_{current_time}.txt"

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"Results for file '{self.data.file_name}' ({self.data.total_rows} total rows):\n")
            file.write(f"Column name: '{self.data.column_name}'\n")
            file.write(f"Longest value row: '{self.data.longest_value_row}'\n")
            file.write(f"Longest value length: '{self.data.longest_value_len}'\n")

        return file_name

    def check_csv_file(self):
        # Check if the file exists
        if not os.path.isfile(self.data.file_name):
            print(f"File '{self.data.file_name}' not found in the script's directory. Exiting.")
            return

        # Open the CSV file
        with open(self.data.file_name, 'r', encoding='utf-8') as file:
            # Create a CSV reader
            csv_reader = csv.DictReader(file)

            # Check if the column exists
            if self.data.column_name not in csv_reader.fieldnames:
                print(f"Column '{self.data.column_name}' not found in the CSV file. Exiting.")
                return

            # Analyze the file
            self.analyze_csv_file(csv_reader, self.data.column_name)

        # Create a log file and write results to it
        results_file_name = self.create_results_file()

        print(f"Analysis complete. Results saved to '{results_file_name}'.")

    def run(self):
        file_name = input("Enter the CSV file name: ")
        column_name = input("Enter the column name to check: ")

        self.data.file_name = file_name
        self.data.column_name = column_name

        self.check_csv_file()

        input("Press Enter to exit...")
